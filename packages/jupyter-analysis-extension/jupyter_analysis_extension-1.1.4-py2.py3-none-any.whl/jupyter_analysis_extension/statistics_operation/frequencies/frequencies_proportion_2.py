import pandas as pd
from scipy.stats import binom_test

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_original import StatisticOperation
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.utils.widget_maker import WidgetMaker


class FrequenciesProportion2(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        self.op_name = "Proportion (2-Outcomes)"
        self.sub = [
            {"name": "Variable(s)", "type": ["N"], "max_count": 0, "min_count": 1}
        ]
        self.option = [
            {"name": "Hypothesis", "type": "numberText-radio", "value": {
                "numberText": {"name": "Test value", "value": 0.5},
                "radio": {"name": None, "value": ["≠ Test value", "> Test value", "< Test value"]}
            }}
        ]
        self.callback = {"refresh": refresh_tab}
        super(FrequenciesProportion2, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

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
        hypothesis_test_value = option['Hypothesis']['number']
        hypothesis_alternative = option['Hypothesis']['radio']
        if hypothesis_alternative == '≠ Test value':
            hypothesis_alternative = 'two-sided'
        elif hypothesis_alternative == '> Test value':
            hypothesis_alternative = 'greater'
        elif hypothesis_alternative == '< Test value':
            hypothesis_alternative = 'less'

        result_widgets = self.get_result_widgets(var_var_list, hypothesis_test_value, hypothesis_alternative)

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):
        error_msg = CommonUtil.check_variables_shapes(control_data, 'Variable(s)',
                                                      ['Object', "Number", "N-category", '2-Category'],
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        return True

    def get_result_widgets(self, var_var_list, hypothesis_test_value, hypothesis_alternative):
        header_list = [" ", "Item", "Count", "Total", "Proportion", "p-value"]

        footer_test_value_equal_mark = ""
        if hypothesis_alternative == 'two-sided':
            footer_test_value_equal_mark = '≠'
        elif hypothesis_alternative == 'greater':
            footer_test_value_equal_mark = '>'
        elif hypothesis_alternative == 'less':
            footer_test_value_equal_mark = '<'

        footer_text = """Hypothesis Proportion {0} {1}""".format(footer_test_value_equal_mark, hypothesis_test_value)

        body_list = []
        for target_column in var_var_list:
            proportion_count_list = self.input_df[target_column].groupby(self.input_df[target_column]).count()
            proportion_count_key_list = proportion_count_list.keys()
            proportion_count_value_list = proportion_count_list.values
            proportion_count_value_sum = sum(proportion_count_value_list)

            for index, item in enumerate(proportion_count_value_list):
                target_column_name = target_column if index == 0 else ""

                p_value = binom_test(item, n=proportion_count_value_sum, p=hypothesis_test_value,
                                     alternative=hypothesis_alternative)
                proportion = round(item / proportion_count_value_sum, 3)
                body_list.append(
                    [target_column_name, proportion_count_key_list[index], item, proportion_count_value_sum, proportion,
                     round(p_value, 3)])

        data_table = WidgetMaker.get_styled_table(header_list, body_list, footer_text)

        return CommonWidget.get_accordion_widget([data_table], ['Data table'])
