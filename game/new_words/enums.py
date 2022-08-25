"""Module containing enums for word types, word categories, and grammar types."""

from enum import Enum


class WordType(Enum):
    """Enums for word types."""

    SUBSTANTIV = 1
    """Noun."""

    VERB = 2
    """Verb."""

    ADJECTIV = 3
    """Adjective."""

    ADVERB = 4
    """Adverb."""

    FRAS = 5
    """Phrase."""

    PREPOSITION = 6
    """Preposition."""


class WordCategory(Enum):
    """Enums for word categories."""

    ALLMÄN = 1
    """General."""

    MAT = 2
    """Food."""

    SPORT = 3
    """Sport."""

    AFFÄR = 4
    """Business."""

    GEOGRAFI = 5
    """Geography."""

    KROPP = 6
    """Body parts."""

    ORDFÖlJD = 7
    """Phrases focusing on word order."""

    TID = 8
    """"Time."""

    PARTIKELVERB = 9
    """Paticle verbs."""

    KLÄDER = 10
    """Clothing."""

    DATASPRÅK = 11
    """Data and technology."""

    VETENSKAP = 12
    """Scientific."""

    DJUR = 13
    """Animals."""


class GrammarType(Enum):
    """Enums for grammar types."""

    NA = 0
    """No grammar id."""

    OBESTÄMDT_SINGULART_SUBSTANTIV = 1
    """Indefinite singular noun."""

    BESTÄMT_SINGULART_SUBSTANTIV = 2
    """Definite singular noun."""

    OBESTÄMT_PLURAL_SUBSTANTIV = 3
    """Indefinite plural noun."""

    BESTÄMT_PLURAL_SUBSTANTIV = 4
    """Definite plural noun."""

    ADJEKTIV_UTRUM = 5
    """Common gender adjective."""

    ADJEKTIV_NEUTRUM = 6
    """Neuter adjective."""

    ADJEKTIV_PLURAL = 7
    """Plural adjective."""

    PREPOSITION = 8
    """Preposition."""

    INFINITIVT_VERB = 9
    """Verb in infinitive form."""

    PRESENS_VERB = 10
    """Verb in present tense."""

    PRETERITUM_VERB = 11
    """Simple past form of a verb."""

    SUPINUM_VERB = 12
    """Past perfect form of a verb."""

    IMPERATIV_VERB = 13
    """Impertive form of verb."""

    ADJEKTIV_KOMPARATIV = 14
    """Comparative adjective."""

    ADJEKTIV_SUPERLATIV = 15
    """"Superlative adjective."""