from dash import Input, Output, callback, State
import pandas as pd
import plotly.express as px
from BDSE.individual_Assignment_2.mongodb.retrieveData import db


@callback(
    Output('page-1-display-value', 'children'),
    Input('page-1-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'


@callback(
    Output('page-2-display-value', 'children'),
    Input('page-2-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'


@callback(
    Output("hotels-map", 'figure'),
    Input('dropdown-score', 'value'))
def update_map(min_hotel_score):
    min_hotel_score = round(float(min_hotel_score))
    query = {"Average_Score": {"$gte": int(min_hotel_score)}}
    results = db.hotels.find(query, {'_id': False})
    hotels = pd.DataFrame(list(results))

    fig = px.scatter_mapbox(hotels,
                            lat="lat",
                            lon="lng",
                            hover_name="Hotel_Name",
                            hover_data=["Hotel_Address",
                                           "Average_Score",
                                           "Total_Number_of_Reviews",
                                           "lat",
                                           "lng"],
                            color_discrete_sequence=["blue"],
                            zoom=3,
                            height=400)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig