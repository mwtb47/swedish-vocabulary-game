"""Module with a class to display summary of game.

Classes:
    Summary: Class containing methods to show a summary of a game session.
"""

import tkinter as tk

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
        mark = np.mean([m["betyg"] for m in self.game.status.marks]) * 100
        score_label = tk.Label(text="Score", font="Helvetica 16 bold", width=5)
        mark_label = tk.Label(
            text=f"{round(mark, 1)}%", font="Helvetica 14 bold", width=5
        )
        score_label.place(relx=0.2, rely=0.34, anchor="c")
        mark_label.place(relx=0.2, rely=0.4, anchor="c")
        self.__show_incorrect_words()

    def __show_incorrect_words(self) -> None:
        """Display incorrect answers in a table showing English and Swedish."""
        incorrect_title = tk.Label(
            text="Fel ord/fraser", font="Helvetica 14 bold", anchor="c", width=25
        )
        incorrect_title.place(relx=0.625, rely=0.23, anchor="c")

        english = [word_pair.en for word_pair in self.game.status.incorrect_answers]
        swedish = [word_pair.sv for word_pair in self.game.status.incorrect_answers]
        en = tk.Label(text="\n".join(english), justify="right", anchor="e", width=25)
        sv = tk.Label(text="\n".join(swedish), justify="left", anchor="w", width=25)
        en.place(relx=0.6, rely=0.25, anchor="ne")
        sv.place(relx=0.65, rely=0.25, anchor="nw")
