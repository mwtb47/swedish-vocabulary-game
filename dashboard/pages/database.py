"""Module docstring"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

from dashboard.app import db_data
from dashboard.components import DatabaseIds
from dashboard.utilities import split_title


dash.register_page(__name__, name="Database Summary", title="Database")


def update_chart_title(ID: str, category: str):
    """_summary_

    Args:
        ID: _description_
        category: _description_

    Returns:
        _description_
    """
    return html.H6(
        f"{split_title(ID)} Count per {category}", className="container-title"
    )


@callback(
    Output(DatabaseIds.WORD_CATEGORY_BAR_CHART_TITLE, "children"),
    Input(DatabaseIds.ID_GROUP_SELECTOR, "value"),
)
def update_word_category_title(ID: str):
    """_summary_

    Args:
        ID: _description_

    Returns:
        _description_
    """
    return update_chart_title(ID, "Word Category")


@callback(
    Output(DatabaseIds.GRAMMAR_CATEGORY_BAR_CHART_TITLE, "children"),
    Input(DatabaseIds.ID_GROUP_SELECTOR, "value"),
)
def update_grammar_category_title(ID: str):
    """_summary_

    Args:
        ID: _description_

    Returns:
        _description_
    """
    return update_chart_title(ID, "Grammar Category")


@callback(
    Output(DatabaseIds.PART_OF_SPEECH_BAR_CHART_TITLE, "children"),
    Input(DatabaseIds.ID_GROUP_SELECTOR, "value"),
)
def update_part_of_speech_title(ID: str):
    """_summary_

    Args:
        ID: _description_

    Returns:
        _description_
    """
    return update_chart_title(ID, "Part of Speech")


layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6(
                            "Number of Words in Database", className="container-title"
                        ),
                        html.Div(db_data.unique_word_count, className="card"),
                    ],
                    className="rounded-border",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "Number of Word Groups in Database",
                            className="container-title",
                        ),
                        html.Div(db_data.unique_word_group_count, className="card"),
                    ],
                    className="rounded-border",
                ),
            ],
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Div(
                        dcc.RadioItems(
                            id=DatabaseIds.ID_GROUP_SELECTOR,
                            options=["WordID", "WordGroup"],
                            value="WordID",
                            inputStyle={"margin-right": "2px"},
                            labelStyle={"margin-right": "10px"},
                        ),
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        id=DatabaseIds.WORD_CATEGORY_BAR_CHART_TITLE
                                    ),
                                    html.Div(id=DatabaseIds.WORD_CATEGORY_BAR_CHART),
                                ],
                                className="rounded-border",
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        id=DatabaseIds.PART_OF_SPEECH_BAR_CHART_TITLE
                                    ),
                                    html.Div(id=DatabaseIds.PART_OF_SPEECH_BAR_CHART),
                                ],
                                className="rounded-border",
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        id=DatabaseIds.GRAMMAR_CATEGORY_BAR_CHART_TITLE
                                    ),
                                    html.Div(id=DatabaseIds.GRAMMAR_CATEGORY_BAR_CHART),
                                ],
                                className="rounded-border",
                            ),
                        ],
                    ),
                ],
                className="rounded-border one-per-row",
            ),
        ),
    ],
)
