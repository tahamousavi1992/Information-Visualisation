import pandas as pd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

'''def getChart(studies):
    # Group by items in studies for "phase" and count the number of studies in each phase
    phase_dist = studies.groupby('phase').size().reset_index(name='counts')
    
    # Create a new column for the percentage of studies in each phase
    phase_dist['percent'] = round(phase_dist['counts'] / phase_dist['counts'].sum() * 100, 2)
    
    # Plot pie chart of the percentage distribution of studies in each phase
    expert_pie_phase = px.pie(phase_dist, values='percent', names='phase', title='Percentage Distribution of Studies in Each Phase',
                              hover_data=['counts'], labels={'counts': '#studies'})
    
    # Define the layout of the app
    result = html.Div([
        html.H1("Expert Analysis: Clinical Trial Phases"),
        dcc.Graph(
            id='pie_chart',
            figure=expert_pie_phase
        )
    ])
    
    return result'''

def getChart(studies):
    # Group by items in studies for "phase" and count the number of studies in each phase
    phase_dist = studies.groupby('phase').size().reset_index(name='counts')
    
    # Create a new column for the percentage of studies in each phase
    phase_dist['percent'] = round(phase_dist['counts'] / phase_dist['counts'].sum() * 100, 2)
    
    # Plot pie chart of the percentage distribution of studies in each phase
    expert_pie_phase = px.pie(phase_dist, values='percent', names='phase', title='Percentage Distribution of Studies in Each Phase',
                              hover_data=['counts'], labels={'counts': '#studies'})
    
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
                    dcc.Graph(
                        id='pie_chart',
                        figure=expert_pie_phase
                    ),
                    width={"size": 2, "offset": 3}
                )
            )
        ],
        fluid=True
    )
    
    return result




