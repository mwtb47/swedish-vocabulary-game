"""Module with a list of new words or phrases to add to database.

The commented out templates for each word type are copied and 
filled in for each new word. They then need to be deleted after 
the add.py script has been run.

I have experimented with a GUI and Excel as an interface for adding
new words. They both have certain advantages over this method, but
I always came back to adding words here due to the multi-cursor and
editing features of VS code making it much faster.
"""

from enums import GrammarType, WordCategory, WordType
from game.new_words.objects import Adjective, Adverb, Generic, Noun, Verb, WordPair


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
    # Noun(
    #     indefinite_singular=WordPair(sv="", da=""),
    #     indefinite_plural=  WordPair(sv="", da=""),
    #     definite_singular=  WordPair(sv="", da=""),
    #     definite_plural=    WordPair(sv="", da=""),
    # ),
    #
    # Verb(
    #     infinitive=     WordPair(sv="att ", da="at "),
    #     present=        WordPair(sv="jag ", da="jag "),
    #     past_simple=    WordPair(sv="jag ", da="jag "),
    #     past_participle=WordPair(sv="jag har ", da="jag har "),
    #     imperative=     WordPair(sv="", da="")
    # ),
    #
    # Generic(
    #     word_phrase=WordPair(
    #         sv="",
    #         da="",
    #         grammar_id=GrammarType.NA
    #     ),
    #     word_type=WordType.,
    #     word_category=WordCategory.,
    # ),
]
