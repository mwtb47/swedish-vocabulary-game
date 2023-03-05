"""Module docstring."""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

from dashboard.app import db_data
from dashboard.components import AnswerIds
from dashboard.components.charts import (
    plot_answers_summary,
    plot_gauge,
)


dash.register_page(__name__, path="/", name="Answers Summary", title="Answers")


@callback(
    Output(AnswerIds.ANSWERS_OVER_TIME_TITLE, "children"),
    Input(AnswerIds.TIME_PERIOD_INPUT, "value"),
)
def update_chart_title(period: str):
    """Update chart title text based on time period input.

    Args:
        period: Either Day, Week, or Month. The value is taken from the
            'time-period-input' selector.

    Returns:
        html.H6 component with updated title text.
    """
    return html.H6(f"Answers Count per {period}")


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
                        html.Div(db_data.answer_count, className="card"),
                    ],
                    className="rounded-border six-per-row",
                ),
                dbc.Col(
                    [
                        html.H6("Weekly Answers Target", className="text-center"),
                        html.Div(
                            plot_gauge(db_data.answer_count_this_week, 560),
                            id=AnswerIds.ANSWER_COUNT_WEEKLY,
                        ),
                    ],
                    className="rounded-border six-per-row",
                ),
                dbc.Col(
                    [
                        html.H6("Daily Answers Target", className="text-center"),
                        html.Div(
                            plot_gauge(db_data.answer_count_today, 80),
                            AnswerIds.ANSWER_COUNT_TODAY,
                        ),
                    ],
                    className="rounded-border six-per-row",
                ),
                dbc.Col(
                    [
                        html.H6("Daily Target Success", className="text-center"),
                        html.Div(
                            db_data.percent_daily_target_achieved,
                            className="card",
                        ),
                    ],
                    className="rounded-border six-per-row",
                ),
                dbc.Col(
                    [
                        html.H6("Weekly Target Success", className="text-center"),
                        html.Div(
                            db_data.percent_weekly_target_achieved,
                            className="card",
                        ),
                    ],
                    className="rounded-border six-per-row",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "% English to Swedish Answers", className="text-center"
                        ),
                        html.Div(
                            plot_gauge(
                                score=db_data.swedish_answer_percentage,
                                axis_limit=1,
                                value_format=".1%",
                                threshold=0.5,
                            ),
                            AnswerIds.ENGLISH_TO_SWEDISH,
                        ),
                    ],
                    className="rounded-border six-per-row",
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
                    className="rounded-border three-per-row",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "Ratio of Total Answers to Words in Database per Grammar Category",
                            className="text-center",
                        ),
                        plot_answers_summary("GrammarCategory"),
                    ],
                    className="rounded-border three-per-row",
                ),
                dbc.Col(
                    [
                        html.H6(
                            "Ratio of Total Answers to Words in Database per Word Category",
                            className="text-center",
                        ),
                        plot_answers_summary("WordCategory"),
                    ],
                    className="rounded-border three-per-row",
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Row(
                        dcc.RadioItems(
                            id=AnswerIds.TIME_PERIOD_INPUT,
                            options=["Day", "Week", "Month"],
                            value="Week",
                            inputStyle={"margin-right": "2px"},
                            labelStyle={"margin-right": "10px"},
                        ),
                    ),
                    dbc.Row(
                        id=AnswerIds.ANSWERS_OVER_TIME_TITLE,
                        className="text-center",
                    ),
                    dbc.Row(html.Div(id=AnswerIds.ANSWERS_OVER_TIME)),
                ],
                className="rounded-border one-per-row",
            )
        ),
    ]
)
