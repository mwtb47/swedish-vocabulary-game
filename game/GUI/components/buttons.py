"""Module with a class to manage buttons in the game.

Classes:
    Buttons: Class containing methods to create buttons in the GUI game.
"""

import tkinter as tk

import GUI


class Buttons:
    """Class with methods to create buttons.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: GUI.Game) -> None:
        self.game = game

    def create_next_button(self) -> None:
        """Create button to move on to next question."""
        next_button = tk.Button(text="Next question", command=self.game.questions.set_question)
        next_button.place(x=400, y=400, anchor="n", width=150)

    def create_submit_button(self) -> None:
        """Create button to submit answer."""
        self.game.gui.bind("<Return>", self.game.answers.check_answer)
        submit_button = tk.Button(text="Submit answer", command=self.game.answers.check_answer, name="submitButton")
        submit_button.place(x=400, y=300, anchor="n", width=150)

    def create_retest_button(self) -> None:
        """Create button to start retesting incorrect answers."""
        retest_button = tk.Button(
            text="Retest incorrect answers",
            command=self.game.questions.start_retest,
            name="createRetest",
        )
        retest_button.place(x=410, y=330, anchor="w", width=250)

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
        summary_button = tk.Button(
            text="Show summary",
            command=lambda: [
                self.game.destroy_widgets_except(names=widgets_to_keep),
                self.game.summary.show_summary(),
            ],
            name="showSummary",
        )
        summary_button.place(x=390, y=330, anchor="e", width=250)

    def _create_start_new_game_button(self) -> None:
        """Create button to restart the game."""
        start_new_game_button = tk.Button(
            text="Start new game", command=self._start_new_game, name="startNewGame"
        )
        start_new_game_button.place(x=390, y=360, anchor="e", width=250)

    def _create_quit_button(self) -> None:
        """Create button to quit game."""
        quit_button = tk.Button(
            text="Quit game", command=self.game.gui.destroy, name="quitGame"
        )
        quit_button.place(x=410, y=360, anchor="w", width=250)

    def create_final_buttons(self):
        """Create start new game and quit game buttons."""
        self._create_start_new_game_button()
        self._create_quit_button()

    def _start_new_game(self):
        """Clear widgets for new game."""
        self.game.commit_marks()
        self.game.destroy_widgets_except(names=["titleText"])
        self.game.menu.create()
        self.game.start()
