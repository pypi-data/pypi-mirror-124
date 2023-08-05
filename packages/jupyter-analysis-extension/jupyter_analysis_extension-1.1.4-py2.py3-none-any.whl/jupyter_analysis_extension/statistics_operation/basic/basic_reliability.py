import numpy as np

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_original import StatisticOperation
from jupyter_analysis_extension.statistics_widget.basic.basic_reliability import WidgetBasicReliability
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.utils.widget_maker import WidgetMaker


class BasicReliability(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        self.op_name = "Reliability Analysis"
        self.sub = [
            {"name": "Group", "type": ["N"], "max_count": 0, "min_count": 1}
        ]
        self.option = [
            {"name": "Statistical table", "type": "checkbox", "value": ['Cronbach\'s', 'Standard table']},
            {"name": "Chart types", "type": "checkbox", "value": ['Box plot', 'Headmap']},
        ]
        self.callback = {"refresh": refresh_tab}
        super(BasicReliability, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

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

        group_layout_var_list = list(self.control_data['Group'])
        group_var_list = []
        for layout_var in group_layout_var_list:
            group_var_list.append(self.column_value[layout_var])

        option = self.control_data['option']
        option_statistical_table = option['Statistical table']
        option_chart_types = option['Chart types']

        result_widgets = self.get_result_widgets(group_var_list, option_statistical_table, option_chart_types)

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):

        error_msg = CommonUtil.check_option_checkbox(control_data, 'Statistical table', 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_option_checkbox(control_data, 'Chart types', 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Group', ['Number'],
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        return True

    def get_result_widgets(self, group_var_list, option_statistical_table, option_chart_types):
        cronbach_alpha_group_list = []

        def cronbach_alpha_group(group_items):
            group_items = np.asarray(group_items)
            items_var = group_items.var(axis=1, ddof=1)
            items_sum = group_items.sum(axis=0)
            items_len = len(group_items)
            return items_len / (items_len - 1.) * (1 - items_var.sum() / items_sum.var(ddof=1))

        for group_var in group_var_list:
            cronbach_alpha_group_list.append(self.input_df[group_var])

        statistic_table_header = ['', 'Cronbach\'s', 'Mean', 'Deviation']
        statistic_table_body = [['Group', round(cronbach_alpha_group(cronbach_alpha_group_list), 3), '-', '-']]
        statistic_table_footer = "* Cronbach\'s > 0.6 is Reliable"
        for group_var in group_var_list:
            target_df = self.input_df[group_var]
            statistic_table_body.append([" - " + group_var, '-', round(target_df.mean(), 3), round(target_df.std(), 3)])

        statistic_table = WidgetMaker.get_styled_table(statistic_table_header, statistic_table_body,
                                                       statistic_table_footer)

        if option_statistical_table['Standard table']:
            standard_table = WidgetBasicReliability.get_standard_table()
            table_children = list(statistic_table.children)
            table_children.append(standard_table)
            statistic_table.children = tuple(table_children)

        chart_accordion_title = "Chart"
        statistic_chart = []
        for group_var in group_var_list:
            statistic_chart.append(self.input_df[group_var])

        if len(self.input_df) > 10000:
            # Sampling only 10000 rows
            chart_accordion_title += " (Sampling 10000 rows)"
            for index, df in enumerate(statistic_chart):
                statistic_chart[index] = df.copy().sample(n=10000, random_state=1, replace=False)

        chart_list = []
        if option_chart_types['Box plot']:
            chart_list.append(WidgetBasicReliability.get_box_plot_plotly(statistic_chart))
        if option_chart_types['Headmap']:
            chart_list.append(WidgetBasicReliability.get_headmap_plotly(self.input_df, group_var_list))
        chart_accordion_item = WidgetMaker.get_vertical_box(box_items=chart_list,
                                                            style=dict(display="flex", width="100%",
                                                                       align_items="center"))

        return CommonWidget.get_accordion_widget([statistic_table, chart_accordion_item],
                                                 ['Statistical table', chart_accordion_title])
