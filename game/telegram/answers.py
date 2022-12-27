"""Module with functions to fetch answers data from database.

Functions:
    unix_to_datetime: Convert unix timestamp to a date.
    count_answers: Count the number of answers during the current day
        and week.
"""

from datetime import datetime

import pandas as pd

import database as db


def unix_to_date(timestamps: pd.Series) -> list:
    """Convert unix timestamps to datetime date objects.

    Args:
        timestamps: Pandas series containing unix timestamps.

    Returns:
        Pandas series with datetime date objects.
    """
    return pd.to_datetime(timestamps, unit="s").apply(lambda x: x.date())


def count_answers() -> tuple[int, int]:
    """Count the number of answers on current day and current week.

    Returns:
        Tuple with the number of answers on current day and number of
        answers during current week.
    """
    df = db.to_pandas("SELECT * FROM Marks")
    today = datetime.now().date()
    df["date"] = unix_to_date(df["Timestamp"])
    df["week"] = [date.isocalendar().week for date in df.date]
    day_count = len(df[df.date >= today])
    week_count = len(df[df.week == today.isocalendar().week])
    return day_count, week_count
