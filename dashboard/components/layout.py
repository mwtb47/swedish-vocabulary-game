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
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"]))
                    for page in dash.page_registry.values()
                ],
                brand="Vocabulary Game Dashboard",
                brand_href="/",
                color="dark",
                dark=True,
            ),
            dash.page_container,
        ],
    )
