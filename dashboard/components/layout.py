"""Module with function to create the app layout.

Functions:
    create_layout: Create the app layout.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc


def create_layout() -> html.Div:
    """Create the app layout.

    Returns:
        Dash HTML Div containing the app layout.
    """

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H3(
                            "Vocabulary Game Dashboard",
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
                            style={"height": "100%"},
                        ),
                    ),
                ],
                style={"background-color": "grey"},
            ),
            dash.page_container,
        ],
    )
