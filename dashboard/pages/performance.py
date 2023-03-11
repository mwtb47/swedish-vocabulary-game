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
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6("Overall % Correct", className="container-title"),
                        html.Div(db_data.percent_correct, className="card"),
                    ],
                    className="rounded-border",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "Mean Score per Translation Direction",
                            className="container-title",
                        ),
                        plot_marks_summary("TranslationDirection", height=120),
                    ],
                    className="rounded-border",
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6(
                            "Mean Score per Part of Speech",
                            className="container-title",
                        ),
                        plot_marks_summary("PartOfSpeech"),
                    ],
                    className="rounded-border",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "Mean Score per Grammar Category",
                            className="container-title",
                        ),
                        plot_marks_summary("GrammarCategory"),
                    ],
                    className="rounded-border",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "Mean Score per Word Category",
                            className="container-title",
                        ),
                        plot_marks_summary("WordCategory"),
                    ],
                    className="rounded-border",
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H6(
                        "Cumulative Mean Score",
                        className="container-title",
                    ),
                    plot_cumulative_average(),
                ],
                className="rounded-border",
            ),
        ),
    ],
)
