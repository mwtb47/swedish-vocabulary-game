"""Module docstring"""

from dash import dcc
import plotly.graph_objects as go


def plot_gauge(
    score: int | float,
    axis_limit: int,
    value_format: str = ".0f",
    threshold: int = None,
    """_summary_
) -> dcc.Graph:

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
            "range": [0, axis_limit],
        },
        "bar": {"color": "steelblue", "thickness": 0.8},
        "bordercolor": "rgb(220,220,220)",
        "borderwidth": 3,
        "shape": "bullet",
    }

    if "%" in value_format:
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

    return dcc.Graph(figure=fig)
