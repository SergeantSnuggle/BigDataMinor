from dash import Input, Output, callback, State, dash_table
import pandas as pd
import plotly.express as px
from BDSE.individual_Assignment_2.mongodb.retrieveData import db, retrieve_unique_hotels
import plotly.graph_objects as go


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
    data = retrieve_unique_hotels(min_hotel_score)

    figure = go.Figure(go.Scattermapbox(
        lat=data['lat'],
        lon=data['lng'],
        text=data['Hotel_Name'],

        # customdata=active_sensors['creation_date'].astype(str),
        selected={'marker': {'opacity': 0.5, 'size': 10}},
        unselected={'marker': {'opacity': 1}},

        mode='markers',
        marker=go.scattermapbox.Marker(
            size=5,
            # color=active_sensors['state'].astype(int),
            # colorscale=['green', 'red']
        ),
        # add <extra></extra> in order to remove trace 0
        hovertemplate="<b>" + data['Hotel_Name'] + "</b><br><br>" +
                      "Locatiebeschrijving: " + data['Hotel_Address'] + "<br>" +
                      "Total number of reviews: " + data['Total_Number_of_Reviews'].astype(str) + "<br>" +
                      "Average Score: " + data['Average_Score'].astype(str) + "<br>" + '<extra></extra>',
    ))

    figure.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox_style='dark',
        clickmode='event+select',
        uirevision=True,
        margin=dict(l=0, r=0, t=0, b=0),
        mapbox=dict(
            accesstoken="pk.eyJ1Ijoic2VyZ2VhbnRzbnVnZ2xlIiwiYSI6ImNsNDh2dG13azAxYWszZG9lOG51Z3Z1Z2QifQ.DcaXcbQ8Purwf9k7"
                        "gdTNFw",
            bearing=0,
            center=dict(
                lat=52.370498703824424,
                lon=4.896632321228936
            ),
            pitch=0,
            zoom=3
        ),
    )
    return figure


@callback(
    Output("reviews-table", "data"),
    Output("reviews-table", "columns"),
    Input('hotels-map', 'clickData')
)
def update_table_map(value=None):
    if value is None:
        variables = {"Negative_Review": "", 'Positive_Review': "", 'Reviewer_Score': ""}
        emptyDf = pd.DataFrame(variables, index=[])
        return emptyDf
    else:
        hotel = value['points'][0]['text']
        filter = {"Hotel_Name": hotel}
        result = db.hotel_reviews_raw.find(filter, {'_id': False})
        source = list(result)
        resultDf = pd.DataFrame(source)
        dataTable = resultDf[['Negative_Review', 'Positive_Review', 'Reviewer_Score']]
        return dataTable.to_dict("records"), [{'id': c, 'name': c} for c in dataTable.columns]