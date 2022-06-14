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
            dcc.Graph(id="hotels-map"),
        ),
    ]),
    dbc.Row([
        dbc.Col(
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
            ),
        ),
    ]),
])
test_site = dbc.Container([
    dbc.Row()

])

models = dbc.Container([
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardHeader('Keras Recurrent Neural Network'),
            dbc.CardBody(
                [
                    dbc.Form(
                        dbc.Row(
                            [
                                dcc.Input(id='input-1-state', type='text'),
                                html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
                            ]
                        )
                    ),
                    html.Div(id='output-state')
                ]
            )], className='text-center'
        ), id='test-keras-recurrent'
        ),
    )
])
