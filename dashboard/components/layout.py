"""Module with a function to create the app layout."""

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc


@callback(Output("subheader", "children"), [Input("url", "pathname")])
def callback_func(pathname):
    if pathname == "/":
        return "Answers Summary"
    if pathname == "/database":
        return "Database Summary"
    return "Performance Summary"


def create_layout() -> html.Div:
    """Create the app layout.

    Returns:
        html.Div containing the app layout.
    """

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H2("Vocabulary Game Dashboard"),
                                html.H4(id="subheader"),
                                dcc.Location(id="url"),
                            ],
                            style={
                                "position": "relative",
                                "top": "50%",
                                "transform": "translateY(-50%)",
                            },
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                dbc.NavLink(
                                    "Answers Summary",
                                    href="/",
                                    className="nav-button",
                                ),
                                dbc.NavLink(
                                    "Database Summary",
                                    href="/database",
                                    className="nav-button",
                                ),
                                dbc.NavLink(
                                    "Performance Summary",
                                    href="/performance",
                                    className="nav-button",
                                ),
                            ],
                            style={"height": "100%", "float": "right"},
                        ),
                    ),
                ],
            ),
            html.Hr(className="header-divider"),
            dash.page_container,
        ],
    )
