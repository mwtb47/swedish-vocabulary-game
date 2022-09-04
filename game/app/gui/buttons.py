"""Module with a class to manage buttons in the game.

Classes:
    Buttons: Class containing methods to create buttons in the GUI game.
"""

import tkinter as tk
from typing import Callable

from app import Game


class Buttons:
    """Class with methods to create buttons.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: Game) -> None:
        self.game = game

    def __create(self, button_kwargs, place_kwargs) -> None:
        """Function to create Tkinter button.

        Args:
            button_kwargs: Dictionary of arguments for Button object.
            place_kwargs: Dictionary of arguments for Button place method.
        """
        button = tk.Button(master=self.game.gui, **button_kwargs)
        button.place(place_kwargs)
        return button

    def create_submit_options_button(self, command: Callable) -> None:
        """Create button used to submit menu option selections.

        Args:
            command: Callable command attached to button.
        """
        button_kwargs = {"text": "Submit values", "command": command}
        place_kwargs = {"relx": 0.5, "rely": 0.875, "anchor": "c", "width": 150}
        self.game.menu.submit_values_button = self.__create(button_kwargs, place_kwargs)

    def create_submit_answer_button(self) -> None:
        """Create button to submit answer."""
        self.game.gui.bind("<Return>", self.game.answers.check_answer)
        button_kwargs = {
            "text": "Submit answer",
            "command": self.game.answers.check_answer,
            "name": "submitButton",
            "font": ("Arial", 16),
        }
        place_kwargs = {"relx": 0.5, "rely": 0.9, "anchor": "n", "width": 150}
        self.__create(button_kwargs, place_kwargs)

    def create_next_button(self) -> None:
        """Create button to move on to next question."""
        button_kwargs = {
            "text": "Next question",
            "command": self.game.questions.set_question,
            "font": ("Arial", 16),
        }
        place_kwargs = {"relx": 0.5, "rely": 0.9, "anchor": "n", "width": 150}
        self.__create(button_kwargs, place_kwargs)

    def create_summary_button(self) -> None:
        """Create button to display summary."""
        widgets_to_keep = [
            "titleText",
            "translationDirection",
            "showSummary",
            "quitGame",
            "startNewGame",
            "createRetest",
        ]
        button_kwargs = {
            "text": "Show summary",
            "command": lambda: [
                self.game.destroy_widgets_except(names=widgets_to_keep),
                self.game.summary.show_summary(),
            ],
            "name": "showSummary",
        }
        place_kwargs = {"relx": 0.49, "rely": 0.88, "anchor": "e", "width": 250}
        self.__create(button_kwargs, place_kwargs)

    def create_retest_button(self) -> None:
        """Create button to start retesting incorrect answers."""
        button_kwargs = {
            "text": "Retest incorrect answers",
            "command": self.game.questions.start_retest,
            "name": "createRetest",
        }
        place_kwargs = {"relx": 0.51, "rely": 0.88, "anchor": "w", "width": 250}
        self.__create(button_kwargs, place_kwargs)

    def __create_start_new_game_button(self) -> None:
        """Create button to restart the game."""
        button_kwargs = {
            "text": "Start new game",
            "command": self.__start_new_game,
            "name": "startNewGame",
        }
        place_kwargs = {"relx": 0.49, "rely": 0.93, "anchor": "e", "width": 250}
        self.__create(button_kwargs, place_kwargs)

    def __create_quit_button(self) -> None:
        """Create button to quit game."""
        button_kwargs = {
            "text": "Quit game",
            "command": self.game.gui.destroy,
            "name": "quitGame",
        }
        place_kwargs = {"relx": 0.51, "rely": 0.93, "anchor": "w", "width": 250}
        self.__create(button_kwargs, place_kwargs)

    def create_final_buttons(self) -> None:
        """Create start new game and quit game buttons."""
        self.__create_start_new_game_button()
        self.__create_quit_button()

    def __start_new_game(self) -> None:
        """Clear widgets for new game."""
        self.game.commit_marks()
        self.game.destroy_widgets_except(names=["titleText"])
        self.game.menu.create()
        self.game.start()
