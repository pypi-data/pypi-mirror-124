#!/usr/bin/env python
# coding: utf-8

import numpy as np
# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
from scipy import stats

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_original import StatisticOperation
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_widget.t_test.t_test_pair_sample import WidgetTTestPairSample


class TTestPairSample(StatisticOperation):

    def __init__(self, df, column_type_list, refresh_tab, logger):
        self.op_name = "T-Test : Paired Sample"
        self.sub = [
                  {"name": "Pair Set 1", "type": ["N"], "max_count": 0, "min_count": 1},
                  {"name": "Pair Set 2", "type": ["N"], "max_count": 0, "min_count": 1}
              ]
        self.option = [
                     {"name": "Test Types", "type": "checkbox", "value": ["Student\'s", "Wilcoxon signed-rank"]},
                     {"name": "Hypothesis", "type": "radio",
                      "value": ["Measure 1 ≠ Measure 2", "Measure 1 > Measure 2", "Measure 1 < Measure 2"]}
                 ]
        self.callback = {"refresh": refresh_tab}

        super(TTestPairSample, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

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
        degree_freedom = len(self.input_df)-1

        pair_set_1_layout_var_list = list(self.control_data['Pair Set 1'])
        pair_set_1_var_list = []
        for layout_var in pair_set_1_layout_var_list:
            pair_set_1_var_list.append(self.column_value[layout_var])

        pair_set_2_layout_var_list = list(self.control_data['Pair Set 2'])
        pair_set_2_var_list = []
        for layout_var in pair_set_2_layout_var_list:
            pair_set_2_var_list.append(self.column_value[layout_var])

        tests_students = option['Test Types']['Student\'s']
        tests_wilcoxon = option['Test Types']['Wilcoxon signed-rank']

        hypothesis_alternative = option['Hypothesis']['radio']
        if hypothesis_alternative == 'Measure 1 ≠ Measure 2':
            hypothesis_alternative = 'two-sided'
        elif hypothesis_alternative == 'Measure 1 > Measure 2':
            hypothesis_alternative = 'greater'
        elif hypothesis_alternative == 'Measure 1 < Measure 2':
            hypothesis_alternative = 'less'

        result_widgets = self.get_result_widgets(
            degree_freedom, pair_set_1_var_list, pair_set_2_var_list, [tests_students, tests_wilcoxon], [hypothesis_alternative])

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):
        error_msg = CommonUtil.check_option_checkbox(control_data, 'Test Types', 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Pair Set 1', 'Number',
                                                     self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Pair Set 2', 'Number',
                                                     self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        pair_set_1_var_list = list(control_data['Pair Set 1'])
        pair_set_2_var_list = list(control_data['Pair Set 2'])

        if len(pair_set_1_var_list) != len(pair_set_2_var_list):
            self.set_analyze_text(
                'Please make Pair Set 1,2 equal in length.', "warning")
            return False

        if (np.array(pair_set_1_var_list) == np.array(pair_set_2_var_list)).max():
            self.set_analyze_text(
                'Only different columns can be compared.', "warning")
            return False

        return True

    def get_result_widgets(self, degree_freedom, pair_set_1_var_list, pair_set_2_var_list, tests_options, hypothesis_options):
        target_column_names = []
        statistic_tests_options = []
        statistic_chart = []
        statistic_result = []

        for index, item in enumerate(pair_set_1_var_list):
            target_column_names.append(
                pair_set_1_var_list[index] + ' | ' + pair_set_2_var_list[index])
            statistic_chart.append(self.input_df[item])
            statistic_chart.append(self.input_df[pair_set_2_var_list[index]])
            if tests_options[0] == True:
                statistic_result.append(stats.ttest_rel(
                    self.input_df[item], self.input_df[pair_set_2_var_list[index]], nan_policy='omit', alternative=hypothesis_options[0]))
                statistic_tests_options.append('Student\'s')

            if tests_options[1] == True:
                if tests_options[0] == True:
                    target_column_names.append('')
                statistic_result.append(stats.wilcoxon(
                    self.input_df[item], self.input_df[pair_set_2_var_list[index]], zero_method="wilcox", alternative=hypothesis_options[0]))
                statistic_tests_options.append('Wilcoxon signed-rank')

        statistic_result_table = WidgetTTestPairSample.get_statistic_result_table(
            target_column_names, degree_freedom, statistic_result, statistic_tests_options)

        box_plot_title = "Box Plot"
        if len(self.input_df) > 10000:
            # Sampling only 10000 rows
            box_plot_title += " (Sampling 10000 rows)"
            for index, df in enumerate(statistic_chart):
                statistic_chart[index] = df.copy().sample(n=10000, random_state=1, replace=False)

        box_plot_plotly = WidgetTTestPairSample.get_box_plot_plotly(
            statistic_chart)

        return CommonWidget.get_accordion_widget([statistic_result_table, box_plot_plotly], ['Test Result(s)', box_plot_title])
