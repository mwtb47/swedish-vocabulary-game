

class ChartLayout:

    GENERAL = {
        "font": {
            "color": "rgb(240, 240, 240)",
        },
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
    }
    """Layout specifications used on all charts.
    
    This specifies the font as well as making the plot and paper
    backgrounds transparent.
    """

    HORIZONTAL_BAR = {
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
        "margin": {
            "t": 20,
            "b": 30,
            "r": 30,
        },
    }
    """Layout specifications for horizontal bar charts."""

    LINE = {
        "xaxis": {
            "gridcolor": "rgba(0, 0, 0, 0)",
        },
        "yaxis": {
            "gridcolor": "rgb(50, 50, 50)",
            "gridwidth": 1,
            "linecolor": "rgb(200, 200, 200)",
            "linewidth": 3,
            "rangemode": "tozero",
        },
    }
    """Layout specifications for line charts."""


class PerformanceColours:
    """Class with colours for performance chart."""

    GREEN = "rgba(20, 125, 0, 0.8)"
    YELLOW = "rgba(255, 191, 0, 0.8)"
    RED = "rgba(220, 40, 40, 0.8)"


class SummaryColours:
    """Class with colours for summary bar chart."""

    BAR = "rgba(50, 160, 200, 0.8)"
    LINE = "rgba(50, 160, 200, 0.8)"
    AVERAGE_LINE = "rgb(200, 50, 80)"
