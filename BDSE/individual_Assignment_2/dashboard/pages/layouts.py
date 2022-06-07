from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import BDSE.individual_Assignment_2.mongodb.retrieveData as retrieve

hotels = retrieve.retrieve_all("hotels")
fig = px.scatter_mapbox(hotels, lat="lat", lon="lng", hover_name="Hotel_Name", hover_data=["Hotel_Address",
                                                                                           "Average_Score",
                                                                                           "Total_Number_of_Reviews",
                                                                                           "lat",
                                                                                           "lng"],
                        color_discrete_sequence=["fuchsia"], zoom=3)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

home = html.Div([
    dcc.Graph(id="map", figure=fig)
])

hotels_map = html.Div([
    html.H3('Home'),
    dcc.Dropdown(
        {f'Page 1 - {i}': f'{i}' for i in ['New York City', 'Montreal', 'Los Angeles']},
        id='page-1-dropdown'
    ),
    html.Div(id='page-1-display-value'),
])
