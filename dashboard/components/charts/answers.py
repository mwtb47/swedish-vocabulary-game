"""Module docstring"""

from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

from dashboard.app import db_data
from dashboard.components import ids
from dashboard.components.charts.layout import (
    general_chart_layout,
    horizontal_bar_layout,
    line_chart_layout,
    SummaryColours,
)
from dashboard.utilities import format_enums


def plot_answers_summary(category: str) -> html.Div:
    """Plot answers summary chart.

    Args:
        category: Category to be used for the y-axis.

    Returns:
        Dash Core Components Graph object containing the plotted chart.
    """
    df = db_data.count_answers_per_category(category)

    categories = [format_enums(cat) for cat in df.get_column(category)]
    customdata = np.stack(
        (df.get_column("Answer Count"), df.get_column("Word Count")),
        axis=-1,
    )
    hovertemplate = (
        "Total Words: %{customdata[0]}"
        + "<br>Total Answers: %{customdata[1]}"
        + "<extra></extra>"
    )

    data = go.Bar(
        y=categories,
        x=df.get_column("Ratio").to_list(),
        marker={"color": SummaryColours.BAR},
        orientation="h",
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

    layout = dict(
        **general_chart_layout,
        **horizontal_bar_layout,
        margin={"t": 15, "r": 30, "b": 40},
    )

    fig = go.Figure(data=data, layout=layout)

    return html.Div(
        dcc.Graph(
            figure=fig,
            style={"height": "30vh"},
        ),
        id=f"answers-summary-{category}",
    )


@callback(
    Output(ids.ANSWERS_OVER_TIME, "children"),
    Input(ids.ANSWERS_OVER_TIME_INPUT, "value"),
)
def plot_answers_over_time(period: str) -> html.Div:
    """Plot number of answers over time.

    Args:
        period: Time period to use for the x-axis.

    Returns:
        Dash Core Components Graph object containing the plotted chart.
    """
    rolling_periods = {
        "Day": 30,
        "Week": 4,
        "Month": 3,
    }
    rolling_period = rolling_periods[period]

    df = db_data.calculate_answers_per_time_period(period, rolling_period)

    periods = df.get_column("Period")
    counts = df.get_column("Count")
    rolling_averages = df.get_column("Rolling Average")
    # TODO fix error with np.stack and period='Day'
    # customdata = np.stack((periods, counts, rolling_averages), axis=-1)
    # hovertemplate = (
    #    "Period: %{customdata[0]}<br>"
    #    + "Answers: %{customdata[1]}<br>"
    #    + "Rolling Average: %{customdata[2]}"
    # )

    data = [
        go.Scatter(
            x=periods,
            y=counts,
            marker={"color": SummaryColours.LINE},
            mode="lines",
            name="Answers",
            # customdata=customdata,
            # hovertemplate=hovertemplate,
        ),
        go.Scatter(
            x=periods,
            y=rolling_averages,
            marker={"color": SummaryColours.AVERAGE_LINE},
            mode="lines",
            line={"dash": "dash"},
            name=f"{rolling_period}-{period.capitalize()} Average",
            # customdata=customdata,
            # hovertemplate=hovertemplate,
        ),
    ]

    layout = dict(
        **general_chart_layout,
        **line_chart_layout,
        title_text=f"Answers per {period.capitalize()}",
        margin={"t": 60},
        height=600,
    )

    fig = go.Figure(data=data, layout=layout)

    return html.Div(dcc.Graph(figure=fig), id=ids.ANSWERS_OVER_TIME)
