"""Module with functions to fetch data from database.

Functions:
    fetch: Fetch the marks table from the database.
    unix_to_datetime: Convert unix timestamp to a date.
    count_answers: Count the number of answers during the
        current day and week.
"""

from datetime import datetime

import pandas as pd

from game import database


def fetch() -> pd.DataFrame:
    """Fetch data from the marks table in the database.

    Returns:
        DataFrame with marks.
    """
    connection = database.connect()
    df = pd.read_sql_query("SELECT * FROM betyg", connection)
    database.disconnect(connection)
    return df


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
        Tuple with the number of answers on current day and number
        of answers during current week.
    """
    df = fetch()
    today = datetime.now().date()
    df["date"] = unix_to_date(df["tidsstämpel"])
    df["week"] = [date.isocalendar().week for date in df.date]
    day_count = len(df[df.date >= today])
    week_count = len(df[df.week == today.isocalendar().week])
    return day_count, week_count
