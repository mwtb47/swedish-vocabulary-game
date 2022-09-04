"""Module with class to create label widgets in the game.

Classes:
    Labels: Class containing methods to create labels in the game.
"""
import textwrap
import tkinter as tk
from typing import Callable
import webbrowser


class Labels:
    """Class with method to create widget labels.

    Args:
        master: The parent window.

    Attributes:
        master: The parent window.
    """

    def __init__(self, master: tk.Tk) -> None:
        self.master = master

    def __create(self, label_kwargs: dict, place_kwargs: dict) -> None:
        """Create the Label object and place it.

        Args:
            label_kwargs: Dictionary of arguments for Label object.
            place_kwargs: Dictionary of arguments for Label place method.
        """
        label = tk.Label(master=self.master, **label_kwargs)
        label.place(**place_kwargs)

    def __create_with_binding(
        self, label_kwargs: dict, place_kwargs: dict, binding: Callable
    ) -> None:
        """Create the Label object, place it and add binding.

        Args:
            label_kwargs: Dictionary of arguments for Label
                object.
            place_kwargs: Dictionary of arguments for Label
                place method.
            binding: The function to bind to the label.
        """
        label = tk.Label(master=self.master, **label_kwargs)
        label.place(**place_kwargs)
        label.bind("<Button-1>", binding)

    def create_answer_indicator(self, text: str) -> None:
        """Create and place answer indicator label.

        Args:
            text: The label text.
        """
        label_kwargs = {"text": text, "name": "answerIndicator", "font": ("Arial", 22)}
        place_kwargs = {"relx": 0.5, "rely": 0.73, "anchor": "s"}
        self.__create(label_kwargs, place_kwargs)

    def create_context_hint(self, text: str, rely: float) -> None:
        """Create and place context hint label.

        Args:
            text: The label text.
            rely: The relative y position of the label.
        """
        label_kwargs = {
            "text": textwrap.fill(text=text, width=80),
            "name": "contextHint",
            "font": ("Arial", 16),
        }
        place_kwargs = {"relx": 0.5, "rely": rely, "anchor": "n"}
        self.__create(label_kwargs, place_kwargs)

    def create_grammar_hint(self, text: str, rely: float) -> None:
        """Create and place grammar hint label.

        Args:
            text: The label text.
            rely: Relative y position of the label.
        """
        label_kwargs = {
            "text": textwrap.fill(text=text, width=80),
            "name": "grammarHint",
            "font": ("Arial", 16),
        }
        place_kwargs = {"relx": 0.5, "rely": rely, "anchor": "n"}
        self.__create(label_kwargs, place_kwargs)

    def create_incorrect_words_column(
        self,
        words: list[str],
        justify: str,
        relx: float,
        text_anchor: str,
        label_anchor: str,
    ) -> None:
        """Create and place incorrect words column label.

        Args:
            words: List of words to display in column.
            justify: Text justification.
            relx: Relative x position of the label.
            text_anchor: Anchor location of the text.
            label_anchor: Anchor location of the label.
        """
        label_kwargs = {
            "text": "\n".join(words),
            "justify": justify,
            "name": f"incorrectWords{justify}",
            "anchor": text_anchor,
        }
        place_kwargs = {"relx": relx, "rely": 0.25, "anchor": label_anchor}
        self.__create(label_kwargs, place_kwargs)

    def create_incorrect_words_title(self) -> None:
        """Create and place incorrect words title label."""
        label_kwargs = {
            "text": "Fel ord/fraser",
            "font": "Helvetica 14 bold",
            "name": "incorrectWordsTitle",
            "width": 25,
            "anchor": "c",
        }
        place_kwargs = {"relx": 0.625, "rely": 0.23, "anchor": "c"}
        self.__create(label_kwargs, place_kwargs)

    def create_menu_characteristic(self, text: str, relx: float, rely: float) -> None:
        """Create and place menu characteristic label.

        Args:
            text: The label text.
            relx: Relative x position of the label.
            rely: Relative y position of the label.
        """
        label_kwargs = {"text": f"Choose {text}", "name": text, "font": ("Arial", 20)}
        place_kwargs = {"relx": relx, "rely": rely, "anchor": "w"}
        self.__create(label_kwargs, place_kwargs)

    def create_no_words_error(self, text: str) -> None:
        """Create and place no words error label.

        Args:
            text: The label text.
        """
        label_kwargs = {
            "text": text,
            "name": "noWordsError",
            "bg": "white",
            "fg": "red",
        }
        place_kwargs = {"relx": 0.5, "rely": 0.92, "anchor": "n"}
        self.__create(label_kwargs, place_kwargs)

    def create_progress_info(self, text: str) -> None:
        """Create and place progress information label.

        Args:
            text: The label text.
        """
        label_kwargs = {"text": text, "name": "progressLabel", "justify": "right"}
        place_kwargs = {"relx": 0.98, "rely": 0.02, "anchor": "ne"}
        self.__create(label_kwargs, place_kwargs)

    def create_question(self, text: str) -> None:
        """Create and place question label.

        Args:
            text: The label text.
        """
        label_kwargs = {
            "text": textwrap.fill(text=text, width=30),
            "name": "question",
            "font": ("Arial", 24),
        }
        place_kwargs = {"relx": 0.4, "rely": 0.35, "anchor": "e"}
        self.__create(label_kwargs, place_kwargs)

    def create_title_text(self) -> None:
        """Create and place title text label."""
        label_kwargs = {
            "text": "Vocabulary Game",
            "name": "titleText",
            "font": ("Arial", 45),
        }
        place_kwargs = {"relx": 0.5, "rely": 0.025, "anchor": "n"}
        self.__create(label_kwargs, place_kwargs)

    def create_translation_direction(self, text: str) -> None:
        """Create and place translation direction label.

        Args:
            text: The label text.
        """
        label_kwargs = {
            "text": text,
            "name": "translationDirection",
            "font": ("Arial", 40),
        }
        place_kwargs = {"relx": 0.5, "rely": 0.125, "anchor": "n"}
        self.__create(label_kwargs, place_kwargs)

    def create_score(self, mark: float) -> None:
        """Create and place score label.

        Args:
            mark: The percentage of correct answers.
        """
        label_kwargs = {
            "text": f"{round(mark, 1)}%",
            "name": "score",
            "width": 5,
            "font": "Helvetica 16 bold",
        }
        place_kwargs = {"relx": 0.2, "rely": 0.4, "anchor": "c"}
        self.__create(label_kwargs, place_kwargs)

    def create_score_title(self) -> None:
        """Create and place score title label."""
        label_kwargs = {
            "text": "Score",
            "name": "scoreTitle",
            "width": 5,
            "font": "Helvetica 16 bold",
        }
        place_kwargs = {"relx": 0.2, "rely": 0.34, "anchor": "c"}
        self.__create(label_kwargs, place_kwargs)

    def create_wiktionary_link(self, text: str, link: str) -> None:
        """Create, place and bind function to wiktionary link label.

        Args:
            text: The label text.
            link: URL link to bind to the label.
        """

        def callback(url: str) -> None:
            webbrowser.open_new(url)

        label_kwargs = {
            "text": text,
            "font": "Helvetica 18 underline",
            "fg": "DeepSkyBlue2",
        }
        place_kwargs = {"relx": 0.5, "rely": 0.77, "anchor": "n"}
        self.__create_with_binding(label_kwargs, place_kwargs, lambda e: callback(link))
