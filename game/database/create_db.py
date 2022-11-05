"""Script to create the vocabulary game database structure.

Arguments:
    db_name: Name of the database file, including .db extension.
    lang1: The name of the field for the first language.
    lang2: The name of the field for the second language.

The database, as described in `README.md`, can be created by running:
    
    python3 create_db.py "vocabulary.db" "English" "Swedish"

Functions:
    exists: Check if the provided file name already exists.
    create_db: Create the database structure for the vocabulary game.
"""

import argparse
import os
import sqlite3


statement = """
CREATE TABLE GrammarCategories (
    GrammarCategoryID INTEGER PRIMARY KEY NOT NULL,
    GrammarCategory   TEXT    NOT NULL
);

CREATE TABLE Hints (
    WordGroup INTEGER PRIMARY KEY NOT NULL,
    Hint      TEXT    NOT NULL
);

CREATE TABLE Links (
    WordGroup      INTEGER PRIMARY KEY NOT NULL,
    WiktionaryLink TEXT    NOT NULL
);

CREATE TABLE Marks (
    AnswerID               INTEGER PRIMARY KEY AUTOINCREMENT,
    WordID                 INTEGER NOT NULL,
    Mark                   INTEGER NOT NULL,
    TranslationDirectionID INTEGER NOT NULL,
    Timestamp              REAL    NOT NULL,

    FOREIGN KEY (WordID)
        REFERENCES Words (WordID),
    FOREIGN KEY (TranslationDirectionID)
        REFERENCES TranslationDirections (TranslationDirectionID)
);

CREATE TABLE TranslationDirections (
    TranslationDirectionID INTEGER PRIMARY KEY NOT NULL,
    TranslationDirection   TEXT    NOT NULL
);

CREATE TABLE WordCategories (
    WordCategoryID INTEGER PRIMARY KEY NOT NULL,
    WordCategory   TEXT    NOT NULL
);

CREATE TABLE Words (
    WordID            INTEGER PRIMARY KEY AUTOINCREMENT,
    {language1}       TEXT    NOT NULL,
    {language2}       TEXT    NOT NULL,
    WordCategoryID    INTEGER NOT NULL,
    PartOfSpeechID    INTEGER NOT NULL,
    WordGroup         INTEGER NOT NULL,
    GrammarCategoryID INTEGER NOT NULL,

    FOREIGN KEY (WordCategoryID)
        REFERENCES WordCategories (WordCategoryID),
    FOREIGN KEY (PartOfSpeechID)
        REFERENCES PartsOfSpeech (PartsOfSpeechID),
    FOREIGN KEY (GrammarCategoryID)
        REFERENCES GrammarCategories (GrammarCategoryID)
);
"""


def exists(db_name: str) -> bool:
    """Check if a file with the provided name already exists.

    Args:
        dn_name: Name of the .db file.

    Returns:
        Returns true if the file already exists, false otherwise.
    """
    if os.path.exists(db_name):
        return True
    return False


def create_db(db_name: str, language1: str, language2: str) -> None:
    """Create the database structure and save to a .db file.

    Args:
        db_name: Name of the .db file.
        language1: Name of the field for the first language.
        language2: Name of the field for the second language.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.executescript(statement.format(language1=language1, language2=language2))
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "db_name", type=str, help="Name of .db file, including extension."
    )
    parser.add_argument("language1", type=str, help="Name of first language field.")
    parser.add_argument("language2", type=str, help="Name of second language field.")
    args = parser.parse_args()

    if not exists(args.db_name):
        create_db(args.db_name, args.language1, args.language2)
    else:
        print(".db file with this name already exists.")
