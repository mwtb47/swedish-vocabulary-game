"""Module containing enums for word classification.

Classes:
    GrammarCategory: Grammar category enums.
    PartOfSpeech: Parts of speech enums.
    WordCategory: Word category enums.
"""

from enum import Enum


class GrammarCategory(Enum):
    """Enums for grammar categories."""

    NA = 0
    """No grammar id."""

    NOUN_INDEFINITE_SINGULAR = 1
    """Indefinite singular noun."""

    NOUN_DEFINITE_SINGULAR = 2
    """Definite singular noun."""

    NOUN_INDEFINITE_PLURAL = 3
    """Indefinite plural noun."""

    NOUN_DEFINITE_PLURAL = 4
    """Definite plural noun."""

    ADJECTIVE_UTRUM = 5
    """Utrum adjective."""

    ADJECTIVE_NEUTRUM = 6
    """Neuter adjective."""

    ADJECTIVE_PLURAL = 7
    """Plural adjective."""

    PREPOSITION = 8
    """Preposition."""

    VERB_INFINITIVE = 9
    """Infinitive verb."""

    VERB_PRESENT_SIMPLE = 10
    """Simple present verb."""

    VERB_PAST_SIMPLE = 11
    """Simple past verb."""

    VERB_PRESENT_PERFECT = 12
    """Perfect present verb."""

    VERB_IMPERATIVE = 13
    """Imperative verb."""

    ADJECTIVE_COMPARATIVE = 14
    """Comparative adjective."""

    ADJECTIVE_SUPERLATIVE = 15
    """"Superlative adjective."""


class PartOfSpeech(Enum):
    """Enums for parts of speech."""

    NOUN = 1
    """Noun."""

    VERB = 2
    """Verb."""

    ADJECTIVE = 3
    """Adjective."""

    ADVERB = 4
    """Adverb."""

    PHRASE = 5
    """Phrase."""

    PREPOSITION = 6
    """Preposition."""

    CONJUNCTION = 7
    """Conjunction."""


class WordCategory(Enum):
    """Enums for word categories."""

    GENERAL = 1
    """General."""

    FOOD = 2
    """Food."""

    SPORT = 3
    """Sport."""

    BUSINESS = 4
    """Business."""

    GEOGRAPHY = 5
    """Geography."""

    BODY = 6
    """Body parts."""

    WORD_ORDER = 7
    """Phrases focusing on word order."""

    TIME = 8
    """"Time."""

    PARTICLE_VERBS = 9
    """Particle verbs."""

    CLOTHES = 10
    """Clothing."""

    COMPUTERS = 11
    """Data and technology."""

    SCIENCE = 12
    """Scientific."""

    ANIMALS = 13
    """Animals."""
