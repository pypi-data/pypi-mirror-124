#!/usr/bin/env python
# coding: utf-8

# Graph
from itertools import chain, combinations

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
import ipywidgets as widgets
from ipyevents import Event
from ipywidgets.widgets.widget_layout import Layout

from jupyter_analysis_extension.statistics_operation.common_util import CommonUtil
from jupyter_analysis_extension.utils.icon_info import BASIC_ICON, T_TEST_ICON, ANOVA_ICON, REGRESSION_ICON, FREQUENCIES_ICON
from jupyter_analysis_extension.utils.widget_maker import WidgetMaker


class CommonWidget:
    @staticmethod
    def make_control_panel(df=None, type_list=None, title="Unknown", sub=None, option=None, callback=None):
        if callback is None:
            callback = {}
        if option is None:
            option = []
        if sub is None:
            sub = []
        if type_list is None:
            type_list = []

        control_data = {}
        # header
        header_widget = CommonWidget.get_header_widget(title)
        control_data["title"] = title

        column_name_type_map = CommonUtil.get_column_name_with_type(df.columns, type_list)
        control_data["column"] = column_name_type_map

        main_layout = CommonWidget.get_multiple(list(column_name_type_map), '300px')
        control_data["main"] = list(column_name_type_map)

        sub_item_list = []
        item_multiple_dict = {}
        add_btn_list = []
        delete_btn_list = []
        for item in sub:
            item_multiple = CommonWidget.get_multiple([], '100%')
            add_button = CommonWidget.get_add_button()
            delete_button = CommonWidget.get_delete_button()
            if item['max_count'] > 0:
                item_layout = CommonWidget.get_limit_multiple_with_button_layout(item["name"], item_multiple,
                                                                                 item['max_count'], add_button,
                                                                                 delete_button)
            else:
                item_layout = CommonWidget.get_multiple_with_button_layout(item["name"], item_multiple, add_button,
                                                                           delete_button)
            item_multiple_dict[item["name"]] = item_multiple
            add_btn_list.append(add_button)
            delete_button.layout = Layout(width="40px", display="none")
            delete_btn_list.append(delete_button)
            CommonUtil.connect_multiples_by_button(
                control_data, "main", main_layout, item["name"], item_multiple, add_button, delete_button,
                max_count=item['max_count'])
            sub_item_list.append(item_layout)

        def on_main_selected(value):
            for btn in delete_btn_list:
                btn.layout = Layout(width="40px", display="none", margin="0px")
            for btn in add_btn_list:
                btn.layout = Layout(width="40px", display="",margin="0px")

        main_layout.observe(on_main_selected, names='value')

        def on_sub_selected(value):
            for btn in add_btn_list:
                btn.layout = Layout(width="40px", display="none",margin="0px")
            for btn in delete_btn_list:
                btn.layout = Layout(width="40px", display="",margin="0px")

        for key in item_multiple_dict.keys():
            item_multiple_dict[key].observe(on_sub_selected, names='value')

        # combine sub
        sub_layout = CommonWidget.get_sub_layout(sub_item_list, "300px")

        # layout
        column_layout = CommonWidget.get_column_layout(
            header_widget, main_layout, sub_layout)

        # option layout
        option_left_item_list = []
        option_center_item_list = []
        option_right_item_list = []
        control_data["option"] = {}
        for item in option:
            if item["type"] == "checkbox":
                item_widget = CommonWidget.get_checkbox(control_data["option"], item["name"], item["value"])

            elif item["type"] == "radio":
                item_widget = CommonWidget.get_radio_buttons(control_data["option"], item["name"], item["value"], 0)

            elif item["type"] == "numberText":
                item_widget = CommonWidget.get_number_text(control_data["option"], item["name"], item["value"])

            elif item["type"] == "numberText-radio":
                widget_value = item["value"]
                item_widget = CommonWidget.get_number_field_and_radio_buttons(
                    control_data["option"],
                    item["name"],
                    widget_value["numberText"]["name"],
                    widget_value["numberText"]["value"],
                    widget_value["radio"]["value"], 0)

            elif item["type"] == "connected_multiple":
                connect_target_widgets = []
                for target in item["connect"]:
                    connect_target_widgets.append(item_multiple_dict[target])
                item_widget = CommonWidget.get_connected_multiple(control_data["option"], item["name"],
                                                                         item["acc_title"],
                                                                         item["value"], connect_target_widgets,
                                                                         column_name_type_map, type_list)

            elif item["type"] == "connected_unique_dropdown":
                connect_target_widget = item_multiple_dict[item["connect"]]
                item_widget = CommonWidget.get_connected_dropdown(control_data["option"], item["name"],
                                                                         connect_target_widget, column_name_type_map,
                                                                         type_list, df=df,
                                                                         place_holder=str(
                                                                             "Check the value of " + item["connect"]))

            elif item["type"] == "individual_connected_unique_dropdown":
                connect_target_widgets = []
                for connect_item in item["connect"]:
                    connect_target_widgets.append(item_multiple_dict[connect_item])

                acc_title = item["acc_title"] if "acc_title" in item else item["name"]
                item_widget = CommonWidget.get_individual_connected_dropdown(control_data["option"],
                                                                                               item["name"],
                                                                                               connect_target_widgets,
                                                                                               column_name_type_map,
                                                                                               type_list, df=df,
                                                                                               acc_title=acc_title)

            elif item["type"] == "individual_connected_unique_numberField":
                connect_target_widgets = []
                for connect_item in item["connect"]:
                    connect_target_widgets.append(item_multiple_dict[connect_item])

                acc_title = item["acc_title"] if "acc_title" in item else item["name"]
                item_widget = WidgetMaker.get_individual_connected_unique_numberField(control_data["option"],
                                                                                               item["name"],
                                                                                               connect_target_widgets,
                                                                                               column_name_type_map,
                                                                                               type_list, df=df,
                                                                                               acc_title=acc_title)
            else:
                print("Type is incorrect in option widgets.")
                item_widget = None

            if item_widget is not None:
                widget_with_label = CommonWidget.get_widget_with_label(item["name"], item_widget, margin="0px 0px 0px 5px")

                if "position-column" in item:
                    if item["position-column"] == "center":
                        option_center_item_list.append(widget_with_label)
                    elif item["position-column"] == "right" :
                        option_right_item_list.append(widget_with_label)
                    else:
                        option_left_item_list.append(widget_with_label)
                else:
                    option_left_item_list.append(widget_with_label)

        option_layout = CommonWidget.get_option_layout(option_left_item_list,option_center_item_list,option_right_item_list )

        # analyze layout
        analyze_button = CommonWidget.get_button_with_icon('analyze')
        refresh_button = CommonWidget.get_button_with_icon('refresh')

        def on_refresh_button_clicked(self):
            if "refresh" in callback:
                callback["refresh"](title)

        refresh_button.on_click(on_refresh_button_clicked)

        analyze_textfield = CommonWidget.get_textfield()
        refresh_textfield = CommonWidget.get_textfield()

        analyze_layout = CommonWidget.get_analyze_layout([analyze_textfield, refresh_textfield],
                                                         [analyze_button, refresh_button])

        result_layout = CommonWidget.get_result_layout()

        control_panel = CommonWidget.get_control_panel_widget(
            column_layout,
            option_layout,
            analyze_layout,
            result_layout)
        return control_panel, control_data

    @staticmethod
    def get_dropdown_with_description(title, options, default_option):
        if default_option not in options:
            default_option = options[0]

        return widgets.Dropdown(
            options=options,
            value=default_option,
            description=title,
            layout=widgets.Layout(height="99%", width="300px",margin="0"),
            style=dict(description_width='150px')
        )

    @staticmethod
    def get_dropdown(options, default_option):
        if default_option not in options:
            default_option = options[0]

        return widgets.Dropdown(
            options=options,
            value=default_option,
            layout=widgets.Layout(height="99%", width="200px",margin="0"),
            style=dict(description_width='100px')
        )

    #
    # layout widget
    #
    # multiple widget #
    @staticmethod
    def get_multiple(columns, height, width="95%"):
        return widgets.SelectMultiple(
            options=columns,
            disabled=False,
            style=dict(description_width='initial'),
            layout=widgets.Layout(
                height=height, width=width, margin='0')
        )

    @staticmethod
    def get_limit_multiple_with_button_layout(label, target_multiple, max_count, add_button, delete_button):
        layout_label = widgets.HTML(
            value=label, layout=widgets.Layout(height="25px", margin="0px"))
        layout_label.add_class("multiple-select-title")
        hidden_button = CommonWidget.get_hidden_button()

        max_height = max_count * 20 + 33
        multiple_height = max_count * 20 + 8
        target_multiple.layout = Layout(width="95%", height=str(multiple_height) + "px", margin="0")
        return widgets.VBox([
            widgets.HBox([hidden_button, layout_label],
                         layout=widgets.Layout(display="flex", justify_content="flex-start", min_height="25px",
                                               margin="0")
                         ),
            widgets.HBox(
                [widgets.VBox([add_button, delete_button],
                              layout=widgets.Layout(display="flex", justify_content="flex-start", width="45px",
                                                    height="100%", margin="0")),
                 widgets.VBox([target_multiple],
                              layout=widgets.Layout(display="flex", align_items="flex-start", width="calc(100% - 45px)",
                                                    height="100%", margin="0"))
                 ],
                layout=widgets.Layout(height="100%", display="flex", margin="0")
            )
        ], layout=widgets.Layout(min_height=str(max_height) + "px", width="300px", display="flex"))

    @staticmethod
    def get_multiple_with_button_layout(label, target_multiple, add_button, delete_button, width="300px"):
        layout_label = widgets.HTML(
            value=label, layout=widgets.Layout(height="25px", margin="0px"))
        layout_label.add_class("multiple-select-title")
        hidden_button = CommonWidget.get_hidden_button()

        return widgets.VBox([
            widgets.HBox([hidden_button, layout_label],
                         layout=widgets.Layout(display="flex", justify_content="flex-start", min_height="25px",
                                               margin="0")
                         ),
            widgets.HBox(
                [widgets.VBox([add_button, delete_button],
                              layout=widgets.Layout(display="flex", justify_content="flex-start", width="45px",
                                                    height="100%",margin="0")),
                 widgets.VBox([target_multiple],
                              layout=widgets.Layout(display="flex", align_items="flex-start", width="calc(100% - 45px)",
                                                    height="100%", margin="0"))
                 ],
                layout=widgets.Layout(height="100%",display="flex", margin="0")
            )
        ], layout=widgets.Layout(height="100%", width=width, display="flex", margin="0", padding="1px 0px 1px 0px"))

    @staticmethod
    def get_multiple_with_label(label, target_multiple, width="300px"):
        layout_label = widgets.HTML(
            value=label, layout=widgets.Layout(height="25px", margin="0"))
        layout_label.add_class("multiple-select-title")

        return widgets.HBox([
            widgets.VBox([layout_label, target_multiple],
                         layout=widgets.Layout(display="flex", align_items="flex-start", width="100%", height="100%",
                                               margin="0"))
        ], layout=widgets.Layout(height="100%", width=width, display="flex", margin="0"))

    # button widget #
    @staticmethod
    def get_add_button():
        return widgets.Button(
            disabled=False,
            tooltip='add',
            icon='arrow-right',
            layout=widgets.Layout(width="40px", margin="0px"))

    @staticmethod
    def get_hidden_button():
        return widgets.Button(
            disabled=False,
            tooltip='add',
            icon='refresh',
            layout=widgets.Layout(width="45px", visibility="hidden", height="25px", margin="0px"))

    @staticmethod
    def get_delete_button():
        return widgets.Button(
            disabled=False,
            button_style='',
            tooltip='delete',
            icon='arrow-left',
            layout=widgets.Layout(width="40px", margin="0px"))

    @staticmethod
    def get_button_with_icon(icon_type):
        if icon_type == 'analyze':
            button_widget = widgets.Button(
                description='Analyze',
                disabled=False,
                button_style='',
                tooltip='Analyze',
                icon='search',
            )

        elif icon_type == 'refresh':
            button_widget = widgets.Button(
                description='Refresh',
                disabled=False,
                button_style='',
                tooltip='Refresh',
                icon='refresh',
            )
        elif icon_type == 'export-html':
            button_widget = widgets.Button(
                description='Export to HTML',
                disabled=False,
                button_style='',
                tooltip='Export to HTML',
                icon='browser',
            )
        elif icon_type == 'export-pdf':
            button_widget = widgets.Button(
                description='Export to PDF',
                disabled=False,
                button_style='',
                tooltip='Export to PDF',
                icon='file-pdf',
            )
        else:
            button_widget = None
            exit(1)
        button_widget.add_class("round-button-5")
        return button_widget

    @staticmethod
    def get_warning_textfield(warning_text):
        return widgets.HTML(
            value=warning_text)

    @staticmethod
    def get_textfield(text="&nbsp"):
        return widgets.HTML(
            value="""<div style="display:flex;justify-content:flex-end">{0}</div>""".format(
                text))

    @staticmethod
    def get_hbox(items, justify_content="center"):
        return widgets.HBox(
            items,
            layout=widgets.Layout(display="flex", width="100%", min_width="600px", justify_content=justify_content),
        )

    @staticmethod
    def get_vbox(items, justify_content="center"):
        return widgets.VBox(
            items,
            layout=widgets.Layout(display="flex", width="100%", min_width="600px", justify_content=justify_content),
        )

    @staticmethod
    def get_header_widget(test_name):
        children = [
            widgets.HTML(
                value="""<div style="font-size:2rem">{0}</div>""".format(test_name)),
        ]
        box_layout = Layout(display='flex',
                            border_bottom='1px solid gray',
                            width='100%')
        return widgets.Box(children=children, layout=box_layout)

    @staticmethod
    def get_analyze_layout(text_field, button):
        text_list = []
        button_list = []
        if isinstance(text_field, list):
            text_list = text_field
        else:
            text_list.append(text_field)

        if isinstance(button, list):
            button_list = button
        else:
            button_list.append(button)

        return widgets.HBox(
            [widgets.VBox(text_list), widgets.VBox(button_list)],
            layout=widgets.Layout(display="flex", height="100%", align_items="flex-end", width="100%",
                                  justify_content="flex-end"))

    @staticmethod
    def get_sub_layout(target, height="100%"):
        return widgets.VBox(target,
                            layout=widgets.Layout(display="flex", height=height, align_items="flex-end", width="100%"))

    @staticmethod
    def get_column_layout(header, var_layout, target_layout):
        return widgets.VBox([
            header,
            widgets.HBox(
                [var_layout, target_layout],
                layout=widgets.Layout(display="flex", width="100%", min_width="600px", justify_content="flex-end")),
        ])

    @staticmethod
    def get_option_layout(option_left_item_list,option_center_item_list,option_right_item_list):
        children = [
            widgets.HTML(
                value="""<div style="font-size:2rem; padding-top:calc(2rem + 4px)">Option</div>"""),
        ]
        option_title = [widgets.Box(children=children, layout=widgets.Layout(display='flex',
                            border_bottom='1px solid gray',
                            width='100%'))]
        layout_children = []
        if len(option_left_item_list) + len(option_center_item_list) +  len(option_right_item_list)> 0:
            left_list = widgets.VBox(option_left_item_list, layout=widgets.Layout(display="flex"))
            center_list = widgets.VBox(option_center_item_list, layout=widgets.Layout(display="flex"))
            right_list = widgets.VBox(option_right_item_list, layout=widgets.Layout(display="flex"))
            option_layout = widgets.HBox([left_list, center_list, right_list])
            layout_children = option_title + [option_layout]
        return widgets.VBox(layout_children,
                            layout=widgets.Layout(display="flex", height="100%", min_height="300px",
                                                  justify_content="flex-start"))

    @staticmethod
    def get_result_layout():
        return widgets.VBox([], layout=widgets.Layout(display='flex', justify_content='center', width="100%"))

    @staticmethod
    def get_control_panel_widget(colmun_layout, option_layout, analyze_layout, result_layout):
        default_style = Layout(display='flex', width="99%",
                               align_items='flex-start', justify_content="center")
        control_panel_widget = widgets.VBox(
            [widgets.HBox([colmun_layout, option_layout], layout=default_style), analyze_layout, result_layout],
            layout=default_style)

        return control_panel_widget

    # @staticmethod
    # def get_box_plot_plotly(data_list):
    #     f = go.FigureWidget()
    #     for data in data_list:
    #         f.add_trace(go.Box(y=data, name=data.name))
    #     return f

    @staticmethod
    def get_accordion_widget(widget_list, title_list, selected_index=0, min_width="10px"):
        accordion_widget = widgets.Accordion(
            children=widget_list,
            layout=widgets.Layout(width="100%", display="flex", justify_content='center', margin="0", min_width=min_width),
            selected_index=selected_index)
        for i in range(len(accordion_widget.children)):
            accordion_widget.set_title(i, title_list[i])
        return accordion_widget

    @staticmethod
    def get_widget_with_label(label_text, widget, orientation="v", margin="0"):
        label = widgets.HTML(
            value="""<div style="font-size:1.5rem; font-weight:bold">{0}</div>""".format(label_text),
            layout=widgets.Layout(width="100%", min_height="25px", margin="0"))
        if orientation == "v":
            result = widgets.VBox(
                [label, widget],
                layout=widgets.Layout(margin=margin))
        else:
            result = widgets.HBox(
                [label, widget],
                layout=widgets.Layout(margin=margin))
        return result


    @staticmethod
    def get_file_meta_widget(file_name, file_size, file_type):
        format_size = str(round(file_size/1024)) + "KB" if file_size < 1024*1024 else str(round(file_size/1024/1024,2)) + "MB"
        file_name_widget = widgets.HTML(
            value=file_name,
            description='Name : ',
            style=dict(description_width='70px')
        )
        file_size = widgets.HTML(
            value=format_size,
            description='Size : ',
            style=dict(description_width='70px')
        )
        file_type = widgets.HTML(
            value=file_type,
            description='Type : ',
            style=dict(description_width='70px')
        )
        file_meta_widget = widgets.VBox([file_name_widget,file_size,file_type], layout=widgets.Layout(margin='0px 0px 0px 10px'))
        return file_meta_widget
    #
    # option widget
    #
    @staticmethod
    def get_radio_buttons(control_data_option, title, values, default_value_index=0):
        control_data_option[title] = {}

        def radio_changed(radio_value):
            control_data_option[title]["radio"] = radio_value['new']

        radio_buttons = widgets.RadioButtons(
            options=values,
            value=values[default_value_index],
            disabled=False,
            layout=widgets.Layout(margin='0px 0px 0px 5px')
        )
        radio_buttons.observe(radio_changed, names="value")
        control_data_option[title]["radio"] = values[default_value_index]
        return widgets.VBox([radio_buttons], layout=widgets.Layout(margin='0px 0px 0px 10px'))    \

    @staticmethod
    def get_number_text(control_data_option, title, default_value=0):
        control_data_option[title] = {}

        def number_changed(value):
            control_data_option[title]= value['new']


        widget = widgets.BoundedIntText(
            value=default_value,
            min=0,
            step=1,
            disabled=False,
            layout=widgets.Layout(margin='0px 0px 0px 5px', width="100px")
        )
        widget.observe(number_changed, names="value")
        control_data_option[title] = default_value
        return widgets.VBox([widget], layout=widgets.Layout(margin='0px 0px 0px 10px'))

    @staticmethod
    def get_checkbox(control_data_option, title, values):
        control_data_option[title] = {}

        def checkbox_clicked(checkbox_value):
            control_data_option[title][checkbox_value['owner'].description] = checkbox_value['new']

        checkbox_list = []
        for value in values:
            checkbox_widget = widgets.Checkbox(
                value=False,
                description=value,
                disabled=False,
                indent=False,
            )
            control_data_option[title][value] = False
            checkbox_widget.observe(checkbox_clicked, names="value")
            checkbox_widget.add_class("styled-check-box")
            checkbox_list.append(checkbox_widget)
        return widgets.VBox(checkbox_list, layout=widgets.Layout(margin='0px 0px 0px 12px'))

    @staticmethod
    def get_popup_menu(op_category, items, click_event):
        icon_op_name = ""
        if op_category == "Basic":
            icon_src = "data:image/svg+xml;base64,{0}".format(BASIC_ICON)
            icon_op_name = "기본"
        elif op_category == "T-test":
            icon_src = "data:image/svg+xml;base64,{0}".format(T_TEST_ICON)
            icon_op_name = "T-검정"
        elif op_category == "ANOVA":
            icon_src = "data:image/svg+xml;base64,{0}".format(ANOVA_ICON)
            icon_op_name = "분산분석"
        elif op_category == "Regression":
            icon_src = "data:image/svg+xml;base64,{0}".format(REGRESSION_ICON)
            icon_op_name = "회귀분석"
        elif op_category == "Frequencies":
            icon_src = "data:image/svg+xml;base64,{0}".format(FREQUENCIES_ICON)
            icon_op_name = "빈도분석"
        else :
            icon_src = "data:image/svg+xml;base64,{0}".format(BASIC_ICON)

        item_widgets = []

        for item in items:
            item_widgets.append(widgets.HTML(
                value="""
                <a>{0}</>
                """.format(item),
            ))
        drop_btn = widgets.HTML(
            value="""
            <img class="drop-img" src="{0}" alt="statistic icon"/>
            <div class="icon-op-name">&nbsp{1}▼</div>
            """.format(icon_src, icon_op_name)
        )
        drop_btn.add_class("dropdown-btn")
        dropdown_content = CommonWidget.get_vbox(item_widgets)
        dropdown_content.layout = widgets.Layout()

        dropdown_content.add_class("dropdown-content")

        dropdown = CommonWidget.get_vbox([drop_btn, dropdown_content])
        dropdown.add_class("dropdown")
        dropdown.layout = widgets.Layout(margin="5px 20px 5px 5px")  # margin 줘서 기존 속성 날림

        def handle_event(index):
            return lambda event: click_event(items[index])

        for index, item_widget in enumerate(item_widgets):
            d = Event(source=item_widget, watched_events=['click'])
            d.on_dom_event(handle_event(index))

        return dropdown

    @staticmethod
    def get_number_field_and_radio_buttons(control_data_option, title, text_title, text_value, radio_values,
                                           default_radio_value_index):
        control_data_option[title] = {}
        control_data_option[title]["number"] = 0
        control_data_option[title]["radio"] = radio_values[default_radio_value_index]

        def textfield_changed(value):
            control_data_option[title]["number"] = value['new']

        def radio_changed(value):
            control_data_option[title]["radio"] = value['new']

        number_field = widgets.FloatText(
            value=text_value,
            description=text_title,
            disabled=False,
            layout=widgets.Layout(width="180px"),
            style=dict(description_width='min-content')
        )
        number_field.observe(textfield_changed, names="value")

        radio_buttons = widgets.RadioButtons(
            options=radio_values,
            value=radio_values[default_radio_value_index],
            disabled=False,
            layout=widgets.Layout(margin='0px 0px 0px 5px')
        )
        control_data_option[title + "-radio"] = radio_values[default_radio_value_index]

        radio_buttons.observe(radio_changed, names="value")
        return widgets.VBox([number_field, radio_buttons],
                            layout=widgets.Layout(margin='0px 0px 0px 10px'))

    @staticmethod
    def get_connected_multiple(control_data_option, title, accordion_title, multiple_titles, connect_widgets,
                               column_name_type_map, type_list):
        delete_btn_list = []
        add_btn_list = []

        main_multiple = CommonWidget.get_multiple([], height='180px',width="200px")
        main_layout = CommonWidget.get_multiple_with_label(multiple_titles[0], main_multiple, width="205px")
        sub_multiple = CommonWidget.get_multiple([],height='180px',width="200px")
        add_btn = CommonWidget.get_add_button()
        delete_btn = CommonWidget.get_delete_button()
        sub_layout = CommonWidget.get_multiple_with_button_layout(multiple_titles[1], sub_multiple,add_btn,delete_btn, width="250px" )
        add_btn_list.append(add_btn)
        delete_btn.layout = Layout(width="40px", display="none")
        delete_btn_list.append(delete_btn)
        CommonUtil.connect_multiples_by_button(
            control_data_option, multiple_titles[0], main_multiple, multiple_titles[1], sub_multiple, add_btn,
            delete_btn)

        def on_main_selected(value):
            for btn in delete_btn_list:
                btn.layout = Layout(width="40px", display="none", margin="0")
            for btn in add_btn_list:
                btn.layout = Layout(width="40px", display="", margin="0")

        main_multiple.observe(on_main_selected, names='value')

        def on_sub_selected(value):
            for btn in add_btn_list:
                btn.layout = Layout(width="40px", display="none", margin="0")
            for btn in delete_btn_list:
                btn.layout = Layout(width="40px", display="", margin="0")

        sub_multiple.observe(on_sub_selected, names='value')

        def on_multiple_changed(value):
            multiples_options = []
            distinct_options = []
            multiple_option = []
            for multiple in connect_widgets:
                multiples_options.extend(list(multiple.options))

            for option in list(set(multiples_options)):
                column_name = column_name_type_map[option]
                if type_list[column_name] != "Number":
                    distinct_options.append(column_name)
                else:
                    multiple_option.append(column_name)

            combi = chain.from_iterable(combinations(distinct_options, r) for r in range(1, len(distinct_options) + 1))
            for item in list(combi):
                multiple_option.append(" ※ ".join(item))
            main_multiple.options = tuple(multiple_option)
            sub_multiple.options = ()

        main_multiple.observe(on_main_selected, names='value')

        for widget in connect_widgets:
            widget.observe(on_multiple_changed, names="options")

        accordion_item = widgets.HBox(
            [main_layout, sub_layout],
            layout=widgets.Layout(display="flex", justify_content="flex-start"))
        connected_multiple = CommonWidget.get_accordion_widget([accordion_item], [accordion_title], selected_index=None, min_width="480px")
        return widgets.VBox([connected_multiple], layout=widgets.Layout(margin='0px 0px 0px 10px'))

    @staticmethod
    def get_connected_dropdown(control_data_option, title, connect_widget, column_name_type_map, type_list, df,
                               place_holder="empty"):
        dropdown_options = [place_holder]
        connected_dropdown = widgets.Dropdown(
            options=dropdown_options,
            value=dropdown_options[0],
            disabled=False,
            layout=widgets.Layout(width="200px")
        )

        def on_dropdown_changed(value):
            control_data_option[title] = connected_dropdown.value

        connected_dropdown.observe(on_dropdown_changed, names="value")

        def on_multiple_changed(value):
            if len(list(connect_widget.options)) > 0:
                for option in list(connect_widget.options):
                    column_name = column_name_type_map[option]
                    type_name = type_list[column_name]
                    if type_name in ['Object', '2-Category', 'N-Category']:
                        unique_items = df[column_name].dropna().unique()
                        connected_dropdown.options = unique_items
                        connected_dropdown.value = unique_items[0]
                    else:
                        connected_dropdown.options = ["Select categorical variable for dependent variable"]
                        connected_dropdown.value = "Select categorical variable for dependent variable"
            else:
                connected_dropdown.options = dropdown_options
                connected_dropdown.value = dropdown_options[0]
            control_data_option[title] = connected_dropdown.value

        connect_widget.observe(on_multiple_changed, names="options")

        return connected_dropdown

    @staticmethod
    def get_individual_connected_dropdown(control_data_option, title, connect_widgets, column_name_type_map, type_list,
                                          df, acc_title):
        individual_connected_dropdown = None
        control_data_option[title] = {}

        def on_dropdown_changed(value):
            control_data_option[title][value['owner'].description] = value['new']

        def on_multiple_changed(value):
            individual_connected_dropdown.children = []
            total_options = []
            for item in connect_widgets:
                total_options.extend(list(item.options))

            dropdown_widgets = []
            changed_option = {}
            for option in total_options:
                column_name = column_name_type_map[option]
                if type_list[column_name] not in ['2-Category', 'N-Category', 'Object']:
                    unique_items = ['Select categorical variable']
                else:
                    unique_items = df[column_name].dropna().unique()
                value = unique_items[0]
                if column_name in control_data_option[title]:
                    value = control_data_option[title][column_name]
                dropdown_widget = CommonWidget.get_dropdown_with_description(title=column_name, options=unique_items,
                                                                             default_option=value)

                changed_option[column_name] = value
                dropdown_widgets.append(dropdown_widget)
                dropdown_widget.observe(on_dropdown_changed, names="value")
                individual_connected_dropdown.children = dropdown_widgets

            control_data_option[title] = changed_option

        for widget in connect_widgets:
            widget.observe(on_multiple_changed, names="options")

        individual_connected_dropdown = widgets.VBox([])

        accordion_item = widgets.HBox(
            [individual_connected_dropdown],
            layout=widgets.Layout(display="flex", justify_content="flex-start", margin="0", width="calc(100% + 5px)"))
        connected_multiple = CommonWidget.get_accordion_widget([accordion_item], [acc_title], selected_index=None, min_width="350px")

        return widgets.VBox([connected_multiple], layout=widgets.Layout(margin='0px 0px 0px 10px'))

    @staticmethod
    def get_export_layout(*args):
        margin = widgets.Layout(margin='5px 5px 5px 5px', align_items='center')
        agg_widget = widgets.VBox([widgets.HBox(list(args), layout=margin)], layout=margin)

        return agg_widget


