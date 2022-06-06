import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback

from pages.layouts import home, hotels_map
import pages.callbacks

app = dash.Dash(
    title='Dashboard',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.config.suppress_callback_exceptions = True

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
NAVBAR_STYLE = {
    "background-color": "#f8f9fa",
    "color": "black",
    "margin-left": "16rem",
}

navbar = dbc.NavbarSimple(

    style=NAVBAR_STYLE,
    brand="Hotel reviews",
)
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H4("Assignment 2", className="display-6"),
        html.Hr(),
        html.P(
            "Dashboard Roy Dijkstra", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", id='home', active="exact"),
                dbc.NavLink("Models", href="/models", id='models', active="exact"),
                dbc.NavLink("Test models", href="/test-models", id='test-models', active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url", refresh=False), navbar, sidebar, content])


@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/home' or pathname == '/':
         return home
    elif pathname == '/models':
         return hotels_map
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)