import plotly.express as px
import pandas as pd
import extract


"""def getChart(facilities):
    country_counts = facilities.groupby('country')['nct_id'].nunique().reset_index()
    country_counts.columns = ['country', 'num_studies']
    top_countries = country_counts.sort_values('num_studies', ascending=False).head(20)
    other_studies = country_counts.sort_values('num_studies', ascending=False).tail(len(country_counts) - 20)['num_studies'].sum()
    other_row = pd.DataFrame({'country': ['Other'], 'num_studies': [other_studies]})
    top_countries = top_countries._append(other_row, ignore_index=True)

    fig = px.bar(top_countries, x='country', y='num_studies', title='Number of Studies by Country (Top 20 + Other)')
    return fig"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def preprocess_data(facilities, studies):
    # Replace NA values with "Unknown" in the status column
    studies['status'] = studies['status'].fillna('Unknown')

    # Remove duplicate nct_ids
    studies = studies.drop_duplicates(subset='nct_id')

    # Merge the dataframes
    merged_df = facilities.merge(studies[['nct_id', 'status']], on='nct_id')

    # Group the data by countries and statuses
    grouped = merged_df.groupby(['country', 'status']).nct_id.nunique().reset_index()

    return grouped

def create_bar_chart(facilities):
    top_countries = facilities['country'].value_counts().head(20).index
    facilities['country'] = facilities['country'].apply(lambda x: x if x in top_countries else 'Others')

    fig = make_subplots(specs=[[{'secondary_y': True}]])
    statuses = facilities['status'].unique()

    for status in statuses:
        filtered_df = facilities[facilities['status'] == status]
        fig.add_trace(go.Bar(x=filtered_df['country'], y=filtered_df['nct_id'], name=status))

    fig.update_layout(title="Number of Studies by Country and Status",
                      xaxis_title="Country",
                      yaxis_title="Number of Studies",
                      barmode='stack')

    return fig

def add_dropdown_menu(fig, facilities):
    statuses = facilities['status'].unique()

    updatemenu = [{
        "buttons": [go.layout.Updatemenu.Button(
            args=[{'visible': [s == status for s in statuses]}],
            label=status,
            method="update") for status in statuses],
        "direction": "down",
        "showactive": True
    }]

    fig.update_layout(updatemenus=updatemenu)
    return fig

def main(data, data2):
    preprocessed_data = preprocess_data(data, data2)
    bar_chart = create_bar_chart(preprocessed_data)
    bar_chart_with_dropdown = add_dropdown_menu(bar_chart, preprocessed_data)
    return bar_chart_with_dropdown

if __name__ == '__main__':
    studies = extract.load_all_data()[0]
    facilities = extract.load_all_data()[2]
    fig = main(studies, facilities)
    fig.show()

else:
    from . import preprocess_data, create_bar_chart, add_dropdown_menu
    def main(facilities, studies):
        preprocessed_data = preprocess_data(facilities, studies)
        bar_chart = create_bar_chart(preprocessed_data)
        bar_chart_with_dropdown = add_dropdown_menu(bar_chart, preprocessed_data)
        return bar_chart_with_dropdown

