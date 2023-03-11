"""Module with a function to plot a horizontal bar chart."""

import plotly.graph_objects as go
import polars as pl
import numpy as np

from dashboard.components.charts.layout import ChartLayout, SummaryColours


def plot(
    x: list,
    y: list,
    customdata: np.ndarray,
    hovertemplate: str,
    marker_colour: pl.Series | str = SummaryColours.BAR,
    height: int = 450,
) -> go.Figure:
    """Plot a horizontal bar chart.

    Args:
        x: Array with x-axis coordinates.
        y: Array with y-axis coordinates.
        customdata: NumPy NDArray with custom hoverlabel data.
        hovertemplate: Template for the custome hoverlabel.
        marker_colour: Either a rgb/rgba/hex string specifying a single
            colour for all bars or a series containing colour values for
            each y value. Defaults to rgba(50, 160, 200, 0.8).
        height: Height of the plot in pixels. Defaults to 450.

    Returns:
        Plotly graph_objects figure containing a horizontal bar chart.
    """

    data = go.Bar(
        y=y,
        x=x,
        marker={"color": marker_colour},
        orientation="h",
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

    layout = dict(
        **ChartLayout.GENERAL,
        **ChartLayout.HORIZONTAL_BAR,
        height=height,
    )

    return go.Figure(data=data, layout=layout)
