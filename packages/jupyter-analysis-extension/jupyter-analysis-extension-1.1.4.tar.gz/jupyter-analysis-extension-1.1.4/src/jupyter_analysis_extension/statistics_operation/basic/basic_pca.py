import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_original import StatisticOperation
from jupyter_analysis_extension.statistics_widget.basic.basic_pca import WidgetBasicPCA
from jupyter_analysis_extension.statistics_widget.basic.basic_reliability import WidgetBasicReliability
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.utils.widget_maker import WidgetMaker


class BasicPCA(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        self.op_name = "Principal Component Analysis"
        self.sub = [
            {"name": "Variable(s)", "type": ["N"], "max_count": 0, "min_count": 1},
        ]
        self.option = [
            {"name": "Components Count", "type": "numberText", "value": 2},
            {"name": "Chart types", "type": "checkbox", "value": ['PCA plot','Scree plot', 'Matrix plot']},
            {"name": "Factor Analysis", "type": "checkbox", "value": ['KMO test', 'Bartlett test']},
        ]
        self.callback = {"refresh": refresh_tab}
        super(BasicPCA, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

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
        option_components_count = option['Components Count']
        option_chart_types = option['Chart types']
        option_factor_analysis = option['Factor Analysis']

        result_widgets = self.get_result_widgets(var_var_list, option_components_count, option_chart_types,option_factor_analysis)

        CommonUtil.update_result_layout(self.control_panel, result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):
        error_msg = CommonUtil.check_option_checkbox(control_data, 'Chart types', 0)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        error_msg = CommonUtil.check_variables_shapes(control_data, 'Variable(s)', ['Number'],
                                                      self.column_type_list, self.column_value, self.sub)
        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        if control_data['option']['Components Count'] > len(control_data['Variable(s)']) is not None:
            self.set_analyze_text('Components Count cannot be bigger than number of Variable(s)', 'warning')
            return False

        return True

    def get_result_widgets(self, var_var_list, option_components_count, option_chart_types,option_factor_analysis):

        X_ = StandardScaler().fit_transform(self.input_df[var_var_list])
        pca = PCA(n_components=len(var_var_list))
        components = pca.fit_transform(X_)
        explained_variance_ratio = pca.explained_variance_ratio_
        cum_explained_variance_ratio = np.cumsum(explained_variance_ratio)

        # Statistical Chart
        statistic_table_header = ['']
        statistic_table_body_item = ['Explained Variance(%)']
        statistic_table_body_item_2 = ['Cumulative EV(%)']
        for i in range(0, len(var_var_list)):
            statistic_table_header.append("PC" + str(i + 1))
            statistic_table_body_item.append(str(round(explained_variance_ratio[i] * 100, 2)) + "%")
            statistic_table_body_item_2.append(str(round(cum_explained_variance_ratio[i] * 100, 2)) + "%")

        statistic_table_body = [statistic_table_body_item, statistic_table_body_item_2]
        statistic_table_footer = "* Components Count " + str(option_components_count) + " is " + str(
            round(cum_explained_variance_ratio[option_components_count - 1] * 100, 2)) + "%"

        statistic_table = WidgetMaker.get_styled_table(statistic_table_header, statistic_table_body,
                                                       statistic_table_footer)

        # EDA Chart
        chart_accordion_title = "Exploratory Data Analysis(EDA) Chart"
        chart_list = []
        if option_chart_types['PCA plot']:
            chart_list.append(WidgetBasicPCA.get_pca_variance_chart(pca.explained_variance_ratio_))

        if option_chart_types['Scree plot']:
            chart_list.append(
                WidgetBasicPCA.get_scree_plot(pca.explained_variance_))

        if option_chart_types['Matrix plot']:
            pca_with_input = PCA(n_components=option_components_count)
            principal_components = pca_with_input.fit_transform(X_)
            columns_list = []
            for i in range(0, option_components_count):
                columns_list.append("PC" + str(i + 1))
            transform_df = pd.DataFrame(data=principal_components, columns=columns_list)
            chart_list.append(
                WidgetBasicPCA.get_matrix_plot(transform_df, columns_list, pca_with_input.explained_variance_ratio_))
        chart_accordion_item = WidgetMaker.get_vertical_box(box_items=chart_list,
                                                            style=dict(display="flex", width="100%",
                                                                       align_items="center", justify_content="space-around"))

        #  Factor Analysis(fa)
        fa_accordion_title = "Factor Analysis"
        fa_list = []
        if option_factor_analysis['KMO test']:
            kmo = self.calculate_kmo(self.input_df[var_var_list])
            kmo_table_header = ['', 'MSA']
            kmo_table_body = [['Overall',kmo[1]]]
            for index, item in enumerate(var_var_list):
                kmo_table_body.append([item, round(kmo[0][index],3)])

            kmo_table = WidgetMaker.get_styled_table(kmo_table_header, kmo_table_body,direation="row")
            standard_table = WidgetBasicPCA.get_kmo_standard_table()
            table_children = list(kmo_table.children)
            table_children.append(standard_table)
            kmo_table.children = tuple(table_children)
            kmo_table.layout=dict(display="flex", width="100%",align_items="center",flex_direction="row" ,justify_content="space-around")

        # if option_factor_analysis['Bartlett test']:
        #     fa_list.append(
        #         WidgetBasicPCA.get_scree_plot(pca.explained_variance_))
        #
        #
        # fa_accordion_item = WidgetMaker.get_vertical_box(box_items=fa_list,
        #                                                     style=dict(display="flex", width="100%",
        #                                                                align_items="center", justify_content="space-around"))

        return CommonWidget.get_accordion_widget([statistic_table, chart_accordion_item, kmo_table],
                                                 ['Statistical table', chart_accordion_title,fa_accordion_title])


    def calculate_kmo(self, x):
        """
        Calculate the Kaiser-Meyer-Olkin criterion
        for items and overall. This statistic represents
        the degree to which each observed variable is
        predicted, without error, by the other variables
        in the dataset. In general, a KMO < 0.6 is considered
        inadequate.
        Parameters
        ----------
        x : array-like
            The array from which to calculate KMOs.
        Returns
        -------
        kmo_per_variable : numpy array
            The KMO score per item.
        kmo_total : float
            The KMO score overall.
        """
        # calculate the partial correlations
        partial_corr = self.partial_correlations(x)

        # calcualte the pair-wise correlations
        x_corr = self.corr(x)

        # fill matrix diagonals with zeros
        # and square all elements
        np.fill_diagonal(x_corr, 0)
        np.fill_diagonal(partial_corr, 0)

        partial_corr = partial_corr**2
        x_corr = x_corr**2

        # calculate KMO per item
        partial_corr_sum = np.sum(partial_corr, axis=0)
        corr_sum = np.sum(x_corr, axis=0)
        kmo_per_item = corr_sum / (corr_sum + partial_corr_sum)

        # calculate KMO overall
        corr_sum_total = np.sum(x_corr)
        partial_corr_sum_total = np.sum(partial_corr)
        kmo_total = corr_sum_total / (corr_sum_total + partial_corr_sum_total)
        return kmo_per_item, kmo_total

    def partial_correlations(self, x):
        numrows, numcols = x.shape
        x_cov = self.cov(x, ddof=1)
        empty_array = np.empty((numcols, numcols))
        empty_array[:] = np.nan
        if numcols > numrows:
            icvx = empty_array
        else:
            try:
                assert np.linalg.det(x_cov) > np.finfo(np.float32).eps
                icvx = np.linalg.inv(x_cov)
            except AssertionError:
                icvx = np.linalg.pinv(x_cov)
            except np.linalg.LinAlgError:
                icvx = empty_array

        pcor = -1 * self.covariance_to_correlation(icvx)
        np.fill_diagonal(pcor, 1.0)
        return pcor

    def cov(self, x, ddof=0):
        r = np.cov(x, rowvar=False, ddof=ddof)
        return r


    def corr(self, x):
        x = (x - x.mean(0)) / x.std(0)
        r = self.cov(x)
        return r

    def covariance_to_correlation(self, m):
        numrows, numcols = m.shape
        if not numrows == numcols:
            raise ValueError('Input matrix must be square')

        Is = np.sqrt(1 / np.diag(m))
        retval = Is * m * np.repeat(Is, numrows).reshape(numrows, numrows)
        np.fill_diagonal(retval, 1.0)
        return retval
