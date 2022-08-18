"""Module with a class to manage GUI game window elements.

Classes:
    Window: Class containing methods to style and create widgets for
        the GUI window.
"""

import tkinter as tk

from app import Game


class Window:
    """Class with methods create window and title objects.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: Game) -> None:
        self.game = game

    def create(self) -> None:
        """Create window and title."""
        self.__create_window()
        self.__create_title()

    def __create_window(self) -> None:
        """Set window title and geometry."""
        self.game.gui.title("Vocabulary Game")
        self.game.gui.geometry("1000x600")

    def __create_title(self) -> None:
        """Create Vocabulary Game title text."""
        title = tk.Label(
            self.game.gui, text="Vocabulary Game", font=("Arial", 45), name="titleText"
        )
        title.place(relx=0.5, rely=0.025, anchor="n")

    def translation_direction_graphic(self) -> None:
        """Create the translation direction graphic."""
        if self.game.settings.translation_direction == 1:
            text = "🇬🇧 ⇒ 🇸🇪"
        else:
            text = "🇸🇪 ⇒ 🇬🇧"
        translation_direction_label = tk.Label(
            text=text, font=("Arial", 40), name="translationDirection"
        )
        translation_direction_label.place(relx=0.5, rely=0.125, anchor="n")

    def display_progress(self) -> None:
        """Display the question number and round number."""
        n_rounds = 2 if self.game.status.retest else self.game.settings.n_rounds
        current_question = self.game.status.question_number_in_round(
            self.game.settings.questions_per_round
        )
        current_round = self.game.status.current_round(
            self.game.settings.questions_per_round
        )
        retest_status = "Retest round" if self.game.status.retest else "Round"
        text = (
            f"Question {current_question} of {self.game.settings.questions_per_round:.0f}\n"
            f"{retest_status} {current_round} of {n_rounds}"
        )
        progress_label = tk.Label(text=text, justify="right")
        progress_label.place(relx=0.98, rely=0.02, anchor="ne")
