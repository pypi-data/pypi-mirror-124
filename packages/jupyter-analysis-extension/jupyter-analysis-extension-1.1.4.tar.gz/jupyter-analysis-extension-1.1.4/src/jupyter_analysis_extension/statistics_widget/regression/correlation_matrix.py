#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.
import ipywidgets as widgets
import matplotlib.pyplot as plt
import plotly.graph_objs as go


class WidgetCorrelationMatrix:

    @staticmethod
    def get_x_dropdown(columns):
        return widgets.Dropdown(
            options=columns,
            description='X Variable: ',
            style=dict(description_width='initial')
        )

    @staticmethod
    def get_y_dropdown(columns):
        return widgets.Dropdown(
            options=columns,
            description='Y Variable: ',
            style=dict(description_width='initial')
        )

    @staticmethod
    def get_click_button():
        return widgets.Button(
            description='Analyze',
            disabled=False,
            button_style='',
            tooltip='Analyze',
            icon='check')

    @staticmethod
    def get_agg_widget(x_dropdown, y_dropdown, click_button):
        margin = widgets.Layout(margin='5px 5px 5px 5px', align_items='center')
        agg_widget = widgets.VBox([widgets.HBox([x_dropdown, y_dropdown, click_button], layout=margin)], layout=margin)
        return agg_widget

    @staticmethod
    def get_accordion_widgets(r_sq, intercept, slope, plt):
        description_widget = WidgetCorrelationMatrix.get_description_widget(r_sq, intercept, slope)
        graph_widget = WidgetCorrelationMatrix.get_graph_widget(plt)

        accordion_widget = widgets.Accordion(children=[description_widget, graph_widget]
                                             , layout=widgets.Layout(width='100%'))
        title_list = ['Description', 'Graph Explanation']
        for i in range(len(accordion_widget.children)):
            accordion_widget.set_title(i, title_list[i])

        return accordion_widget

    @staticmethod
    def get_description_widget(r_sq, intercept, slope):
        r_sq_widget = widgets.HTML(
            value='R^2 Square: {0}'.format(r_sq),
            disabled=True
        )
        intercept_widget = widgets.HTML(
            value='Intercept: {0}'.format(4),
            disabled=True
        )
        slope_widget = widgets.HTML(
            value='Slope: {0}'.format(slope),
            disabled=True
        )
        description_widget = widgets.VBox([r_sq_widget, intercept_widget, slope_widget])
        return description_widget

    @staticmethod
    def get_graph_widget():
        out = widgets.Output()
        with out:
            plt.show()
        return out

    @staticmethod
    def get_statistic_sep_result_table(col_names, r_sq, intercept, slope):
        model_info_table = widgets.HTML(
            value="""
                <table style="width:100%">
                <tr style="border-bottom: 1px solid black;">
                    <th>R^2 Square</th>
                    <th>Intercept</th>
                </tr>
                        <tr>
                            <td>{0}</td>
                            <td>{1}</td>
                        </tr>
                </table>""".format(r_sq, intercept, slope),
            disabled=True
        )
        res_table_info = ''
        for idx, name in enumerate(col_names):
            res_table_info += """
                        <tr>
                            <td>{0}</td>
                            <td>{1}</td>
                        </tr>
                        """.format(name, slope[idx])

        res_table = widgets.HTML(
            value="""
                <table style="width:100%">
                <tr style="border-bottom: 1px solid black;">
                    <th>Target Column</th>
                    <th>Slope</th>
                </tr>
               {0}
                </table>""".format(res_table_info),
            disabled=True
        )
        statistic_result_table = widgets.VBox([model_info_table, res_table])
        statistic_result_table.add_class('styledTable')

        return statistic_result_table

    @staticmethod
    def get_statistic_result_table(corr_info, corr_coefficients, addi_ops):
        """
        Parameters
        ----------
        corr_info : dict
        corr_coefficients : list
        addi_ops : list

        Returns
        -------
        object
        """
        res_table_info = ''

        for col_names in corr_info.keys():
            pearson_data = ""
            spearman_data = ""
            kendall_data = ""
            if "Report significance (p-value)" in addi_ops:
                if "Pearson" in corr_coefficients:
                    pearson_data = "{0}<br>(p-value:{1})".format(corr_info[col_names]["Pearson(corr)"],
                                                                 corr_info[col_names]["Pearson(p)"])
                if "Spearman" in corr_coefficients:
                    spearman_data = "{0}<br>(p-value:{1})".format(corr_info[col_names]["Spearman(corr)"],
                                                                  corr_info[col_names]["Spearman(p)"])
                if "Kendall's tau-b" in corr_coefficients:
                    kendall_data = "{0}<br>(p-value:{1})".format(corr_info[col_names]["Kendall's tau-b(corr)"],
                                                                 corr_info[col_names]["Kendall's tau-b(p)"])
            else:
                if "Pearson" in corr_coefficients:
                    pearson_data = corr_info[col_names]["Pearson(corr)"]
                if "Spearman" in corr_coefficients:
                    spearman_data = corr_info[col_names]["Spearman(corr)"]
                if "Kendall's tau-b" in corr_coefficients:
                    kendall_data = corr_info[col_names]["Kendall's tau-b(corr)"]

            if pearson_data != "":
                pearson_data = "<td>{0}</td>".format(pearson_data)
            if spearman_data != "":
                spearman_data = "<td>{0}</td>".format(spearman_data)
            if kendall_data != "":
                kendall_data = "<td>{0}</td>".format(kendall_data)

            res_table_info += """
                        <tr>
                            <td>{0}</td>
                            <td>{1}</td>
                            {2}
                            {3}
                            {4}
                        </tr>
                        """.format(col_names[0], col_names[1], pearson_data, spearman_data, kendall_data)

        res_table = widgets.HTML(
            value="""
                <table style="width:100%">
                <tr style="border-bottom: 1px solid black;">
                    <th colspan="2">Target Columns</th>
                    {0}
                    {1}
                    {2}
                </tr>
               {3}
                </table>""".format("<th>Pearson</th>" if "Pearson" in corr_coefficients else "",
                                   "<th>Spearman</th>" if "Spearman" in corr_coefficients else "",
                                   "<th>Kendall's tau-b</th>" if "Kendall's tau-b" in corr_coefficients else "",
                                   res_table_info),
            disabled=True
        )

        statistic_result_table = widgets.VBox([res_table])
        statistic_result_table.add_class('styledTable')
        return statistic_result_table

    @staticmethod
    def get_all_scatter_plot(data, columns):
        dim_list = []
        for column in columns:
            dim_dict = {'label': column, 'values': data[column]}
            dim_list.append(dim_dict)
        fig = go.FigureWidget()
        # fig.add_trace(go.Splom(dimensions=[dict(label='Period', values=data['Period']), dict(label='Data_value', values=data['Data_value'])]))
        fig.add_trace(go.Splom(dimensions=dim_list))
        fig.update_layout(
            title='Scatter Plot',
            title_x=0.5,
            title_font_size=30,
            dragmode='select',
            width=600,
            height=600,
            hovermode='closest',
        )

        return fig

    @staticmethod
    def get_heatmap_plot(data, columns):
        fig = go.FigureWidget()
        fig.add_trace(go.Heatmap(x=columns, y=columns, z=data.corr()))
        fig.update_layout(
            title='Heatmap of Variables',
            title_x=0.5,
            title_font_size=30,
            dragmode='select',
            width=600,
            height=600,
            hovermode='closest',
        )
        return fig

    @staticmethod
    def get_all_scatter_categorical_plot(data, columns, categorical_names):
        dim_list = []

        for column in columns:
            dim_dict = {'label': column, 'values': data[column]}
            dim_list.append(dim_dict)
        fig = go.FigureWidget()
        for name in categorical_names:
            index_vals = data[name].astype('category').cat.codes
            # fig.add_trace(go.Splom(dimensions=[dict(label='Period', values=data['Period']), dict(label='Data_value', values=data['Data_value'])]))
            fig.add_trace(go.Splom(dimensions=dim_list, text=data[name], textsrc="aa",
                                   marker=dict(color=index_vals, showscale=True,
                                               line_color='white', line_width=0.5)))
        fig.update_layout(
            title='Scatter Plot',
            title_x=0.5,
            title_font_size=30,
            dragmode='select',
            width=600,
            height=600,
            hovermode='closest',
        )

        return fig

    @staticmethod
    def get_eda_plot(data, columns):
        scatter_plot = WidgetCorrelationMatrix.get_all_scatter_plot(data, columns)
        heatmap_plot = WidgetCorrelationMatrix.get_heatmap_plot(data, columns)
        return widgets.HBox([scatter_plot, heatmap_plot])

    @staticmethod
    def get_categorical_eda_plot(data, columns, categorical_names):
        pair_plot = WidgetCorrelationMatrix.get_all_scatter_categorical_plot(data, columns, categorical_names)
        return widgets.HBox([pair_plot])

    @staticmethod
    def get_all_scatter_plot(data, columns):
        dim_list = []
        for column in columns:
            dim_dict = {'label': column, 'values': data[column]}
            dim_list.append(dim_dict)
        fig = go.FigureWidget()
        # fig.add_trace(go.Splom(dimensions=[dict(label='Period', values=data['Period']), dict(label='Data_value', values=data['Data_value'])]))
        fig.add_trace(go.Splom(dimensions=dim_list))
        fig.update_layout(
            title='Scatter Plot',
            title_x=0.5,
            title_font_size=30,
            dragmode='select',
            width=600,
            height=600,
            hovermode='closest',
        )

        return fig
