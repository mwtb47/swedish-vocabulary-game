"""Docstring. This is a horrible bit of code, but it does the job."""

import pandas as pd

from game import database


def fetch_table(table: str) -> pd.DataFrame:
    """Fetch a table from the Vocabulary database.

    Args:
        table: The name of the sql table.

    Returns:
        A dataframe version of the sql table.
    """
    connection = database.connect()
    df = pd.read_sql_query(f"SELECT * FROM {table}", connection)
    database.disconnect(connection, commit=True)
    return df


def add_spacing(row_id: int, length: int) -> str:
    """Add spacing to row to align columns.

    Regardless of the number of digits each row's id, the last digit
    of each row's id should always be vertically aligned. To achieve
    this, spacing needs to be added depending on how many digits the
    id has relative to the largest id in the table.

    Args:
        t: The id for the row.
        length: The number of digits in the largest id in the table.

    Returns:
        Row id as a string, with leading spacing if required.
    """
    row_id = str(row_id)
    if (row_id_len := len(row_id)) > length:
        raise ValueError("Length longer than max value.")
    return row_id if row_id_len == length else " " * (length - row_id_len) + row_id


def table_to_string(df: pd.DataFrame, table_name: str) -> str:
    """Create string representation of dataframe.

    Args:
        df: The dataframe to convert to text table.
        table_name: Title of the table.

    Returns:
        String representation of dataframe.
    """
    longest_index = max(max(len(str(i)) for i in df.iloc[:, 0]), len(df.columns[0]))
    longest_row = max(len(str(i)) for i in df.iloc[:, 1]) + longest_index + 2
    lines = [list(df.columns)] + [["-" * longest_row]]
    lines += [
        [add_spacing(df.iloc[row, 0], longest_index), df.iloc[row, 1]]
        for row in df.index
    ]
    return "\n".join(["  ".join(line) for line in lines])


def main() -> None:
    """Create txt file with word type, word category and grammar tables."""
    strings = []
    for table_name in ["PartsOfSpeech", "WordCategories", "Grammar"]:
        df = fetch_table(table_name)
        strings.append(table_to_string(df, table_name))

    with open("game/new_words/table_summaries.txt", "w", encoding="utf-8") as file:
        file.write("\n\n\n".join(strings))


if __name__ == "__main__":
    main()
