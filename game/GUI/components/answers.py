"""Module with a class to manage the answers in the game.

Classes:
    Answers: A class with methods to check answers and add marks.
"""

import tkinter as tk
from time import time
import webbrowser

import GUI


class Answers:
    """Class with methods to check answers and store marks.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: GUI.Game) -> None:
        self.game = game

    def check_answer(self, *args) -> None:
        """Check the answers against the list of valid answers."""
        word_pair = self.game.settings.word_pairs[self.game.status.question_number]
        formatted_answer = GUI.format_text(self.game.questions.answer_entry.get())
        if formatted_answer in word_pair.valid_answers:
            mark = 1
            answer_description = "✅ Correct"
        else:
            mark = 0
            answer_description = f"❌ Incorrect\nCorrect answer: {word_pair.answer}"
            if not self.game.status.retest:
                self.game.status.incorrect_answers.add(word_pair)

        self.display_answer_check(word_pair, answer_description)
        self.add_mark(word_pair.id, mark)

        self.game.status.question_number += 1
        self.game.questions.move_to_next()

    def display_answer_check(self, word_pair: "GUI.WordPair", description: str) -> None:
        """Display if answer is correct or not plus a link to Wiktionary entry."""
        answer_indicator = tk.Label(text=description)
        answer_indicator.place(x=400, y=250, anchor="n")
        self.game.destroy_widgets(names=["submitButton"])
        if word_pair.wiktionary_link:
            self._create_wiktionary_link(word_pair)

    def _create_wiktionary_link(self, word_pair: "GUI.WordPair") -> None:
        """Create a link to the Wiktionary entry for a word if it has one."""

        def callback(url: str):
            webbrowser.open_new(url)

        link = word_pair.wiktionary_link
        link_text = f"Wiktionary SV: {link.split('/')[-1]}"
        wiktionary_link = tk.Label(
            text=link_text, font="Helvetica 12 underline", fg="DeepSkyBlue2"
        )
        wiktionary_link.place(x=400, y=290, anchor="n")
        wiktionary_link.bind("<Button-1>", lambda e: callback(link))

    def add_mark(self, word_id: int, mark: int) -> None:
        """Add mark to marklist if not during retest.

        Args:
            word_id: The word_id of the word to add.
            mark: 1 if correct, 0 if incorrect.
        """
        if not self.game.status.retest:
            self.game.status.marks.append(
                {
                    "ord_id": word_id,
                    "betyg": mark,
                    "översättningsriktning": self.game.settings.translation_direction,
                    "tidsstämpel": time(),
                }
            )
