import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import extract
import dash_bootstrap_components as dbc

def getChart(app, studies, sponsors):
    # Preprocess the data
    studies = studies.dropna(subset=['study_first_submitted_date'], inplace=False)
    studies['year'] = pd.to_datetime(studies['study_first_submitted_date']).dt.year
    unique_sponsors = sponsors['name'].value_counts().nlargest(20).index.tolist()
    unique_sponsors = sorted(list(unique_sponsors))
    unique_sponsors.insert(0, 'All')

    # App layout
    result = dbc.Col([
        html.H3("Yearly Studies Line Chart"),
        dbc.Row([
            dbc.Col([
                dbc.Label(' Sponsor : '),
            ], width={"size": 2}),
            dbc.Col([
                dcc.Dropdown(
                    id='sponsor_dropdown',
                    options=[{'label': s, 'value': s} for s in unique_sponsors],
                    value='All'
                ),
            ], width={"size": 5}),
        ]),
        dcc.Graph(id='yearly_studies_line_chart')
    ])

    # Callback to update line chart
    @app.callback(
        Output('yearly_studies_line_chart', 'figure'),
        Input('sponsor_dropdown', 'value'),
        Input('date-slider', 'value'),
        Input('study_type_dropdown', 'value'),
        Input('study_gender_dropdown', 'value'))
    def update_line_chart(selected_sponsor, date_range, study_type, study_gender):
        filtered_studies = extract.filter_by_date(studies, date_range, study_type, study_gender)
        if selected_sponsor != 'All':
            studies_with_selected_sponsor = sponsors[sponsors['name'] == selected_sponsor]['nct_id']
            filtered_studies = filtered_studies[filtered_studies['nct_id'].isin(studies_with_selected_sponsor)]
        yearly_study_count = filtered_studies.groupby('year')['nct_id'].count().reset_index()
        fig = px.line(yearly_study_count, x='year', y='nct_id', title='Number of Studies per Year')
        fig.update_yaxes(title_text='number of studies')
        fig.update_traces(
            hovertemplate="Year: %{x}<br>Count: %{y}"
        )
        return fig

    return result

