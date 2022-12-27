"""Module with functions to interact with database.

Functions:
    connect: Return sqlite3 connection to database.
    connect_with_cursor: Return sqlite3 connection to database and a
        cursor.
    commit_and_close: Commit changes to database and close connection.
"""

import sqlite3


# Connection uri used by Polars to connect to database file.
connection_uri = "sqlite://./database/vocabulary.db"


def connect() -> sqlite3.Connection:
    """Return sqlite3 connection to database.

    Returns:
        sqlite3 connection to database.
    """
    return sqlite3.connect("database/vocabulary.db")


def connect_with_cursor() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Return sqlite3 connection to database with a cursor.

    Returns:
        Tuple with sqlite3 connection to database and cursor.
    """
    connection = sqlite3.connect("database/vocabulary.db")
    cursor = connection.cursor()
    return connection, cursor


def commit_and_close(connection: sqlite3.Connection) -> None:
    """Commit changes to database and close connection.

    Args:
        connection: Connection object to commit and close.
    """
    connection.commit()
    connection.close()
