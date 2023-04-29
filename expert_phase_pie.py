import pandas as pd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import extract
import pandas as pd

def getChart(app, studies):
    def get_expert_pie_phase(date_range):
        filtered_studies = extract.filter_by_date(studies, date_range)
        # Group by items in studies for "phase" and count the number of studies in each phase
        phase_dist = filtered_studies.groupby('phase').size().reset_index(name='counts')

        # Create a new column for the percentage of studies in each phase
        phase_dist['percent'] = round(phase_dist['counts'] / phase_dist['counts'].sum() * 100, 2)

        # Plot pie chart of the percentage distribution of studies in each phase
        expert_pie_phase = px.pie(phase_dist, values='percent', names='phase', title='Percentage Distribution of Studies in Each Phase',
                                hover_data=['counts'], labels={'counts': '#studies'})
        return expert_pie_phase

    # Define the layout of the app
    result = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1("Expert Analysis: Clinical Trial Phases"),
                    width={"size": 3, "offset": 2}
                )
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='pie_chart'),
                    width={"size": 2, "offset": 3}
                )
            )
        ],
        fluid=True
    )

    @app.callback(
    Output('pie_chart', 'figure'),
    Input('date-slider', 'value')
    )
    def update_pie_chart(date_range):
        return get_expert_pie_phase(date_range)

    return result


