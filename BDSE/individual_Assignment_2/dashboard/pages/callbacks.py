import base64

from dash import Input, Output, callback, State, dash_table, callback_context, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from BDSE.individual_Assignment_2.mongodb.retrieveData import db, retrieve_unique_hotels, retrieve_amount_reviews, \
    retrieve_amount_labelled, retrieve_amount_hotels, retrieve_avg_nat
from BDSE.individual_Assignment_2.models.dask import daskML
from BDSE.individual_Assignment_2.models.keras.regular import regular
from BDSE.individual_Assignment_2.models.keras.recurrent import recurrent
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate


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
        return emptyDf.to_dict('records'), [{'id': c, 'name': c} for c in emptyDf.columns]
    else:
        hotel = value['points'][0]['text']
        filter = {"Hotel_Name": hotel}
        result = db.hotel_reviews_raw.find(filter, {'_id': False})
        source = list(result)
        resultDf = pd.DataFrame(source)
        dataTable = resultDf[['Negative_Review', 'Positive_Review', 'Reviewer_Score']]
        return dataTable.to_dict("records"), [{'id': c, 'name': c} for c in dataTable.columns]


@callback(
    Output('dask-output', 'children'),
    Input('dask-button', 'n_clicks'),
    State('dask-input', 'value'),
)
def dask_result(n_clicks, value):
    value = str(value)
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'dask-button' not in changed_id:
        raise PreventUpdate
    result = daskML.live_predict_dask(value)
    if result > 0.5:
        return 'positive'
    else:
        return 'negative'


@callback(
    Output('keras-ann-output', 'children'),
    Input('keras-ann-button', 'n_clicks'),
    State('keras-ann-input', 'value'),
)
def keras_ann_result(n_clicks, value):
    value = str(value)
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'keras-ann-button' not in changed_id:
        raise PreventUpdate
    result = regular.live_predict_model_regular(value)
    if result > 0.5:
        return 'positive'
    else:
        return 'negative'


@callback(
    Output('keras-rnn-output', 'children'),
    Input('keras-rnn-button', 'n_clicks'),
    State('keras-rnn-input', 'value'),
)
def keras_rnn_result(n_clicks, value):
    value = str(value)
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'keras-rnn-button' not in changed_id:
        raise PreventUpdate
    result = recurrent.live_predict_model_recurrent(value)
    if result > 0.5:
        return 'positive'
    else:
        return 'negative'


@callback(
    Output('dask-results', 'children'),
    Output('keras-ann-results', 'children'),
    Output('keras-rnn-results', 'children'),
    Input('model_results', 'value'),
)
def get_model_results(result_id):
    daskResults = daskML.get_dask_results()
    kerasAnnResults = regular.get_regular_results()
    kerasRnnResults = recurrent.get_recurrent_results()

    daskImage = 'E:/Roy Dijkstra/School/BigData/BDSE/individual_Assignment_2/dashboard/images/daskModel.png'
    encodedDaskImage = base64.b64encode(open(daskImage, 'rb').read())
    kerasAnnImage = 'E:/Roy Dijkstra/School/BigData/BDSE/individual_Assignment_2/dashboard/images/annmodel.png'
    encodedKerasAnnImage = base64.b64encode(open(kerasAnnImage, 'rb').read())
    kerasRnnImage = 'E:/Roy Dijkstra/School/BigData/BDSE/individual_Assignment_2/dashboard/images/rnnmodel.png'
    encodedkerasRnnImage = base64.b64encode(open(kerasRnnImage, 'rb').read())

    daskCard = dbc.Card([
        dbc.CardHeader("Dask Incremental"),
        html.Img(src='data:image/png;base64,{}'.format(encodedDaskImage.decode())),
        dbc.CardBody([
            html.P(children=[create_values(name, value) for name, value in daskResults.items()]), html.Br(),
        ])
    ])
    kerasAnnCard = dbc.Card([
        dbc.CardHeader("Keras ANN"),
        html.Img(src='data:image/png;base64,{}'.format(encodedKerasAnnImage.decode())),
        dbc.CardBody([
            html.P(children=[create_values(name, value) for name, value in kerasAnnResults.items()]), html.Br(),
        ])
    ])
    kerasRnnCard = dbc.Card([
        dbc.CardHeader("Keras RNN"),
        html.Img(src='data:image/png;base64,{}'.format(encodedkerasRnnImage.decode())),
        dbc.CardBody([
            html.P(children=[create_values(name, value) for name, value in kerasRnnResults.items()]), html.Br(),
        ])
    ])

    return daskCard, kerasAnnCard, kerasRnnCard


def create_values(name, value):
    return html.P(str(name) + ": " + str(value))


@callback(
    Output('dashboard-top', 'children'),
    Input('dashboard-top', 'value'),
)
def get_top_dashboard(value):
    cardGroup = dbc.CardGroup([
        dbc.Card([
            dbc.CardHeader('Hoeveelheid reviews:'),
            dbc.CardBody(
                html.P(str(retrieve_amount_reviews()), className='card-text'),

            ),
        ]),
        dbc.Card([
            dbc.CardHeader('Hoeveel labelled:'),
            dbc.CardBody([
                html.P("Positief: " + str(retrieve_amount_labelled(1)), className='card-text'),
                html.P("Negatief: " + str(retrieve_amount_labelled(0)), className='card-text'),
            ]),
        ]),
        dbc.Card([
            dbc.CardHeader('Hoeveelheid hotels:'),
            dbc.CardBody(
                html.P(str(retrieve_amount_hotels()), className='card-text'),

            ),
        ]),
        dbc.Card([
            dbc.CardHeader('Gemiddelde score per nationaliteit'),
            dbc.CardBody(
                html.Div(
                    dbc.Table.from_dataframe(retrieve_avg_nat(), striped=True, bordered=True, hover=True),
                    style={"maxHeight": "200px", "overflow": "scroll"}
                )

            ),
        ])
    ])
    return cardGroup