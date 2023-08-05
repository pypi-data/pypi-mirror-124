
import numpy as np
import ipywidgets as widgets

# Graph
import plotly.graph_objs as go


class WidgetBasicPCA:
    @staticmethod
    def get_pca_variance_chart(variance_ratio_list):
        fig = go.FigureWidget()

        chart_x = []
        for i in range(0, len(variance_ratio_list)):
            chart_x.append("PC"+str(i+1))

        fig.add_trace(
            go.Bar(
                x=chart_x,
                y=variance_ratio_list,
                name='Individual'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=chart_x,
                y=np.cumsum(variance_ratio_list),
                mode='lines+markers',
                name='Cumulative'
            )
        )

        fig.update_layout(
            title='PCA plot',
            title_x=0.5,
            title_font_size=25,
            yaxis_title="Explained variance in percent",
            width=550,
            height=450,
            hovermode='closest',
        )
        return fig

    @staticmethod
    def get_matrix_plot(transform_df, column_list, variance_ratio_list):
        fig = go.FigureWidget()
        dimensions =[]
        for column in column_list:
            dimensions.append({"label" : column, "values" :transform_df[column]})
        total_var = variance_ratio_list.sum() * 100
        fig.add_trace(
            go.Splom(
                dimensions=dimensions,
                diagonal_visible=False,
                marker=dict(
                            showscale=False,
                            line_color='white', line_width=0.5)
            )
        )
        fig.update_layout(
            title=f'Matrix Plot<br>Total Explained Variance: {total_var:.2f}%',
            title_x=0.5,
            title_font_size=25,
            width=450,
            height=450,
        )
        return fig

    @staticmethod
    def get_scree_plot(variance_ratio_list):
        fig = go.FigureWidget()

        chart_x = []
        for i in range(0, len(variance_ratio_list)):
            chart_x.append(str(i+1))

        fig.add_trace(
            go.Scatter(
                x=chart_x,
                y=variance_ratio_list,
                name='Eigenvalue',
                mode='lines+markers',
            )
        )

        fig.add_trace(
            go.Scatter(
                x=chart_x,
                y=[1 for i in range(len(chart_x))],
                mode='lines',
                name="Selection baseline"
            )
        )
        fig.update_layout(
            title='Scree plot',
            title_x=0.5,
            title_font_size=25,
            xaxis_title="Number of Componenets",
            yaxis_title="Eigenvalue",
            width=550,
            height=450,
            hovermode='closest',
        )
        return fig

    @staticmethod
    def get_kmo_standard_table():
        standard_table = widgets.HTML(
            value="""<table style="width: 300px">
                       <thead>
                       <th>Value</th>
                       <th>Status</th>
                       </thead>
                       <tbody>
                           <tr>
                               <td>0.9 > k</td>
                               <td>매우 좋음</td>
                           </tr>
                           <tr>
                               <td>0.8 < k < 0.89</td>
                               <td>꽤 좋음</td>
                           </tr>
                           <tr>
                               <td>0.7 < k < 0.79</td>
                               <td>적당함</td>
                           </tr>
                           <tr>
                               <td>0.6 < k < 0.69</td>
                               <td>평범함</td>
                           </tr>
                           <tr>
                               <td>0.5 < k < 0.59</td>
                               <td>좋지 않음</td>
                           </tr>
                            <tr>
                               <td>k < 0.5</td>
                               <td>사용할 수 없음</td>
                           </tr>
                       </tbody>
                   </table>
                   <div>k = Overall MSA value<div>
                   """,
            disabled=True
        )
        standard_table.add_class('styledTable')

        return standard_table