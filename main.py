import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import extract
import expert_phase_pie, expert_numStudy_bar, expert_study_type_map, expert_studies_by_condition_bar, expert_status_bar, expert_yearly_studies_line,\
expert_intervention_radar, volunteer_studies

from dateutil.relativedelta import relativedelta

# Sample data
def generate_slider_marks(min_date, max_date):
    marks = {}
    current_date = min_date.replace(month=1, day=1)
    while current_date <= max_date:
        marks[int(current_date.timestamp())] = str(current_date.year)
        current_date += relativedelta(years=1)

    return marks


studies, sponsors, facilities, design_groups, conditions, interventions = extract.load_all_data()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

min_date = pd.to_datetime(studies['study_first_submitted_date']).min()
max_date = pd.to_datetime(studies['study_first_submitted_date']).max()

study_types = list(studies['study_type'].unique())
study_types.insert(0, 'All')

study_genders = list(studies['gender'].replace('All', 'Both male and female').fillna('unknown').unique())
study_genders.insert(0, 'All')

app.layout = html.Div([
    html.Div([
        dbc.Button('Volunteer', id='volunteer-button', n_clicks=0, color='primary', className='mr-2' , style={'margin-right': '10px'}),
        dbc.Button('Expert', id='expert-button', n_clicks=0, color='dark', className='mr-2'),
    ], style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col(
            dcc.RangeSlider(
                id='date-slider',
                min=int(min_date.timestamp()),
                max=int(max_date.timestamp()),
                value=[int(min_date.timestamp()), int(max_date.timestamp())],
                marks = generate_slider_marks(min_date, max_date),
                step=30*24*60*60
            ),
            width={"size": 12}
        )
    ]),
    html.Div([
        volunteer_studies.getChart(app, studies, sponsors, facilities, conditions, interventions)
    ], id='Volunteer-div'),

    html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='study_type_dropdown',
                    options=[{'label': st, 'value': st} for st in study_types],
                    value=study_types[0],
                    placeholder="Select a study type"
                ),
                width={"size": 5, "offset": 1}
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='study_gender_dropdown',
                    options=[{'label': st, 'value': st} for st in study_genders],
                    value=study_genders[0],
                    placeholder='Select a gender'
                ),
                width={"size": 5}
            )
        ]
        ),
        html.Br(),
        dbc.Row([
            expert_phase_pie.getChart(app, studies),
            expert_intervention_radar.getChart(app, studies, design_groups),
        ]),
        html.Br(),
        dbc.Row([
            expert_status_bar.getChart(app, studies, design_groups),
            expert_yearly_studies_line.getChart(app, studies, sponsors),
        ]),
        html.Br(),
        expert_study_type_map.getChart(app, studies, facilities),
        html.Br(),
        expert_studies_by_condition_bar.get_chart(app, studies, conditions),
        html.Br(),
        expert_numStudy_bar.getChart(app, facilities, studies),

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

if __name__ == '__main__':
    app.run_server(debug=False)
