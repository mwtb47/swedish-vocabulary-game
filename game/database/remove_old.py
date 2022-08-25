"""Script with functions to clear out old marks from database.

Functions:
    fetch_table: Fetch a table from the database.
    fetch_words_and_marks: Fetch words and marks tables from the database.
    remove_old_marks: Remove old marks from the table.
    print_summary: Print a summary of what has been removed.
    commit: Commit the new table to the database and close connection.
    main: Function to run the script.
"""

import pandas as pd

from game import connect, disconnect


connection = connect()


def fetch_table(table_name: str) -> pd.DataFrame:
    """Fetch all columns from table.

    Args:
        table_name: The name of the table to fetch.

    Returns:
        DataFrame containing all columns from the table.
    """
    return pd.read_sql_query(f"SELECT * FROM {table_name}", connection)


def fetch_words_and_marks() -> tuple[pd.DataFrame]:
    """Fetch word and marks tables.

    Returns:
        Tuple of DataFrames. The first DataFrame is the words
        table, the second is the marks table.
    """
    words = fetch_table("ord")
    marks = fetch_table("betyg")
    return words, marks


def remove_old_marks() -> pd.DataFrame:
    """Remove old marks from marks table.

    Remove all marks for word ids which are no longer present
    in the words table.
    """
    words, marks = fetch_words_and_marks()
    merged = words.merge(
        marks,
        left_on="id",
        right_on="ord_id",
        how="outer",
        indicator=True,
    )
    old_words = list(merged[merged["_merge"] == "right_only"].ord_id)
    print_summary(old_words)

    return marks.drop(marks[marks.ord_id.isin(old_words)].index)


def print_summary(old_words: list[int]) -> None:
    """Print a summary of the number of words removed.

    Args:
        old_words: A list of word ids.
    """
    removed_marks = len(old_words)
    removed_words = len(set(old_words))
    if removed_words > 0:
        print(f"Removed {removed_marks} marks from {removed_words} unique words.")
    else:
        print("No old marks found.")


def commit(new_marks: pd.DataFrame) -> None:
    """Replace the marks table with the updated one.

    Update the table, commit the changes to the database and
    then close the connections.

    Args:
        new_marks: Dataframe to replace the marks table.
    """
    new_marks.to_sql("betyg", connection, if_exists="replace", index=False)
    disconnect(connection, commit=True)


def main() -> None:
    """Main function to run script."""
    new_marks = remove_old_marks()
    commit(new_marks)


if __name__ == "__main__":
    main()
