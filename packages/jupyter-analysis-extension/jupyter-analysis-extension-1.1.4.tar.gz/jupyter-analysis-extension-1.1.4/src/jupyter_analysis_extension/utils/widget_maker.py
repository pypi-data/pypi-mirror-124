import ipywidgets as widgets


class WidgetMaker:
    @staticmethod
    def get_vertical_box(box_items=[], style={}):
        return widgets.HBox(
            box_items,
            layout=widgets.Layout(**style),
        )

    @staticmethod
    def get_btn(description="", disabled=False, tooltip="", style={}):
        return widgets.Button(
            description=description,
            disabled=disabled,
            tooltip=tooltip,
            layout=widgets.Layout(**style),
        )

    @staticmethod
    def get_html(value="", style={}):
        return widgets.HTML(
            value=value,
            layout=widgets.Layout(**style),
        )

    @staticmethod
    def get_styled_table(header_list, body_list, footer="", direation="column"):
        table_header_info = ""
        for item in header_list:
            table_header_info += "<th>{0}</th>".format(item)

        table_body_info = ""
        for body_item in body_list:
            table_row_info =""
            for row_item in body_item:
                table_row_info += "<td>{0}</td>".format(row_item)
            table_body_info += "<tr>{0}</tr>".format(table_row_info)

        res_table = widgets.HTML(
            value="""
                <table>
                    <thead>
                    {0}
                    </thead>
                    <tbody>
                    {1}
                    </tbody>
                </table>
                <div>{2}<div>
                """.format(table_header_info,table_body_info,footer),
            disabled=True
        )
        res_table.add_class('styledTable')
        if direation=="row" :
            return widgets.HBox([res_table])
        return widgets.VBox([res_table])

    @staticmethod
    def get_individual_connected_unique_numberField(control_data_option, title, connect_widgets, column_name_type_map, type_list,
                                          df, acc_title):
        individual_connected_unique_numberField = None
        control_data_option[title] = {}

        def on_numberField_changed(value):
            control_data_option[title][value['owner'].description] = value['new']

        def on_multiple_changed(value):
            total_options = []
            column_name = column_name_type_map[connect_widgets[0].options[0]]
            unique_items = df[column_name].unique()
            for item in connect_widgets:
                total_options.extend(list(item.options))

            number_field_widgets = []
            changed_option = {}
            for item in unique_items:
                number_field_widget = widgets.BoundedIntText(
                                        value=1,
                                        min=0,
                                        description=str(item),
                                        disabled=False,
                                        layout=widgets.Layout(width="180px"),

                                    )
                number_field_widgets.append(number_field_widget)
                number_field_widget.observe(on_numberField_changed, names="value")
                individual_connected_unique_numberField.children = number_field_widgets

            control_data_option[title] = changed_option

        for widget in connect_widgets:
            widget.observe(on_multiple_changed, names="options")

        individual_connected_unique_numberField = widgets.VBox([])

        accordion_item = widgets.HBox(
            [individual_connected_unique_numberField],
            layout=widgets.Layout(display="flex", justify_content="flex-start", margin="0", width="calc(100% + 5px)"))
        connected_multiple = WidgetMaker.get_accordion_widget([accordion_item], [acc_title], selected_index=None,
                                                               style=dict(width="100%", display="flex", justify_content='center', margin="0",max_height="500px"))

        return widgets.VBox([connected_multiple], layout=widgets.Layout(margin='0px 0px 0px 10px'))


    @staticmethod
    def get_accordion_widget(widget_list, title_list, selected_index=0,style={}):
        accordion_widget = widgets.Accordion(
            children=widget_list,
            layout=widgets.Layout(**style),
            selected_index=selected_index)
        for i in range(len(accordion_widget.children)):
            accordion_widget.set_title(i, title_list[i])
        return accordion_widget