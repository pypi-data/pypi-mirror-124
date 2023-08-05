import ipywidgets as widgets

# Graph
import plotly.graph_objs as go


class WidgetBasicReliability:
    @ staticmethod
    def get_standard_table():
        standard_table = widgets.HTML(
            value="""<table style="width: 300px">
                    <thead>
                    <th>Score</th>
                    <th>Status</th>
                    </thead>
                    <tbody>
                        <tr>
                            <td>0.6 < α</td>
                            <td>No Reliable</td>
                        </tr>
                        <tr>
                            <td>0.6 > α</td>
                            <td>Acceptable</td>
                        </tr>
                        <tr>
                            <td>0.7 > α</td>
                            <td>Desirable</td>
                        </tr>
                        <tr>
                            <td>0.8 > α</td>
                            <td>High reliable</td>
                        </tr>
                        <tr>
                            <td>0.9 > α</td>
                            <td>Very reliable</td>
                        </tr>
                    </tbody>
                </table>
                <div>α = cronbach\'s value<div>
                """,
            disabled=True
        )
        standard_table.add_class('styledTable')

        return standard_table

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
            title='Box plot',
            title_x=0.5,
            title_font_size=25,
            width=500,
            height=500,
            hovermode='closest',
        )
        return fig

    @staticmethod
    def get_headmap_plotly(data, columns):
        fig = go.FigureWidget()
        fig.add_trace(go.Heatmap(x=columns, y=columns, z=data.corr()))
        fig.update_layout(
            title='Heatmap',
            title_x=0.5,
            title_font_size=25,
            width=500,
            height=500,
            hovermode='closest',
        )
        return fig