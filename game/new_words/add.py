"""Module to add new words to the database.

Classes:
    Counter: Dataclass to count number of entries added.

Functions:
    read_current_words: Read the words table from the database.
    get_next_attribute_id: Get the next available id.
    check_not_duplicated: Check the word pair does not already exist.
    add_word_info: Add word to the word table.
    add_context_hint: Add context hint.
    add_wiktionary_hint: Add wiktionary hint.
    add_hint_and_link: Add context and wiktionary hints.
    add_new_word: Add a word to the database.
    add_words: Call add_new_word for all words.
    close_connection: Commit changes to database and close connection.
    main: Function to run the script.
"""

from dataclasses import dataclass
import sqlite3

import pandas as pd
import numpy as np

from objects import *
from words import words_phrases


@dataclass
class Counter:
    adjectives: int = 0
    adverbs: int = 0
    nouns: int = 0
    verbs: int = 0
    words: int = 0

    def tick(self, word: Adjective | Adverb | Generic | Noun | Verb):
        """Increase count of word object type.

        Args:
            word: The word object.
        """
        match word:
            case Adjective():
                self.adjectives += 1
            case Adverb():
                self.adverbs += 1
            case Generic():
                self.words += 1
            case Noun():
                self.nouns += 1
            case Verb():
                self.verbs += 1

    def print_summary(self):
        """Print summary of word types added."""
        print(
            (
                "Number of entries added:\n"
                f"Adjectives - {self.adjectives}\n"
                f"Adverbs - {self.adverbs}\n"
                f"Nouns - {self.nouns}\n"
                f"Verbs - {self.verbs}\n"
                f"Generic - {self.words}"
            )
        )


connection = sqlite3.connect("game/database/vocabulary.db")
cursor = connection.cursor()

# sqlite does not accept integers of more than 8 bytes therefore
# the np.int64 returned by get_next_attribute_id has to be cast
# to an int.
sqlite3.register_adapter(np.int64, int)

counter = Counter()


def read_current_words() -> pd.DataFrame:
    """Fetch all columns from the ord table.

    Returns:
        DataFrame containing words table from database.
    """
    return pd.read_sql_query("""SELECT * FROM ord""", connection)


def get_next_attribute_id(attribute: str) -> int:
    """Get an unused attribute id. This is the max current id + 1.

    Args:
        attribute: The name of the column to find the next id for.

    Returns:
        Integer to be used as next id.
    """
    df = pd.read_sql_query(f"""SELECT {attribute} FROM ord""", connection)
    return df[attribute].max() + 1


def check_not_duplicated(word_pair: WordPair) -> bool:
    """Check for duplicate entry of the English - Swedish pair.

    Args:
        word_pair: WordPair object to be added to the database.

    Returns:
        True if the word or phrase pair is not already in the
        database, False if it is.
    """
    current_words = read_current_words()
    current_pairs = [(row.engelska, row.svenska) for row in current_words.itertuples()]
    if (word_pair.en, word_pair.sv) not in current_pairs:
        return True
    print(f"Word pair already in database. {word_pair.en} - {word_pair.sv}")
    return False


def add_word_info(
    id_: int, word_type: int, word_category: int, ordgrupp: int, word_pair: WordPair
) -> None:
    """Add word information to the word table.

    Args:
        id_: The word id for the word pair.
        word_type: The word type of the word pair.
        word_category: The word category of the word pair.
        ordgrupp: The word group id of the word pair.
        word_pair: The WordPair object.
    """
    query = """
        INSERT INTO ord (
            id,
            engelska,
            svenska,
            ordtyp_id,
            ordkategori_id,
            ordgrupp,
            grammar_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    values = (
        id_,
        word_pair.en,
        word_pair.sv,
        word_type,
        word_category,
        ordgrupp,
        word_pair.grammar_id,
    )
    cursor.execute(query, values)


def add_context_hint(ordgrupp: int, context_hint: str) -> None:
    """Add hints to tips table.

    Args:
        ordgrupp: The word group id of the word pair.
        context_hint: The context hint of the word pair.
    """
    query = """
        INSERT INTO tips (
            ordgrupp,
            sammanhang_tips
        )
        VALUES (?, ?)
    """
    values = (ordgrupp, context_hint)
    cursor.execute(query, values)


def add_wiktionary_link(ordgrupp: int, wiktionary_link: str) -> None:
    """Add Wiktionary link to wiktionary table.

    Args:
        ordgrupp: The word group id of the word pair.
        wiktionary_link: Wiktionary link for word pair.
    """
    query = """
        INSERT INTO wiktionary (
            ordgrupp,
            länk
        )
        VALUES (?, ?)
    """
    values = (ordgrupp, wiktionary_link)
    cursor.execute(query, values)


def add_hint_and_link(
    word_object: Adjective | Adverb | Generic | Noun | Verb, ordgrupp: int
) -> None:
    """Add context hint and Wiktionary link to database.

    Args:
        ordgrupp: Word group id.
    """
    if word_object.context_hint:
        add_context_hint(ordgrupp, word_object.context_hint)
    if word_object.wiktionary_link:
        add_wiktionary_link(ordgrupp, word_object.wiktionary_link)


def add_new_word(word_object: Adjective | Adverb | Generic | Noun | Verb) -> None:
    """Add new word pairs to the database.

    For each word pair in the word group, check if the pair is already
    in the database. If is not, add the word pair. If any of the word
    pairs for a word group are already in the database, the context
    hint and Wiktionary link for that word group is not added.

    Args:
        word_object: The word object to add.
    """
    found_duplicate = False
    ordgrupp = get_next_attribute_id("ordgrupp")
    for word_pair in word_object.word_list:
        if check_not_duplicated(word_pair):
            id_ = get_next_attribute_id("id")
            add_word_info(
                id_,
                word_object.word_type,
                word_object.word_category,
                ordgrupp,
                word_pair,
            )
            counter.tick(word_object)
        else:
            found_duplicate = True

    if not found_duplicate:
        add_hint_and_link(word_object, ordgrupp)


def add_words(words_phrases: list[Adjective | Adverb | Generic | Noun | Verb]) -> None:
    """Add words.

    Args:
        words_phrases: A list of words and phrases to add.
    """
    for word_phrase in words_phrases:
        add_new_word(word_phrase)


def close_connection(connection: sqlite3.Connection) -> None:
    """Commit and close connection to Vocabulary database.

    Args:
        connection: The sqlite3 Connection to close.
    """
    connection.commit()
    connection.close()


def main() -> None:
    """Main function to run script."""
    add_words(words_phrases)
    close_connection(connection)
    counter.print_summary()


if __name__ == "__main__":
    main()
