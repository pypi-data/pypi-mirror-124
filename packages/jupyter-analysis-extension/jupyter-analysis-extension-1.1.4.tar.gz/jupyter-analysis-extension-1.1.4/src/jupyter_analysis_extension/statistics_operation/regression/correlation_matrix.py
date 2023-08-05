#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
import json
import logging
from itertools import combinations
import numpy as np
from ipywidgets import IntSlider
from ipywidgets.embed import embed_minimal_html, embed_data, dependency_state
from scipy.stats import pearsonr, spearmanr, kendalltau

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.statistics_operation.statistic_op import StatisticOperation
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget

# Graph
from jupyter_analysis_extension.statistics_widget.regression.correlation_matrix import WidgetCorrelationMatrix
from jupyter_analysis_extension.utils.preprocess import preprocess_values


class CorrelationMatrix(StatisticOperation):
    def __init__(self, df, column_type_list, refresh_tab, logger):
        # Additional init codes for specific operations.
        self.op_name = "Correlation Matrix"
        self.sub = [
            {"name": "Variables", "type": ["N"], "max_count": 0, "min_count": 2}
        ]
        self.option = [
            {"name": "Correlation Coefficients", "type": "checkbox",
             "value": ["Pearson", "Spearman", "Kendall's tau-b"]},
            {"name": "Additional Options", "type": "checkbox",
             "value": ["Report significance (p-value)"]}
        ]
        self.callback = {"refresh": refresh_tab}

        super(CorrelationMatrix, self).__init__(self.op_name, df, column_type_list, refresh_tab, logger)

    def construct_control_panel(self):
        """
        Construct the overall visual frames of correlation matrix.
        Returns
        -------
        None
        """
        #                 {"name": "Hypothesis", "type": "radio",
        #                  "value": ["Correlated", "Correlated positively", "Correlated negatively"]}
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
        """
        Perform the check of column types and the creation of analysis results of accordion widgets.
        Returns
        -------
        None
        """
        self.set_analyze_text('In progress...')

        # catch invalid data
        is_valid = self.validate_input_data(self.control_data)
        if not is_valid:
            return

        obj_vars = None
        if 'Variables' in self.control_data.keys():
            obj_vars = []
            for item in self.control_data['Variables']:
                obj_vars.append(self.column_value[item])

        option = self.control_data['option']
        corr_coefficients = [x for x in option["Correlation Coefficients"].keys() if
                             option["Correlation Coefficients"][x] is True]
        addi_ops = [x for x in option["Additional Options"].keys() if option["Additional Options"][x] is True]
        # hypo = option["Hypothesis"]['radio']

        self.result_widgets = self.get_result_widgets(obj_vars, corr_coefficients, addi_ops)

        CommonUtil.update_result_layout(self.control_panel, self.result_widgets)

        self.set_analyze_text('Done.')

    def validate_input_data(self, control_data):
        """
        Check the requirement numbers of columns and types.
        Returns
        -------
        str
            None if successful, error message otherwise.
        """
        error_msg = CommonUtil.check_variables_shapes(control_data, 'Variables', 'Number',
                                                      self.column_type_list, self.column_value, self.sub)

        if error_msg is not None:
            self.set_analyze_text(error_msg, 'warning')
            return False

        return True

    def get_result_widgets(self, var_names, corr_coefficients, addi_ops):
        # self.logger.info(corr_coefficients)
        # self.logger.info(addi_ops)
        # self.logger.info(hypo)

        plot_list, title_list = self.get_correlation_matrix_info(var_names, corr_coefficients, addi_ops)

        # Set the info widgets for exporting
        self.info_widgets = CommonWidget.get_accordion_widget(plot_list, title_list)

        # Export Info
        # release 1.0.0 대비 비활성화 처리
        # # HTML
        # export_html_button = CommonWidget.get_button_with_icon('export-html')
        # export_html_button.on_click(self.on_export_html_button_clicked)
        #
        # # PDF
        # # export_pdf_button = CommonWidget.get_button_with_icon('export-pdf')
        # # export_pdf_button.on_click(self.on_export_pdf_button_clicked)
        #
        # # export_layout = CommonWidget.get_export_layout(export_html_button, export_pdf_button)
        # export_layout = CommonWidget.get_export_layout(export_html_button)
        # plot_list.append(export_layout)
        #
        # title_list.append("Export Results")
        return CommonWidget.get_accordion_widget(plot_list, title_list)

        # self.result_widgets = CommonWidget.add_export_layout_on_accordion(self.result_widgets, export_html_button)

    def get_correlation_matrix_info(self, var_names, corr_coefficients, addi_ops):
        result_plot = []
        result_title = []

        EDA_plot_title = "Exploratory Data Analysis (EDA)"
        sampled_df = self.input_df.copy()
        if len(self.input_df) > 10000:
            EDA_plot_title += " (Sampling 10000 rows)"
            # Sampling only 10000 rows
            sampled_df = sampled_df.sample(n=10000, random_state=1, replace=False)
        # EDA Plot
        eda_plot = WidgetCorrelationMatrix.get_all_scatter_plot(sampled_df, var_names)

        result_plot.append(eda_plot)
        result_title.append(EDA_plot_title)

        # Corr Info
        corr_info = {}
        for combo in combinations(var_names, 2):
            df = self.input_df[[combo[0], combo[1]]]
            df = preprocess_values(df)

            x = np.array(df[combo[0]])
            y = np.array(df[combo[1]])

            corr_info[combo] = {}
            if "Pearson" in corr_coefficients:
                corr_info[combo]["Pearson(corr)"], corr_info[combo]["Pearson(p)"] = pearsonr(x, y)
                corr_info[combo]["Pearson(corr)"] = round(corr_info[combo]["Pearson(corr)"], 4)
                corr_info[combo]["Pearson(p)"] = "< 0.001" if corr_info[combo]["Pearson(p)"] < 0.001 else \
                    round(corr_info[combo]["Pearson(p)"], 4)
            if "Spearman" in corr_coefficients:
                corr_info[combo]["Spearman(corr)"], corr_info[combo]["Spearman(p)"] = spearmanr(x, y)
                corr_info[combo]["Spearman(corr)"] = round(corr_info[combo]["Spearman(corr)"], 4)
                corr_info[combo]["Spearman(p)"] = "< 0.001" if corr_info[combo]["Spearman(p)"] < 0.001 else \
                    round(corr_info[combo]["Spearman(p)"], 4)
            if "Kendall's tau-b" in corr_coefficients:
                corr_info[combo]["Kendall's tau-b(corr)"], corr_info[combo]["Kendall's tau-b(p)"] = kendalltau(x, y)
                corr_info[combo]["Kendall's tau-b(corr)"] = round(corr_info[combo]["Kendall's tau-b(corr)"], 4)
                corr_info[combo]["Kendall's tau-b(p)"] = "< 0.001" if corr_info[combo]["Kendall's tau-b(p)"] < 0.001 \
                    else round(corr_info[combo]["Kendall's tau-b(p)"], 4)

        stat_result_table = WidgetCorrelationMatrix.get_statistic_result_table(corr_info, corr_coefficients, addi_ops)

        result_plot.append(stat_result_table)
        result_title.append("Correlation Matrix")

        return result_plot, result_title
