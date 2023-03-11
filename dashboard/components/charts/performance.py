"""Module with functions to plot charts on the performance summary page."""

from dash import dcc, html
import plotly.graph_objects as go
import polars as pl
import numpy as np

from dashboard.app import db_data
from dashboard.components import PerformanceIds
from dashboard.components.charts import horizontal_bar
from dashboard.components.charts.layout import ChartLayout, PerformanceColours
from dashboard.utilities import format_enums


def add_colours(df: pl.DataFrame) -> pl.DataFrame:
    """Add BarColour column to DataFrame.

    Attributes with a mean score >= 0.8 are assigned green, >= 0.7
    yellow, and <0.7 red.

    Args:
        df: DataFrame to add colour column to.

    Returns:
        DataFrame with added BarColour column.
    """
    return df.with_column(
        pl.when(pl.col("Mean") >= 0.8)
        .then(PerformanceColours.GREEN)
        .when(pl.col("Mean") >= 0.7)
        .then(PerformanceColours.YELLOW)
        .otherwise(PerformanceColours.RED)
        .alias("BarColour")
    )


def plot_marks_summary(category: str, height: int = 450) -> html.Div:
    """Plot horizontal bar chart with mean marks per category attribute.

    Args:
        category: Category to aggregate marks by. This can be
            GrammarCategory, PartofSpeech or WordCategory.
        height: Height of the plot in pixels. Defaults to 450.

    Returns:
        html.Div containing a Dash Core Components Graph object with
        the plotted chart.
    """
    df = db_data.calculate_mean_marks_by_category(category)
    df = add_colours(df)

    categories = [format_enums(cat) for cat in df.get_column("Category").to_list()]
    means = df.get_column("Mean")
    customdata = np.stack((categories, means), axis=-1)
    hovertemplate = "%{customdata[0]}<br>%{customdata[1]:.3f}<extra></extra>"

    fig = horizontal_bar.plot(
        x=means,
        y=categories,
        customdata=customdata,
        hovertemplate=hovertemplate,
        marker_colour=df.get_column("BarColour"),
        height=height,
    )

    return html.Div(dcc.Graph(figure=fig), id=f"marks-summary-{category}")


def plot_cumulative_average() -> html.Div:
    """Plot line chart showing cumulative average mean score.

    The line chart shows the cumulative average mean score over time for
    each word category, including an All category which includes all
    words.

    Returns:
        html.Div containing a Dash Core Components Graph object with
        the plotted chart.
    """
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
        **ChartLayout.GENERAL,
        **ChartLayout.LINE,
        margin={"t": 30},
    )

    fig = go.Figure(data=data, layout=layout)

    return html.Div(dcc.Graph(figure=fig), id=PerformanceIds.CUMULATIVE_AVERAGE)
