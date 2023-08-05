#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.

# GUI

import ipywidgets as widgets
import qgrid
from IPython import get_ipython
from IPython.display import display

from jupyter_analysis_extension.utils.logger import OutputWidgetHandler
#from nbformat import v4 as nbf
# from nbformat import current as nbf
import nbformat
from nbformat import v4 as nbf

# Hyderdata

try:
    import hyper
except ModuleNotFoundError:
    pass

# Common Class
from jupyter_analysis_extension.utils.widget_style import WidgetStyle
from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil

# Statistic basic
from jupyter_analysis_extension.statistics_operation.basic.basic_analysis import BasicAnalysis

# Statistic ANOVA
from jupyter_analysis_extension.statistics_operation.anova.anova_oneway import ANOVAOneWay
from jupyter_analysis_extension.statistics_operation.anova.anova_ancova import ANOVAANCOVA
from jupyter_analysis_extension.statistics_operation.anova.anova_kruskal import ANOVAKruskal
from jupyter_analysis_extension.statistics_operation.anova.anova_rm import ANOVARM

# Statistic Regression
from jupyter_analysis_extension.statistics_operation.regression.general_linear_regression import GeneralLinearRegression
from jupyter_analysis_extension.statistics_operation.regression.logistic_regression import LogisticRegression

# Statistic T-test
from jupyter_analysis_extension.statistics_operation.t_test.t_test_one_sample import TTestOneSample
from jupyter_analysis_extension.statistics_operation.t_test.t_test_ind_sample import TTestIndSample
from jupyter_analysis_extension.statistics_operation.t_test.t_test_pair_sample import TTestPairSample

# Statistic Frequencies
from jupyter_analysis_extension.statistics_operation.frequencies.frequencies_chi_square import FrequenciesChiSquare
from jupyter_analysis_extension.statistics_operation.frequencies.frequencies_mcnemar import FrequenciesMcnemar

import logging
from jupyter_analysis_extension.utils.file_selecter import FileSelector

OPERATION_LIST = {
    "Basic" : ["Basic : Analysis"],
    "T-test": ['T-Test : One Sample', 'T-Test : Independent Sample', 'T-Test : Paired Sample'],
    "ANOVA": ['One-way ANOVA', 'ANOVA (Kruskal-Wallis)', 'Repeated Measure ANOVA', 'ANOVA & ANCOVA'],
    "Regression": ['Linear Regression', 'Logistic Regression'],
    "Frequencies": ['Frequencies : Chi-Square', "Frequencies : McNemar"]
}


