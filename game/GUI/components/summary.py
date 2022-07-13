"""Module with a class to display summary of game.

Classes:
    Summary: Class containing methods to show a summary of a game session.
"""

import tkinter as tk

import numpy as np

import GUI


class Summary:
    """Class with methods show summary of game.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: GUI.Game) -> None:
        self.game = game

    def show_summary(self) -> None:
        """Display % correct answers."""
        mark = np.mean([m["betyg"] for m in self.game.status.marks]) * 100
        score_label = tk.Label(text="Score", font="Helvetica 16 bold", width=5)
        mark_label = tk.Label(
            text=f"{round(mark, 1)}%", font="Helvetica 14 bold", width=5
        )
        score_label.place(x=160, y=170, anchor="c")
        mark_label.place(x=160, y=200, anchor="c")
        self._show_incorrect_words()

    def _show_incorrect_words(self) -> None:
        """Display incorrect answers in a table showing English and Swedish."""
        incorrect_title = tk.Label(
            text="Fel ord/fraser", font="Helvetica 14 bold", anchor="c", width=25
        )
        incorrect_title.place(x=505, y=115, anchor="c")

        english = [word_pair.en for word_pair in self.game.status.incorrect_answers]
        swedish = [word_pair.sv for word_pair in self.game.status.incorrect_answers]
        en = tk.Label(text="\n".join(english), justify="right", anchor="e", width=25)
        sv = tk.Label(text="\n".join(swedish), justify="left", anchor="w", width=25)
        en.place(x=500, y=125, anchor="ne")
        sv.place(x=510, y=125, anchor="nw")
