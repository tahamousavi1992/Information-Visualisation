
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px


def getChart(app, studies, sponsors):
    # Preprocess the data
    studies = studies.dropna(subset=['study_first_submitted_date'], inplace=False)
    studies['year'] = pd.to_datetime(studies['study_first_submitted_date']).dt.year
    unique_sponsors = sponsors['name'].unique()
    unique_sponsors = sorted(list(unique_sponsors))
    unique_sponsors.insert(0, 'All')

    # App layout
    result = html.Div([
        dcc.Dropdown(
            id='sponsor_dropdown',
            options=[{'label': s, 'value': s} for s in unique_sponsors],
            value='All'
        ),
        dcc.Graph(id='yearly_studies_line_chart')
    ])

    # Callback to update line chart
    @app.callback(
        Output('yearly_studies_line_chart', 'figure'),
        Input('sponsor_dropdown', 'value')
    )
    def update_line_chart(selected_sponsor):
        if selected_sponsor == 'All':
            filtered_studies = studies
        else:
            studies_with_selected_sponsor = sponsors[sponsors['name'] == selected_sponsor]['nct_id']
            filtered_studies = studies[studies['nct_id'].isin(studies_with_selected_sponsor)]
        yearly_study_count = filtered_studies.groupby('year')['nct_id'].count().reset_index()
        fig = px.line(yearly_study_count, x='year', y='nct_id', title='Number of Studies per Year')
        fig.update_yaxes(title_text='number of studies')
        fig.update_traces(
            hovertemplate="Year: %{x}<br>Count: %{y}"
        )
        return fig

    return result

