"""Module docstring"""

from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

from dashboard.app import db_data
from dashboard.components import ids
from dashboard.components.charts.layout import (
    general_chart_layout,
    horizontal_bar_layout,
)
from dashboard.utilities import format_enums, split_title


def plot_database_summary(field: str, component_id: str, category: str) -> html.Div:
    """_summary_

    Args:
        component_id: _description_
        category: _description_
    """
    df = db_data.count_words_per_category(field, category)

    categories = [format_enums(s) for s in df.get_column(category).to_list()]
    customdata = np.stack((df.get_column(field), categories), axis=-1)
    hovertemplate = "%{customdata[1]}<br>%{customdata[0]}<extra></extra>"

    data = go.Bar(
        y=categories,
        x=df.get_column(field).to_list(),
        marker={"color": "steelblue"},
        orientation="h",
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

    layout = dict(
        **general_chart_layout,
        **horizontal_bar_layout,
        title_text=f"{split_title(field)} Count per {split_title(category)}",
        margin={"t": 60, "r": 30},
    )

    fig = go.Figure(data=data, layout=layout)

    return html.Div(dcc.Graph(figure=fig), id=component_id)


@callback(
    Output(ids.PART_OF_SPEECH_BAR_CHART, "children"),
    Input(ids.ID_WORD_SELECTOR, "value"),
)
def plot_database_part_of_speech_summary(field: str) -> html.Div:
    return plot_database_summary(field, ids.PART_OF_SPEECH_BAR_CHART, "PartOfSpeech")


@callback(
    Output(ids.WORD_CATEGORY_BAR_CHART, "children"),
    Input(ids.ID_WORD_SELECTOR, "value"),
)
def plot_database_word_category_summary(field: str) -> html.Div:
    return plot_database_summary(field, ids.WORD_CATEGORY_BAR_CHART, "WordCategory")


@callback(
    Output(ids.GRAMMAR_CATEGORY_BAR_CHART, "children"),
    Input(ids.ID_WORD_SELECTOR, "value"),
)
def plot_database_grammar_category_summary(field: str) -> html.Div:
    return plot_database_summary(
        field, ids.GRAMMAR_CATEGORY_BAR_CHART, "GrammarCategory"
    )
