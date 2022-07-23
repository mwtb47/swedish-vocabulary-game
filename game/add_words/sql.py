"""Module with a class and a function to add new words to the database.

# TODO: I don't like how this is organised. Should this be a class? 
# If not, how best organise functionality?

Classes:
    Database: A class with methods to add a new word object to
        the database.
"""

import sqlite3

import pandas as pd
import numpy as np

from objects import Adjective, Generic, Noun, Verb, Word


class Database:
    """Class containing methods to add a new word pair to the database.
    
    Args:
        new_word: Object representing a new word.
    
    Attributes:
        new_word: Object representing a new word.
        connection: sqlite3 connection to vocabulary database.
        cursor: Cursor for the connection.
        words: DataFrame containing data from words table in database.
        found_duplicate: Boolean indicating if any word pair in word
            object is already in the database.
    """

    def __init__(self, new_word: Adjective | Generic | Noun | Verb):
        self.new_word = new_word

    def _open_connection(self):
        """Open conncection to Vocabulary database and create cursor."""
        self.connection = sqlite3.connect("game/database/vocabulary.db")
        self.cursor = self.connection.cursor()

        # sqlite does not accept integers of more than 8 bytes therefore
        # the np.int64 returned by _get_next_attribute_id has to be cast
        # to an int.
        sqlite3.register_adapter(np.int64, int)

    def _close_connection(self):
        """Commit and close connection to Vocabulary database."""
        self.connection.commit()
        self.connection.close()

    def _read_current_words(self):
        """Fetch all columns from the ord table."""
        self.words = pd.read_sql_query("""SELECT * FROM ord""", self.connection)

    def _get_next_attribute_id(self, attribute: str) -> int:
        """Get an unused word group id. This is the max current id + 1.

        Args:
            attribute: The name of the column to find the next id for.

        Returns:
            Integer to be used as word group id.
        """
        df = pd.read_sql_query(f"""SELECT {attribute} FROM ord""", self.connection)
        return df[attribute].max() + 1

    def _check_not_duplicate(self, word_pair: Word) -> bool:
        """Check for duplicate entry of the English - Swedish pair.

        Args:
            word_info: Adjective, Generic, Noun, or Verb object to
                be added to database.

        Returns:
            True if the word or phrase pair is not already in the
            database, False if it is.
        """
        current_pairs = [(row.engelska, row.svenska) for row in self.words.itertuples()]
        if (word_pair.en, word_pair.sv) not in current_pairs:
            self.found_duplicate = False
            return True
        print(f"Word pair already in database. {word_pair.en} - {word_pair.sv}")
        self.found_duplicate = True
        return False

    def _add_word_info(
        self,
        id_: int,
        word_type: int,
        word_category: int,
        ordgrupp: int,
        word_pair: Word,
    ) -> None:
        """Add Wiktionary link to wiktionary table.

        Args:
            id_: The word id for the word pair.
            word_type: The word type of the word pair.
            word_category: The word category of the word pair.
            ordgrupp: The word group id of the word pair.
            word_pair: The Word object.
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
        self.cursor.execute(query, values)

    def _add_context_hint(self, ordgrupp: int, context_hint: str) -> None:
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

    def _add_wiktionary_link(self, ordgrupp: int, wiktionary_link: str) -> None:
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

    def _add_hint_and_link(self, ordgrupp: int) -> None:
        """Add context hint and Wiktionary link to database.
        
        Args:
            ordgrupp: Word group id.
        """
        if self.new_word.context_hint and not self.found_duplicate:
            self._add_context_hint(ordgrupp, self.new_word.context_hint)
        if self.new_word.wiktionary_link and not self.found_duplicate:
            self._add_wiktionary_link(ordgrupp, self.new_word.wiktionary_link)

    def add_new_word(self) -> None:
        """Add new word pairs to the database.

        For each word pair in the word group, check if the pair is already
        in the database. If is not, add the word pair. If any of the word
        pairs for a word group are already in the database, the context
        hint and Wiktionary link for that word group is not added.
        """
        self._open_connection()
        self._read_current_words()
        ordgrupp = self._get_next_attribute_id("ordgrupp")
        for word_pair in self.new_word.word_list:
            if word_pair and self._check_not_duplicate(word_pair):
                id_ = self._get_next_attribute_id("id")
                self._add_word_info(
                    id_,
                    self.new_word.word_type,
                    self.new_word.word_category,
                    ordgrupp,
                    word_pair,
                )
        self._add_hint_and_link(ordgrupp)
        self._close_connection()
