"""Module docstring."""

# TODO Answers over time callback causes page to jump to top
# TODO Alignment of containers in first two rows is off

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from dashboard.app import db_data
from dashboard.components import ids
from dashboard.components.charts import (
    plot_answers_summary,
    plot_gauge,
)


dash.register_page(__name__, path="/", name="Answers Summary", title="Answers")

layout = html.Div(
    children=[
        html.H1(
            children="Summary of Answers",
            style={"margin-bottom": "15px"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6("Total Answers", className="text-center"),
                        html.Div(db_data.answer_count, className="divCard"),
                    ],
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    [
                        html.H6("Weekly Answers Target", className="text-center"),
                        plot_gauge(db_data.answer_count_this_week, 560),
                    ],
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    [
                        html.H6("Daily Answers Target", className="text-center"),
                        plot_gauge(db_data.answer_count_today, 80),
                    ],
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    [
                        html.H6("Daily Target Success", className="text-center"),
                        html.Div(
                            db_data.percent_daily_target_achieved, className="divCard"
                        ),
                    ],
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    [
                        html.H6("Weekly Target Success", className="text-center"),
                        html.Div(
                            db_data.percent_weekly_target_achieved, className="divCard"
                        ),
                    ],
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "% English to Swedish Answers", className="text-center"
                        ),
                        plot_gauge(
                            score=db_data.english_to_swedish_percentage,
                            upper_limit=1,
                            is_percentage=True,
                            value_format=".1%",
                            threshold=0.5,
                        ),
                    ],
                    className="divRoundedBorder",
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6(
                            "Ratio of Total Answers to Words in Database per Part of Speech",
                            className="text-center",
                        ),
                        plot_answers_summary("PartOfSpeech"),
                    ],
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "Ratio of Total Answers to Words in Database per Grammar Category",
                            className="text-center",
                        ),
                        plot_answers_summary("GrammarCategory"),
                    ],
                    className="divRoundedBorder",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "Ratio of Total Answers to Words in Database per Word Category",
                            className="text-center",
                        ),
                        plot_answers_summary("WordCategory"),
                    ],
                    className="divRoundedBorder",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Row(
                    dcc.RadioItems(
                        id=ids.ANSWERS_OVER_TIME_INPUT,
                        options=["Day", "Week", "Month"],
                        value="Week",
                    ),
                ),
                dbc.Row(html.Div(id=ids.ANSWERS_OVER_TIME)),
            ],
            className="divRoundedBorder",
        ),
    ]
)
