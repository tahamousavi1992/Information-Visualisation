import extract
import pycountry
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


def get_expert_study_type_map(app, studies, facilities):
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

    studies.dropna(subset=['study_type'], inplace=True)
    country_dictionary = get_country_dictionary(facilities['country'].unique())

    facilities['country_code'] = facilities['country'].apply(lambda x: country_dictionary[x] if type(x) is not float else None)

    # app = dash.Dash(__name__)
    merged_df = studies.merge(facilities, on='nct_id')

    def generate_map(study_type):
        filtered_df = merged_df[merged_df['study_type'] == study_type]
        unique_studies_df = filtered_df.drop_duplicates(subset=['nct_id', 'country_code'])
        grouped_df = unique_studies_df.groupby(['country', 'country_code'], as_index=False).count()

        fig = px.choropleth(grouped_df,
                            locations='country_code',
                            color='nct_id',
                            hover_name='country',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            labels={'nct_id': 'Number of Studies'},
                            title=f'Number of Studies by Country for {study_type}')
        return fig

    study_types = list(studies['study_type'].unique())

    result_div = html.Div([
    html.H1("Choropleth Map of Studies by Study Type"),
    dcc.Dropdown(id='study_type_dropdown',
                 options=[{'label': st, 'value': st} for st in study_types],
                 value=study_types[0]),
    dcc.Graph(id='choropleth_map')
    ])

    @app.callback(
        Output('choropleth_map', 'figure'),
        Input('study_type_dropdown', 'value'))
    def update_map(study_type):
        return generate_map(study_type)

    return result_div


