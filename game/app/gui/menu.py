"""Module with a class to create start game menu.

Functions:
    fetch_options: Get a list of options for a menu item from the
        database.
    fetch_checkbox_options: Get a DataFrame of checkbox options.
    checkbox_position: Return the position for the nth checkbox.

Classes:
    Menu: Base class for menu items.
    CharacteristicEntry: Base class for characteristic entry.
    TranslationDirection: Contains methods to create translation
        direction menu items.
    Round: Contains methods to create number of rounds menu items.
    NumberOfWords: Contains methods to create number of rounds menu
        items.
    PartOfSpeech: Contains methods to create part of speech menu items.
    WordCategory: Contains methods to create word category menu items.
"""

from abc import abstractmethod
import tkinter as tk

import polars as pl

from app import Game, NoWordsError
import database as db


def format_option_text(option: str) -> str:
    """Format the string of the option checkboxes.

    Replace "_" with spaces and capitalise the first letter of the
    string.

    Args:
        option: String to format.

    Returns:
        Formatted string with a capitalised first letter.
    """
    return option.replace("_", " ").capitalize()


def fetch_options(table: str, column: str) -> list[str]:
    """Fetch the options from the Vocabulary database.

    Args:
        table: The name of the sql table.
        column: The name of the column containing the options.

    Returns:
        A list of the options.
    """
    return db.to_polars(f"SELECT {column} FROM {table}").get_column(column).to_list()


