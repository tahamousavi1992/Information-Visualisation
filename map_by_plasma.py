# Define the original array

import pandas as pd
import extract
import numpy as np

# studies, sponsors, facilities, design_groups, conditions, interventions = extract.load_all_data()

# facilities = extract.load_csv('data/facilities.txt', ['nct_id', 'status','name','city','state','country'])
# all_cities = extract.load_csv('data/all-cities.csv', ['Name','ASCII Name','Alternate Names'])
# f_u = facilities['city'].unique()
# a_u = np.concatenate((all_cities['Name'].unique(), all_cities['ASCII Name'].unique(), all_cities['Alternate Names'].unique()))
# not_in_array1 = [x for x in f_u if x not in a_u]
# print(len(not_in_array1))



# Read data from CSV
cities = pd.read_csv("data.csv")

import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

# Create a scatter plot on a map with red markers
fig = go.Figure()

fig.add_trace(go.Scattergeo(
    lat=cities["latitude"],
    lon=cities["longitude"],
    mode="markers",
    marker=dict(
        size=6,  # Set a fixed size for the red dot markers
        color="red"
    ),
    text=cities["city"] + ", Population: " + cities["population"].astype(str),
    hoverinfo="text"
))

fig.add_trace(go.Scattergeo(
    lon=cities["longitude"],
    lat=cities["latitude"],
    mode="markers",
    marker=dict(
        size=3,
        color="blue"
    ),
    text=cities["city"],
    hoverinfo="text",
    showlegend=False,  # Do not show a legend for city markers
    locations=[f"{city}, {country}" for city, country in zip(cities["city"], cities["country"])],  # Combine city and country names
    locationmode="country names"  # Specify that city locations are given as country names in the locations list
))

fig.update_layout(
    geo=dict(
        showland=True,
        showcountries=True,
        showocean=True,
        resolution=50,
        projection=dict(type='natural earth'),
        countrycolor="rgb(217, 217, 217)",  # Set country border color
        showsubunits=True,
        subunitcolor="rgb(217, 217, 217)",  # Set subunit border color
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='city-population-map',
        figure=fig,
        style={'height': '100vh'}  # Set the height of the graph
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
