"""Module with a class to manage the answers in the game.

Classes:
    Answers: A class with methods to check answers and add marks.
"""

import tkinter as tk
from time import time
import webbrowser

import app


class Answers:
    """Class with methods to check answers and store marks.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: app.Game) -> None:
        self.game = game

    def check_answer(self, *args) -> None:
        """Check the answers against the list of valid answers."""
        formatted_answer = app.format_text(self.game.questions.answer_entry.get())
        if formatted_answer in self.game.settings.current_word_pair.valid_answers:
            mark = 1
            answer_description = "✅ Correct"
        else:
            mark = 0
            answer_description = f"❌ Incorrect\n\nCorrect answer: {self.game.settings.current_word_pair.answer}"
            if not self.game.status.retest:
                self.game.status.incorrect_answers.add(
                    self.game.settings.current_word_pair
                )

        self.display_answer_check(answer_description)
        self.add_mark(mark)

        self.game.status.question_number += 1
        self.game.questions.move_to_next()

    def display_answer_check(self, description: str) -> None:
        """Display if answer is correct or not plus a link to Wiktionary entry."""
        answer_indicator = tk.Label(text=description, font=("Arial", 22))
        answer_indicator.place(relx=0.5, rely=0.55, anchor="n")
        self.game.destroy_widgets(names=["submitButton"])
        if self.game.settings.current_word_pair.wiktionary_link:
            self.__create_wiktionary_link()

    def __create_wiktionary_link(self) -> None:
        """Create a Wiktionary link for the Swedish word in the word pair."""

        def callback(url: str) -> None:
            webbrowser.open_new(url)

        link = self.game.settings.current_word_pair.wiktionary_link
        link_text = f"Wiktionary SV: {link.split('/')[-1]}"
        self.game.labels.create_wiktionary_link(link_text, link)

    def add_mark(self, mark: int) -> None:
        """Add mark to marklist if not during retest.

        Args:
            mark: 1 if correct, 0 if incorrect.
        """
        if not self.game.status.retest:
            self.game.status.marks.append(
                {
                    "ord_id": self.game.settings.current_word_pair.id,
                    "betyg": mark,
                    "översättningsriktning": self.game.settings.translation_direction,
                    "tidsstämpel": time(),
                }
            )
