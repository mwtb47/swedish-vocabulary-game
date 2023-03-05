"""Module docstring"""

from dash import dcc, Input, Output, callback
import numpy as np

from dashboard.app import db_data
from dashboard.components import DatabaseIds
from dashboard.components.charts import horizontal_bar
from dashboard.utilities import format_enums


    """_summary_
def plot_database_summary(group_by: str, count_by: str) -> dcc.Graph:

    Args:
        field: _description_
        category: _description_
    """
    df = db_data.count_words_by_category(group_by, count_by)

    categories = [format_enums(s) for s in df.get_column("Category").to_list()]
    counts = df.get_column("Count").to_list()
    customdata = np.stack((counts, categories), axis=-1)
    hovertemplate = "%{customdata[1]}<br>%{customdata[0]}<extra></extra>"

    fig = horizontal_bar.plot(
        x=counts,
        y=categories,
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

    return dcc.Graph(figure=fig)


@callback(
    Output(DatabaseIds.PART_OF_SPEECH_BAR_CHART, "children"),
    Input(DatabaseIds.ID_GROUP_SELECTOR, "value"),
)
def plot_database_part_of_speech_summary(count_by: str) -> dcc.Graph:
    return plot_database_summary("PartOfSpeech", count_by)


@callback(
    Output(DatabaseIds.WORD_CATEGORY_BAR_CHART, "children"),
    Input(DatabaseIds.ID_GROUP_SELECTOR, "value"),
)
def plot_database_word_category_summary(count_by: str) -> dcc.Graph:
    return plot_database_summary("WordCategory", count_by)


@callback(
    Output(DatabaseIds.GRAMMAR_CATEGORY_BAR_CHART, "children"),
    Input(DatabaseIds.ID_GROUP_SELECTOR, "value"),
)
def plot_database_grammar_category_summary(count_by: str) -> dcc.Graph:
    return plot_database_summary("GrammarCategory", count_by)
