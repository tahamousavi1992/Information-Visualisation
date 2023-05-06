import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import colorlover as cl
import extract
import pandas as pd

def getChart(app, studies):
    def get_expert_pie_phase(date_range, study_type, study_gender):
        filtered_studies = extract.filter_by_date(studies, date_range, study_type, study_gender)
        # Group by items in studies for "phase" and count the number of studies in each phase
        phase_dist = filtered_studies.groupby('phase').size().reset_index(name='counts')

        # Create a new column for the percentage of studies in each phase
        phase_dist['percent'] = round(phase_dist['counts'] / phase_dist['counts'].sum() * 100, 2)

        expert_pie_phase = px.pie(phase_dist, values='percent', names='phase', 
                                title='Percentage Distribution of Studies in Each Phase',
                                hover_data=['counts'], labels={'counts': '# Studies'})

        # Define a colorblind-friendly color palette with 7 colors
        colors = cl.scales['7']['qual']['Pastel1']

        # Update the pie chart colors, text positioning, and text information
        expert_pie_phase.update_traces(marker_colors=colors, textposition='inside', textinfo='percent+label', hole=0.3)

        # Update the layout
        expert_pie_phase.update_layout(title={'font': {'size': 24}}, font={'size': 16}, legend={'font': {'size': 14}}, plot_bgcolor='#f7f7f7')
        
        return expert_pie_phase

    # Define the layout of the app
    result = dbc.Col(
        [
            dbc.Row(
                dbc.Col(
                    html.H3("Expert Analysis: Clinical Trial Phases"),
                    width={"size": 12}
                )
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='pie_chart'),
                    width={"size": 12}
                )
            )
        ],
    )

    @app.callback(
    Output('pie_chart', 'figure'),
    Input('date-slider', 'value'),
    Input('study_type_dropdown', 'value'),
    Input('study_gender_dropdown', 'value'))
    def update_pie_chart(date_range, study_type, study_gender):
        return get_expert_pie_phase(date_range, study_type, study_gender)

    return result


