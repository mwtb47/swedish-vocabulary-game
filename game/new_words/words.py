"""Module with a list of new words or phrases to add to database.

The commented out templates for each part of speech are copied and
filled in for each new word. They then need to be deleted after the
add.py script has been run. (This can also be done by adding the
--checkout flag when running game/new_words/add.py)

I have experimented with a GUI and Excel as an interface for adding new
words. They both have certain advantages over this method, but I always
came back to adding words here due to the multi-cursor and editing
features of VS code making it much faster.
"""

from enums import GrammarCategory, PartOfSpeech, WordCategory
from game.new_words.objects import (
    Adjective,
    Conjunction,
    Adverb,
    Generic,
    Noun,
    Verb,
    WordPair,
)


words_phrases = [
    # Adjective(
    #     neutrum=     WordPair(en="", sv=""),
    #     utrum=       WordPair(en="", sv=""),
    #     plural=      WordPair(en="", sv=""),
    #     comparative= WordPair(en="", sv=""),
    #     superlative= WordPair(en="", sv="")
    # ),
    #
    # Adverb(
    #     word=WordPair(en="", sv=""),
    # ),
    #
    # Conjunction(
    #     word=WordPair(en="", sv=""),
    # ),
    #
    # Noun(
    #     indefinite_singular=WordPair(en="a ", sv="en "),
    #     indefinite_plural=  WordPair(en="", sv=""),
    #     definite_singular=  WordPair(en="the ", sv=""),
    #     definite_plural=    WordPair(en="the ", sv=""),
    # ),
    #
    # Verb(
    #     infinitive=     WordPair(en="to ", sv="att "),
    #     present_simple= WordPair(en="I ", sv="jag "),
    #     past_simple=    WordPair(en="I ", sv="jag "),
    #     present_perfect=WordPair(en="I have ", sv="jag har "),
    #     imperative=     WordPair(en="", sv="")
    # ),
    #
    # Generic(
    #     words_phrases=[
    #         WordPair(
    #             en="",
    #             sv="",
    #             grammar_id=GrammarCategory.NA
    #         ),
    #     ],
    #     part_of_speech=PartOfSpeech.,
    #     word_category=WordCategory.,
    # ),
]
