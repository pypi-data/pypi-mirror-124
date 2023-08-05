
import ipywidgets as widgets

# Graph
import plotly.graph_objs as go


class WidgetBasicAnalysis:
    @ staticmethod
    def get_statistic_result_table(name, degree_freedom, test_result, statistic_tests_options):
        res_table_header = ''
        variable_list = list(test_result["Base(기초)"].keys())
        variable_count = len(test_result["Base(기초)"].items())

        for key, value in test_result["Base(기초)"].items():
            res_table_header += """<th>{0}</th>""".format(key)
            res_table_row_info =""
            for key_1, value_1 in value.items():
                res_table_row_info_child =""
                for i in range(0, variable_count):
                    res_table_row_info_child += """
                    <td>{0}</td>
                    """.format(test_result["Base(기초)"][variable_list[i]][key_1])
                res_table_row_info += """
                                    <tr>
                                        <td>{0}</td>
                                        {1}
                                    </tr>
                                """.format(key_1,res_table_row_info_child)

        res_table = widgets.HTML(
            value="""
                <table style="width:100%">
                <tr style="border-bottom: 1px solid black;">
                    <th></th>
                    {0}
                </tr>
               {1}
                </table>""".format(res_table_header, res_table_row_info),
            disabled=True
        )
        statistic_result_table = widgets.VBox([res_table])
        statistic_result_table.add_class('styledTable')

        return statistic_result_table

    @staticmethod
    def get_box_plot_plotly(data_list):
        fig = go.FigureWidget()
        for data in data_list:
            fig.add_trace(
                go.Box(y=data,
                       name=data.name,
                       boxpoints='all',
                       jitter=0.2,
                       pointpos=-1.8
                       ))

        fig.update_layout(
            width=500,
            height=500,
        )
        return fig
