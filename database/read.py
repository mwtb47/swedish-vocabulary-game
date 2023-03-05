"""Module with functions to read database data.

Functions:
    to_pandas: Read an SQL query into a Pandas DataFrame.
    to_polars: Read an SQL query into a Polars DataFrame.
"""

import pandas as pd
import polars as pl

import database


def to_pandas(query: str) -> pd.DataFrame:
    """Read an SQL query into a Pandas DataFrame.

    Args:
        query: SQL query.

    Returns:
        Result of SQL query as a Pandas DataFrame.
    """
    connection = database.connect()
    df = pd.read_sql_query(sql=query, con=connection)
    connection.close()
    return df


def to_polars(query: str) -> pl.DataFrame:
    """Read an SQL query into a Polars DataFrame.

    Args:
        query: SQL query.

    Returns:
        Result of SQL query as a Polars DataFrame.
    """
    return pl.read_sql(sql=query, connection_uri=database.connection_uri)
