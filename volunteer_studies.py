import dash
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import extract
import os

studies, sponsors, facilities, design_groups, conditions, interventions = extract.load_all_data()

extended_studies_path = 'data/extended-studies.csv'

def getExtended_studies(studies, sponsors, facilities, conditions, interventions):
    if os.path.exists(extended_studies_path):
        print('Loading extended studies from file...')
        return pd.read_csv(extended_studies_path, delimiter='|', header=0)

    # Define format functions
    def format_sponsor(row):
        return f"(class: {row['agency_class']}, lead or collaborator: {row['lead_or_collaborator']}, name: {row['name']})"
    def format_condition(row):
        return f"(name: {row['downcase_name']})"
    def format_intervention(row):
        return f"(type: {row['intervention_type']}, name: {row['name']})"
    def format_facility(row):
        return f"(name: {row['name']}, country: {row['country']}, city: {row['city']})"

    # Apply format functions and group by nct_id for each dataframe
    sponsors['sponsor'] = sponsors.apply(format_sponsor, axis=1)
    grouped_sponsors = sponsors.groupby('nct_id').agg({'sponsor': ', '.join}).reset_index()

    conditions['condition'] = conditions.apply(format_condition, axis=1)
    grouped_conditions = conditions.groupby('nct_id').agg({'condition': ', '.join}).reset_index()

    interventions['intervention'] = interventions.apply(format_intervention, axis=1)
    grouped_interventions = interventions.groupby('nct_id').agg({'intervention': ', '.join}).reset_index()

    facilities['facility'] = facilities.apply(format_facility, axis=1)
    grouped_facilities = facilities.groupby('nct_id').agg({'facility': ', '.join}).reset_index()

    # Merge studies with the aggregated dataframes on the shared 'nct_id' column
    studies = studies.merge(grouped_sponsors, on='nct_id', how='left')
    studies = studies.merge(grouped_conditions, on='nct_id', how='left')
    studies = studies.merge(grouped_interventions, on='nct_id', how='left')
    studies = studies.merge(grouped_facilities, on='nct_id', how='left')

    studies.to_csv(extended_studies_path, index=False)
    return studies

# import dash
# import dash_table
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State
# import pandas as pd

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             dash_table.DataTable(
#                 id='studies-table',
#                 columns=[
#                     {"name": "nct_id", "id": "nct_id"},
#                     {"name": "study_first_submitted_date", "id": "study_first_submitted_date"},
#                     {"name": "official_title", "id": "official_title"},
#                 ],
#                 data=studies.tail(5000).to_dict('records'),
#                 row_selectable='single',
#                 page_size=20,
#                 style_cell={'textAlign': 'left'},
#                 style_header={'fontWeight': 'bold'},
#                 filter_action='native',
#             )
#         ])
#     ]),
#     dbc.Row([
#         dbc.Col([
#             html.Div(id='study-details')
#         ])
#     ])
# ], fluid=True)


# @app.callback(
#     Output('study-details', 'children'),
#     [Input('studies-table', 'selected_rows')],
#     [State('studies-table', 'data')]
# )
# def display_study_details(selected_rows, data):
#     if selected_rows:
#         selected_study = pd.DataFrame(data).iloc[selected_rows[0]]
#         return dbc.Table.from_dataframe(selected_study.to_frame().T, striped=True, bordered=True, hover=True)
#     else:
#         return ''


# if __name__ == '__main__':
#     app.run_server(debug=True)
