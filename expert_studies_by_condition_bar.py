import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import colorlover as cl
import colorsys
import extract
import dash_bootstrap_components as dbc

def get_chart(app, studies, conditions):

    result = dbc.Row([
        html.H3("Top Conditions by Number of Studies"),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Top: '),
                ], width={"size": 2}),
                dbc.Col([
                    dcc.Dropdown(
                        id='num_conditions',
                        options=[
                            {'label': 'Top 5', 'value': 5},
                            {'label': 'Top 10', 'value': 10},
                            {'label': 'Top 20', 'value': 20},
                            {'label': 'Top 30', 'value': 30},
                            {'label': 'Top 40', 'value': 40},
                            {'label': 'Top 50', 'value': 50},
                        ],
                        value=5
                    ),
                ], width={"size": 5}),
            ]),
            ], width={"size": 6}),
            dbc.Row(
                dbc.Col([
                    dcc.Graph(id='bar_top_conditions_chart'),
                ])
            )
    ])

    @app.callback(
        Output('bar_top_conditions_chart', 'figure'),
        Input('num_conditions', 'value'),
        Input('date-slider', 'value'),
        Input('study_type_dropdown', 'value'),
        Input('study_gender_dropdown', 'value'))
    def update_bar_top_conditions_chart(num_conditions, date_range, study_type, study_gender):
        filtered_studies = extract.filter_by_date(studies, date_range, study_type, study_gender)
        # Merge the two DataFrames on 'nct_id'
        merged_data = pd.merge(filtered_studies, conditions, on='nct_id')

        # Count the number of studies for each condition
        condition_counts = merged_data.groupby('downcase_name')['nct_id'].nunique().reset_index()
        condition_counts.columns = ['downcase_name', 'study count']
        condition_counts['name'] = condition_counts['downcase_name']
        condition_counts = condition_counts.sort_values('study count', ascending=False)

        top_conditions = condition_counts.head(num_conditions)

        fig = px.bar(top_conditions, x='study count', y='name',
             orientation='h', text='study count',
             title=f"Top {num_conditions} Conditions by Study Count")

        def distribute_colors(colors):
            num_colors = len(colors)
            new_colors = [colors[i::num_colors//2] for i in range(num_colors//2)]
            distributed_colors = [color for sublist in zip(*new_colors) for color in sublist]
            return distributed_colors

        colors = cl.interp(cl.scales['9']['qual']['Pastel1'], 50)
        # Reorder the colors
        distributed_colors = distribute_colors(colors)
        # pastel1 = cl.scales['9']['qual']['Pastel1']
        # colors = pastel1 * 6

        # Create the plot
        fig = px.bar(top_conditions, x='study count', y='name',
                    orientation='h', text='study count')

        # Update the plot layout
        fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'},
                        plot_bgcolor='#f7f7f7', margin=dict(l=100, r=20, t=70, b=70),
                        xaxis_title='Number of Studies', yaxis_title='Condition')

        # Update the trace colors and text positioning
        fig.update_traces(marker_color=distributed_colors, texttemplate='%{text:.2s}', textposition='inside')

        # Add a grid to the plot
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

        # Increase the font size of the text on the plot
        fig.update_layout(font=dict(size=14))

        return fig

    return result


