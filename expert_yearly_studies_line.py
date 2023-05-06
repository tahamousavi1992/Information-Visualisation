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
        html.H3("Number of Studies Per Year"),
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

        fig = px.line(yearly_study_count, x='year', y='nct_id')
        fig.update_yaxes(title_text='Number of Studies')
        fig.update_xaxes(title_text='Year')
        fig.update_traces(
            hovertemplate="Year: %{x}<br>#Studies: %{y}",
            line=dict(width=3, color='#3A5FCD'),
        )

        # Update the plot layout
        fig.update_layout(
            plot_bgcolor='#f7f7f7',
            margin=dict(l=100, r=20, t=70, b=70),
        )

        # Add a grid to the plot
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

        return fig

    return result

