from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from BDSE.individual_Assignment_2.mongodb.retrieveData import retrieve_all, db
import plotly.graph_objects as go

data = retrieve_all('hotels')

variables = {"Negative_Review": "", 'Positive_Review': "", 'Reviewer_Score': ""}
emptyDf = pd.DataFrame(variables, index=[])

score_choices = []
for i in range(1, 11):
    score_choices.append({"label": str(i), "value": i})

home = dbc.Container([
    dbc.Row(
        dbc.Col(
            [
                html.P('Minimum score'),
                dcc.Dropdown(
                    id='dropdown-score',
                    options=score_choices,
                    value=1,
                    clearable=False
                )
            ], className='text-center'
        )
    ),
    dbc.Row([
        dbc.Col(
            dbc.Spinner(children=[dcc.Graph(id="hotels-map")], color='primary'),
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Spinner(children=[
                dash_table.DataTable(
                    id='reviews-table',
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'lineHeight': '15px'
                    },
                    data=emptyDf.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in emptyDf.columns],
                    page_action='none',
                    editable=True,
                    sort_action="native",
                    sort_mode='multi',
                    style_table={'height': '400px', 'overflowY': 'auto'}
                )],
            )
        ),
    ]),
])

models = dbc.Container([
    dbc.Row([
        dbc.Col(
            id='dask-results',
            md=4,
        ),
        dbc.Col(
            id='keras-ann-results',
            md=4,
        ),
        dbc.Col(
            id='keras-rnn-results',
            md=4,
        ),
    ], id='model_results'
    )
])

test_site = dbc.Container([
    dbc.Row()
])

test_models = dbc.Container([
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardHeader('Test models:'),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Label("Dask:", width=2),
                            dbc.Col(
                                dbc.Input(id='dask-input', type='text'),
                                width=6
                            ),
                            dbc.Col(
                                dbc.Button(id='dask-button', n_clicks=0, children='Submit'),
                                width=2
                            ),
                            dbc.Col(
                                dbc.Spinner(children=[html.Div(id='dask-output')], size='sm', color='primary'),
                                width=2
                            ),
                        ], className='mb-3',
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Keras ANN:", width=2),
                            dbc.Col(
                                dbc.Input(id='keras-ann-input', type='text'),
                                width=6
                            ),
                            dbc.Col(
                                dbc.Button(id='keras-ann-button', n_clicks=0, children='Submit'),
                                width=2
                            ),
                            dbc.Col(
                                dbc.Spinner(children=[html.Div(id='keras-ann-output')], size='sm', color='primary'),
                                width=2
                            ),
                        ], className='mb-3',
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Keras RNN:", width=2),
                            dbc.Col(
                                dbc.Input(id='keras-rnn-input', type='text'),
                                width=6
                            ),
                            dbc.Col(
                                dbc.Button(id='keras-rnn-button', n_clicks=0, children='Submit'),
                                width=2
                            ),
                            dbc.Col(
                                dbc.Spinner(children=[html.Div(id='keras-rnn-output')], size='sm', color='primary'),
                                width=2
                            ),
                        ], className='mb-3',
                    )
                ]
            )], className='text-center'
        ), id='test-keras-artificial'
        ),
    )
])
