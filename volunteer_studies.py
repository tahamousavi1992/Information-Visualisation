import pandas as pd
import dash_html_components as html
import os
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import re
import extract

extended_studies_path = 'data/extended-studies.csv'

def getChart(app, studies, sponsors, facilities, conditions, interventions):
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

        print('saving extended studies file...')
        studies.to_csv(extended_studies_path, index=False, sep='|')

        return studies

    studies = getExtended_studies(studies, sponsors, facilities, conditions, interventions)

    result = html.Div([
        html.Link(rel="stylesheet", href="data:text/css;charset=utf-8,"
                                        " .dash-filter input {"
                                        "     text-align: left !important;"
                                        " }", type="text/css"),
        dbc.Row([
            dbc.Col([
                html.H2("List of Studies"),
                dash_table.DataTable(
                    id='studies-table',
                    columns=[{"name": col.replace("_", " "), "id": col} for col in ['nct_id', 'study_first_submitted_date', 'official_title', 'facility']],
                    page_current=0,
                    page_size=10,
                    page_action='custom',
                    filter_action='custom',
                    sort_action='custom',
                    sort_mode='multi',
                    style_table={'overflowX': 'scroll'},
                    style_as_list_view=True,
                    style_header={'fontWeight': 'bold'},
                    style_cell={'textAlign': 'left'},
                    style_filter={'direction': 'ltr','textAlign': 'left'},
                    filter_query='',
                    row_selectable="single",
                ),
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H2("Study Details"),
                html.Div(id='study-details')
            ], width=12)
        ])
    ])

    @app.callback(
        Output('studies-table', 'data'),
        [Input('studies-table', "page_current"),
        Input('studies-table', "page_size"),
        Input('studies-table', "filter_query"),
        Input('studies-table', "sort_by"),
        Input('date-slider', 'value')])
    def update_table(page_current, page_size, filter_query, sort_by, date_range):
        filtered_studies = extract.filter_by_date(studies, date_range, None, None)
        filtering_expressions = filter_query.split(' && ')
        for filter_part in filtering_expressions:
            if ' eq ' in filter_part:
                col_name, filter_value = re.search(r"{(.*?)} eq \"?(.*?)\"?$", filter_part).groups()
                col_name = col_name.strip()
                filter_value = filter_value.strip()
                filtered_studies = filtered_studies.loc[filtered_studies[col_name] == filter_value]
            elif ' contains ' in filter_part:
                col_name, filter_value = re.search(r"{(.*?)} contains \"?(.*?)\"?$", filter_part).groups()
                col_name = col_name.strip()
                filter_value = filter_value.strip()
                filtered_studies[col_name] = filtered_studies[col_name].fillna('') # fill NaN values with empty string
                filtered_studies = filtered_studies.loc[filtered_studies[col_name].str.contains(filter_value)]
            elif ' scontains ' in filter_part:
                col_name, filter_value = re.search(r"{(.*?)} scontains \"?(.*?)\"?$", filter_part).groups()
                col_name = col_name.strip()
                filter_value = filter_value.strip()
                filtered_studies[col_name] = filtered_studies[col_name].fillna('') # fill NaN values with empty string
                filtered_studies = filtered_studies.loc[filtered_studies[col_name].str.contains(filter_value, case=False)]


        if sort_by and len(sort_by):
            filtered_studies = filtered_studies.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )

        start = page_current * page_size
        end = (page_current + 1) * page_size
        return filtered_studies.iloc[start:end].to_dict('records')

    @app.callback(
        Output('study-details', 'children'),
        [Input('studies-table', 'selected_rows'), Input('studies-table', 'data')])
    def display_study_details(selected_rows, data):
        if selected_rows and selected_rows[0] is not None:
            selected_study = pd.DataFrame(data).iloc[selected_rows[0]]
            return html.Table(
                [html.Tr([
                    html.Th(col.replace("_", " "), style={'border': '1px solid black', 'padding': '5px', 'textAlign': 'left'}),
                    html.Td(selected_study[col], style={'border': '1px solid black', 'padding': '5px', 'textAlign': 'left'})
                ]) for col in selected_study.index],
                style={'borderCollapse': 'collapse'}
            )
        return "Please select a study from the table."

    return result
