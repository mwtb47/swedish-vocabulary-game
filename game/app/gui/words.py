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

import pandas as pd

from app import Game, NoWordsError
from game import database


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
        word_stats: DataFrame with statistics on words.
        lowest_scores: DataFrame with lowest scoring words.
        lowest_frequency: DataFrame with lowest frequency words.
        unselected_word_groups: DataFrame with randomly selected words.
    """

    def __init__(self, game: Game) -> None:
        self.game = game
        self.words: pd.DataFrame = None
        self.lowest_scores: pd.DataFrame = None
        self.lowest_frequency: pd.DataFrame = None
        self.unselected_word_groups: pd.DataFrame = None

    def __fetch_words(self) -> None:
        """Fetch words from the database.

        Raises:
            NoWordsError: No words are available for the selected
                word_types and word_categories combination.
        """
        word_types = ", ".join(f"'{s}'" for s in self.game.settings.word_types)
        word_categories = ", ".join(
            f"'{s}'" for s in self.game.settings.word_categories
        )
        query = f"""
            SELECT 
                O.id,
                O.ordtyp_id,
                O.engelska,
                O.svenska,
                O.ordgrupp,
                B.betyg,
                B.tidsstämpel,
                G.beskrivning,
                T.sammanhang_tips,
                W.länk
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
                OT.typ IN ({word_types})
                AND OK.kategori IN ({word_categories})
        """
        connection = database.connect()
        self.words = pd.read_sql_query(query, connection)
        database.disconnect(connection)
        if len(self.words.index) == 0:
            raise NoWordsError

    def __select_words(self) -> list[int]:
        """Select the words for the game."""

        def select_inflection(group: pd.DataFrame) -> pd.Series:
            """Select single word inflection from a word group.

            For a word group, pick one of the inflections of the
            word (e.g. indefinite plural), count how many times it
            has been answered previously, and calculate the mean
            score for those previous answers.

            Args:
                group: A DataFrame containing multiple inflections
                    of a single word.

            Returns:
                Pandas series with:
                    : the selected word inflection.
                    : the number of times the word inflection has
                        been answered.
                    : the mean score of the word inflection.
                    : the mean score for the previous 3 answers of
                        the word inflection.
            """
            selected_inflection = group.id.sample(n=1).values[0]
            group = group[group.id == selected_inflection]
            frequency = sum(i for i in group.betyg if i in (0, 1))
            mean_score = group.betyg.mean()
            mean_score_last_3 = group.sort_values("tidsstämpel").betyg[-3:].mean()
            return pd.Series(
                data=[selected_inflection, frequency, mean_score, mean_score_last_3],
                index=["id", "frequency", "mean_score", "mean_score_last_3"],
            )

        words_per_group = self.game.settings.n_words // 3
        inflections = (
            self.words.groupby("ordgrupp").apply(select_inflection).reset_index()
        )
        inflections.id = inflections.id.astype(int)

        return self.__select_game_words(inflections, words_per_group)

    def __select_game_words(
        self, inflections: pd.DataFrame, words_per_group: int
    ) -> list[int]:
        """Return list of word ids to be used in the game.

        Args:
            inflections:
            words_per_group: The number of words to select
                using the lowest scoring and lowest frequency
                methods.

        Returns:
            List of word ids.
        """
        self.__select_lowest_scoring(inflections, words_per_group)
        self.__select_lowest_frequency(inflections, words_per_group)
        selected_words = list(
            set(self.lowest_scores.id) | set(self.lowest_frequency.id)
        )
        return self.__add_random_words(selected_words)

    def __select_lowest_scoring(
        self, inflections: pd.DataFrame, words_per_group: int
    ) -> None:
        """Select the words with the lowest score.

        The lowest score is calculated using the mean of the previous
        three answer attempts. This aims to focus on the words less
        likely to be known at present as opposed to words answered
        incorrectly in the past but with many correct answers since.

        Args:
            inflections: DataFrame with selected inflections.
            words_per_group: The number of lowest scoring words to select.
        """
        self.lowest_scores = (
            inflections[inflections.mean_score_last_3 < 1]
            .sort_values("mean_score")
            .head(words_per_group)
        )
        self.unselected_word_groups = [
            w for w in self.words.ordgrupp if w not in list(self.lowest_scores.ordgrupp)
        ]

    def __select_lowest_frequency(
        self, inflections: pd.DataFrame, words_per_group: int
    ) -> None:
        """Select the words with the fewest number of answers.

        Args:
            inflections: DataFrame with selected inflections.
            words_per_group: The number of lowest frequency words to select.
        """
        self.lowest_frequency = (
            inflections[inflections.ordgrupp.isin(self.unselected_word_groups)]
            .sort_values("frequency")
            .head(words_per_group)
        )
        self.unselected_word_groups = [
            w
            for w in self.words.ordgrupp
            if w not in list(self.lowest_scores.ordgrupp)
            and w not in list(self.lowest_frequency.ordgrupp)
        ]

    def __add_random_words(self, selected_words: list[int]) -> list[int]:
        """Select remaining words at random.

        Args:
            selected_words: A list of already selected word ids.
        """
        remaining_words = self.words[
            self.words.ordgrupp.isin(self.unselected_word_groups)
        ]
        n_missing_words = self.game.settings.n_words - len(selected_words)
        sample_size = min(n_missing_words, len(remaining_words.id))
        random_words = list(
            self.words[self.words.ordgrupp.isin(self.unselected_word_groups)]
            .sample(frac=1)
            .drop_duplicates(subset=["ordgrupp"])
            .id.sample(n=sample_size)
        )
        return selected_words + random_words

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
        wiktionary_link = self.words.loc[self.words.id == word_id, "länk"].iloc[0]

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
