"""Module with a class to create start game menu.

Functions:
    fetch_options: Get a list of options for a menu item from
        the database.
    checkbox_position: Return the position for the nth checkbox.

Classes:
    Menu: Base class for menu items.
    CharacteristicEntry: Base class for characteristic entry.
    TranslationDirection: Contains methods to create translation direction
        menu items.
    Round: Contains methods to create number of rounds menu items.
    NumberOfWords: Contains methods to create number of rounds menu items.
    WordType: Contains methods to create word type menu items.
    WordCategory: Contains methods to create word category menu items.
"""

from abc import abstractmethod
import tkinter as tk

import pandas as pd

from app import Game, NoWordsError
from game import database


def fetch_options(table: str, column: str) -> list[str]:
    """Fetch the options from the Vocabulary database.

    Args:
        table: The name of the sql table.
        column: The name of the column containing the options.

    Returns:
        A list of the options.
    """
    connection = database.connect()
    options = pd.read_sql_query(f"SELECT {column} FROM {table}", connection)
    database.disconnect(connection)
    return list(options[column])


def checkbox_position(checkbox_number: int, relx: int, rely: int) -> tuple[int, int]:
    """Return the position for the nth checkbox in a collection.

    Args:
        checkbox_number: Index of the checkbox in the collection.
        relx: The relative x position of the first checkbox in
            collection.
        rely: The relative y postiion of the first checkbox in
            collection.

    Returns:
        Tuple with relative x and relative y positions of checkbox.
    """
    y = rely + checkbox_number // 2 * 0.04
    return (relx, y) if checkbox_number % 2 == 0 else (relx + 0.2, y)


class Menu:
    """Class with methods to display game options.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
        values_set_indicator: Indicator which is set to 1 when the
            submit values button is pressed.
        submit_values_button: Button used to submit values.
        translation_direction: Instance of TranslationDirection.
        n_words: Instance of NumberofWords.
        n_rounds: Instance of Rounds.
        word_types: Instance of WordType.
        word_cvategories: Instance of WordCategory.
    """

    def __init__(self, game: Game) -> None:
        self.game = game
        self.values_set_indicator = None
        self.submit_values_button = None
        self.translation_direction = DropdownEntry(
            game=self.game,
            label_text="translation direction",
            relx=0.1,
            rely=0.25,
            options=["en till sv", "sv till en"],
        )
        self.n_words = TextEntry(
            game=self.game,
            label_text="number of words per round",
            relx=0.1,
            rely=0.4,
        )
        self.n_rounds = DropdownEntry(
            game=self.game,
            label_text="number of rounds",
            relx=0.1,
            rely=0.55,
            options=[1, 2, 3, 4, 5],
        )
        self.word_types = CheckboxEntry(
            game=self.game,
            label_text="word type",
            relx=0.6,
            rely=0.25,
            table="ordtyp",
            column="typ",
        )
        self.word_categories = CheckboxEntry(
            game=self.game,
            label_text="word category",
            relx=0.6,
            rely=0.45,
            table="ordkategori",
            column="kategori",
        )

    def create(self) -> None:
        """Display all widgets which form the menu."""
        self.translation_direction.create_menu_items()
        self.n_rounds.create_menu_items()
        self.n_words.create_menu_items()
        self.word_types.create_menu_items()
        self.word_categories.create_menu_items()
        self.__create_submit_button()

    def __create_submit_button(self) -> None:
        """Create button to submit selections."""
        self.values_set_indicator = tk.IntVar()
        self.game.buttons.create_submit_options_button(self._get_values)

    def _get_values(self) -> None:
        """Get the values from the option selections and destroy menu."""
        self.game.settings.n_rounds = int(self.n_rounds.value)
        self.game.settings.n_words = int(self.n_words.value or 5)
        self.game.settings.word_types = self.word_types.values
        self.game.settings.word_categories = self.word_categories.values
        self.game.settings.translation_direction = self.translation_direction.value
        self.game.settings.set_langauges()
        self.__try_get_words()

    def __try_get_words(self) -> None:
        """Get the words."""
        try:
            self.game.settings.word_pairs = self.game.game_words.return_word_pairs()
            self.game.menu.values_set_indicator.set(1)
            self.game.destroy_widgets_except(names=["titleText"])
            self.game.destroy_widgets(names=["no_word_error"])
        except NoWordsError:
            self.game.labels.create_no_words_error(
                "No words available with selected word types and word categories.",
            )
            )


