"""Module docstring"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from dashboard.app import db_data
from dashboard.components import ids


dash.register_page(__name__, name="Database Summary", title="Database")

layout = html.Div(
    children=[
        html.H1("Database Summary", style={"height": "4vh"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Number of Words in Database", className="text-center"),
                        html.Div(db_data.unique_word_count, className="divCard"),
                    ],
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    [
                        html.H4(
                            "Number of Word Groups in Database",
                            className="text-center",
                        ),
                        html.Div(db_data.unique_word_group_count, className="divCard"),
                    ],
                    className="divRoundedBorder",
                ),
            ],
        ),
        html.Div(
            [
                "Input: ",
                dcc.RadioItems(
                    id=ids.ID_WORD_SELECTOR,
                    options=["WordID", "WordGroup"],
                    value="WordID",
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id=ids.WORD_CATEGORY_BAR_CHART),
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    html.Div(id=ids.PART_OF_SPEECH_BAR_CHART),
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    html.Div(id=ids.GRAMMAR_CATEGORY_BAR_CHART),
                    className="divRoundedBorder",
                ),
            ],
        ),
    ],
)
