"""Module with functions and classes to manage word pairs.

Functions:
    format_text: Clean up text for answer comparison.

Classes:
    WordPair: A dataclass containing information about a word pair
        which forms a question and answer in the game.
    GameWords: A class with methods to fetch and select words for
        session of the game.
    """

from dataclasses import dataclass, field
import random
import re
import sqlite3

import pandas as pd

import app


def format_text(text: str) -> str:
    """Format text for string comparison.

    To avoid answers being marked as incorrect due erroneous
    keystrikes, three steps are taken:
        - any character which is not a digit, letter, space or dash
          is removed.
        - any sequence of 2 or more spaces is replace by a single
          space.
        - convert to lower case.
        - strip leading and trailing spaces.

    Args:
        text: The text string to format.

    Returns:
        The formatted text string.
    """
    text = re.sub("[^\d\w -]", "", text)
    text = re.sub("[\s]{2,}", " ", text)
    text = text.lower().strip()
    return text


@dataclass(unsafe_hash=True)
class WordPair:
    """Dataclass representing a word or phrase pair.

    Attributes:
        id: The word pair or phrase pair id.
        en: The English part of the pair.
        sv: The Swedish part of the pair.
        call_language: The language the question is set in.
        grammar_hint: A grammar hint for the word or phrase pair.
        context_hint: A context hint for the word of phrase pair.
        wiktionary_hint: Link to Wiktionary article on the word
            or phrase pair.
        question: The string which forms the question.
        answer: The string which forms the answer.
        valid_answers: A list of valid answers for comparison.
    """

    id: int
    en: str
    sv: str
    call_language: str
    grammar_hint: str = None
    context_hint: str = None
    wiktionary_link: str = None
    question: str = field(init=False)
    answer: str = field(init=False)
    valid_answers: list[str] = field(init=False, compare=False)

    def __post_init__(self) -> None:
        self.__set_question_answer()
        self.__split_question()
        self.__split_answers()

    def __set_question_answer(self) -> None:
        """Set the question and answer based on the call language."""
        self.question = self.en if self.call_language == "en" else self.sv
        self.answer = self.sv if self.call_language == "en" else self.en

    def __split_question(self) -> None:
        """Select only the first word or phrase option.

        Words and phrases can have multiple options where there is
        more than one valid translation. These options are split by
        a '/'.
        """
        self.question = self.question.split("/")[0]

    def __split_answers(self) -> None:
        """Create list of valid answers."""
        self.valid_answers = [format_text(text) for text in self.answer.split("/")]


