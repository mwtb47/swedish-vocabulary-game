"""Module with a list of new words or phrases to add to database.

The commented out templates for each part of speech are copied and 
filled in for each new word. They then need to be deleted after 
the add.py script has been run. (This can also be done by adding
the --checkout flag when running game/new_words/add.py)

I have experimented with a GUI and Excel as an interface for adding
new words. They both have certain advantages over this method, but
I always came back to adding words here due to the multi-cursor and
editing features of VS code making it much faster.
"""

from enums import GrammarType, PartOfSpeech, WordCategory
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
    #     neuter=       WordPair(sv="", da=""),
    #     common_gender=WordPair(sv="", da=""),
    #     plural=       WordPair(sv="", da=""),
    #     comparative=  WordPair(sv="", da=""),
    #     superlative=  WordPair(sv="", da="")
    # ),
    #
    # Adverb(
    #     word=WordPair(sv="", da=""),
    # ),
    #
    # Conjunction(
    #     word=WordPair(en="", sv=""),
    # ),
    #
    # Noun(
    #     indefinite_singular=WordPair(sv="", da=""),
    #     indefinite_plural=  WordPair(sv="", da=""),
    #     definite_singular=  WordPair(sv="", da=""),
    #     definite_plural=    WordPair(sv="", da=""),
    # ),
    #
    # Verb(
    #     infinitive=     WordPair(sv="att ", da="at "),
    #     present=        WordPair(sv="jag ", da="jeg "),
    #     past_simple=    WordPair(sv="jag ", da="jeg "),
    #     past_participle=WordPair(sv="jag har ", da="jeg har "),
    #     imperative=     WordPair(sv="", da="")
    # ),
    #
    # Generic(
    #     word_phrase=WordPair(
    #         sv="",
    #         da="",
    #         grammar_id=GrammarType.NA
    #     ),
    #     part_of_speech=PartOfSpeech.,
    #     word_category=WordCategory.,
    # ),
]
