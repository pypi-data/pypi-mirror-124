from scipy import stats

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_original import StatisticOperation
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_widget.t_test.t_test_one_sample import WidgetTTestOneSample
from jupyter_analysis_extension.utils.chart_maker import ChartMaker
from jupyter_analysis_extension.utils.widget_maker import WidgetMaker


class TTestOneSample(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        self.op_name = "T-Test : One Sample"
        self.sub = [
                  {"name": "Dependent Variable(s)", "type": ["N"], "max_count": 0, "min_count": 1},
              ]
        self.option = [
                    {"name": "Assumption", "type": "checkbox", "value": ["Normality test", "Q-Q plot"]},
                     {"name": "Test Types", "type": "checkbox", "value": ["Student\'s", "Wilcoxon signed-rank"]},
                     {"name": "Hypothesis", "type": "numberText-radio", "value": {
                         "numberText": {"name": "Hypothesis", "value": 0},
                         "radio": {"name": None, "value": ["≠ Hypothesis", "> Hypothesis", "< Hypothesis"]}
                     }}
                 ]
        self.callback = {"refresh": refresh_tab}

        super(TTestOneSample, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

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

        self.connect_button_layout(self.control_panel.children[1],self.on_analyze_button_clicked )

    def on_analyze_button_clicked(self, widget):

        self.set_analyze_text('In progress...')

        # catch invalid data
        is_valid = self.validate_input_data(self.control_data)
        if not is_valid:
            return

        # get analysis data & option
        degree_freedom = len(self.input_df) - 1

        dependent_var_list = []
        for layout_var in self.control_data['Dependent Variable(s)']:
            dependent_var_list.append(self.column_value[layout_var])

        option = self.control_data['option']

        # Assumption 옵션
        option_assumption = option['Assumption']

        # Test Types 옵션
        option_test_type = option['Test Types']
        tests_students = option['Test Types']['Student\'s']
        tests_wilcoxon = option['Test Types']['Wilcoxon signed-rank']


        # Hypothesis 옵션
        option_hypothesis = option['Hypothesis']
        hypothesis_test_value = option['Hypothesis']['number']
        hypothesis_alternative = option['Hypothesis']['radio']

        if hypothesis_alternative == '≠ Hypothesis':
            hypothesis_alternative = 'two-sided'
        elif hypothesis_alternative == '> Hypothesis':
            hypothesis_alternative = 'greater'
        elif hypothesis_alternative == '< Hypothesis':
            hypothesis_alternative = 'less'

        result_widgets = self.get_result_widgets(
            degree_freedom, dependent_var_list, option_assumption, option_test_type,
            [hypothesis_test_value, hypothesis_alternative])

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):
        error_msg = CommonUtil.check_variables_shapes(control_data, 'Dependent Variable(s)', 'Number',
                                                     self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_option_checkbox(control_data, 'Test Types', 1)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        return True

    def get_result_widgets(self, degree_freedom, dependent_var_list, option_assumption, option_test_type, hypothesis_options):
        target_column_names = []
        statistic_tests_options = []
        statistic_chart = []
        statistic_result = []
        accordion_items = []
        accordion_titles = []

        # Assumption 차트 아코디언
        assumption_item = []
        table_header = ['', 'Shapiro-Wilk', 'p-value' , 'Anderson-Darling', 'Critical Value']
        table_body= []
        table_footer ="* Critical Value significance_level is 5.0"
        if option_assumption['Normality test']:
            for item in dependent_var_list:
                shapiro_statistic, shapiro_pvalue = stats.shapiro(self.input_df[item])
                AndersonResult = stats.anderson(self.input_df[item], dist = 'norm')
                table_body.append([item, round(shapiro_statistic, 3), shapiro_pvalue, round(AndersonResult[0], 1), AndersonResult[1][2] ])

            normality_table = WidgetMaker.get_styled_table(table_header, table_body,table_footer)
            assumption_item.append(normality_table)

        if option_assumption['Q-Q plot']:
            for item in dependent_var_list:
                assumption_item.append(ChartMaker.get_qq_plot_plotly(item, self.input_df[item]))

        accordion_assumption = WidgetMaker.get_vertical_box(box_items=assumption_item,
                                     style=dict(display="flex", width="100%",
                                                align_items="center", justify_content="space-around", flex_flow='row wrap'))
        if len(assumption_item) > 0 :
            accordion_items.append(accordion_assumption)
            accordion_titles.append("Assumption")

        # 통계 분석 테이블 아코디언
        table_header = ['', '', 'Statistic', 'df', 'p-value']
        table_body = []

        for item in dependent_var_list:
            target_column_names.append(item)

            if option_test_type['Student\'s']:
                Ttest_1sampResult =stats.ttest_1samp(self.input_df[item], popmean=hypothesis_options[0], alternative=hypothesis_options[1], nan_policy='omit')
                table_body.append([item, 'Student\'s', round(Ttest_1sampResult[0],2), degree_freedom, round(Ttest_1sampResult[1],3)])

            if option_test_type['Wilcoxon signed-rank']:
                first_column = item
                if option_test_type['Student\'s']:
                    first_column = ''
                wilcoxon, pvalue = stats.wilcoxon(
                    self.input_df[item], [hypothesis_options[0] for i in range(len(self.input_df[item]))] ,  alternative=hypothesis_options[1])
                table_body.append(
                    [first_column, 'Wilcoxon signed-rank', round(wilcoxon), '', round(pvalue,3)])

        statistic_analysis_table = WidgetMaker.get_styled_table(table_header, table_body)
        accordion_items.append(statistic_analysis_table)
        accordion_titles.append('Test Result(s)')

        # 데이터 분포 아코디언 생성
        for item in dependent_var_list:
            statistic_chart.append(self.input_df[item])
        accordion_item_title = "Box Plot"
        if len(self.input_df) > 10000:
            # Sampling only 10000 rows
            accordion_item_title += " (Sampling 10000 rows)"
            for index,df in enumerate(statistic_chart):
                statistic_chart[index] = df.copy().sample(n=10000, random_state=1, replace=False)

        accordion_items.append(ChartMaker.get_box_plot_plotly(statistic_chart))
        accordion_titles.append(accordion_item_title)

        return CommonWidget.get_accordion_widget(accordion_items,accordion_titles)
