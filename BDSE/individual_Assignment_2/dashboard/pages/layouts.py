from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from BDSE.individual_Assignment_2.mongodb.retrieveData import retrieve_all, db
import plotly.graph_objects as go

data = retrieve_all('hotels')
# filter = {"Hotel_Name": "hotel"}
# result = db.hotel_reviews_raw.find(filter, {'_id': False})
# source = list(result)
# resultDf = pd.DataFrame(source)
# dataTable = resultDf[['Negative_Review', 'Positive_Review', 'Reviewer_Score']]


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
