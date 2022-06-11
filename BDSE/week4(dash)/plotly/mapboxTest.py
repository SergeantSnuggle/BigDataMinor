import dash
import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash_table import DataTable

import pandas as pd

url = "https://github.com/plotly/datasets/raw/master/" "26k-consumer-complaints.csv"
df = pd.read_csv(url)

app = dash.Dash(__name__)
app.scripts.config.serve_locally = True

columns = [
    {"id": 0, "name": "Complaint ID"},
    {"id": 1, "name": "Product"},
    {"id": 2, "name": "Sub-product"},
    {"id": 3, "name": "Issue"},
    {"id": 4, "name": "Sub-issue"},
    {"id": 5, "name": "State"},
    {"id": 6, "name": "ZIP"},
    {"id": 7, "name": "code"},
    {"id": 8, "name": "Date received"},
    {"id": 9, "name": "Date sent to company"},
    {"id": 10, "name": "Company"},
    {"id": 11, "name": "Company response"},
    {"id": 12, "name": "Timely response?"},
    {"id": 13, "name": "Consumer disputed?"},
]

app.layout = html.Div([
    html.Button(
        ['Update'],
        id='btn'
    ),
    DataTable(
        id='table',
        data=[]
    )
])

@app.callback(
    [Output("table", "data"), Output('table', 'columns')],
    [Input("btn", "n_clicks")]
)
def updateTable(n_clicks):
    if n_clicks is None:
        return df.values[0:100], columns

    return df.values[100:110], columns[0:3]

if __name__ == "__main__":
    app.run_server(port=8050)