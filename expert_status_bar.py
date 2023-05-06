import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import extract
import colorlover as cl
import dash_bootstrap_components as dbc

def getChart(app, studies, design_groups):
    # Merge 'studies' and 'design_groups' dataframes on 'nct_id'
    merged_df = pd.merge(studies, design_groups, on='nct_id')

    # Get unique 'group_type' values from the 'design_groups' dataframe
    unique_group_types = design_groups['group_type'].unique()

    # Define the layout of the app
    # Define the layout of the app
    result = dbc.Col([
        html.H3("Studies Status by Group Type"),
        dbc.Row([
            dbc.Col([
                dbc.Label(' Group Type: '),
            ], width={"size": 2}),
            dbc.Col([
                dcc.Dropdown(
                    id='group_type_dropdown',
                    options=[{'label': group_type, 'value': group_type} for group_type in unique_group_types],
                    value=unique_group_types[0]
                ),
            ], width={"size": 5}),
        ]),
        dcc.Graph(id='bar_status_chart')
    ])

    # Create a callback function to update the bar chart based on the selected 'group type'
    @app.callback(
        Output('bar_status_chart', 'figure'),
        Input('group_type_dropdown', 'value'),
        Input('date-slider', 'value'),
        Input('study_type_dropdown', 'value'),
        Input('study_gender_dropdown', 'value'))
    
    def update_bar_status_chart(selected_group_type, date_range, study_type, study_gender):
        filtered_studies = extract.filter_by_date(merged_df, date_range, study_type, study_gender)
        filtered_studies = filtered_studies[filtered_studies['group_type'] == selected_group_type]
        status_counts = filtered_studies['overall_status'].value_counts().reset_index()
        status_counts.columns = ['overall_status', 'count']
        fig = px.bar(status_counts, x='overall_status', y='count', text='count')

        # Update the plot layout
        fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'},
                          plot_bgcolor='#f7f7f7', margin=dict(l=100, r=20, t=70, b=70), 
                          xaxis_title='Status', yaxis_title='Number of Studies')

        colors = cl.scales['7']['qual']['Pastel1']
        # Update the trace colors and text positioning
        fig.update_traces(marker_color=colors, texttemplate='%{text:.2s}')

        # Add a grid to the plot
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

        fig.update_traces(
            hovertemplate="Status: %{x}<br>#Studies: %{y}"
        )
        return fig

    return result

