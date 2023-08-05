from abc import *

class StatisticOperation:
    """operation default class"""
    # main integrated widget
    control_panel = None

    def __init__(self, op_name, df, column_type_list, refresh_tab, logger):
        # Data
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

    def refresh_tab(self):
        if self.analyze_textfield is not None:
            self.analyze_textfield.value=""

        if self.refresh_textfield is not None:
            self.refresh_textfield.value=""
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
        self.button_layout = button_layout
        self.analyze_textfield = button_layout.children[0].children[0]
        self.refresh_textfield = button_layout.children[0].children[1]
        self.button_layout.children[1].children[0].on_click(analyze_btn_event)

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