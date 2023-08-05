import pandas as pd
from scipy import stats

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_original import StatisticOperation
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.utils.widget_maker import WidgetMaker


class FrequenciesProportion(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        self.op_name = "Proportion (N-Outcomes)"
        self.sub = [
            {"name": "Variable", "type": ["N"], "max_count": 1, "min_count": 1},
        ]
        self.option = [
            {"name": "Expected", "type": "checkbox", "value": ["Visible"]},
            {"name": "Expected Proportion",
             "type": "individual_connected_unique_numberField",
             "connect": ["Variable"], "acc_title": "change proportion"}
        ]
        self.callback = {"refresh": refresh_tab}
        super(FrequenciesProportion, self).__init__(self.op_name, df, column_type_list, refresh_tab,
                                                    logger)

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

        var_layout_var_list = list(self.control_data['Variable'])
        var_var_list = []
        for layout_var in var_layout_var_list:
            var_var_list.append(self.column_value[layout_var])

        option = self.control_data['option']
        option_expected_visible = option['Expected']['Visible']
        option_expected_proportion = option['Expected Proportion']

        result_widgets = self.get_result_widgets(var_var_list, option_expected_proportion, option_expected_visible)

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):
        error_msg = CommonUtil.check_variables_shapes(control_data, 'Variable',
                                                      ['Object', "Number", "N-category", '2-Category'],
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        return True

    def get_result_widgets(self, var_var_list, option_expected_proportion, option_expected_visible):

        statistic_result = {}
        target_column = var_var_list[0]

        proportion_count_list = self.input_df[target_column].groupby(self.input_df[target_column]).count()
        proportion_count_key_list = proportion_count_list.keys()
        proportion_count_value_list = proportion_count_list.values
        proportion_count_value_sum = sum(proportion_count_value_list)

        expected_proportion_count_list = [1 for i in self.input_df[target_column].unique()]
        for key, value in option_expected_proportion.items():
            type_key = key if self.column_type_list[target_column] != 'Number' else int(key)
            expected_proportion_count_list[list(proportion_count_list.keys()).index(type_key)] = value
        expected_proportion_radio_sum = sum(expected_proportion_count_list)

        for index, item in enumerate(expected_proportion_count_list):
            expected_proportion_count_list[index] = round(
                item * proportion_count_value_sum / expected_proportion_radio_sum)

        expected_proportion_count_value_sum = sum(expected_proportion_count_list)
        origin_expected_count_0 = expected_proportion_count_list[0]
        difference_correction_value = proportion_count_value_sum - expected_proportion_count_value_sum
        if proportion_count_value_sum != expected_proportion_count_value_sum:
            expected_proportion_count_list[0] += difference_correction_value

        # result table
        df_count = len(self.input_df[target_column].unique()) - 1
        statistic_result["Proportion"] = stats.chisquare(list(proportion_count_list.values),
                                                         f_exp=expected_proportion_count_list)
        statistic_table_header = ["statistic", "df", "p-value"]
        statistic_table_body = [[round(statistic_result["Proportion"].statistic, 1), df_count,
                                 round(statistic_result["Proportion"].pvalue, 3)]]
        statistic_table = WidgetMaker.get_styled_table(statistic_table_header, statistic_table_body)

        # data table
        header_list = ["Item", "Count", "Proportion"]
        footer_text = ""
        if option_expected_visible:
            header_list = ["Item", " ", "Count", "Proportion"]
            footer_text = "*Values for correcting differences : [{0}] : {1} ({2})".format(
                list(proportion_count_key_list)[0],
                origin_expected_count_0,
                difference_correction_value)
        body_list = []
        for index, item in enumerate(proportion_count_list.keys()):
            if option_expected_visible:
                body_list.append([item, "observed", proportion_count_value_list[index],
                                  round(int(proportion_count_value_list[index]) / int(proportion_count_value_sum), 3)])
                body_list.append(["", "expected", expected_proportion_count_list[index],
                                  round(int(expected_proportion_count_list[index]) / int(proportion_count_value_sum),
                                        3)])
            else:
                body_list.append([item, proportion_count_value_list[index],
                                  round(int(proportion_count_value_list[index]) / int(proportion_count_value_sum), 3)])

        data_table = WidgetMaker.get_styled_table(header_list, body_list, footer_text)

        return CommonWidget.get_accordion_widget([statistic_table, data_table], ['Test Result(s)', 'Data table'])
