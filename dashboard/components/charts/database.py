"""Module docstring"""

from dash import dcc, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

from dashboard.app import db_data
from dashboard.components import ids
from dashboard.components.charts.layout import (
    general_chart_layout,
    horizontal_bar_layout,
    SummaryColours,
)
from dashboard.utilities import format_enums


def plot_database_summary(field: str, category: str) -> dcc.Graph:
    """_summary_

    Args:
        field: _description_
        category: _description_
    """
    df = db_data.count_words_per_category(field, category)

    categories = [format_enums(s) for s in df.get_column(category).to_list()]
    customdata = np.stack((df.get_column(field), categories), axis=-1)
    hovertemplate = "%{customdata[1]}<br>%{customdata[0]}<extra></extra>"

    data = go.Bar(
        y=categories,
        x=df.get_column(field).to_list(),
        marker={"color": SummaryColours.BAR},
        orientation="h",
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

    layout = dict(
        **general_chart_layout,
        **horizontal_bar_layout,
    )

    fig = go.Figure(data=data, layout=layout)

    return dcc.Graph(figure=fig)


@callback(
    Output(ids.PART_OF_SPEECH_BAR_CHART, "children"),
    Input(ids.ID_GROUP_SELECTOR, "value"),
)
def plot_database_part_of_speech_summary(field: str) -> dcc.Graph:
    return plot_database_summary(field, "PartOfSpeech")


@callback(
    Output(ids.WORD_CATEGORY_BAR_CHART, "children"),
    Input(ids.ID_GROUP_SELECTOR, "value"),
)
def plot_database_word_category_summary(field: str) -> dcc.Graph:
    return plot_database_summary(field, "WordCategory")


@callback(
    Output(ids.GRAMMAR_CATEGORY_BAR_CHART, "children"),
    Input(ids.ID_GROUP_SELECTOR, "value"),
)
def plot_database_grammar_category_summary(field: str) -> dcc.Graph:
    return plot_database_summary(field, "GrammarCategory")