class WidgetGuide:
    def __init__(self, mode=None, data=None, debug=False):
        WidgetStyle.style_default()

        self.output = widgets.Output()

        self.tab = widgets.Tab()
        self.tab_count = 0
        self.tab_titles = []
        self.tab_children = []

        self.active_op_class = []
        self.combobox = None

        self.input_df = None
        self.column_type_dict = None
        self.mode = mode

        # Logging
        if debug:
            self.logger = logging.getLogger(__name__)
            handler = OutputWidgetHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s  - [%(levelname)s] %(message)s'))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
            handler.show_logs()

        self.FileSelector = FileSelector(mode, data, self.set_main_frame, self.logger)
        display(self.FileSelector.get_file_selector_container())

    def set_main_frame(self, df):
        # start_time = time.time()
        # self.reset_widget()
        # self.logger.info(time.time() - start_time)
        self.input_df = df

        # Sampling only 10000 rows
        max_len = 10000

        sampled_df = self.input_df.copy()
        if len(self.input_df) > max_len:
            sampled_df = sampled_df.sample(n=max_len, random_state=1, replace=False)

        qgrid_widget = qgrid.show_grid(sampled_df, show_toolbar=False)

        self.column_type_dict = self.get_type_dict()
        type_widget = self.get_type_dict_accordion(self.column_type_dict)

        qgrid_widget_width_label = CommonWidget.get_widget_with_label("Table Info (10,000 Rows Sampled)", qgrid_widget)

        menu_widgets = []
        for key in OPERATION_LIST.keys():
            menu_widget = CommonWidget.get_popup_menu(
                op_category=key,
                items=OPERATION_LIST[key],
                click_event=self.on_append_tab)
            menu_widgets.append(menu_widget)

        menu_layout = CommonWidget.get_hbox(menu_widgets, justify_content="flex-start")
        menu_layout.add_class("icon_menu")
        menu_layout_with_label = CommonWidget.get_widget_with_label("Operation Type", menu_layout)
        menu_layout_with_label.add_class("icon_menu")
        self.tab_children = [widgets.VBox(
            [menu_layout_with_label,qgrid_widget_width_label, type_widget])]

        self.tab_titles = ['Main']

        self.tab.children = self.tab_children
        self.tab.set_title(self.tab_count, self.tab_titles[self.tab_count])
        self.tab_count += 1

        display(self.tab)

    def reset_widget(self):
        self.tab.close_all()
        self.output.clear_output()
        self.output.close_all()
        self.__init__()

    def refresh_tab(self, target_op):
        target_widget = self.get_operation_widget(target_op)
        tab_children = list(self.tab.children)
        tab_children[self.tab.selected_index] = target_widget
        self.tab.children = tuple(tab_children)

    def on_func_selected(self, value):
        if value['name'] == 'value' and value['new'] != {} and value['new'] != "":
            if value['owner'].options[0] == value['new']:
                return
            op_name = value['new']
            self.on_append_tab(op_name)
            value['owner'].index = 0

    def on_append_tab(self, op_name):
        if op_name not in self.tab_titles:
            self.tab_children.append(self.get_operation_widget(op_name))
            self.tab_titles.append(op_name)
            self.tab.children = self.tab_children
            self.tab.set_title(
                self.tab_count, self.tab_titles[self.tab_count])
            self.tab.selected_index = self.tab_count
            self.tab_count += 1
        else:
            self.tab.selected_index = self.tab_titles.index(op_name)

    def on_type_changed(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            self.column_type_dict[change['owner'].description] = change['new']
            for op_class in self.active_op_class:
                op_class.set_refresh_text(
                    str("Column types changed! Please refresh the tab (e.g., " + change['owner'].description)
                    + "'s type -> " + str(change['new']) + ").")
        return

    def get_type_dict(self):
        column_type_dict = {}
        for column in self.input_df.columns:
            abstract_type = CommonUtil.get_abstract_type(
                self.input_df[column])
            column_type_dict[column] = abstract_type
        return column_type_dict

    def get_type_dict_accordion(self, column_type_dict):
        accordion_widget_children = []
        for key in list(column_type_dict.keys()):
            avail_type_list = CommonUtil.get_avail_type_list(
                self.input_df[key])
            dropdown_with_label = CommonWidget.get_dropdown_with_description(
                key, avail_type_list, column_type_dict[key])
            accordion_widget_children.append(dropdown_with_label)
            dropdown_with_label.observe(self.on_type_changed)

        accordion_widget = widgets.Accordion(
            children=[widgets.VBox(accordion_widget_children,
                                   layout=widgets.Layout(margin="0px", width="100%", display="flex",
                                                         flex_flow="wrap"))], selected_index=None,
            layout=widgets.Layout(margin="0px", width="100%"))
        accordion_widget.set_title(0, "Controls of Column Types")
        return accordion_widget

    def get_operation_widget(self, op_name):
        result_widget = None
        target_op = None
        if op_name == "Basic : Analysis":
            self.logger.info("entered")
            nb = nbf.new_notebook()
            cell = nbf.new_code_cell("ss")
            nb.cells.extend(cell)
            with open('Untitled_guide.ipynb', 'w') as f:
                nbformat.write(nb, f)
        else:
            result_widget = widgets.Text(description="New Tab")

        result_widget = target_op.get_tab_widget()

        if target_op is not None:
            self.active_op_class.append(target_op)

        return result_widget
