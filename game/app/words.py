"""Module with functions and classes to manage word pairs.

Functions:
    format_text: Clean up text for answer comparison.

Classes:
    WordPair: A dataclass containing information about a word pair
        which forms a question and answer in the game.
    GameWords: A class with methods to fetch and select words for
        session of the game.
    """

from dataclasses import dataclass
import random
import re
import warnings

# Suppress FutureWarnings in Polars
warnings.simplefilter(action="ignore", category=FutureWarning)

import polars as pl

from app import Game, NoWordsError
from game import database


def format_text(text: str) -> str:
    """Format text for string comparison.

    To avoid answers being marked as incorrect due erroneous
    keystrikes, three steps are taken:
        - any character which is not a digit, letter, space, dash
          or colon is removed.
        - any sequence of 2 or more spaces is replace by a single
          space.
        - convert to lower case.
        - strip leading and trailing spaces.

    Args:
        text: The text string to format.

    Returns:
        The formatted text string.
    """
    text = re.sub("[^\d\w -:]", "", text)
    text = re.sub("[\s]{2,}", " ", text)
    return text.lower().strip()


@dataclass(unsafe_hash=True)
class WordPair:
    """Dataclass representing a word or phrase pair.

    Attributes:
        id: The word pair or phrase pair id.
        sv: The Swedish part of the pair.
        da: The Danish part of the pair.
        call_language: The language the question is set in.
        grammar_hint: A grammar hint for the word or phrase pair.
        context_hint: A context hint for the word of phrase pair.
        wiktionary_hint: Link to Wiktionary article on the word
            or phrase pair.
    """

    id: int
    sv: str
    da: str
    call_language: str
    grammar_hint: str = None
    context_hint: str = None
    wiktionary_link: str = None

    def __post_init__(self) -> None:
        """Set the question and answer strings."""
        if self.call_language == "sv":
            self._question_string = self.sv
            self._answer_string = self.da
        else:
            self._question_string = self.da
            self._answer_string = self.sv

    @property
    def question(self) -> str:
        """The string which forms the question."""
        return self._question_string.split("/")[0]

    @property
    def answer(self) -> str:
        """The string which contains all answer options."""
        return self._answer_string.replace("/", " / ")

    @property
    def valid_answers(self) -> list[str]:
        """A list of valid answers."""
        return [format_text(text) for text in self._answer_string.split("/")]


