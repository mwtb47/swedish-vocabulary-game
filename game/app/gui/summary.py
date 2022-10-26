"""Module with a class to display summary of game.

Classes:
    Summary: Class containing methods to show a summary of a game session.
"""

import numpy as np

from app import Game


class Summary:
    """Class with methods show summary of game.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: Game) -> None:
        self.game = game

    def show_summary(self) -> None:
        """Display % correct answers."""
        mark = np.mean([m["Mark"] for m in self.game.status.marks]) * 100
        self.game.labels.create_score_title()
        self.game.labels.create_score(mark)
        self.__show_incorrect_words()

    def __show_incorrect_words(self) -> None:
        """Display incorrect answers in a table showing English and Swedish."""
        self.game.labels.create_incorrect_words_title()
        self.game.labels.create_incorrect_words_column(
            words=self.__incorrect_words("sv"),
            justify="left",
            relx=0.65,
            text_anchor="w",
            label_anchor="nw",
        )
        self.game.labels.create_incorrect_words_column(
            words=self.__incorrect_words("en"),
            justify="right",
            relx=0.6,
            text_anchor="e",
            label_anchor="ne",
        )

    def __incorrect_words(self, language: str) -> str:
        """Return a list of incorrectly answered words.

        The list contains the specified language version of
        each incorrectly answered word pair.

        Args:
            language: Which language version of the word pair to return.

        Returns:
            A list of words.
        """
        return [
            getattr(word_pair, language)
            for word_pair in self.game.status.incorrect_answers
        ]
