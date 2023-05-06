# studies_bar_plot.py
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import extract
import dash_bootstrap_components as dbc
def getChart(app, facilities, studies):

    # Create a layout with a dropdown menu and a bar plot
    layout = dbc.Row([
        html.H3("Studies by Country"),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Overall Status: '),
                ], width={"size": 2}),
                dbc.Col([
                    dcc.Dropdown(
                        id='status-dropdown',
                        options=[{'label': status, 'value': status} for status in studies['overall_status'].unique()],
                        value=studies['overall_status'].unique()[0]
                    ),
                ], width={"size": 5}),
            ]),
            ], width={"size": 6}),
            dbc.Row(
                dbc.Col([
                    dcc.Graph(id='bar-plot')
                ])
            )
    ])

    # Callback function to update the bar plot based on the selected status
    @app.callback(
        Output('bar-plot', 'figure'),
        Input('status-dropdown', 'value'),
        Input('date-slider', 'value'),
        Input('study_type_dropdown', 'value'),
        Input('study_gender_dropdown', 'value'))
    def update_bar_plot(selected_status, date_range, study_type, study_gender):
        filtered_studies = extract.filter_by_date(studies, date_range, study_type, study_gender)
        # Merge the dataframes
        merged_df = facilities.merge(filtered_studies, on='nct_id')
        # Group the data by country and count the studies
        country_counts = merged_df.groupby(['country', 'overall_status']).size().reset_index(name='count')
        # Get the top 20 countries
        top_countries = country_counts.groupby('country')['count'].sum().nlargest(20).index.tolist()

        filtered_df = country_counts[country_counts['overall_status'] == selected_status]

        top_20_filtered = filtered_df[filtered_df['country'].isin(top_countries)]
        others_filtered = filtered_df[~filtered_df['country'].isin(top_countries)].groupby('overall_status')['count'].sum().reset_index(name='count')
        others_filtered['country'] = 'Others'

        final_df = pd.concat([top_20_filtered, others_filtered], ignore_index=True)

        figure = px.bar(final_df.sort_values('count', ascending=False), x='country', y='count', title='Number of Studies by Country', text='count')

        return figure

    return layout
