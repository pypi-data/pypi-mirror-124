import pandas as pd
from tkinter import Tk, filedialog

from jupyter_analysis_extension.statistics_widget.common_widget import CommonWidget
from jupyter_analysis_extension.utils.widget_maker import WidgetMaker
import os

try:
    from mlplatform_lib.mllab import MllabApi
except ModuleNotFoundError:
    pass


class FileSelector:
    """ Custom FileSelector for pd.readCSV support """

    def __init__(self, mode=None, data=None, set_main_tab=None, logger=None):
        # data
        self.df = None

        # widget
        self.file_selector_widget = None
        self.uploaded_progress_widget = None

        # logger
        self.logger = logger

        if mode == "HD":
            hyper = MllabApi()
            hyper_do_list = {"Select DO": "Select DO"}
            hyper_do_list.update(hyper.get_do_list())

            dropdown = CommonWidget.get_dropdown(options=hyper_do_list, default_option="Select DO")
            dropdown.observe(self.on_hyper_do_click, names='value')
            self.file_selector_widget = CommonWidget.get_widget_with_label("HyperData", dropdown,
                                                                           margin="0px 0px 0px 0px")

        elif data is not None:
            # 210817 KJPARK
            if type(data) is pd.DataFrame:
                # Case: Dataframe
                self.df = data
            else:
                # Case: Path
                if os.path.exists(data):
                    self.df = pd.read_csv(data)
                else:
                    self.logger.error("File does not exist on path: %s", data)
                    exit(1)
            set_main_tab(self.df)
        else:
            self.file_selector_widget = WidgetMaker.get_btn(description="File select")
            self.file_selector_widget.on_click(self.on_file_selector_click)

        self.uploaded_progress_widget = WidgetMaker.get_html(
            value=" <div></div>",
            style=dict(margin="0px 0px 0px 10px"),
        )
        # callback
        self.set_main_tab = set_main_tab

    def on_file_selector_click(self, button):
        """ get file path by tkinter library & readCSV logic """
        self.set_file_uploading()
        root = Tk()
        root.withdraw()  # Hide the main window.
        root.call('wm', 'attributes', '.', '-topmost', True)  # Raise the root to the top of all windows.
        button.files = filedialog.askopenfilename(title="Select file", filetypes=(
        ("CSV Files", "*.csv"),))  # List of selected files will be set button's file attribute.

        if len(list(button.files)) == 0:
            return self.set_file_uploading_finish()

        self.df = pd.read_csv(str(button.files), encoding='utf-8')
        self.set_main_tab(self.df)
        self.set_file_uploading_finish()

    def on_hyper_do_click(self, value):
        """ get DataObject by Hyperdata python library & Change dataFrame """
        if value['new'] == "Select DO":
            return
        hyper = MllabApi()
        self.df = hyper.get_do(value['new'])
        self.set_main_tab(self.df)
        self.set_file_uploading_finish()

    def set_file_uploading(self):
        self.file_selector_widget.description = "Uploading.."
        self.uploaded_progress_widget.add_class("load")

    def set_file_uploading_finish(self):
        self.file_selector_widget.description = "File select"
        self.uploaded_progress_widget.remove_class("load")

    def get_file_selector_container(self):
        file_selector_container = []
        if self.file_selector_widget is not None:
            file_selector_container.append(self.file_selector_widget)

        if self.uploaded_progress_widget is not None:
            file_selector_container.append(self.uploaded_progress_widget)

        return WidgetMaker.get_vertical_box(
            box_items=file_selector_container,
            style=dict(display="flex", width="100%", align_items="center")
        )