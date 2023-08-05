import plotly.graph_objs as go
import scipy.stats as stats


class ChartMaker:
    @staticmethod
    def get_qq_plot_plotly(name, data):
        qqplot_data = stats.probplot(data, dist="norm")
        fig = go.FigureWidget()

        fig.add_trace({
            'type': 'scatter',
            'x': qqplot_data[0][0],
            'y': qqplot_data[0][1],
            'mode': 'markers',
        })

        # TO-Do 45도 기울기의 그래프 그리는거
        # fig.add_trace({
        #     'type': 'scatter',
        #     'x': [qqplot_data[0][0][0], qqplot_data[0][0][-1]],
        #     'y': qqplot_data[1][0:2],
        #     'mode': 'lines',
        # })

        fig.update_layout(
            title=name+" qq-plot",
            title_x=0.5,
            title_font_size=20,
            width=400,
            height=400,
            xaxis_title = "Theoritical Quantities",
            xaxis_zeroline = False,
            yaxis_title="Sample Quantities",
            showlegend = False
        )
        return fig

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

        chart_width = 300 + len(data_list)*50
        fig.update_layout(
            width=chart_width,
            height=500,
        )
        return fig
