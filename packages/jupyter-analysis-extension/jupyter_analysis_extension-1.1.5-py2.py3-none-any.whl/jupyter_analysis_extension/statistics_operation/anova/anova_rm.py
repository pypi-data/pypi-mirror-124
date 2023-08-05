#!/usr/bin/env python
# coding: utf-8

# Copyright (c) TmaxBI.
# Distributed under the terms of the Modified BSD License.

from statsmodels.stats.anova import AnovaRM

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_original import StatisticOperation
from jupyter_analysis_extension.statistics_widget.anova.anova_rm import WidgetANOVARM
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget


class ANOVARM(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        self.op_name = "Repeated Measure ANOVA"
        self.sub = [
                       {"name": "Dependent Variable (R.M.)", "type": ["N"], "max_count": 1, "min_count": 1},
                       {"name": "Subject ID", "type": [], "max_count": 1, "min_count": 1},
                       {"name": "Within-Subject Factrs", "type": ["C"], "max_count": 0, "min_count": 0}
                   ]
        self.option = []
        self.callback = {"refresh": refresh_tab}

        super(ANOVARM, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

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
        degree_freedom = len(self.input_df) - 2

        dependent_var = list(self.control_data['Dependent Variable (R.M.)'])[0]

        # self.input_df.dropna(inplace = True)

        subject_id = list(self.control_data['Subject ID'])[0]
        if 'Within-Subject Factors' in self.control_data.keys():
            within_factors_list = list(self.control_data['Within-Subject Factors'])
        else:
            within_factors_list = []
        result_widgets = self.get_result_widgets(
            degree_freedom, dependent_var, subject_id, within_factors_list)
        if CommonUtil.update_result_layout(self.control_panel, result_widgets):
            self.set_analyze_text('Done.')
        else:
            return

    def validate_input_data(self, control_data):

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Dependent Variable (R.M.)', 'Number',
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Subject ID', ['Object', 'N-Category', 'Number'],
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Within-Subject Factors',
                                                      ['N-Category', '2-Category'],
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        return True

    def get_result_widgets(self, degree_freedom, dependent_var, subject_id, within_factors_list):
        statistic_chart = []
        statistic_chart_title = []
        dep_var = self.column_value[dependent_var]
        subject = self.column_value[subject_id]
        within_factors_ls = []
        if len(within_factors_list) > 0:
            for within_factor in within_factors_list:
                within_factors_ls.append(self.column_value[within_factor])
        try:
            aovrm = AnovaRM(self.input_df, dep_var, subject, within=within_factors_ls)
            table = aovrm.fit().anova_table
        except Exception as e:
            self.set_analyze_text(str(e).split('.')[0], 'warning')
            return None

        statistic_result_table = WidgetANOVARM.get_statistic_result_table(table)

        """
        boxplot_sns = WidgetANOVAANCOVA.get_boxplot_sns()
        statistic_chart.append(boxplot_sns)
        statistic_chart_title.append('Box Plot (plotly): ' + str(dep))
        """

        return CommonWidget.get_accordion_widget([statistic_result_table, *statistic_chart],
                                                 ['Test Result(s)', *statistic_chart_title])
