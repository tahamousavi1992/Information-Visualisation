import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def getChart(app, studies, design_groups):
    # Merge 'studies' and 'design_groups' dataframes on 'nct_id'
    merged_df = pd.merge(studies, design_groups, on='nct_id')

    # Get unique 'group_type' values from the 'design_groups' dataframe
    unique_group_types = design_groups['group_type'].unique()

    # Define the layout of the app
    result = html.Div([
        html.H1("Studies Status by Group Type"),
        dcc.Dropdown(
            id='group_type_dropdown',
            options=[{'label': group_type, 'value': group_type} for group_type in unique_group_types],
            value=unique_group_types[0]
        ),
        dcc.Graph(id='bar_status_chart')
    ])

    # Create a callback function to update the bar chart based on the selected 'group type'
    @app.callback(
        Output('bar_status_chart', 'figure'),
        [Input('group_type_dropdown', 'value')]
    )
    def update_bar_status_chart(selected_group_type):
        filtered_df = merged_df[merged_df['group_type'] == selected_group_type]
        status_counts = filtered_df['overall_status'].value_counts().reset_index()
        status_counts.columns = ['overall_status', 'count']
        fig = px.bar(status_counts, x='overall_status', y='count', text='count')
        fig.update_xaxes(title_text='Overall Status')
        fig.update_traces(
            hovertemplate="Overall Status: %{x}<br>Count: %{y}"
        )
        return fig

    return result