class CharacteristicEntry:
    """Base class for characteristic label and option input in menu.

    Args:
        game: Game class containing all game components.
        label_text: Text to complete the label 'Choose <label_text>'.
        relx: Relative x position of the label.
        rely: Relative y position of the label.

    Attributes:
        game: Game class containing all game components.
        label_text: Text to complete the label 'Choose <label_text>'.
        relx: Relative x position of the label.
        rely: Relative y position of the label.
        label: The label widget.
        entry: The entry field for the characteristic.
    """

    def __init__(self, game: Game, label_text: str, relx: int, rely: int) -> None:
        self.game = game
        self.label_text = label_text
        self.relx = relx
        self.rely = rely
        self.label: tk.Label = None
        self.entry: tk.Checkbutton | tk.Entry | tk.OptionMenu = None

    @abstractmethod
    def create_entry(self):
        """Create input functionality for characterstic."""

    def create_menu_items(self) -> None:
        """Create label and button."""
        self.label = self.game.labels.create_menu_characteristic(
            self.label_text, self.relx, self.rely
        )
        self.create_entry()


class CheckboxEntry(CharacteristicEntry):
    """Class with methods to create checkbox entries.

    Args:
        game: Game class containing all game components.
        label_text: Text to complete the label 'Choose <label_text>'.
        relx: Relative x position of the label.
        rely: Relative y position of the label.
        table: Name of the database table containing column with options.
        column: Name of the column containing the options.

    Attributes:
        game: Game class containing all game components.
        label_text: Text to complete the label 'Choose <label_text>'.
        relx: Relative x position of the label.
        rely: Relative y position of the label.
        label: The label widget.
        table: Name of the database table containing column with options.
        column: Name of the column containing the options.
        option_vars: Dictionary of option names and variables.
    """

    def __init__(
        self,
        game: Game,
        label_text: str,
        relx: int,
        rely: int,
        table: str,
        column: str,
    ) -> None:
        super().__init__(game, label_text, relx, rely)
        self.table = table
        self.column = column
        self.option_vars = None

    def create_entry(self) -> None:
        """Create word category button."""
        options = fetch_options(self.table, self.column)
        self.option_vars = {option: tk.IntVar() for option in options}
        for i, (option, variable) in enumerate(self.option_vars.items()):
            button = tk.Checkbutton(
                text=option, variable=variable, onvalue=1, offvalue=0
            )
            relx, rely = checkbox_position(i, self.relx, self.rely)
            button.place(relx=relx, rely=rely + 0.05, anchor="w")

    @property
    def values(self):
        """Return the selected value(s)."""
        return [
            option
            for option, variable in self.option_vars.items()
            if variable.get() == 1
        ]


class DropdownEntry(CharacteristicEntry):
    """Class with methods to create translation direction menu items.

    Args:
        game: Game class containing all game components.
        label_text: Text to complete the label 'Choose <label_text>'.
        relx: Relative x position of the label.
        rely: Relative y position of the label.
        options: List of options to display in the dropdown.

    Attributes:
        game: Game class containing all game components.
        label_text: Text to complete the label 'Choose <label_text>'.
        relx: Relative x position of the label.
        rely: Relative y position of the label.
        label: The label widget.
        options: List of options to display in the dropdown.
        selection: The variable selected in the option menu.
    """

    def __init__(
        self,
        game: Game,
        label_text: str,
        relx: int,
        rely: int,
        options: list[str | int],
    ) -> None:
        super().__init__(game, label_text, relx, rely)
        self.options = options
        self.selection = tk.StringVar()

    def create_entry(self) -> None:
        """Create language select button."""
        self.selection.set(self.options[0])
        entry = tk.OptionMenu(self.game.gui, self.selection, *self.options)
        entry.place(relx=self.relx, rely=self.rely + 0.05, anchor="w")

    @property
    def value(self):
        """Return the selected value."""
        return self.selection.get()


class TextEntry(CharacteristicEntry):
    """Class with methods to number of words menu items.

    Args:
        game: Game class containing all game components.
        label_text: Text to complete the label 'Choose <label_text>'.
        relx: Relative x position of the label.
        rely: Relative y position of the label.

    Attributes:
        game: Game class containing all game components.
        label_text: Text to complete the label 'Choose <label_text>'.
        relx: Relative x position of the label.
        rely: Relative y position of the label.
        label: The label widget.
        entry: The entry field for the characteristic.
    """

    def __init__(self, game: Game, label_text: str, relx: int, rely: int) -> None:
        super().__init__(game, label_text, relx, rely)

    def create_entry(self) -> None:
        """Create number of words button."""
        self.entry = tk.Entry()
        self.entry.place(relx=self.relx, rely=self.rely + 0.05, anchor="w")

    @property
    def value(self):
        """Return the selected value."""
        return self.entry.get()
