"""
Created on Tue Sep  3 14:06:02 2019

@author: MCAngel
"""
import flask
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import base64
import pandas as pd
from dash.dependencies import Input, Output, State
import os
from blueprints.auth.decorators import login_required
from . import appsettings as config


def protect_dashviews(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])


def create_dashapp(server):
    """
    Init our dashapp, to be embedded into flask
    """
    app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/dash/',
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        assets_folder='assets')
    app.config['suppress_callback_exceptions'] = True
    app.title = 'My Dash App'
    protect_dashviews(app)

    app.layout = get_layout(server)

    # add callback for toggling the mavbar collapse on small screens
    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")])
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # Add callback for writing name of user to navbar and rendering main content
    @app.callback([Output('page-content', 'children'),
                   Output('navbar-navigation', 'label')],
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if 'user.displayName' in flask.session:
            user = flask.session['user.displayName']
        else:
            user = 'Unknown'

        switcher = {
            '/dash/'                            : layout_main(),
            '/about'                            : layout_about(),
            # Add new pages here
        }
        page_content = switcher.get(pathname, layout_main())
        return page_content, user

    #Add other callbacks here 
    # ...

    # End of create_app method, return the flask app aka server (not the dash app)
    return app.server


def get_layout(server, flash_messages: list = []):
    navbar = __layout_navbar()
    dash_main = html.Div([       
        dcc.Location(id='url', refresh=False), # represents the URL bar, doesn't render anything
        html.Div(id='page-content') #placeholder for content
    ]) 
    
    body = dbc.Container([dash_main], fluid=True)
    layout = html.Div([navbar, body])
    return layout


def layout_about():
    return html.Div(html.P(f'Example dash app with AAD authentication, v{config.APP_VERSION}'))


def layout_main():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

    from .services.RapidApiRugbyServiceClient import get_rugby_standings
    title, df = get_rugby_standings()
    
    standings_table = dash_table.DataTable(
        id='table',
        columns=[{"name": i.title().replace('_', ' '), "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_data_conditional=[
        {
            'if': { 'filter_query': '{id} = 3317' },
            'backgroundColor': '#9D2235',
            'color': 'white'
        }]
    )
    return [html.Br(), html.P(html.B(title)), standings_table]


def __layout_navbar():
    PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
    return dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("andysprague.com", className="ml-2", style={'letter-spacing': '5px'})),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href=config.APPLICATION_HOME,
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Nav(
                        dbc.DropdownMenu(
                            id="navbar-navigation",
                            nav=True,
                            in_navbar=True,
                            label='Unknown User',
                            children=[
                                dbc.DropdownMenuItem("About", href="/about"),
                                dbc.DropdownMenuItem("Logout", href="/auth/logout", external_link=True),
                            ]),
                        className="ml-auto", navbar=True
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
        sticky="top"
    )
