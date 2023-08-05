#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_original import StatisticOperation
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_widget.frequencies.frequencies_mcnemar import WidgetFrequenciesMcnemar


class FrequenciesMcnemar(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        self.op_name = "McNemar test"
        self.sub = [
            {"name": "Rows", "type": ["N"], "max_count": 1, "min_count": 1},
            {"name": "Columns", "type": ["N"], "max_count": 1, "min_count": 1},
        ]
        self.option = [
            {"name": "Test Types", "type": "checkbox", "value": ['Mcnemar', 'Continuity correction']}
        ]
        self.callback = {"refresh": refresh_tab}
        super(FrequenciesMcnemar, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

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

        rows_layout_var_list = list(self.control_data['Rows'])
        rows_var_list = []
        for layout_var in rows_layout_var_list:
            rows_var_list.append(self.column_value[layout_var])

        columns_layout_var_list = list(self.control_data['Columns'])
        columns_var_list = []
        for layout_var in columns_layout_var_list:
            columns_var_list.append(self.column_value[layout_var])

        option = self.control_data['option']
        tests_chi = option['Test Types']['Mcnemar']
        tests_fisher = option['Test Types']['Continuity correction']

        result_widgets = self.get_result_widgets(rows_var_list, columns_var_list, [tests_chi, tests_fisher])

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):

        error_msg = CommonUtil.check_option_checkbox(control_data, 'Test Types', 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Rows', ['2-Category'],
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Columns', ['2-Category'],
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        return True

    def get_result_widgets(self, rows_var_list, columns_var_list, tests_options):
        first_col_values = []
        statistic_tests_options = []
        statistic_result = {}

        cross_tab = pd.crosstab(self.input_df[rows_var_list[0]], self.input_df[columns_var_list[0]])

        if tests_options[0]:
            statistic_result["Mcnemar"] = mcnemar(cross_tab, exact=False, correction=False)
            first_col_values.append("Mcnemar")

        if tests_options[1]:
            statistic_result["Continuity correction"] = mcnemar(cross_tab, exact=False, correction=True)
            first_col_values.append("Continuity correction")

        cross_tab = pd.crosstab(self.input_df[rows_var_list[0]], self.input_df[columns_var_list[0]], margins=True,
                                margins_name='Total')
        df_count = len(self.input_df)

        statistic_result_table = WidgetFrequenciesMcnemar.get_statistic_result_table(first_col_values, df_count,
                                                                                     statistic_result,
                                                                                     statistic_tests_options)

        data_table = WidgetFrequenciesMcnemar.get_data_table(cross_tab)

        return CommonWidget.get_accordion_widget([statistic_result_table, data_table], ['Test Result(s)', 'Data table'])
