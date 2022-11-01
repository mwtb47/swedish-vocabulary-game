"""Module with methods to interact with database.

Functions:
    connect: Return sqlite3 connection to database.
    connect_with_cursor: Return sqlite3 connection to database and a
        cursor.
    disconnect: Close connection to server with option to commit.
"""

import sqlite3


# Connection uri used by Polars to connect to database file.
connection_uri = "sqlite://./game/database/vocabulary.db"


def connect() -> sqlite3.Connection:
    """Return connection to database.

    Returns:
        Connection to database.
    """
    return sqlite3.connect("game/database/vocabulary.db")


def connect_with_cursor() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Return connection to database with a cursor.

    Returns:
        Tuple with connection to database and cursor.
    """
    connection = sqlite3.connect("game/database/vocabulary.db")
    cursor = connection.cursor()
    return connection, cursor


def disconnect(connection: sqlite3.Connection, commit: bool = False) -> None:
    """Disconnect from the database with option to commit.

    Args:
        connection: Connection object to close.
        commit: Boolean selecting whether to commit. Default is False.
    """
    if commit:
        connection.commit()
    connection.close()
