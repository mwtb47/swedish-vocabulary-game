"""Module containing word type dataclasses.

Classes:
    Word: A dataclass to represent an English and Swedish version
        of a word or phrase.
    Adjective: A dataclass to represent adjectives.
    Generic: A dataclass to represent generic words or phrases.
    Noun: A dataclass to represent nouns.
    Verb: A dataclass to represent verbs.
"""

from dataclasses import dataclass


@dataclass
class Word:
    """Dataclass to represent a word or phrase.

    Attributes:
        en: Word or phrase in English
        sv: Word of phrase in Swedish
    """

    en: str
    sv: str
    grammar_id: str | None = None


@dataclass
class Adjective:
    """Dataclass to represent an adjective.

    Attributes:
        neuter: Word object containing neuter form of adjective.
            Defaults to None.
        common_gender: Word object containing common gender form
            of adjective. Defaults to None.
        comparative: Word object containing comparative form of
            adjective. Defaults to None.
        superlative: Word object containing superlative form of
            adjective. Defaults to None.
        plural: Word object containing plural form of
            adjective. Defaults to None.
        word_type: See table_summaries.txt for word types.
        word_category: See table_summaries.txt for word categories.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    # pylint: disable=too-many-instance-attributes

    common_gender: Word | None = None
    neuter: Word | None = None
    plural: Word | None = None
    comparative: Word | None = None
    superlative: Word | None = None
    word_type: int = 3
    word_category: int = 1
    context_hint: str | None = None
    wiktionary_link: str | None = None

    def __post_init__(self) -> None:
        self.assign_grammar_ids()
        self.create_word_list()

    def assign_grammar_ids(self) -> None:
        """Assign grammar ids where Word has been set."""
        if self.common_gender:
            self.common_gender.grammar_id = 5
        if self.neuter:
            self.neuter.grammar_id = 6
        if self.plural:
            self.plural.grammar_id = 7
        if self.comparative:
            self.comparative.grammar_id = 14
        if self.superlative:
            self.superlative.grammar_id = 15

    def create_word_list(self):
        """Create a list of words."""
        self.word_list = [
            self.common_gender,
            self.neuter,
            self.plural,
            self.comparative,
            self.superlative,
        ]


@dataclass
class Generic:
    """Dataclass to represent a generic word or phrase.

    Attributes:
        word_phrase: Word object containing word of phrase.
        grammar_id: See table_summaries.txt for grammar ids.
        word_type: See table_summaries.txt for word types.
        word_category: See table_summaries.txt for word categories.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    word_phrase: Word
    word_type: int
    word_category: int
    context_hint: str | None = None
    wiktionary_link: str | None = None

    def __post_init__(self) -> None:
        self.word_list = [self.word_phrase]


@dataclass
class Noun:
    """Dataclass to represent a noun.

    Attributes:
        indefinite_singular: Word object containing indefinite
            singular form of adjective. Defaults to None.
        indefinite_plural: Word object containing indefinite
            plural form of adjective. Defaults to None.
        definite_singular: Word object containing definite
            singular form of adjective. Defaults to None.
        definite_plural: Word object containing definite
            plural form of adjective. Defaults to None.
        word_type: See table_summaries.txt for word types.
            Defaults to 1.
        word_category: See table_summaries.txt for word
            categories. Defaults to 1.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    # pylint: disable=too-many-instance-attributes

    indefinite_singular: Word | None = None
    indefinite_plural: Word | None = None
    definite_singular: Word | None = None
    definite_plural: Word | None = None
    word_type: int = 1
    word_category: int = 1
    context_hint: str | None = None
    wiktionary_link: str | None = None

    def __post_init__(self) -> None:
        self.assign_grammar_ids()
        self.create_word_list()

    def assign_grammar_ids(self) -> None:
        """Assign grammar ids where Word has been set."""
        if self.indefinite_singular:
            self.indefinite_singular.grammar_id = 1
        if self.indefinite_plural:
            self.indefinite_plural.grammar_id = 3
        if self.definite_singular:
            self.definite_singular.grammar_id = 2
        if self.definite_plural:
            self.definite_plural.grammar_id = 4

    def create_word_list(self):
        """Create a list of words."""
        self.word_list = [
            self.indefinite_singular,
            self.indefinite_plural,
            self.definite_singular,
            self.definite_plural,
        ]


@dataclass
class Verb:
    """Dataclass to represent a verb.

    Attributes:
        infinitive: Word object containing verb in infinitive form.
            Defaults to None.
        present: Word object containing verb in present tense form.
            Defaults to None.
        past_simple: Word object containing verb in past simple
            tense form. Defaults to None.
        past_participle: Word object containing verb in past
            participle tense form. Defaults to None.
        imperative: Word object containing verb in imperative form.
            Defaults to None.
        word_type: See table_summaries.txt for word types.
            Defaults to 2.
        word_category: see table_summaries.txt for word
            categories. Defaults to 1.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    # pylint: disable=too-many-instance-attributes

    infinitive: Word | None = None
    present: Word | None = None
    past_simple: Word | None = None
    past_participle: Word | None = None
    imperative: Word | None = None
    word_type: int = 2
    word_category: int = 1
    context_hint: str | None = None
    wiktionary_link: str | None = None

    def __post_init__(self) -> None:
        self.assign_grammar_ids()
        self.create_word_list()

    def assign_grammar_ids(self) -> None:
        """Assign grammar ids where Word has been set."""
        if self.infinitive:
            self.infinitive.grammar_id = 9
        if self.present:
            self.present.grammar_id = 10
        if self.past_simple:
            self.past_simple.grammar_id = 11
        if self.past_participle:
            self.past_participle.grammar_id = 12
        if self.imperative:
            self.imperative.grammar_id = 13

    def create_word_list(self):
        """Create a list of words."""
        self.word_list = [
            self.infinitive,
            self.present,
            self.past_simple,
            self.past_participle,
            self.imperative,
        ]