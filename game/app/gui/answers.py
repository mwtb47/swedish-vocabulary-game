"""Module with a class to manage the answers in the game.

Classes:
    Answers: A class with methods to check answers and add marks.
"""

from time import time

import app


class Answers:
    """Class with methods to check answers and store marks.

    Args:
        game: Game class containing all game components.

    Attributes:
        game: Game class containing all game components.
    """

    def __init__(self, game: app.Game) -> None:
        self.game = game

    def check_answer(self, *args) -> None:
        """Check the answers against the list of valid answers."""
        formatted_answer = app.format_text(self.game.questions.answer_entry.get())
        if formatted_answer in self.game.settings.current_word_pair.valid_answers:
            self.__add_mark(1)
            answer_description = "✅ Correct"
        else:
            self.__add_mark(0)
            self.__record_incorrect_answer()
            answer_description = f"❌ Incorrect\nCorrect answer: {self.game.settings.current_word_pair.answer}"

        self.__display_answer_check(answer_description)
        self.game.questions.move_to_next()

    def __record_incorrect_answer(self) -> None:
        """Record an incorrectly answered WordPair.

        The incorrectly answered WordPair is added to a set of incorrect
        answers.
        """
        if not self.game.status.retest:
            self.game.status.incorrect_answers.add(self.game.settings.current_word_pair)

    def __display_answer_check(self, description: str) -> None:
        """Display if answer is correct or not.

        If the answer is incorrect, display the correct answer. Also
        display a link to Wiktionary page if a link exists.

        Args:
            description: String either indicating the answer is correct
                or that it is incorrect. If it is incorrect, the correct
                answer is included.
        """
        self.game.labels.create_answer_indicator(description)
        self.game.destroy_widgets(names=["submitButton"])
        self.__display_wiktionary_link()

    def __create_wiktionary_link(self) -> None:
        """Create the Wiktionary link.

        The string in the URL after the final "/" is used as the display
        text for the link.
        """
        link = self.game.settings.current_word_pair.wiktionary_link
        link_text = f"Wiktionary SV: {link.split('/')[-1]}"
        self.game.labels.create_wiktionary_link(link_text, link)

    def __display_wiktionary_link(self) -> None:
        """Display Wiktionary link if the current word pair has one."""
        if self.game.settings.current_word_pair.wiktionary_link:
            self.__create_wiktionary_link()

    def __add_mark(self, mark: int) -> None:
        """Add mark to marklist if not during retest.

        Args:
            mark: 1 if correct, 0 if incorrect.
        """
        if not self.game.status.retest:
            self.game.status.marks.append(
                {
                    "WordID": self.game.settings.current_word_pair.id,
                    "Mark": mark,
                    "TranslationDirection": self.game.settings.translation_direction,
                    "Timestamp": time(),
                }
            )
