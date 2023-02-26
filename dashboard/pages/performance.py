import dash
from dash import html
import dash_bootstrap_components as dbc

from dashboard.app import db_data
from dashboard.components.charts import (
    plot_marks_summary,
    plot_cumulative_average,
)


dash.register_page(__name__, name="Performance Summary")

layout = html.Div(
    children=[
        html.H1(children="Performance Summary"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Overall % Correct", className="text-center"),
                        html.Div(db_data.percent_correct, className="divCard"),
                    ],
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    html.Div(
                        plot_marks_summary("TranslationDirection"),
                    ),
                    className="divRoundedBorder",
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        plot_marks_summary("PartOfSpeech"),
                    ),
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    html.Div(
                        plot_marks_summary("GrammarCategory"),
                    ),
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    html.Div(
                        plot_marks_summary("WordCategory"),
                    ),
                    className="divRoundedBorder",
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    plot_cumulative_average(),
                ),
                className="divRoundedBorder",
            ),
        ),
    ],
)
