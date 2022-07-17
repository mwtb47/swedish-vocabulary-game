"""Module with a class to manage questions in the game.

Classes:
    Questions: Class containing methods to set questions in the GUI game.
"""

import textwrap
import tkinter as tk

import GUI


class Questions:
    """Class with methods to set questions in the game.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        answer_entry: Entry field for answer.
    """

    def __init__(self, game: GUI.Game) -> None:
        self.game = game
        self.answer_entry: tk.Entry = None

    def initialise(self) -> None:
        """Prepare game for qustions and then set the first question."""
        self.game.settings.word_pairs = self.game.game_words.return_word_pairs()
        self.game.settings.set_question_stats()
        self.game.window.translation_direction_graphic()
        self.set_question()

    def _prepare_questions_frame(self) -> None:
        """Create submit button, destroy unwanted widgets and update progress."""
        self.game.destroy_widgets_except(names=["titleText", "translationDirection"])
        self.game.buttons.create_submit_button()
        self.game.window.display_progress()

    def set_question(self, *args) -> None:
        """Display the question, any hints it has and an answer box."""
        self._prepare_questions_frame()
        self._display_hints()
        word_pair = self.game.settings.word_pairs[self.game.status.question_number]
        question = tk.Label(text=word_pair.question)
        question.place(x=266, y=150, anchor="n")
        self.answer_entry = tk.Entry(width=30)
        self.answer_entry.focus_set()
        self.answer_entry.place(x=533, y=150, anchor="n")

    def move_to_next(self) -> None:
        """Move on to the next frame."""
        if self.game.status.question_number == self.game.settings.total_questions:
            self.game.gui.unbind("<Return>")
            if self.game.status.retest:
                pass
            elif len(self.game.status.incorrect_answers) == 0:
                self.game.buttons.create_summary_button()
            else:
                self.game.buttons.create_summary_button()
                self.game.buttons.create_retest_button()
            self.game.buttons.create_final_buttons()
        else:
            self.game.buttons.create_next_button()
            self.game.gui.bind("<Return>", self.set_question)

    def _display_hints(self) -> None:
        """Display grammar and context hints if a word pair has them."""
        word_pair = self.game.settings.word_pairs[self.game.status.question_number]
        hint_count = 0
        hint_locations = [200, 230]

        if hint := word_pair.grammar_hint:
            text = f"Grammatik: {hint}"
            grammar_hint = tk.Label(text=textwrap.fill(text=text, width=35))
            grammar_hint.place(x=266, y=hint_locations[hint_count], anchor="n")
            hint_count += 1

        if hint := word_pair.context_hint:
            hints = "\n".join(hint.split("/"))
            text = f"Sammanhang: {hints}"
            context_hint = tk.Label(text=textwrap.fill(text=text, width=35))
            context_hint.place(x=266, y=hint_locations[hint_count], anchor="n")

    def _create_retest(self) -> None:
        """Set up game for retesting incorrect answers."""
        self.game.status.set_up_retest()
        self.game.settings.set_up_retest(list(self.game.status.incorrect_answers) * 2)

    def start_retest(self) -> None:
        """Start retesting incorrect answers."""
        self.game.destroy_widgets(
            names=["incorrect_title", "mark_label", "score_label", "en", "sv"]
        )
        self.game.window.translation_direction_graphic()
        self._create_retest()
        self.set_question()
