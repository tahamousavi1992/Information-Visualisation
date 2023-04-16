import dash
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import extract

studies = extract.load_csv(file_name = 'data/studies.txt', includes = ['nct_id', 'study_first_submitted_date', 'completion_date', 'study_type',
    'brief_title', 'official_title' , 'overall_status' ,'phase' ,'enrollment', 'source', 'number_of_arms'])


import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='studies-table',
                columns=[
                    {"name": "nct_id", "id": "nct_id"},
                    {"name": "study_first_submitted_date", "id": "study_first_submitted_date"},
                    {"name": "official_title", "id": "official_title"},
                ],
                data=studies.tail(5000).to_dict('records'),
                row_selectable='single',
                page_size=20,
                style_cell={'textAlign': 'left'},
                style_header={'fontWeight': 'bold'},
                filter_action='native',
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='study-details')
        ])
    ])
], fluid=True)


@app.callback(
    Output('study-details', 'children'),
    [Input('studies-table', 'selected_rows')],
    [State('studies-table', 'data')]
)
def display_study_details(selected_rows, data):
    if selected_rows:
        selected_study = pd.DataFrame(data).iloc[selected_rows[0]]
        return dbc.Table.from_dataframe(selected_study.to_frame().T, striped=True, bordered=True, hover=True)
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=True)