def checkbox_position(checkbox_number: int, relx: int, rely: int) -> tuple[int, int]:
    """Return the position for the nth checkbox in a collection.

    Checkboxes are arranged in two columns and are populated row by row.

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
        translation_direction: Instance of DropDownEntry for translation
            direction selection.
        n_words: Instance of TextEntry for selection of number of words
            per game.
        n_rounds: Instance of DropDownEntry for selection of number of
            rounds in game.
        parts_of_speech: Instance of CheckboxEntry for selection of
            parts of speech.
        word_categories: Instance of CheckboxEntry for selection of word
            categories.
    """

    def __init__(self, game: Game) -> None:
        self.game = game
        self.checkbox_options = db.to_polars(db.views.checkboxes)
        self.values_set_indicator = None
        self.submit_values_button = None
        self.__initialise_options()

    def __initialise_options(self) -> None:
        """Initialise CharacteristicEntry objects."""
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
        self.parts_of_speech = CheckboxEntry(
            game=self.game,
            label_text="part of speech",
            relx=0.6,
            rely=0.25,
            table="PartsOfSpeech",
            column="PartOfSpeech",
        )
        self.word_categories = CheckboxEntry(
            game=self.game,
            label_text="word category",
            relx=0.6,
            rely=0.5,
            table="WordCategories",
            column="WordCategory",
        )

    def create(self) -> None:
        """Display all widgets which form the menu."""
        self.translation_direction.create_menu_items()
        self.n_rounds.create_menu_items()
        self.n_words.create_menu_items()
        self.parts_of_speech.create_menu_items()
        self.word_categories.create_menu_items()
        self.__create_submit_button()

    def __create_submit_button(self) -> None:
        """Create button to submit selections.

        When the commit button is pressed, this triggers the function
        which populates the game settings and attempts to get words from
        the database.
        """
        self.values_set_indicator = tk.IntVar()
        self.game.buttons.create_submit_options_button(self._get_values)

    def _get_values(self) -> None:
        """Get the values from the option selections and destroy menu."""
        self.game.settings.n_rounds = int(self.n_rounds.value)
        self.game.settings.n_words = int(self.n_words.value or 5)
        self.game.settings.parts_of_speech = self.parts_of_speech.values
        self.game.settings.word_categories = self.word_categories.values
        self.game.settings.translation_direction = self.translation_direction.value
        self.game.settings.set_langauges()
        self.__try_get_words()

    def __try_get_words(self) -> None:
        """Try to get words with specified settings.

        Try to get words from the database which match the specified
        parts of speech and word categories selected. If there are no
        words available, prompt the user to select a different
        combination.
        """
        try:
            self.game.settings.word_pairs = self.game.game_words.return_word_pairs()
            self.game.menu.values_set_indicator.set(1)
            self.game.destroy_widgets_except(names=["titleText"])
            self.game.destroy_widgets(names=["no_word_error"])
        except NoWordsError:
            self.game.labels.create_no_words_error(
                "No words available with selected parts of speech and word categories.",
            )

    def update_checkbox_fonts(self, updated_option: str) -> None:
        """Update checkbox font colours to show available combinations.

        Args:
            updated_option: The characteristic which has just been
                updated, either part of speech of word category.
        """
        if updated_option == "PartOfSpeech":
            values = self.parts_of_speech.values
            buttons = self.word_categories.buttons
        else:
            values = self.word_categories.values
            buttons = self.parts_of_speech.buttons

        if not values:
            self.__reset_font_colour(buttons)
        else:
            self.__update_characteristic(updated_option, values, buttons)

    def __reset_font_colour(self, buttons: dict[str, tk.Checkbutton]) -> None:
        """Reset label font colour to white for all buttons.

        Args:
            buttons: Dictionary containing buttons to reset font colour
                of.
        """
        for button in buttons.values():
            button.config(fg="white")

    def __update_characteristic(
        self,
        updated_option: str,
        values: list[str],
        buttons: dict[str, tk.Checkbutton],
    ) -> None:
        """Update font colour to reflect available combinations.

        When a checkbox has been selected in either the part of speech
        or word category section, get the available options in the other
        section and update the font colour to indicate which options are
        now available.

        Args:
            updated_option: The updated characteristic, either part of
                speech or word category.
            values: List of selected values for the updated
                characteristic.
            buttons: Dictionary containing buttons to update font
                colours of.
        """
        unchanged_option = (
            "WordCategory" if updated_option == "PartOfSpeech" else "PartOfSpeech"
        )

        options = (
            self.checkbox_options.filter(pl.col(updated_option).is_in(values))
            .get_column(unchanged_option)
            .unique()
            .to_list()
        )

        for option, button in buttons.items():
            if option not in options:
                button.config(fg="grey")
            else:
                button.config(fg="white")


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
        label: The label widget for the characteristic.
        entry: The entry widget for the characteristic.
    """

    def __init__(self, game: Game, label_text: str, relx: int, rely: int) -> None:
        self.game = game
        self.label_text = label_text
        self.relx = relx
        self.rely = rely
        self.label: tk.Label = None
        self.entry: tk.Checkbutton | tk.Entry | tk.OptionMenu = None

    @abstractmethod
    def create_entry(self) -> None:
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
        table: Name of the database table containing column with
            options.
        column: Name of the column containing the options.

    Attributes:
        game: Game class containing all game components.
        label_text: Text to complete the label 'Choose <label_text>'.
        relx: Relative x position of the label.
        rely: Relative y position of the label.
        label: The label widget.
        table: Name of the database table containing column with
            options.
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
        self.buttons: dict[str, tk.Checkbutton] = None

    def create_entry(self) -> None:
        """Create word category button."""
        options = fetch_options(self.table, self.column)
        self.option_vars = {option: tk.IntVar() for option in options}
        self.buttons = {}
        for i, (option, variable) in enumerate(self.option_vars.items()):
            formatted_option = format_option_text(option)
            button = tk.Checkbutton(
                text=formatted_option,
                variable=variable,
                onvalue=1,
                command=lambda: self.game.menu.update_checkbox_fonts(self.column),
            )
            relx, rely = checkbox_position(i, self.relx, self.rely)
            button.place(relx=relx, rely=rely + 0.05, anchor="w")
            self.buttons[option] = button

    @property
    def values(self) -> list[str]:
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
    def value(self) -> str:
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
    def value(self) -> str:
        """Return the inputed value."""
        return self.entry.get()
