""""""
from enum import Enum


general_chart_layout = {
    "title": {"x": 0.5},
    "font": {"color": "rgb(240, 240, 240)"},
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
}

horizontal_bar_layout = {
    "xaxis": {
        "gridcolor": "rgb(100, 100, 100)",
        "gridwidth": 1,
        "linecolor": "rgb(200, 200, 200)",
        "linewidth": 3,
    },
    "yaxis": {
        "linecolor": "rgb(200, 200, 200)",
        "linewidth": 3,
    },
}

line_chart_layout = {
    "xaxis": {
        "gridcolor": "rgb(50, 50, 50)",
        "gridwidth": 1,
    },
    "yaxis": {
        "rangemode": "tozero",
        "gridcolor": "rgb(50, 50, 50)",
        "gridwidth": 1,
        "linecolor": "rgb(200, 200, 200)",
        "linewidth": 3,
    },
}


class PerformanceColours:
    """Class with colours for performance chart."""

    GREEN = "rgba(20, 125, 0, 0.8)"
    YELLOW = "rgba(255, 191, 0, 0.8)"
    RED = "rgba(220, 40, 40, 0.8)"


class SummaryColours:
    """Class with colours for summary bar chart."""

    BAR = "rgba(50, 160, 200, 0.8)"
    LINE = "rgb(50, 130, 180)"
    AVERAGE_LINE = "rgb(200, 50, 80)"
