#!/usr/bin/env python
# coding: utf-8

# Copyright (c) TmaxBI.
# Distributed under the terms of the Modified BSD License.
import ipywidgets as widgets

# Graph
import plotly.graph_objs as go


class WidgetANOVAFriedman:
    @ staticmethod
    def get_statistic_result_table(degree_freedom, test_result):
        res_table_info = ''
        res_table_info += """
                         <tr>
                             <td>{0}</td>
                             <td>{1}</td>
                             <td>{2}</td>
                         </tr>
                         """.format(round(test_result.statistic,2), degree_freedom,test_result.pvalue)

        res_table = widgets.HTML(
            value="""
                      <table style="width:100%">
                      <tr style="border-bottom: 1px solid black;">
                          <th>Statistic</th>
                          <th>df</th>
                          <th>p-value</th>
                      </tr>
                     {0}
                      </table>""".format(res_table_info),
            disabled=True
        )
        statistic_result_table = widgets.VBox([res_table])
        statistic_result_table.add_class('styledTable')
        return statistic_result_table

    @staticmethod
    def get_boxplot_sns(grouped_data, group_val_distinct):
        fig = go.FigureWidget()
        for data, index in zip(grouped_data, group_val_distinct):
            fig.add_trace(go.Box(y=data, name=index))

        fig.update_layout(
            width=500,
            height=500,
        )
        return fig