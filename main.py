import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import extract
import expert_phase_pie, expert_numStudy_bar, expert_study_type_map, expert_studies_by_condition_bar, expert_status_bar, expert_yearly_studies_line,\
expert_intervention_radar, volunteer_studies

# Sample data
sample_data = pd.DataFrame({
    'X': range(10),
    'Line': [x * 2 for x in range(10)],
    'Bar': [x ** 2 for x in range(10)]
})
studies, sponsors, facilities, design_groups, conditions, interventions = extract.load_all_data()
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Button('Volunteer', id='volunteer-button', n_clicks=0),
        html.Button('Expert', id='expert-button', n_clicks=0),
    ], style={'textAlign': 'center'}),

    html.Div([
        volunteer_studies.getChart(app, studies, sponsors, facilities, conditions, interventions)
    ], id='Volunteer-div'),

    html.Div([
        dcc.Graph(
            id='bar-chart',
            figure={
                'data': [
                    go.Bar(
                        x=sample_data['X'],
                        y=sample_data['Bar'],
                        name='Bar Chart'
                    )
                ],
                'layout': go.Layout(title='Bar Chart')
            }
        ),
        dcc.Graph(
            id='piePhase-chart',
            figure=expert_phase_pie.getChart(studies)
        ),
        expert_study_type_map.getChart(app, studies, facilities),
        expert_studies_by_condition_bar.get_chart(app, studies, conditions),
        expert_numStudy_bar.create_studies_bar_plot(app, facilities, studies),
        expert_status_bar.getChart(app, studies, design_groups),
        expert_yearly_studies_line.getChart(app, studies, sponsors),
        expert_intervention_radar.create_radar_layout(design_groups),

    ], id='expert-div', style={'display': 'none'})
])

@app.callback(
    Output('Volunteer-div', 'style'),
    Output('expert-div', 'style'),
    Input('volunteer-button', 'n_clicks'),
    Input('expert-button', 'n_clicks')
)
def toggle_charts(line_clicks, bar_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'volunteer-button' in changed_id or (bar_clicks == 0 and line_clicks == 0):
        return {'display': 'block'}, {'display': 'none'}
    if 'expert-button' in changed_id :
        return {'display': 'none'}, {'display': 'block'}




expert_phase_pie.getChart(studies)

if __name__ == '__main__':
    app.run_server(debug=True)
