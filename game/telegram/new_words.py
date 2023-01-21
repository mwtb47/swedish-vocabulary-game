"""Module with functions to add new words to database.

A new word can be added to the database by sending a message in the
following format:

    #newword english word/phrase - swedish word/phrase ~part_of_speech ~word_category

This is currently only available for generic words. All word categories
in the WordCategories enum can be specified.

Parts of speech:
~noun
~verb
~adjective
~adverb
~phrase
~preposition
~conjunction

Word categories:
~general
~food
~sport
~business
~geography
~body
~word_order
~time
~particle_verbs
~clothes
~computers
~science
~animals
"""

from enum import Enum
import re

from database.new_words.add import NewWords
from game.words import GrammarCategory, PartOfSpeech, WordCategory, Generic, WordPair


def return_valid_flags(attribute: Enum, flags: list[str]) -> list[str]:
    """Return a list of valid flags for specified attribute.

    Args:
        enum: PartOfSpeech or WordCategory enum.
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

    Parse the word, getting the English part, Swedish part, part of
    speech and word category. These are then used to create a Generic
    word instance.

    Args:
        message: The message to parse.

    Returns:
        New word from the message as a Generic word instance.
    """
    flags = re.findall("~\\w+", message)

    # TODO This will raise an error if empty. It should perhaps send an
    # error message instead.
    part_of_speech = return_valid_flags(PartOfSpeech, flags)[0]
    word_categories = return_valid_flags(WordCategory, flags)

    # Default to generic word category if either no word category or
    # more than one word category has been specified.
    if len(word_categories) == 1:
        word_category = word_categories[0]
    else:
        word_category = WordCategory.GENERAL

    return Generic(
        word_phrase=WordPair(
            en=re.search("#newword (.*?) - ", message).group(1),
            sv=re.search(" - (.*?)(?=$| ~)", message).group(1),
            grammar_id=GrammarCategory.NA,
        ),
        part_of_speech=part_of_speech,
        word_category=word_category,
    )


def add(new_words: list[str]) -> None:
    """Add all the new word messages to the database.

    Args:
        new_words: List of messages containing new words.
    """
    new_words = [parse_new_word(line) for line in new_words]
    NewWords(new_words).add()
