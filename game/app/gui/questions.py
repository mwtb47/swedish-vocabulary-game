"""Module with a class to manage questions in the game.

Classes:
    Questions: Class containing methods to set questions in the GUI game.
"""

import textwrap
import tkinter as tk

from app import Game


class Questions:
    """Class with methods to set questions in the game.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        answer_entry: Entry field for answer.
    """

    def __init__(self, game: Game) -> None:
        self.game = game
        self.answer_entry: tk.Entry = None

    def initialise(self) -> None:
        """Prepare game for qustions and then set the first question."""
        self.game.settings.set_question_stats()
        self.game.window.translation_direction_graphic()
        self.set_question()

    def __prepare_questions_frame(self) -> None:
        """Create submit button, destroy unwanted widgets and update progress."""
        self.game.destroy_widgets_except(names=["titleText", "translationDirection"])
        self.game.buttons.create_submit_button()
        self.game.window.display_progress()

    def set_question(self, *args) -> None:
        """Display the question, any hints it has and an answer box."""
        self.__prepare_questions_frame()
        self.game.settings.set_current_word_pair(self.game.status.question_number)
        self.__display_hints()
        question = tk.Label(
            text=textwrap.fill(
                text=self.game.settings.current_word_pair.question, width=30
            ),
            font=("Arial", 24),
        )
        question.place(relx=0.4, rely=0.35, anchor="e")
        self.answer_entry = tk.Entry(width=30, font=("Arial", 24))
        self.answer_entry.focus_set()
        self.answer_entry.place(relx=0.5, rely=0.35, anchor="w")

    def move_to_next(self) -> None:
        """Move on to the next frame."""
        if self.game.status.question_number == self.game.settings.total_questions:
            self.game.gui.unbind("<Return>")
            if not self.game.status.retest:
                self.game.buttons.create_summary_button()
                if self.game.status.incorrect_answers:
                    self.game.buttons.create_retest_button()
            self.game.buttons.create_final_buttons()
        else:
            self.game.buttons.create_next_button()
            self.game.gui.bind("<Return>", self.set_question)

    def __display_hints(self) -> None:
        """Display grammar and context hints if a word pair has them."""
        hint_count = 0
        hint_locations = [0.43, 0.5]

        if hint := self.game.settings.current_word_pair.grammar_hint:
            text = f"Grammatik: {hint}"
            grammar_hint = tk.Label(
                text=textwrap.fill(text=text, width=35), font=("Arial", 16)
            )
            grammar_hint.place(relx=0.5, rely=hint_locations[hint_count], anchor="n")
            hint_count += 1

        if hint := self.game.settings.current_word_pair.context_hint:
            hints = "\n".join(hint.split("/"))
            text = f"Sammanhang: {hints}"
            context_hint = tk.Label(
                text=textwrap.fill(text=text, width=35), font=("Arial", 16)
            )
            context_hint.place(relx=0.5, rely=hint_locations[hint_count], anchor="n")

    def __create_retest(self) -> None:
        """Set up game for retesting incorrect answers."""
        self.game.status.set_up_retest()
        self.game.settings.set_up_retest(list(self.game.status.incorrect_answers) * 2)

    def start_retest(self) -> None:
        """Start retesting incorrect answers."""
        self.game.destroy_widgets(
            names=["incorrect_title", "mark_label", "score_label", "en", "sv"]
        )
        self.game.window.translation_direction_graphic()
        self.__create_retest()
        self.set_question()
