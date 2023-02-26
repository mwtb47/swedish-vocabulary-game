"""Module docstring"""

from dash import dcc
import plotly.graph_objects as go


def plot_gauge(
    score: int | float,
    upper_limit: int,
    is_percentage: bool = False,
    value_format: str = ".0f",
    threshold: int = None,
) -> dcc.Graph:
    """_summary_

    Args:
        score: _description_
        upper_limit: _description_
        is_percentage:
        threshold:

    Returns:
        _description_
    """

    gauge = {
        "axis": {
            "range": [0, upper_limit],
        },
        "bar": {"color": "steelblue", "thickness": 0.8},
        "bordercolor": "rgb(220,220,220)",
        "borderwidth": 3,
        "shape": "bullet",
    }

    if is_percentage:
        gauge["axis"]["tickformat"] = ".0%"

    if threshold:
        gauge["threshold"] = {
            "line": {"color": "red", "width": 4},
            "thickness": 0.75,
            "value": threshold,
        }

    data = go.Indicator(
        domain={"x": [0, 1], "y": [0, 1]},
        value=score,
        mode="gauge+number",
        gauge=gauge,
        number={"valueformat": value_format},
    )

    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "rgb(220,220,220)"},
        margin={"l": 30, "r": 30, "t": 30, "b": 30},
        height=100,
    )

    fig = go.Figure(data=data, layout=layout)

    return dcc.Graph(id="indicator", figure=fig)
