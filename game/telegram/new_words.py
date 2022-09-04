"""Module with functions to add new words to database.

A new word can be added to the database by sending a message in the following format:

    #newword swedish word/phrase - danish word/phrase ~word_type ~word_category

This is currently only available for generic words. All word categories in the
WordCategories enum can be specified.

Word types:
~substantiv
~verb
~adjektiv
~adverb
~fras
~preposition

Word categories:
~allmän
"""

from enum import Enum
import re

from game.new_words.add import NewWords
from game.new_words.enums import WordCategory, WordType, GrammarType
from game.new_words.objects import Generic, WordPair


def return_valid_flags(attribute: Enum, flags: list[str]) -> list[str]:
    """Return a list of valid flags for specified attribute.

    Args:
        enum: WordType or WordCategory enum.
        flags: List of flags from the message.

    Returns:
        List of valid flags.
    """
    valid_flags = [f"~{s.lower()}" for s in attribute.__members__]
    return [
        attribute.__getitem__(flag[1:].upper()) for flag in flags if flag in valid_flags
    ]


def parse_new_word(message: str) -> Generic:
    """Parse new word and return as a Generic word instance.

    Parse the word, getting the Swedish part, Danish part, word type
    and word category. These are then used to create a Generic word
    type instance.

    Args:
        message: The message to parse.

    Returns:
        New word from the message as a Generic word instance.
    """
    flags = re.findall("~\\w+", message)

    # TODO This will raise an error if empty. It should perhaps
    # send an error message instead.
    word_type = return_valid_flags(WordType, flags)[0]
    word_categories = return_valid_flags(WordCategory, flags)

    # Default to generic word category if either no word category
    # or more than one word category has been specified.
    if len(word_categories) == 1:
        word_category = word_categories[0]
    else:
        word_category = WordCategory.ALLMÄN

    return Generic(
        word_phrase=WordPair(
            sv=re.search("#newword (.*?) - ", message).group(1),
            da=re.search(" - (.*?)(?=$| ~)", message).group(1),
            grammar_id=GrammarType.NA,
        ),
        word_type=word_type,
        word_category=word_category,
    )


def add(new_words: list[str]) -> None:
    """Add all the new word messages to the database.

    Args:
        new_words: List of messages containing new words.
    """
    new_words = [parse_new_word(line) for line in new_words]
    NewWords(new_words).add()
