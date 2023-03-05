"""Module docstring"""

from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

from dashboard.app import db_data
from dashboard.components import AnswerIds
from dashboard.components.charts import horizontal_bar
from dashboard.components.charts.layout import ChartLayout, SummaryColours
from dashboard.utilities import format_enums


def plot_answers_summary(category: str) -> html.Div:
    """Plot answers summary chart.

    Args:
        category: Category to be used for the y-axis.

    Returns:
        Dash Core Components Graph object containing the plotted chart.
    """
    df = db_data.count_answers_by_category(category)

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

    fig = horizontal_bar.plot(
        x=df.get_column("Ratio").to_list(),
        y=categories,
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

    return html.Div(
        dcc.Graph(figure=fig, style={"height": "30vh"}),
        id=f"answers-summary-{category}",
    )


@callback(
    Output(AnswerIds.ANSWERS_OVER_TIME, "children"),
    Input(AnswerIds.TIME_PERIOD_INPUT, "value"),
)
def plot_answers_over_time(period: str) -> dcc.Graph:
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

    df = db_data.count_answers_by_time_period(period, rolling_period)

    periods = df.get_column("Period")
    counts = df.get_column("Count")
    rolling_averages = df.get_column("Rolling Average")
    customdata = np.stack(
        (periods.cast(str), counts.cast(str), rolling_averages.round(2).cast(str)),
        axis=-1,
    )
    hovertemplate = (
        "Period: %{customdata[0]}<br>"
        + "Answers: %{customdata[1]}<br>"
        + "Rolling Average: %{customdata[2]}"
    )

    data = [
        go.Scatter(
            x=periods,
            y=counts,
            marker={"color": SummaryColours.LINE},
            mode="lines",
            name="Answers",
            customdata=customdata,
            hovertemplate=hovertemplate,
        ),
        go.Scatter(
            x=periods,
            y=rolling_averages,
            marker={"color": SummaryColours.AVERAGE_LINE},
            mode="lines",
            line={"dash": "dash"},
            name=f"{rolling_period}-{period.capitalize()} Average",
            customdata=customdata,
            hovertemplate=hovertemplate,
        ),
    ]

    layout = dict(
        **ChartLayout.GENERAL,
        **ChartLayout.LINE,
        margin={"t": 30},
        height=600,
    )

    fig = go.Figure(data=data, layout=layout)

    return dcc.Graph(figure=fig)
