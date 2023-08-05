#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
import pandas as pd
from scipy import stats

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_original import StatisticOperation
from jupyter_analysis_extension.statistics_widget.basic.basic_analysis import WidgetBasicAnalysis
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_widget.frequencies.frequencies_chi_square import WidgetFrequenciesChiSquare


class BasicAnalysis(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        self.op_name = "Basic : Analysis"
        self.sub = [
            {"name": "Variable(s)", "type": ["N"], "max_count": 0, "min_count": 1},
        ]
        self.option = [
            {"name": "Statistical table", "type": "checkbox", "value": ['Base(기초)']},
            {"name": "Chart Types", "type": "checkbox", "value": ['Box plot']}
        ]
        self.callback = {"refresh": refresh_tab}

        super(BasicAnalysis, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

    def construct_control_panel(self):
        self.control_panel, self.control_data = CommonWidget.make_control_panel(
            df=self.input_df,
            type_list=self.column_type_list,
            title=self.op_name,
            sub=self.sub,
            option=self.option,
            callback=self.callback
        )

        self.column_value = self.control_data["column"]

        self.connect_button_layout(self.control_panel.children[1], self.on_analyze_button_clicked)

    def on_analyze_button_clicked(self, widget):
        self.set_analyze_text('In progress...')

        # catch invalid data
        is_valid = self.validate_input_data(self.control_data)
        if not is_valid:
            return

        # get analysis data & option

        var_layout_var_list = list(self.control_data['Variable(s)'])
        var_var_list = []
        for layout_var in var_layout_var_list:
            var_var_list.append(self.column_value[layout_var])

        option = self.control_data['option']
        option_statistucal_table = option['Statistical table']
        option_chart_types = option['Chart Types']

        result_widgets = self.get_result_widgets(var_var_list, [option_statistucal_table, option_chart_types])

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):

        error_msg = CommonUtil.check_option_checkbox(control_data, 'Statistical table', 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_option_checkbox(control_data, 'Chart Types', 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Variable(s)',
                                                      ['N-Category', '2-Category', 'Object', 'Number'],
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        return True

    def get_result_widgets(self, var_var_list, tests_options):
        first_col_values = []
        statistic_chart = []
        statistic_tests_options = []
        statistic_result = {}

        for var_var in var_var_list:
            statistic_chart.append(self.input_df[var_var])

        if tests_options[0]['Base(기초)']:
            statistic_result['Base(기초)'] = {}
            for rows_var in var_var_list:
                statistic_result['Base(기초)'][rows_var] = self.input_df[rows_var].describe()
                first_col_values.append(rows_var)

        df_count = len(self.input_df)

        statistic_result_table = WidgetBasicAnalysis.get_statistic_result_table(first_col_values, df_count,
                                                                                statistic_result,
                                                                                statistic_tests_options)

        box_plot_title = "Data Chart"
        if len(self.input_df) > 10000:
            # Sampling only 10000 rows
            box_plot_title += " (Sampling 10000 rows)"
            for index, df in enumerate(statistic_chart):
                statistic_chart[index] = df.copy().sample(n=10000, random_state=1, replace=False)

        box_plot_plotly = WidgetBasicAnalysis.get_box_plot_plotly(statistic_chart)

        return CommonWidget.get_accordion_widget([statistic_result_table, box_plot_plotly],
                                                 ['Statistical table', box_plot_title])
