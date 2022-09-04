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

from game import database
from game.new_words.enums import WordCategory, WordType
from game.new_words.objects import Adjective, Adverb, Generic, Noun, Verb, WordPair


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

    def print_summary(self) -> None:
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

    def __init__(
        self, words_phrases: list[Adjective | Adverb | Generic | Noun | Verb]
    ) -> None:
        self.words_phrases = words_phrases
        self.counter = Counter()
        self.__create_connection_and_cursor()
        self.__set_sqlite3_cast_rule()

    def __create_connection_and_cursor(self) -> None:
        """Create sqlite3 database connection and cursor."""
        self.connection, self.cursor = database.connect_with_cursor()

    def __set_sqlite3_cast_rule(self) -> None:
        """sqlite does not accept integers of more than 8 bytes therefore
        the np.int64 returned by get_next_attribute_id has to be cast to
        an int.
        """
        sqlite3.register_adapter(np.int64, int)

    def __read_current_words(self) -> pd.DataFrame:
        """Fetch all columns from the ord table.

        Returns:
            DataFrame containing words table from database.
        """
        return pd.read_sql_query("""SELECT * FROM ord""", self.connection)

    def __get_next_attribute_id(self, attribute: str) -> int:
        """Get an unused attribute id. This is the max current id + 1.

        Args:
            attribute: The name of the column to find the next id for.

        Returns:
            Integer to be used as next id.
        """
        df = pd.read_sql_query(f"""SELECT {attribute} FROM ord""", self.connection)
        return df[attribute].max() + 1

    def __check_not_duplicated(self, word_pair: WordPair) -> bool:
        """Check for duplicate entry of the Swedish - Danish pair.

        Args:
            word_pair: WordPair object to be added to the database.

        Returns:
            True if the word or phrase pair is not already in the
            database, False if it is.
        """
        current_words = self.__read_current_words()
        current_pairs = [
            (row.svenska, row.danska, row.grammar_id)
            for row in current_words.itertuples()
        ]
        if (word_pair.sv, word_pair.da, word_pair.grammar_id) not in current_pairs:
            return True
        print(f"Word pair already in database. {word_pair.sv} - {word_pair.da}")
        return False

    def __add_word_info(
        self,
        id_: int,
        word_type: WordType,
        word_category: WordCategory,
        ordgrupp: int,
        word_pair: WordPair,
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
                svenska,
                danska,
                ordtyp_id,
                ordkategori_id,
                ordgrupp,
                grammar_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            id_,
            word_pair.sv,
            word_pair.da,
            word_type.value,
            word_category.value,
            ordgrupp,
            word_pair.grammar_id.value,
        )
        self.cursor.execute(query, values)

    def __add_context_hint(self, ordgrupp: int, context_hint: str) -> None:
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
        self.cursor.execute(query, values)

    def __add_wiktionary_link(self, ordgrupp: int, wiktionary_link: str) -> None:
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
        self.cursor.execute(query, values)

    def __add_hint_and_link(
        self, word_object: Adjective | Adverb | Generic | Noun | Verb, ordgrupp: int
    ) -> None:
        """Add context hint and Wiktionary link to database.

        Args:
            ordgrupp: Word group id.
        """
        if word_object.context_hint:
            self.__add_context_hint(ordgrupp, word_object.context_hint)
        if word_object.wiktionary_link:
            self.__add_wiktionary_link(ordgrupp, word_object.wiktionary_link)

    def __add_new_word(
        self, word_object: Adjective | Adverb | Generic | Noun | Verb
    ) -> None:
        """Add new word pairs to the database.

        For each word pair in the word group, check if the pair is already
        in the database. If is not, add the word pair. If any of the word
        pairs for a word group are already in the database, the context
        hint and Wiktionary link for that word group is not added.

        Args:
            word_object: The word object to add.
        """
        found_duplicate = False
        ordgrupp = self.__get_next_attribute_id("ordgrupp")
        for word_pair in word_object.word_list:
            if self.__check_not_duplicated(word_pair):
                id_ = self.__get_next_attribute_id("id")
                self.__add_word_info(
                    id_,
                    word_object.word_type,
                    word_object.word_category,
                    ordgrupp,
                    word_pair,
                )
                self.counter.tick(word_object)
            else:
                found_duplicate = True

        if not found_duplicate:
            self.__add_hint_and_link(word_object, ordgrupp)

    def add(self) -> None:
        """Add words to database.

        Args:
            words_phrases: A list of words and phrases to add.
        """
        for word_phrase in self.words_phrases:
            self.__add_new_word(word_phrase)
        database.disconnect(self.connection, commit=True)
        self.counter.print_summary()


if __name__ == "__main__":
    from words import words_phrases

    NewWords(words_phrases).add()
