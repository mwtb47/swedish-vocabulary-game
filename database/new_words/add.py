"""Module to add new words to the database.

Using the --checkout flag will run the following command after adding
the words to the database, removing the added words from
database/new_words/words.py:

    git checkout database/new_words/words.py

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

import argparse
from dataclasses import dataclass
import sqlite3
import subprocess

import numpy as np

import database as db
from game.words import (
    PartOfSpeech,
    WordCategory,
    Adjective,
    Adverb,
    Conjunction,
    Generic,
    Noun,
    Verb,
    Word,
    WordPair,
)


@dataclass
class Counter:
    adjectives: int = 0
    adverbs: int = 0
    conjunctions: int = 0
    nouns: int = 0
    verbs: int = 0
    words: int = 0

    def tick(self, word: Word) -> None:
        """Increase count of word object type.

        Args:
            word: The word object.
        """
        match word:
            case Adjective():
                self.adjectives += 1
            case Adverb():
                self.adverbs += 1
            case Conjunction():
                self.conjunctions += 1
            case Generic():
                self.words += 1
            case Noun():
                self.nouns += 1
            case Verb():
                self.verbs += 1

    def print_summary(self) -> None:
        """Print summary of words added."""
        print(
            (
                "Number of entries added:\n"
                f"Adjectives - {self.adjectives}\n"
                f"Adverbs - {self.adverbs}\n"
                f"Conjuctions - {self.conjunctions}\n"
                f"Nouns - {self.nouns}\n"
                f"Verbs - {self.verbs}\n"
                f"Generic - {self.words}"
            )
        )


class NewWords:
    """Class with methods to add new words and phrases to database.

    Args:
        words_phrases: List of words and phrases to add.

    Attributes:
        words_phrases: List of words and phrases to add.
        counter: Instance of Counter to track added words and phrases.
        connection: sqlite3 database connection.
        cursor: Cursor for the database connection.
    """

    def __init__(self, words_phrases: list[Word]) -> None:
        self.words_phrases = words_phrases
        self.counter = Counter()
        self.connection, self.cursor = db.connect_with_cursor()
        self.__set_sqlite3_cast_rule()

    def __set_sqlite3_cast_rule(self) -> None:
        """Set sqlite3 cast rule for NumPy int64 type.

        sqlite does not accept integers of more than 8 bytes therefore
        the np.int64 returned by get_next_attribute_id has to be cast to
        an int.
        """
        sqlite3.register_adapter(np.int64, int)

    def __get_next_attribute_id(self, attribute: str) -> int:
        """Get an unused attribute id. This is the max current id + 1.

        Args:
            attribute: The name of the column to find the next id for.

        Returns:
            Integer to be used as next id.
        """
        df = db.to_pandas(f"""SELECT {attribute} FROM Words""")
        return df[attribute].max() + 1

    def __check_not_duplicated(self, word_pair: WordPair) -> bool:
        """Check for duplicate entry of the English - Swedish pair.

        Args:
            word_pair: WordPair object to be added to the database.

        Returns:
            True if the word or phrase pair is not already in the
            database, False if it is.
        """
        current_words = db.to_pandas("SELECT * FROM Words")
        current_pairs = [
            (row.English, row.Swedish, row.GrammarCategoryID)
            for row in current_words.itertuples()
        ]
        if (
            word_pair.en,
            word_pair.sv,
            word_pair.grammar_id.value,
        ) not in current_pairs:
            return True
        print(f"Word pair already in database. {word_pair.en} - {word_pair.sv}")
        return False

    def __add_word_info(
        self,
        part_of_speech: PartOfSpeech,
        word_category: WordCategory,
        word_group: int,
        word_pair: WordPair,
    ) -> None:
        """Add word information to the word table.

        Args:
            part_of_speech: The part of speech of the word pair.
            word_category: The word category of the word pair.
            word_group: The word group id of the word pair.
            word_pair: The WordPair object.
        """
        query = """
            INSERT INTO Words (
                English,
                Swedish,
                PartOfSpeechID,
                WordCategoryID,
                WordGroup,
                GrammarCategoryID
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (
            word_pair.en,
            word_pair.sv,
            part_of_speech.value,
            word_category.value,
            word_group,
            word_pair.grammar_id.value,
        )
        self.cursor.execute(query, values)

    def __add_context_hint(self, word_group: int, context_hint: str) -> None:
        """Add hints to tips table.

        Args:
            word_group: The word group id of the word pair.
            context_hint: The context hint of the word pair.
        """
        query = """
            INSERT INTO Hints (
                WordGroup,
                Hint
            )
            VALUES (?, ?)
        """
        values = (word_group, context_hint)
        self.cursor.execute(query, values)

    def __add_wiktionary_link(self, word_group: int, wiktionary_link: str) -> None:
        """Add Wiktionary link to wiktionary table.

        Args:
            word_group: The word group id of the word pair.
            wiktionary_link: Wiktionary link for word pair.
        """
        query = """
            INSERT INTO Links (
                WordGroup,
                WiktionaryLink
            )
            VALUES (?, ?)
        """
        values = (word_group, wiktionary_link)
        self.cursor.execute(query, values)

    def __add_hint_and_link(self, word_object: Word, word_group: int) -> None:
        """Add context hint and Wiktionary link to database.

        Args:
            word_group: Word group id.
        """
        if word_object.context_hint:
            self.__add_context_hint(word_group, word_object.context_hint)
        if word_object.wiktionary_link:
            self.__add_wiktionary_link(word_group, word_object.wiktionary_link)

    def __add_new_word(self, word_object: Word) -> None:
        """Add new word pairs to the database.

        For each word pair in the word group, check if the pair is
        already in the database. If is not, add the word pair. If any of
        the word pairs for a word group are already in the database, the
        context hint and Wiktionary link for that word group is not
        added.

        Args:
            word_object: The word object to add.
        """
        found_duplicate = False
        word_group = self.__get_next_attribute_id("WordGroup")
        for word_pair in word_object.word_list:
            if self.__check_not_duplicated(word_pair):
                self.__add_word_info(
                    word_object.part_of_speech,
                    word_object.word_category,
                    word_group,
                    word_pair,
                )
                self.counter.tick(word_object)
            else:
                found_duplicate = True

        if not found_duplicate:
            self.__add_hint_and_link(word_object, word_group)

        self.connection.commit()

    def add(self) -> None:
        """Add words to database.

        Args:
            words_phrases: A list of words and phrases to add.
        """
        for word_phrase in self.words_phrases:
            self.__add_new_word(word_phrase)
        self.connection.close()
        self.counter.print_summary()


if __name__ == "__main__":
    from words import words_phrases

    NewWords(words_phrases).add()

    parser = argparse.ArgumentParser()
    parser.add_argument("--checkout", action="store_true")
    args = parser.parse_args()

    # Remove changes after they have been committed to database.
    if args.checkout:
        subprocess.call(["git", "checkout", "database/new_words/words.py"])