class GameWords:
    """Class with methods to fetch and select the words for the game.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: Game) -> None:
        self.game = game

    def __fetch_words(self) -> None:
        """Fetch words from the database.

        Raises:
            NoWordsError: No words are available for the selected
                parts_of_speech and word_categories combination.
        """
        parts_of_speech = ", ".join(
            f"'{s}'" for s in self.game.settings.parts_of_speech
        )
        word_categories = ", ".join(
            f"'{s}'" for s in self.game.settings.word_categories
        )
        query = f"""
            SELECT
                O.id,
                O.ordtyp_id,
                O.svenska,
                O.danska,
                O.ordgrupp,
                B.betyg,
                B.tidsstämpel,
                G.beskrivning,
                T.sammanhang_tips,
                W.länk
            FROM
                ord as O
            LEFT OUTER JOIN betyg as B
                ON O.id = B.ord_id
            JOIN ordtyp OT 
                ON O.ordtyp_id = OT.id
            JOIN ordkategori OK 
                ON O.ordkategori_id = OK.id
            JOIN grammatik G
                ON O.grammar_id = G.id
            LEFT JOIN tips T 
                ON O.ordgrupp = T.ordgrupp
            LEFT JOIN wiktionary W 
                ON O.ordgrupp = W.ordgrupp
            WHERE 
                OT.typ IN ({parts_of_speech})
                AND OK.kategori IN ({word_categories})
        """

        words = pl.read_sql(query, database.connection_uri)
        if words.shape[0] == 0:
            raise NoWordsError
        return words

    def __select_inflections(self, words: pl.DataFrame) -> pl.DataFrame:
        """Select the inflections from which game words will be chosen.

        One inflection from each word group is selected at random. Three
        statistics are then calculated for each inflection:
            count: The number of times the inflection has been answered.
            mean: The mean mark for all answers.
            mean_last_3: The mean mark for the last three answers.

        Args:
            words: DataFrame with words from database.

        Returns:
            DataFrame with selected inflections and summary statistics.
        """
        inflections = (
            words.select(pl.col(["id", "ordgrupp"]))
            .groupby(by="ordgrupp")
            .agg(pl.all().sample(n=1))
            .explode("id")
            .select(["id", "ordgrupp"])
        )
        return (
            inflections.join(words, how="left", on="id")
            .groupby(["id", "ordgrupp"])
            .agg(
                [
                    pl.col("betyg").drop_nulls().count().alias("count"),
                    pl.col("betyg").mean().alias("mean"),
                    pl.col("betyg").tail(3).mean().alias("mean_last_3"),
                ]
            )
        )

    def __select_game_words(self, words: pl.DataFrame) -> list[int]:
        """Return list of word ids to be used in the game.

        Words are selected using three methods, each responsible for
        one third of the words in the game.

        1. The inflections with the lowest mean_last_3 value.
        2. The inflections with the fewest answers.
        3. A random selection of inflections.

        For each method, the inflections which have already been
        selected for the game are not available for selection again.

        Args:
            DataFrame with words from the database.

        Returns:
            List of word ids.
        """
        words_per_group = self.game.settings.n_words // 3
        inflections = self.__select_inflections(words)
        low_scores = self.__select_low_scoring(inflections, words_per_group)
        low_count = self.__select_low_count(inflections, low_scores, words_per_group)
        random_words = self.__select_random(inflections, low_scores, low_count)
        return (
            pl.concat([low_scores, low_count, random_words]).get_column("id").to_list()
        )

    def __select_low_scoring(
        self, inflections: pl.DataFrame, words_per_group: int
    ) -> pl.DataFrame:
        """Select the words with the lowest score.

        The lowest score is calculated using the mean of the previous
        three answer attempts. This aims to focus on the words less
        likely to be known at present as opposed to words answered
        incorrectly in the past but with many correct answers since.

        Args:
            inflections: DataFrame with inflections to choose from.
            words_per_group: The number of lowest scoring words to
                select.

        Returns:
            DataFrame with selection of lowest scoring words.
        """
        return (
            inflections.filter(pl.col("mean_last_3") < 1)
            .sort(["mean_last_3", "mean"])
            .head(words_per_group)
        )

    def __select_low_count(
        self, inflections: pl.DataFrame, low_scores: pl.DataFrame, words_per_group: int
    ) -> pl.DataFrame:
        """Select the words with the fewest number of answers.

        Args:
            inflections: DataFrame with selected inflections.
            low_scores: DataFrame with selection of lowest scoring words.
            words_per_group: The number of lowest scoring words to
                select.

        Results:
            DataFrame with selection of lowest frequency words.
        """
        return (
            inflections.filter(
                ~pl.col("ordgrupp").is_in(low_scores.get_column("ordgrupp"))
            )
            .sort("count")
            .head(words_per_group)
        )

    def __select_random(
        self,
        inflections: pl.DataFrame,
        low_scores: pl.DataFrame,
        low_frequency: pl.DataFrame,
    ) -> pl.DataFrame:
        """Select remaining words at random.

        Args:
            inflections: DataFrame with selected inflections.
            low_scores: DataFrame with selection of lowest scoring words.
            low_frequency: DataFrame with selection of lowest frequency
                words.

        Returns:
            DataFrame with randomly selected words.
        """
        selected_words = pl.concat([low_scores, low_frequency])
        remaining_words = inflections.filter(
            ~pl.col("ordgrupp").is_in(selected_words.get_column("ordgrupp"))
        )

        n_missing_words = self.game.settings.n_words - selected_words.shape[0]
        sample_size = min(n_missing_words, remaining_words.shape[0])
        return remaining_words.sample(n=sample_size)

    def __get_word_pair(self, words: pl.DataFrame, word_id: int) -> WordPair:
        """Create WordPair object for a word.

        Args:
            words: DataFrame with words from the database.
            word_id: Integer word id.

        Returns:
            WordPair object for the word with id = word_id.
        """
        word = words.filter(pl.col("id") == word_id)
        swedish = word.get_column("svenska")[0]
        danish = word.get_column("danska")[0]

        # Provide a grammar hint for adjectives. Neuter, plural, etc.
        if word.get_column("ordtyp_id")[0] == 3:
            grammar_hint = word.get_column("beskrivning")[0]
        else:
            grammar_hint = None

        context_hint = word.get_column("sammanhang_tips")[0]
        wiktionary_link = word.get_column("länk")[0]

        return WordPair(
            id=word_id,
            sv=swedish,
            da=danish,
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
        words = self.__fetch_words()
        game_words = self.__select_game_words(words)
        round_words = [self.__get_word_pair(words, word_id) for word_id in game_words]
        game_words = []
        for _ in range(self.game.settings.n_rounds):
            random.shuffle(round_words)
            game_words.extend(round_words)
        return game_words
