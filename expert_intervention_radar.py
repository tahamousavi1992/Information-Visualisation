import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import extract

def getChart(app, studies: pd.DataFrame, design_groups: pd.DataFrame) -> html.Div:
    def get_intervention_radar_plot(date_range, study_type, study_gender):
        filtered_studies = extract.filter_by_date(studies, date_range, study_type, study_gender)
        merged_df = design_groups.merge(filtered_studies, on='nct_id')
        # Group the dataframe by 'intervention_type' and count the number of 'nct_id'
        counts = merged_df.groupby('group_type')['nct_id'].count().reset_index()
        # Create a radar plot using Plotly
        fig = go.Figure(go.Scatterpolar(
            r=counts['nct_id'],
            theta=counts['group_type'],
            mode='lines',
            fill='toself',

        ))

        # Set up the layout for the radar plot
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, counts['nct_id'].max()]
                )),
            showlegend=False
        )
        return fig

    # Return the layout containing the radar plot
    result =  dbc.Col(html.Div([
        html.H3("Radar Chart of Group Types"),
        dcc.Graph(id='intervention-radar-plot')
    ]),
    )

    @app.callback(
        Output('intervention-radar-plot', 'figure'),
        Input('date-slider', 'value'),
        Input('study_type_dropdown', 'value'),
        Input('study_gender_dropdown', 'value'))
    def update_pie_chart(date_range, study_type, study_gender):
        return get_intervention_radar_plot(date_range, study_type, study_gender)

    return result
