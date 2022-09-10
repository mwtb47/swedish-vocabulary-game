"""Module containing utilities for game.

Classes:
    Settings: Class containing the game's settings.
    Status: Class containing variables to track game status.
"""

from dataclasses import dataclass, field

import pandas as pd

import app
from game import database


@dataclass
class Settings:
    """Class containing the game's settings.

    All settings, except for total_questions and word_pairs,
    do not change during the game after being set.
    total_questions and word_pairs are updated if a retest
    is started.

    Attributes:
        n_words: The number of words per round.
        n_rounds: The number of rounds.
        parts_of_speech: The parts of speech chosen for the game.
        word_categories: The word categories chosen for the game.
        translation_direction: 'en to sv' or 'sv to en'.
        call_language: The language of the question.
        response_language: The language of the response.
        translation_direction: Integer representation for database.
        total_questions: The number of questions.
        word_pairs: A list of WordPair objects.
        current_word_pair: The current WordPair object.
    """

    n_words: int = field(init=False)
    n_rounds: int = field(init=False)
    parts_of_speech: list[str] = field(init=False)
    word_categories: list[str] = field(init=False)
    translation_direction: str = field(init=False)
    call_language: str = field(init=False)
    response_language: str = field(init=False)
    translation_direction: int = field(init=False)
    questions_per_round: int = field(init=False)
    total_questions: int = field(init=False)
    word_pairs: "list[app.WordPair]" = field(init=False)
    current_word_pair: "app.WordPair" = field(init=False)

    def set_question_stats(self) -> None:
        """Set the total number of question and questions per round."""
        n_questions = len(self.word_pairs)
        self.questions_per_round = int(n_questions / self.n_rounds)
        self.total_questions = n_questions

    def set_langauges(self) -> None:
        """Set the call and response language plus the int translaton direction."""
        self.call_language = self.translation_direction.split(" ")[0]
        self.response_language = self.translation_direction.split(" ")[2]
        self.translation_direction = 1 if self.response_language == "sv" else 2

    def set_up_retest(self, incorrect_answers: "list[app.WordPair]") -> None:
        """Set up settings for retesting incorrect answers.

        Args:
            incorrect_answers: List of WordPair objects.
        """
        self.word_pairs = incorrect_answers
        self.n_rounds = 2
        self.set_question_stats()

    def set_current_word_pair(self, question_number: int) -> None:
        """Set the current word pair.

        Args:
            question_number: Current question number.
        """
        self.current_word_pair = self.word_pairs[question_number]


@dataclass
class Status:
    """Class containing variables to track game status.

    Attributes:
        incorrect_answers: A set of incorrect answers.
        marks: A list of marks.
        question_number: The current question number.
        retest: A boolean indicating if game is in normal or retest mode.
    """

    incorrect_answers: "set[app.WordPair]" = field(default_factory=set)
    marks: list[int] = field(default_factory=list)
    question_number: int = 0
    retest: bool = False

    def commit_marks_to_database(self) -> None:
        """Add marks from the game to the marks table in the database.

        The marks for the game include the word id, mark, translation
        directions, and Unix time stamp for each translation in the
        game.
        """
        marks = pd.DataFrame(self.marks)
        connection = database.connect()
        marks.to_sql("betyg", connection, if_exists="append", index=False)
        database.disconnect(connection, commit=True)

    def question_number_in_round(self, questions_per_round: int) -> int:
        """Return the question number within the round.

        Args:
            questions_per_round: The number of questions per round.

        Returns:
            Current question number of the round.
        """
        return int(self.question_number % questions_per_round) + 1

    def current_round(self, questions_per_round: int) -> int:
        """Return the current round.

        Args:
            questions_per_round: The number of questions per round.

        Returns:
            The current round.
        """
        return int(self.question_number // questions_per_round) + 1

    def set_up_retest(self) -> None:
        """Change retest status and set question number to 0."""
        self.retest = True
        self.question_number = 0
