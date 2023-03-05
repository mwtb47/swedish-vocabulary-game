"""Module with a class and functions to get database data.

Classes:
    Database:
    
Functions:
    add_missing_dates: Add missing dates to DataFrame.
    add_period_columns:
    join_answers_and_words:
    aggregate_marks: Calculate number of marks per day.
    start_of_today: Return datatime object for today.
"""

from datetime import datetime, timedelta

import polars as pl

import database as db
from dashboard.utilities import format_percentage


def start_of_today() -> datetime:
    """Return datetime object for today.

    The time is set to midnight, i.e. the start of the day.

    Returns:
        Datetime object representing midnight on the current date.
    """
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)


def add_missing_dates(df: pl.DataFrame) -> pl.DataFrame:
    """Add all dates which are missing from the DataFrame's date range.

    Any date in the range of the DataFrame's minimum and maximum date
    which is missing is added to the DataFrame. The 'Answer Indicator'
    column for these added dates is populated with 0s to indicate that
    there were no answers given on these dates.

    Args:
        df: DataFrame to add missing dates to.

    Returns:
        DataFrame with missing dates added.

        Columns:
            Date: Datetime
            Daily Answers: Int
    """
    dates = df.get_column("Date")
    low: datetime = dates.min()
    high: datetime = dates.max()
    date_range = pl.DataFrame(
        {"Date": pl.date_range(low, high, timedelta(days=1)).cast(pl.Date)}
    )

    # Use an anti-join to find all dates not present in the database
    # responses and assign them a daily answers count of 0.
    missing_dates = date_range.join(df, on="Date", how="anti").with_column(
        pl.lit(0).cast(pl.UInt32).alias("Daily Answers")
    )
    return pl.concat([df, missing_dates])


def add_period_columns(df: pl.DataFrame, period: str) -> pl.DataFrame:
    """Add a period and period sort column to the DataFrame.

    The period column gives the date for each entry in the specified
    period format. E.g. if the date value is '2022-12-01' and the period
    is Month, the Period value will be "Dec '22".

    The Period Sort column assigned an integer value to each period
    which allows them to be sorted in chronological order. This is
    needed as week and month periods are strings and therefore do not
    sort chronologically.

    Note: ISO weeks and years are used.

    Args:
        df: DataFrame to add Period and Period Sort columns to.
        period: Period format to use. Day, Week or Month.

    Returns:
        DataFrame with Period and Period Sort columns added.

        Columns:
            Date: Datetime
            Daily Answers: Int
            Period: Datetime | String
            Period Sort: Int
    """
    # fmt: off
    if period == "Day":
        return (
            df.with_column(pl.col("Date").alias("Period"))
            .with_column(pl.col("Date").alias("Period Sort"))
        )

    if period == "Week":
        return (
            df.with_column(pl.col("Date").dt.strftime("w%V '%G").alias("Period"))
            .with_column(
                (pl.col("Date").dt.iso_year() * 100 + pl.col("Date").dt.week())
                .alias("Period Sort")
            )
        )

    if period == "Month":
        return (
            df.with_column(pl.col("Date").dt.strftime("%b '%y").alias("Period"))
            .with_column(
                (pl.col("Date").dt.year() * 100 + pl.col("Date").dt.month())
                .alias("Period Sort")
            )
        )
    # fmt: on

    raise ValueError(f"Unsupported time period: {period}.")


def aggregate_marks(marks: pl.DataFrame) -> pl.DataFrame:
    """Aggregate the responses, counting the number of marks per day.

    Convert the Unix timestamp into a date object and then count the
    number of responses per day. Add all dates missing from the response
    date range, assigning them response counts of 0.

    Args:
        marks: DataFrame with Marks database table.

    Returns:
        A DataFrame with an answer count by day for all days in the
        Marks table date range.
    """
    dates = marks.select(
        (pl.col("Timestamp") * 1000000).cast(pl.Datetime).cast(pl.Date).alias("Date")
    )
    per_day = dates.groupby("Date").agg(pl.col("Date").count().alias("Daily Answers"))
    return add_missing_dates(per_day)


