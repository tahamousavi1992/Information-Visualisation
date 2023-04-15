# Define the original array

# import pandas as pd
# import extract
# import numpy as np

# # studies, sponsors, facilities, design_groups, conditions, interventions = extract.load_all_data()

# facilities = extract.load_csv('data/facilities.txt', ['nct_id', 'status','name','city','state','country'])
# all_cities = extract.load_csv('data/all-cities.csv', ['Name','ASCII Name','Alternate Names'])
# f_u = facilities['city'].unique()
# a_u = np.concatenate((all_cities['Name'].unique(), all_cities['ASCII Name'].unique(), all_cities['Alternate Names'].unique()))
# # Convert all strings to lowercase
# a_u_lower = [str(s).lower() for s in a_u]
# f_u_lower = [str(s).lower() for s in f_u]

# not_in_array1 = []
# for f in  f_u_lower:
#     for a in a_u_lower:
#         if f in a:
#             break
#     else:  # This else block is executed if the inner loop does not encounter a break statement
#         not_in_array1.append(f)
#         continue

# print(len(not_in_array1))

import plotly.graph_objects as go

# Create a choropleth map with data
fig = go.Figure(go.Choropleth(
    locations = ['USA', 'CAN', 'MEX'], # example countries
    z = [1, 2, 3], # example data
    colorscale = 'Blues',
    text = ['United States', 'Canada', 'Mexico'], # example country names
    marker_line_color='darkgray',
    marker_line_width=0.5,
))

# Add a title and adjust layout
fig.update_layout(
    title_text = 'Example Map with Country Names',
    geo_scope='north america', # adjust the map size to region
)

# Show the figure
fig.show()

# # Read data from CSV
# cities = pd.read_csv("data.csv")


# import pandas as pd
# import plotly.graph_objects as go
# import dash
# import dash_core_components as dcc
# import dash_html_components as html

# # Create a scatter plot on a map with red markers
# fig = go.Figure()

# fig.add_trace(go.Scattermapbox(
#     lat=cities["latitude"],
#     lon=cities["longitude"],
#     mode="markers",
#     marker=dict(
#         size=6,  # Set a fixed size for the red dot markers
#         color="red"
#     ),
#     text=cities["city"] + ", Population: " + cities["population"].astype(str),
#     hoverinfo="text"
# ))

# fig.add_trace(go.Scattermapbox(
#     lat=cities["latitude"],
#     lon=cities["longitude"],
#     mode="markers",
#     marker=dict(
#         size=3,
#         color="blue"
#     ),
#     text=cities["city"],
#     hoverinfo="text",
#     showlegend=False,  # Do not show a legend for city markers
# ))

# fig.update_layout(
#     mapbox=dict(
#         center=dict(lat=0, lon=0),
#         style="carto-positron",
#         zoom=1,
#     ),
#     margin=dict(l=0, r=0, t=0, b=0)
# )

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     dcc.Graph(
#         id='city-population-map',
#         figure=fig,
#         style={'height': '100vh'}  # Set the height of the graph
#     )
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)


# Find all strings in f_u_lower that are not in a_u_lower

