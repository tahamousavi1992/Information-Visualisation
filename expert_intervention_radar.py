import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import extract

def getChart(app, studies: pd.DataFrame, design_groups: pd.DataFrame) -> html.Div:
    def get_intervention_radar_plot(date_range, study_type, study_gender):
        filtered_studies = extract.filter_by_date(studies, date_range, study_type, study_gender)
        merged_df = design_groups.merge(filtered_studies, on='nct_id')
        # Group the dataframe by 'intervention_type' and count the number of 'nct_id'
        counts = merged_df.groupby('group_type')['nct_id'].count().reset_index()

        # Choose a colorblind-friendly color palette
        colors = px.colors.sequential.Viridis

        fig = go.Figure(go.Scatterpolar(
            r=counts['nct_id'],
            theta=counts['group_type'],
            mode='lines',
            fill='toself',
            line=dict(color=colors[0]),
            fillcolor=colors[0],
        ))

        # Increase the font size and add axis labels
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, counts['nct_id'].max()],
                    showline=False,
                    gridcolor='lightgrey',
                    gridwidth=1,
                ),
                angularaxis=dict(
                    visible=True,
                    showline=True,
                    linewidth=2,
                    linecolor='lightgrey',
                    gridcolor='lightgrey',
                    gridwidth=1,
                ),
                bgcolor='#f7f7f7',
            ),
            font=dict(size=16, color='black'),
            showlegend=False,
        )

        # Remove unnecessary elements
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)


        return fig

    # Return the layout containing the radar plot
    result =  dbc.Col(html.Div([
        html.H3("Number of Studies Per Group Type"),
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
