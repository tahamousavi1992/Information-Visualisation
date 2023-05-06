import pycountry
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import extract
import dash_bootstrap_components as dbc

def getChart(app, studies, facilities):
    def get_country_code(country_name):
        try:
            country = pycountry.countries.search_fuzzy(country_name)[0]
            return country.alpha_3
        except:
            if country_name == 'Palestinian Territories, Occupied':
                return 'PSE'
            else:
                return None

    def get_country_dictionary(country_names):
        country_dict = {}
        for name in country_names:
                country_dict[name] = get_country_code(name)
        return country_dict


    country_dictionary = get_country_dictionary(facilities['country'].unique())

    facilities['country_code'] = facilities['country'].apply(lambda x: country_dictionary[x] if type(x) is not float else None)

    # app = dash.Dash(__name__)
    merged_df = studies.merge(facilities, on='nct_id')

    def generate_map(study_type, date_range, study_gender):
        filtered_studies = extract.filter_by_date(merged_df, date_range, study_type, study_gender)
        unique_studies_df = filtered_studies.drop_duplicates(subset=['nct_id', 'country_code'])
        grouped_df = unique_studies_df.groupby(['country', 'country_code'], as_index=False).count()

        fig = px.choropleth(grouped_df,
                            locations='country_code',
                            color='nct_id',
                            hover_name='country',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            labels={'nct_id': 'Number of Studies'})


        return fig

    result_div = dbc.Row([
    html.H3("Choropleth Map of Studies Per Country"),
    dbc.Col([dcc.Graph(id='choropleth_map')], width={"size": 12}),
    ])

    @app.callback(
        Output('choropleth_map', 'figure'),
        Input('date-slider', 'value'),
        Input('study_type_dropdown', 'value'),
        Input('study_gender_dropdown', 'value'))

    def update_map(date_range, study_type, study_gender):
        return generate_map(study_type, date_range, study_gender)

    return result_div


