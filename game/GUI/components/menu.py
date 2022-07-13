"""Module with a class to create start game menu.

Functions:
    fetch_options: get a list of options for a menu item from
        the database

Classes:
    Menu: base class for menu items
    TranslationDirection: contains methods to create translation direction
        menu items
    Round: contains methods to create number of rounds menu items
    NumberOfWords: contains methods to create number of rounds menu items
    WordType: contains methods to create word type menu items
    WordCategory: contains methods to create word category menu items
"""

from abc import abstractmethod
import sqlite3
import tkinter as tk

import pandas as pd

import GUI


def fetch_options(table: str, column: str) -> list[str]:
    """Fetch the options from the Vocabulary database.

    Args:
        table: the name of the sql table
        column: the name of the column containing the options

    Returns:
        A list of the options.
    """
    connection = sqlite3.connect("game/database/vocabulary.db")
    options = pd.read_sql_query(f"SELECT {column} FROM {table}", connection)
    connection.close()
    return list(options[column])


class Menu:
    """Class with methods to display game options.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: GUI.Game) -> None:
        self.game = game
        self.values_set_indicator = None
        self.submit_values_button = None
        self.translation_direction = TranslationDirection(self.game)
        self.n_rounds = Rounds(self.game)
        self.n_words = NumberOfWords(self.game)
        self.word_type = WordType(self.game)
        self.word_category = WordCategory(self.game)

    def create(self) -> None:
        """Display all widgets which form the menu."""
        self.translation_direction.create_menu_items()
        self.n_rounds.create_menu_items()
        self.n_words.create_menu_items()
        self.word_type.create_menu_items()
        self.word_category.create_menu_items()
        self._create_submit_button()

    def _create_submit_button(self) -> None:
        """Create button to submit selections."""
        self.values_set_indicator = tk.IntVar()
        self.submit_values_button = tk.Button(
            self.game.gui,
            text="Submit values",
            command=lambda: [self._get_values(), self.values_set_indicator.set(1)],
        )
        self.submit_values_button.place(x=400, y=350, anchor="c", width=150)

    def _get_values(self) -> None:
        """Get the values from the option selections and destroy menu."""
        self.game.settings.n_rounds = self.n_rounds.selection.get()
        n_words_entry = self.n_words.entry.get()
        self.game.settings.n_words = int(n_words_entry if n_words_entry != "" else 5)
        self.game.settings.word_type = self.word_type.selection.get()
        self.game.settings.word_category = self.word_category.selection.get()
        self.game.settings.translation_direction = (
            self.translation_direction.selection.get()
        )
        self.game.settings.set_langauges()
        self.game.destroy_widgets_except(names=["titleText"])


class CharacteristicEntry:
    """Base class for characteristic label and option input in menu.
    
    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        label: The label for the characteristic.
        entry: The entry field for the characteristic.
    """

    def __init__(self, game: GUI.Game):
        self.game = game
        self.label: tk.Label = None
        self.entry: tk.Entry | tk.OptionMenu = None

    @abstractmethod
    def _create_label(self):
        """Create characterstic input label."""

    @abstractmethod
    def _create_entry(self):
        """Create input functionality for characterstic."""

    @abstractmethod
    def create_menu_items(self):
        """Create label and input options/field for characteristic."""

    def destroy_widgets(self):
        """Destroy the widgets."""
        self.label.destroy()
        self.entry.destroy()


class TranslationDirection(CharacteristicEntry):
    """Class with methods to create translation direction menu items.
    
    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        label: The label for the characteristic.
        entry: The entry field for the characteristic.
        selection: The variable selected in the option menu.
    """

    def __init__(self, game: GUI.Game):
        super().__init__(game)
        self.selection = tk.StringVar()

    def _create_label(self) -> None:
        """Create language select label."""
        self.label = tk.Label(text="Choose translation direction", font=("Arial", 15))
        self.label.place(x=200, y=90, anchor="w")

    def _create_entry(self) -> None:
        """Create language select button."""
        self.selection.set("en till sv")
        self.entry = tk.OptionMenu(
            self.game.gui, self.selection, "en till sv", "sv till en"
        )
        self.entry.place(x=450, y=90, anchor="w")

    def create_menu_items(self) -> None:
        """Create label and button."""
        self._create_label()
        self._create_entry()


class Rounds(CharacteristicEntry):
    """Class with methods to create number of rounds menu items.
    
    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        label: The label for the characteristic.
        entry: The entry field for the characteristic.
        selection: The variable selected in the option menu.
    """

    def __init__(self, game: GUI.Game):
        super().__init__(game)
        self.selection = tk.IntVar()

    def _create_label(self) -> None:
        """Create number of rounds label."""
        self.label = tk.Label(text="Choose number of rounds", font=("Arial", 15))
        self.label.place(x=200, y=290, anchor="w")

    def _create_entry(self) -> None:
        """Create number of rounds button."""
        self.selection.set(1)
        self.entry = tk.OptionMenu(self.game.gui, self.selection, 1, 2, 3, 4, 5)
        self.entry.place(x=450, y=290, anchor="w")

    def create_menu_items(self) -> None:
        """Create label and button."""
        self._create_label()
        self._create_entry()


class NumberOfWords(CharacteristicEntry):
    """Class with methods to number of words menu items.
    
    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        label: The label for the characteristic.
        entry: The entry field for the characteristic.
    """

    def _create_label(self) -> None:
        """Create number of words label."""
        self.label = tk.Label(text="Choose number of words", font=("Arial", 15))
        self.label.place(x=200, y=240, anchor="w")

    def _create_entry(self) -> None:
        """Create number of words button."""
        self.entry = tk.Entry()
        self.entry.place(x=450, y=240, anchor="w")

    def create_menu_items(self) -> None:
        """Create label and entry."""
        self._create_label()
        self._create_entry()


class WordType(CharacteristicEntry):
    """Class with methods to create word type menu items.
    
    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        label: The label for the characteristic.
        entry: The entry field for the characteristic.
        selection: The variable selected in the option menu.
    """

    def __init__(self, game: GUI.Game):
        super().__init__(game)
        self.selection = tk.StringVar()

    def _create_label(self) -> None:
        """Create word type label."""
        self.label = tk.Label(text="Choose word type", font=("Arial", 15))
        self.label.place(x=200, y=140, anchor="w")

    def _create_entry(self) -> None:
        """Create word type button."""
        options = fetch_options("ordtyp", "typ")
        self.selection.set(options[0])
        self.entry = tk.OptionMenu(self.game.gui, self.selection, *options)
        self.entry.place(x=450, y=140, anchor="w")

    def create_menu_items(self) -> None:
        """Create label and button."""
        self._create_label()
        self._create_entry()


class WordCategory(CharacteristicEntry):
    """Class with methods to create word category menu items.
    
    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        label: The label for the characteristic.
        entry: The entry field for the characteristic.
        selection: The variable selected in the option menu.
    """

    def __init__(self, game: GUI.Game):
        super().__init__(game)
        self.selection = None

    def _create_label(self) -> None:
        """Create word category label."""
        self.label = tk.Label(text="Choose word category", font=("Arial", 15))
        self.label.place(x=200, y=190, anchor="w")

    def _create_entry(self) -> None:
        """Create word category button."""
        options = fetch_options("ordkategori", "kategori")
        self.selection = tk.StringVar()
        self.selection.set(options[0])
        self.entry = tk.OptionMenu(self.game.gui, self.selection, *options)
        self.entry.place(x=450, y=190, anchor="w")

    def create_menu_items(self) -> None:
        """Create label and button."""
        self._create_label()
        self._create_entry()
