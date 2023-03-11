"""Script with functions to clear out old marks from database.

Entries are sometimes removed from the words table in the database. The
marks for these removed entries, however, remain in the marks table.
This script removes all entries in the marks table for word ids which
are no longer present in the words table.

Functions:
    remove_old_marks: Remove old marks from the table.
    print_summary: Print a summary of what has been removed.
    commit: Commit the new table to the database and close connection.
    main: Function to run the script.
"""

import pandas as pd

import database as db


def remove_old_marks() -> pd.DataFrame:
    """Remove old marks from marks table.

    Remove all marks for word ids which are no longer present in the
    words table.
    """
    words = db.to_pandas("SELECT * FROM Word")
    marks = db.to_pandas("SELECT * FROM Answer")
    merged = words.merge(
        marks,
        on="WordID",
        how="outer",
        indicator=True,
    )
    old_words = list(merged[merged["_merge"] == "right_only"].WordID)
    print_summary(old_words)

    return marks.drop(marks[marks.WordID.isin(old_words)].index)


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

    Update the table, commit the changes to the database and then close
    the connections.

    Args:
        new_marks: DataFrame to replace the marks table.
    """
    connection = db.connect()
    new_marks.to_sql("Answer", connection, if_exists="replace", index=False)
    db.commit_and_close(connection)


def main() -> None:
    """Main function to run script."""
    new_marks = remove_old_marks()
    commit(new_marks)


if __name__ == "__main__":
    main()
