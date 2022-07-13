"""Module with class to control the game.

Classes:
    Game: The base class for the game GUI.
"""

import tkinter as tk

import GUI


class Game:
    """The base class for the translation game GUI.
    
    Args:
        no_commit: Boolean denoting whether marks are committed to database.
    
    Attributes:
        no_commit: Boolean denoting whether marks are committed to database.
        gui: tkinter top level widget.
        window: Instance of the Window class.
        settings: Instance of the Settings class.
        status: Instance of the Status class.
        answers: Instance of the Answers class.
        buttons: Instance of the Buttons class.
        game_words: Instance of the GameWords class.
        menu: Instance of the Menu class.
        questions: Instance of the Questions class.
        summary: Instance of the Summary class.
    """

    def __init__(self, no_commit: bool) -> None:
        self.no_commit = no_commit
        self.gui = tk.Tk()
        self.window = GUI.Window(self)
        self.window.create()
        self.start()

    def start(self) -> None:
        """Start a new instance of the game.

        Create new instances of the game elements. Display the options
        menu and wait for the user to select the options. Then set the
        first question.
        """
        self.settings = GUI.Settings()
        self.status = GUI.Status()
        self.answers = GUI.Answers(self)
        self.buttons = GUI.Buttons(self)
        self.game_words = GUI.GameWords(self)
        self.menu = GUI.Menu(self)
        self.questions = GUI.Questions(self)
        self.summary = GUI.Summary(self)
        self.menu.create()
        self.menu.submit_values_button.wait_variable(self.menu.values_set_indicator)
        self.questions.initialise()

    def run(self) -> None:
        """Call mainloop."""
        self.gui.mainloop()

    def commit_marks(self):
        """Commit marks to database."""
        if not self.no_commit:
            self.status.commit_marks_to_database()

    def destroy_widgets(self, names: list[str]) -> None:
        """Destroy all widgets in the window which are in names list.

        Args:
            names: list of widget names to destroy
        """
        for widget in self.gui.winfo_children():
            if widget.winfo_name() in names:
                widget.destroy()

    def destroy_widgets_except(self, names: list[str]) -> None:
        """Destroy all widgets in the window except for those in names list.

        Args:
            names: list of widget names to not destroy
        """
        for widget in self.gui.winfo_children():
            if widget.winfo_name() not in names:
                widget.destroy()
