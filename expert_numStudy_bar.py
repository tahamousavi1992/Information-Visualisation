# studies_bar_plot.py
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def create_studies_bar_plot(app, facilities, studies):

    # Merge the dataframes
    merged_df = facilities.merge(studies, on='nct_id')

    # Group the data by country and count the studies
    country_counts = merged_df.groupby(['country', 'overall_status']).size().reset_index(name='count')

    # Get the top 20 countries
    top_countries = country_counts.groupby('country')['count'].sum().nlargest(20).index.tolist()

    # Create a layout with a dropdown menu and a bar plot
    layout = html.Div([
        html.H1("Studies by Country"),
        dcc.Dropdown(
            id='status-dropdown',
            options=[{'label': status, 'value': status} for status in merged_df['overall_status'].unique()],
            value=merged_df['overall_status'].unique()[0]
        ),
        dcc.Graph(id='bar-plot')
    ])

    # Callback function to update the bar plot based on the selected status
    @app.callback(
        Output('bar-plot', 'figure'),
        [Input('status-dropdown', 'value')]
    )
    def update_bar_plot(selected_status):
        filtered_df = country_counts[country_counts['overall_status'] == selected_status]

        top_20_filtered = filtered_df[filtered_df['country'].isin(top_countries)]
        others_filtered = filtered_df[~filtered_df['country'].isin(top_countries)].groupby('overall_status')['count'].sum().reset_index(name='count')
        others_filtered['country'] = 'Others'

        final_df = pd.concat([top_20_filtered, others_filtered], ignore_index=True)

        figure = px.bar(final_df, x='country', y='count', title='Number of Studies by Country', text='count')
        return figure

    return layout
