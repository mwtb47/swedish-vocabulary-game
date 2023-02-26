"""Module docstring"""

from dash import dcc, html
import plotly.graph_objects as go
import polars as pl
import numpy as np

from dashboard.app import db_data
from dashboard.components import ids
from dashboard.components.charts.layout import (
    general_chart_layout,
    horizontal_bar_layout,
    line_chart_layout,
    PerformanceColours,
)
from dashboard.utilities import format_enums, split_title


def add_colours(df: pl.DataFrame) -> pl.DataFrame:
    """_summary_

    Args:
        df: _description_

    Returns:
        _description_
    """
    return df.with_column(
        pl.when(pl.col("Mean") >= 0.8)
        .then(PerformanceColours.GREEN)
        .when(pl.col("Mean") >= 0.7)
        .then(PerformanceColours.YELLOW)
        .otherwise(PerformanceColours.RED)
        .alias("PerformanceIndicator")
    )


def plot_marks_summary(category: str) -> html.Div:
    """_summary_

    Args:
        category: _description_
        height: _description_

    Returns:
        _description_
    """
    df = db_data.calculate_answer_percentage_per_category(category)
    df = add_colours(df)

    categories = [format_enums(cat) for cat in df.get_column(category).to_list()]
    means = df.get_column("Mean")
    customdata = np.stack((means, categories), axis=-1)
    hovertemplate = "%{customdata[0]}<br>%{customdata[1]:.3f}<extra></extra>"

    data = go.Bar(
        y=categories,
        x=means,
        marker={"color": df.get_column("PerformanceIndicator")},
        orientation="h",
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

    layout = dict(
        **general_chart_layout,
        **horizontal_bar_layout,
        title_text=f"Mean Score per {split_title(category)}",
        margin={"t": 60},
    )

    fig = go.Figure(data=data, layout=layout)

    return html.Div(dcc.Graph(figure=fig), id=f"marks-summary-{category}")


def plot_cumulative_average() -> html.Div:
    """"""
    df = db_data.calculate_cumulative_average_score()
    word_categories = df.get_column("WordCategory").unique().sort()

    data = [
        go.Scatter(
            x=df.filter(pl.col("WordCategory") == word_category).get_column("Date"),
            y=df.filter(pl.col("WordCategory") == word_category).get_column(
                "Cumulative Average"
            ),
            mode="lines",
            name=format_enums(word_category),
        )
        for word_category in word_categories
    ]

    layout = dict(
        **general_chart_layout,
        **line_chart_layout,
        title_text="Cumulative Mean Score",
        margin={"t": 60},
    )

    fig = go.Figure(data=data, layout=layout)

    return html.Div(dcc.Graph(figure=fig), id=ids.CUMULATIVE_AVERAGE)