class GameWords:
    """Class with methods to fetch and select the words for the game.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        words: DataFrame containing filtered words table from database.
        words_per_group: The number of words to go in the worst score,
            lowest frequency, and random groups of words.
        word_stats: DataFrame with statistics on words.
        lowest_scores: DataFrame with lowest scoring words.
        lowest_frequency: DataFrame with lowest frequency words.
        unselected_word_groups: DataFrame with randomly selected words.
    """

    def __init__(self, game: app.Game) -> None:
        self.game = game
        self.words: pd.DataFrame = None
        self.words_per_group: int = None
        self.word_stats: pd.DataFrame = None
        self.lowest_scores: pd.DataFrame = None
        self.lowest_frequency: pd.DataFrame = None
        self.unselected_word_groups: pd.DataFrame = None

    def __open_connection(self) -> sqlite3.Connection:
        """Open connection to vocabulary database.

        Returns:
            A connection to the vocabulary database.
        """
        return sqlite3.connect("game/database/vocabulary.db")

    def __close_connection(self, connection: sqlite3.Connection) -> None:
        """Commit and close connection to vocabulary database.

        Args:
            connection: The connection to close.
        """
        connection.commit()
        connection.close()

    def __fetch_words(self) -> None:
        """Fetch words from the database.

        Raises:
            ValueError: If no words are available for the selected
                word_type and word_category combination.
        """
        query = f"""
            SELECT 
                O.id,
                O.ordtyp_id,
                O.engelska,
                O.svenska,
                O.ordgrupp,
                B.betyg,
                G.beskrivning,
                T.sammanhang_tips,
                W.l??nk
            FROM 
                ord as O
            JOIN ordtyp OT 
                ON O.ordtyp_id = OT.id
            JOIN ordkategori OK 
                ON O.ordkategori_id = OK.id
            JOIN grammatik G
                ON O.grammar_id = G.id
            LEFT JOIN betyg B  
                ON O.id = B.ord_id  
            LEFT JOIN tips T 
                ON O.ordgrupp = T.ordgrupp
            LEFT JOIN wiktionary W 
                ON O.ordgrupp = W.ordgrupp
            WHERE 
                OT.typ = '{self.game.settings.word_type}'
                AND OK.kategori = '{self.game.settings.word_category}'
        """
        connection = self.__open_connection()
        self.words = pd.read_sql_query(query, connection)
        self.__close_connection(connection)
        if len(self.words.index) == 0:
            raise ValueError(
                (
                    f"There are no words for word type {self.game.settings.word_type}, "
                    f"and word category {self.game.settings.word_category}"
                )
            )

    def __select_words(self) -> list[int]:
        """Select the words for the game."""

        def select_group_word(group: pd.DataFrame) -> pd.Series:
            """Select single word from a group.

            For a word group, pick one of the versions of the
            word (e.g. indefinite plural), count how many times it
            has been answered previously, and calculate the mean
            score for those previous answers.

            Args:
                group: A DataFrame to select a word from.

            Returns:
                Pandas series with:
                    - the selected word.
                    - the number of times the word has been answered.
                    - the mean score.
                    - the mean score for the previous 3 answers.
            """
            selected_word = group.id.sample(n=1).values[0]
            group = group[group.id == selected_word]
            frequency = sum(i for i in group.betyg if i in (0, 1))
            mean_score = group.betyg.mean()
            mean_score_last_3 = group.betyg.iloc[-3:].mean()
            return pd.Series(
                data=[selected_word, frequency, mean_score, mean_score_last_3],
                index=["id", "frequency", "mean_score", "mean_score_last_3"],
            )

        self.words_per_group = self.game.settings.n_words // 3
        self.word_stats = (
            self.words.groupby("ordgrupp").apply(select_group_word).reset_index()
        )
        self.word_stats.id = self.word_stats.id.astype(int)

        self.__select_lowest_scoring_words()
        self.__select_lowest_frequency_words()
        stats_words = self.__combine_low_score_low_frequency()
        game_words = self.__select_other_words(stats_words)
        return game_words

    def __select_lowest_scoring_words(self) -> None:
        """Select the lowest scoring words"""
        self.lowest_scores = (
            self.word_stats[self.word_stats.mean_score_last_3 < 1]
            .sort_values("mean_score")
            .head(self.words_per_group)
        )
        self.unselected_word_groups = [
            w for w in self.words.ordgrupp if w not in list(self.lowest_scores.ordgrupp)
        ]

    def __select_lowest_frequency_words(self) -> None:
        """Select the words answered least often."""
        self.lowest_frequency = (
            self.word_stats[self.word_stats.ordgrupp.isin(self.unselected_word_groups)]
            .sort_values("frequency")
            .head(self.words_per_group)
        )
        self.unselected_word_groups = [
            w
            for w in self.words.ordgrupp
            if w not in list(self.lowest_scores.ordgrupp)
            and w not in list(self.lowest_frequency.ordgrupp)
        ]

    def __combine_low_score_low_frequency(self) -> list[int]:
        """Combine lowest score and frequency words, dropping duplicates.

        Returns:
            A list of word ids.
        """
        lowest_scores = list(self.lowest_scores.id)
        lowest_frequency = list(self.lowest_frequency.id)
        return list(set(lowest_scores + lowest_frequency))

    def __select_other_words(self, stats_words: list[int]) -> list[int]:
        """Select remaining words at random.

        Args:
            stats_words: A list of already selected word ids.
        """
        remaining_words = self.words[
            self.words.ordgrupp.isin(self.unselected_word_groups)
        ]
        remaining_words = remaining_words.sample(frac=1).drop_duplicates(
            subset=["ordgrupp"]
        )
        n_remaining_words = self.game.settings.n_words - len(stats_words)
        sample_size = min(n_remaining_words, len(remaining_words.id))
        remaining_words = list(remaining_words.id.sample(n=sample_size))
        return stats_words + remaining_words

    def __get_word_pair(self, word_id: int) -> WordPair:
        """Create WordPair object for a word.

        Args:
            word_id: Integer word id.

        Returns:
            WordPair object for the word with id = word_id.
        """
        english = self.words.loc[self.words.id == word_id, "engelska"].iloc[0]
        swedish = self.words.loc[self.words.id == word_id, "svenska"].iloc[0]

        # Provide a grammar hint for adjectives. Neuter, plural, etc.
        if self.words.loc[self.words.id == word_id, "ordtyp_id"].iloc[0] == 3:
            grammar_hint = self.words.loc[self.words.id == word_id, "beskrivning"].iloc[
                0
            ]
        else:
            grammar_hint = None

        context_hint = self.words.loc[self.words.id == word_id, "sammanhang_tips"].iloc[
            0
        ]
        wiktionary_link = self.words.loc[self.words.id == word_id, "l??nk"].iloc[0]

        return WordPair(
            id=word_id,
            en=english,
            sv=swedish,
            call_language=self.game.settings.call_language,
            grammar_hint=grammar_hint,
            context_hint=context_hint,
            wiktionary_link=wiktionary_link,
        )

    def return_word_pairs(self) -> list[WordPair]:
        """Return a list of WordPair objects.

        Create a single list of words for the game, including
        repetitions for multiple rounds. The word list is shuffled
        before adding another round so words appear in a different
        order each round.

        Returns:
            List of WordPair objects, one for each word in the game.
        """
        self.__fetch_words()
        game_words = self.__select_words()
        round_words = [self.__get_word_pair(word_id) for word_id in game_words]
        game_words = []
        for _ in range(self.game.settings.n_rounds):
            random.shuffle(round_words)
            game_words.extend(round_words)
        return game_words
