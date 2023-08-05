import json
import logging
import os
import webbrowser
from abc import *

import pdfkit
import imgkit
from ipywidgets.embed import dependency_state, embed_data
import ipywidgets as widgets
from jupyter_analysis_extension.utils.export_info import HTML_TEMPLATE, WIDGET_VIEW_TEMPLATE, convert_html_to_pdf
from jupyter_analysis_extension.utils.logger import OutputWidgetHandler


class StatisticOperation:
    """operation default class"""
    # Type Hint
    info_widgets: widgets.Accordion()
    result_widgets: widgets.Accordion()
    logger: logging.Logger

    # main integrated widget
    control_panel = None

    def __init__(self, op_name, df, column_type_list, refresh_tab, logger):
        # Data
        self.info_widgets = None
        self.result_widgets = None
        self.input_df = df
        self.column_type_list = column_type_list
        self.op_name = op_name

        self.column_value = {}
        self.control_data = None

        # Widget & Layout
        self.control_panel = None
        self.analyze_layout = None
        self.analyze_textfield = None
        self.refresh_textfield = None

        # func
        self.refresh_tab = refresh_tab

        # log
        self.logger = logger
        self.construct_control_panel()

    @abstractmethod
    def construct_control_panel(self):
        pass

    @abstractmethod
    def on_analyze_button_clicked(self, widget):
        pass

    def refresh_tab(self):
        if self.analyze_textfield is not None:
            self.analyze_textfield.value = ""

        if self.refresh_textfield is not None:
            self.refresh_textfield.value = ""
        return

    def get_tab_widget(self):
        return self.control_panel

    def connect_button_layout(self, button_layout, analyze_btn_event):
        """

        Parameters
        ----------
        button_layout
            button-textField widget layout
        analyze_btn_event
            trigger analyze btn event
        -------
        """
        button_layout = button_layout
        self.analyze_textfield = button_layout.children[0].children[0]
        self.refresh_textfield = button_layout.children[0].children[1]
        button_layout.children[1].children[0].on_click(analyze_btn_event)

    def set_analyze_text(self, text, mode="plain"):
        """

        Parameters
        ----------
        text
            real textField string
        mode
            plain | warning
        """
        target_text = """<div style="display:flex;justify-content:flex-end">{0}</div>""".format(
            text)
        if mode == "warning":
            target_text = """<div style="font-size:1.5rem;color:red;display:flex;justify-content:flex-end">{0}</div>""".format(
                text)
        self.analyze_textfield.value = target_text

    def set_refresh_text(self, text):
        """

        Parameters
        ----------
        text
            real textField string
        """
        if hasattr(self, "refresh_textfield"):
            self.refresh_textfield.value = """<div style="font-size:1.5rem;color:red;display:flex;justify-content:flex-end">{0}</div>""".format(
                text)

    def on_export_html_button_clicked(self, widget):
        self.create_html_file(file_name=self.op_name + ".html")

    def on_export_pdf_button_clicked(self, widget):
        self.create_html_file(file_name=self.op_name + ".html", open_tab=False)
        # convert_html_to_pdf(self.op_name + ".html", self.op_name + ".pdf")
        imgkit.from_file(self.op_name + ".html", self.op_name + ".png")
        os.remove(self.op_name + ".html")
        webbrowser.open_new_tab(self.op_name + ".png")

    def create_html_file(self, file_name, open_tab=True):
        # Simple version
        # embed_minimal_html('export2.html', views=widget, state=dependency_state(widget))

        # Customized version (**)
        data = embed_data(views=self.info_widgets.children)

        manager_state = data['manager_state']
        manager_state["state"] = dependency_state(self.info_widgets.children)
        widget_views = [json.dumps(view) for view in data['view_specs']]
        widget_agg_views = ""
        for i, widget_view in enumerate(widget_views):
            widget_agg_views += WIDGET_VIEW_TEMPLATE.format(title=self.info_widgets.get_title(i), num=i,
                                                            widget_view=widget_view)

        rendered_template = HTML_TEMPLATE.format(title=self.op_name, manager_state=json.dumps(manager_state),
                                                 widget_views=widget_agg_views)
        with open(file_name, 'w') as fp:
            fp.write(rendered_template)

        if open_tab:
            webbrowser.open_new_tab(file_name)

