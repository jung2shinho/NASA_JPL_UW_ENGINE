import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from flask import Flask
import os
import sys

# Adjusting PYTHONPATH to os.getcwd()
sys.path.append(os.getcwd())

flask_server = Flask(__name__)

JPL_LOGO = 'https://upload.wikimedia.org/wikipedia/commons/c/c6/Jet_Propulsion_Laboratory_logo.svg'
UW_LOGO = 'https://upload.wikimedia.org/wikipedia/commons/1/17/Washington_Huskies_logo.svg'

# Create App with external style sheet
app = Dash(__name__,
        #    pages_folder="../pages",
           server = flask_server,
           use_pages=True,
           external_stylesheets=['assets/css/markdown.css', dbc.themes.PULSE],
           meta_tags=[{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0'}]
)

server = app.server

# NAVBAR
navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    page['name'], 
                    href=page['path']))
                for page in dash.page_registry.values()
        ],
        brand=dbc.Row(
            [
            dbc.Col(
                [html.Img(src=UW_LOGO, height="30px", width="40px")],
            ),
            dbc.Col(
                [html.Img(src=JPL_LOGO, height="30px", width="40px")],
                ),
            dbc.Col(html.H4("2024 UW ENGINE")), # Adjust the brand name and margin as needed
            ],
        style={"max-width": "80vw"}
        ),
        brand_href="/",
        color="primary",
        dark=True,
        className='navbar-title'
)
# Define the main content
content = html.Div(
    [dash.page_container],
    style={"padding":"1rem"}
)

# Enter layout here
app.layout = html.Div([
    # NAVBAR
    navbar,
    # MAIN CONTENT
    content
    ],
    className="justify-center"
)


if __name__ == '__main__':
    app.run(debug=True, port=8050)