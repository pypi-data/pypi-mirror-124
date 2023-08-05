#!/usr/bin/env python
# coding: utf-8

# Copyright (c) TmaxBI.
# Distributed under the terms of the Modified BSD License.

import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import friedmanchisquare

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_op import StatisticOperation
from jupyter_analysis_extension.statistics_widget.anova.anova_ancova import WidgetANOVAANCOVA
from jupyter_analysis_extension.statistics_widget.anova.anova_friedman import WidgetANOVAFriedman
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget


class ANOVAFriedman(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        # Data
        self.input_df = df
        self.column_type_list = column_type_list
        self.op_name = "Repeated Measure(Friedman)"
        self.sub = [
            {"name": "Measures", "type": ["N"], "max_count": 0, "min_count": 1},
        ]
        self.option = []
        self.callback = {"refresh": refresh_tab}

        super(ANOVAFriedman, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

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
        option = self.control_data['option']
        is_valid = self.validate_input_data(self.control_data)
        if not is_valid:
            return

        # get analysis data & option
        measures_list = []
        for measures in self.control_data['Measures']:
            measures_list.append(self.column_value[measures])

        degree_freedom = len(measures_list) - 1

        result_widgets = self.get_result_widgets(degree_freedom, measures_list)

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Measures', 'Number',
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        return True

    def get_result_widgets(self, degree_freedom, measures_list):

        statistic_chart = []
        statistic_chart_title = []

        friedmanchisquare_parameter = []
        for measures in measures_list:
            friedmanchisquare_parameter.append(self.input_df[measures])
        print(friedmanchisquare_parameter)
        statistic_result = friedmanchisquare(*friedmanchisquare_parameter)

        statistic_result_table = WidgetANOVAFriedman.get_statistic_result_table(degree_freedom, statistic_result)

        return CommonWidget.get_accordion_widget([statistic_result_table, ], ['Test Result(s)'])
