"""Script to add new words to database.

Functions:
    main: Add words in words_phrases to vocabulary database.
"""

from objects import Adjective, Generic, Noun, Verb, Word
from sql import Database


words_phrases = [
    # Verb(
    #     infinitive=     Word(en="to ", sv="att "),
    #     present=        Word(en="I ", sv="jag "),
    #     past_simple=    Word(en="I ", sv="jag "),
    #     past_participle=Word(en="I have ", sv="jag har "),
    #     imperative=     Word(en="", sv="")
    # ),

    # Adjective(
    #     neuter=       Word(en="", sv=""),
    #     common_gender=Word(en="", sv=""),
    #     plural=       Word(en="", sv=""),
    #     comparative=  Word(en="", sv=""),
    #     superlative=  Word(en="", sv="")
    # ),

    # Noun(
    #     indefinite_singular=Word(en="a ", sv="en "),
    #     indefinite_plural=  Word(en="", sv=""),
    #     definite_singular=  Word(en="the ", sv=""),
    #     definite_plural=    Word(en="the ", sv=""),
    #     word_category=      1
    # ),

    # Generic(
    #    word_phrase=  Word(en="", sv="", grammar_id=0),
    #    grammar_id=   None,
    #    word_type=    None,
    #    word_category=None
    # ),

]


def main():
    """Main function to add words to database."""
    for word_phrase in words_phrases:
        Database(word_phrase).add_new_word()


if __name__ == "__main__":
    main()
