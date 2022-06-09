from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from BDSE.individual_Assignment_2.mongodb.retrieveData import retrieve_all

data = retrieve_all('hotels')
data = data[['Hotel_Name', 'Average_Score', 'Total_Number_of_Reviews']]
data = data.rename(columns={'Hotel_Name': 'Hotel Name', 'Average_Score': 'Average Score',
                            'Total_Number_of_Reviews': 'Reviews amount'})
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
            md=8
            ),
        dbc.Col(
            dash_table.DataTable(
                style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'lineHeight': '15px'
                    },
                data=data.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in data.columns],
                page_action='none',
                style_table={'height': '400px', 'overflowY': 'auto'}
            ),
            md=4
        ),
    ]),
])

hotels_map = html.Div([
    html.H3('Home'),
    dcc.Dropdown(
        {f'Page 1 - {i}': f'{i}' for i in ['New York City', 'Montreal', 'Los Angeles']},
        id='page-1-dropdown'
    ),
    html.Div(id='page-1-display-value'),
])