class Data:
    """_summary_"""

    def __init__(self) -> None:
        """_summary_"""
        self.fetch()

    def fetch(self) -> None:
        """Fetch data from the database."""
        self._marks = db.to_polars("SELECT * FROM Answer")
        self._words = db.to_polars(db.views.words_info)
        self._answers = db.to_polars(db.views.answers)
        self._aggregated_marks = aggregate_marks(self._marks)

    @property
    def answer_count(self) -> int:
        """Number of answers given."""
        return self._marks.shape[0]

    @property
    def answer_count_this_week(self) -> int:
        """Number of answers this calendar week."""
        today = datetime.today()
        week_start = (today - timedelta(days=today.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        return self._marks.filter(
            pl.col("Timestamp") >= datetime.timestamp(week_start)
        ).shape[0]

    @property
    def answer_count_today(self) -> int:
        """Number of answers during the current day."""
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        return self._marks.filter(
            pl.col("Timestamp") >= datetime.timestamp(today)
        ).shape[0]

    @property
    def swedish_answer_percentage(self) -> None:
        """Percentage of all answers answered in Swedish."""
        return (
            self._marks.filter(pl.col("TranslationDirectionID") == 1).shape[0]
            / self._marks.shape[0]
        )

    @property
    def percent_correct(self) -> float:
        """Percentage of correct answers."""
        return format_percentage(self._marks.get_column("Mark").mean())

    @property
    def percent_daily_target_achieved(self) -> float:
        """Percentage of days where the daily target was achieved."""
        return format_percentage(
            self._aggregated_marks.with_column(
                pl.when(pl.col("Daily Answers") >= 80)
                .then(1)
                .otherwise(0)
                .alias("Success")
            )
            .get_column("Success")
            .mean()
        )

    @property
    def percent_weekly_target_achieved(self) -> float:
        """Percentage of weeks where the weekly target was achieved."""
        return format_percentage(
            self._aggregated_marks.groupby(pl.col("Date").dt.week())
            .agg(pl.col("Daily Answers").sum().alias("Weekly Answers"))
            .with_column(
                pl.when(pl.col("Weekly Answers") >= 560)
                .then(1)
                .otherwise(0)
                .alias("Success")
            )
            .get_column("Success")
            .mean()
        )

    @property
    def unique_word_count(self) -> int:
        """Number of unique word or phrase pairs."""
        return self._words.shape[0]

    @property
    def unique_word_group_count(self) -> int:
        """Number of unique word groups."""
        return self._words.get_column("WordGroup").unique().len()

    def count_answers_by_category(self, category: str) -> pl.DataFrame:
        """_summary_

        Args:
            category: _description_

        Returns:
            _description_
        """
        word_count = self._words.groupby(category).agg(pl.count().alias("Word Count"))
        answer_count = (
            self._answers.select(pl.col(category))
            .groupby(category)
            .agg(pl.count().alias("Answer Count"))
        )
        return (
            answer_count.join(word_count, on=category)
            .with_column((pl.col("Answer Count") / pl.col("Word Count")).alias("Ratio"))
            .sort("Ratio")
        )

    def calculate_mean_marks_by_category(self, category: str) -> pl.DataFrame:
        """Calculate mean mark per attribute of the specified category.

        Args:
            category: Attribute to group by, either GrammarCategory,
                PartofSpeech or WordCategory

        Returns:
            DataFrame with mean mark per attribute of the specified
            category.

            Columns:
                Category: Attributes of the specified category.
                Mean: Mean mark for all answers per attribute.
        """
        return (
            self._answers.groupby(category)
            .agg(pl.col("Mark").mean().alias("Mean"))
            .sort("Mean")
            .rename({category: "Category"})
        )

    def count_answers_by_time_period(self, period: str, rolling_period) -> pl.DataFrame:
        """Calculate answer count by time period with a rolling average.

        Args:
            period: Time interval to show answer count by. Day, Week or
                Month.
            rolling_period: Number of periods to use in the rolling
                average.

        Returns:
            DataFrame containing answer counts aggregated by the
            specified period and a rolling average.

            Columns:
                Period: Datetime | String
                Period Sort: Int
                Count: Int
                Rolling Average: Float

        """
        df = add_period_columns(self._aggregated_marks, period)

        return (
            df.groupby(["Period", "Period Sort"])
            .agg(pl.col("Daily Answers").sum().alias("Count"))
            .sort("Period Sort")
            .with_column(
                pl.col("Count")
                .rolling_mean(rolling_period, min_periods=3)
                .alias("Rolling Average")
            )
        )

    def calculate_cumulative_average_score(self) -> pl.DataFrame:
        """_summary_

        Returns:
            _description_

            Columns:
                Date: Datetime
                WordCategory: Str
                Average: Float
                Cumulative Average: Float
        """
        all_answers = self._answers.with_column(pl.lit("All").alias("WordCategory"))
        df = pl.concat([all_answers, self._answers])
        return (
            df.with_column(
                (pl.col("Timestamp") * 1000000)
                .cast(pl.Datetime)
                .cast(pl.Date)
                .alias("Date")
            )
            .groupby(["Date", "WordCategory"])
            .agg(pl.col("Mark").mean().alias("Average"))
            .sort("Date")
            .with_column(
                pl.col("Average")
                .cumulative_eval(pl.element().mean())
                .over("WordCategory")
                .alias("Cumulative Average")
            )
        )

    def count_words_by_category(self, group_by: str, count_by: str) -> pl.DataFrame:
        """Count unique WordIDs or WordGroups per category.

        Args:
            group_by: Attribute to group by, either GrammarCategory,
                PartofSpeech or WordCategory
            count_by: Attribute to count by, either WordID or
                WordCategory.

        Returns:
            DataFrame with a count of either WordIDs or WordGroups per
            category.

            Columns:
                Category: String
                Count: Int
        """
        return (
            self._words.groupby(group_by)
            .agg(pl.col(count_by).unique().count().alias("Count"))
            .sort("Count", reverse=False)
            .rename({group_by: "Category"})
        )
