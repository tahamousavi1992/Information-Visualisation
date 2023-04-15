import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def get_chart(app, studies, conditions):
    # Merge the two DataFrames on 'nct_id'
    merged_data = pd.merge(studies, conditions, on='nct_id')

    # Count the number of studies for each condition
    condition_counts = merged_data.groupby('downcase_name')['nct_id'].nunique().reset_index()
    condition_counts.columns = ['downcase_name', 'study count']
    condition_counts['name'] = condition_counts['downcase_name']
    condition_counts = condition_counts.sort_values('study count', ascending=False)

    result = html.Div([
        html.H1("Top Conditions by Study Count"),
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
        dcc.Graph(id='bar_top_conditions_chart'),
    ])

    @app.callback(
        Output('bar_top_conditions_chart', 'figure'),
        [Input('num_conditions', 'value')]
    )
    def update_bar_top_conditions_chart(num_conditions):
        top_conditions = condition_counts.head(num_conditions)

        fig = px.bar(top_conditions, x='study count', y='name',
                    text='study count', orientation='h', title=f"Top {num_conditions} Conditions by Study Count")
        fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
        fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

        return fig

    return result


