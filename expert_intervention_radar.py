import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

def create_radar_layout(design_groups: pd.DataFrame) -> html.Div:
    # Group the dataframe by 'intervention_type' and count the number of 'nct_id'
    counts = design_groups.groupby('group_type')['nct_id'].count().reset_index()
    
    # Create a radar plot using Plotly
    fig = go.Figure(go.Scatterpolar(
        r=counts['nct_id'],
        theta=counts['group_type'],
        mode='lines',
        fill='toself',
        
    ))
    
    # Set up the layout for the radar plot
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, counts['nct_id'].max()]
            )),
        showlegend=False
    )

    # Return the layout containing the radar plot
    return html.Div([
        dcc.Graph(id='intervention-radar-plot', figure=fig)
    ])
