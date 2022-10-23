"""Module containing word object dataclasses.

Classes:
    WordPair: A dataclass to represent the Swedish and Danish version
        of a word or phrase.
    Word: Base class for all types of word objects.
    Adjective: A dataclass to represent adjectives.
    Adverb: A dataclass to represent adverbs.
    Generic: A dataclass to represent generic words or phrases.
    Noun: A dataclass to represent nouns.
    Verb: A dataclass to represent verbs.
"""

from dataclasses import dataclass

from game.new_words.enums import GrammarType, PartOfSpeech, WordCategory


@dataclass
class WordPair:
    """Dataclass to represent a word or phrase pair.

    Attributes:
        sv: Word or phrase in Swedish.
        da: Word of phrase in Danish.
        grammar_id: See table_summaries.txt for grammar ids.
    """

    sv: str
    da: str
    grammar_id: GrammarType = GrammarType.NA


@dataclass
class Word:
    """Base class for a word object.

    Attributes:
        word_category: See table_summaries.txt for word categories.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    word_category: WordCategory = WordCategory.ALLMÄN
    context_hint: str | None = None
    wiktionary_link: str | None = None


@dataclass
class Adjective(Word):
    """Dataclass to represent an adjective.

    Attributes:
        neuter: WordPair object containing neuter form of adjective.
            Defaults to None.
        common_gender: WordPair object containing common gender form
            of adjective. Defaults to None.
        comparative: WordPair object containing comparative form of
            adjective. Defaults to None.
        superlative: WordPair object containing superlative form of
            adjective. Defaults to None.
        plural: WordPair object containing plural form of
            adjective. Defaults to None.
        part_of_speech: See table_summaries.txt for parts of speech.
            Defaults to ADJECTIVE.
        word_category: See table_summaries.txt for word categories.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    common_gender: WordPair | None = None
    neuter: WordPair | None = None
    plural: WordPair | None = None
    comparative: WordPair | None = None
    superlative: WordPair | None = None
    part_of_speech: PartOfSpeech = PartOfSpeech.ADJECTIV

    def __post_init__(self) -> None:
        self.__assign_grammar_ids()
        self.__create_word_list()

    def __assign_grammar_ids(self) -> None:
        """Assign grammar ids where WordPair has been set."""
        if self.common_gender:
            self.common_gender.grammar_id = GrammarType.ADJEKTIV_UTRUM
        if self.neuter:
            self.neuter.grammar_id = GrammarType.ADJEKTIV_NEUTRUM
        if self.plural:
            self.plural.grammar_id = GrammarType.ADJEKTIV_PLURAL
        if self.comparative:
            self.comparative.grammar_id = GrammarType.ADJEKTIV_KOMPARATIV
        if self.superlative:
            self.superlative.grammar_id = GrammarType.ADJEKTIV_SUPERLATIV

    def __create_word_list(self) -> None:
        """Create a list of words."""
        word_pairs = [
            self.common_gender,
            self.neuter,
            self.plural,
            self.comparative,
            self.superlative,
        ]
        self.word_list = [wp for wp in word_pairs if wp is not None]


@dataclass(kw_only=True)
class Adverb(Word):
    """Dataclass to represent an adverb.

    Attributes:
        word: WordPair object containing word of phrase.
        part_of_speech: See table_summaries.txt for parts of speech.
            Defaults to ADVERB.
        word_category: See table_summaries.txt for word categories.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    word: WordPair
    part_of_speech: PartOfSpeech = PartOfSpeech.ADVERB

    def __post_init__(self) -> None:
        self.word.grammar_id = GrammarType.NA
        self.word_list = [self.word]


@dataclass(kw_only=True)
class Conjunction(Word):
    """Dataclass to represent a conjunction.

    Attributes:
        word: WordPair object containing conjunction.
        part_of_speech: See table_summaries.txt for parts of speech.
            Defaults to ADVERB.
        word_category: See table_summaries.txt for word categories.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    word: WordPair
    part_of_speech: PartOfSpeech = PartOfSpeech.KONJUNKTION

    def __post_init__(self) -> None:
        self.word.grammar_id = GrammarType.NA
        self.word_list = [self.word]


@dataclass(kw_only=True)
class Generic(Word):
    """Dataclass to represent a generic word or phrase.

    Attributes:
        word_phrase: WordPair object containing word of phrase.
        part_of_speech: See table_summaries.txt for parts of speech.
        word_category: See table_summaries.txt for word categories.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    word_phrase: WordPair
    part_of_speech: PartOfSpeech

    def __post_init__(self) -> None:
        self.word_list = [self.word_phrase]


@dataclass
class Noun(Word):
    """Dataclass to represent a noun.

    Attributes:
        indefinite_singular: WordPair object containing indefinite
            singular form of adjective. Defaults to None.
        indefinite_plural: WordPair object containing indefinite
            plural form of adjective. Defaults to None.
        definite_singular: WordPair object containing definite
            singular form of adjective. Defaults to None.
        definite_plural: WordPair object containing definite
            plural form of adjective. Defaults to None.
        part_of_speech: See table_summaries.txt for parts of
            speech. Defaults to NOUN.
        word_category: See table_summaries.txt for word
            categories. Defaults to 1.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    indefinite_singular: WordPair | None = None
    indefinite_plural: WordPair | None = None
    definite_singular: WordPair | None = None
    definite_plural: WordPair | None = None
    part_of_speech: PartOfSpeech = PartOfSpeech.SUBSTANTIV

    def __post_init__(self) -> None:
        self.__assign_grammar_ids()
        self.__create_word_list()

    def __assign_grammar_ids(self) -> None:
        """Assign grammar ids where WordPair has been set."""
        if self.indefinite_singular:
            self.indefinite_singular.grammar_id = (
                GrammarType.OBESTÄMDT_SINGULART_SUBSTANTIV
            )
        if self.indefinite_plural:
            self.indefinite_plural.grammar_id = GrammarType.OBESTÄMT_PLURAL_SUBSTANTIV
        if self.definite_singular:
            self.definite_singular.grammar_id = GrammarType.BESTÄMT_SINGULART_SUBSTANTIV
        if self.definite_plural:
            self.definite_plural.grammar_id = GrammarType.BESTÄMT_PLURAL_SUBSTANTIV

    def __create_word_list(self) -> None:
        """Create a list of words."""
        word_pairs = [
            self.indefinite_singular,
            self.indefinite_plural,
            self.definite_singular,
            self.definite_plural,
        ]
        self.word_list = [wp for wp in word_pairs if wp is not None]


@dataclass
class Verb(Word):
    """Dataclass to represent a verb.

    Attributes:
        infinitive: WordPair object containing verb in infinitive form.
            Defaults to None.
        present: WordPair object containing verb in present tense form.
            Defaults to None.
        past_simple: WordPair object containing verb in past simple
            tense form. Defaults to None.
        past_participle: WordPair object containing verb in past
            participle tense form. Defaults to None.
        imperative: WordPair object containing verb in imperative form.
            Defaults to None.
        part_of_speech: See table_summaries.txt for parts of speech.
            Defaults to VERB.
        word_category: see table_summaries.txt for word
            categories. Defaults to 1.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    infinitive: WordPair | None = None
    present: WordPair | None = None
    past_simple: WordPair | None = None
    past_participle: WordPair | None = None
    imperative: WordPair | None = None
    part_of_speech: PartOfSpeech = PartOfSpeech.VERB

    def __post_init__(self) -> None:
        self.__assign_grammar_ids()
        self.__create_word_list()

    def __assign_grammar_ids(self) -> None:
        """Assign grammar ids where WordPair has been set."""
        if self.infinitive:
            self.infinitive.grammar_id = GrammarType.INFINITIVT_VERB
        if self.present:
            self.present.grammar_id = GrammarType.PRESENS_VERB
        if self.past_simple:
            self.past_simple.grammar_id = GrammarType.PRETERITUM_VERB
        if self.past_participle:
            self.past_participle.grammar_id = GrammarType.SUPINUM_VERB
        if self.imperative:
            self.imperative.grammar_id = GrammarType.IMPERATIV_VERB

    def __create_word_list(self) -> None:
        """Create a list of words."""
        word_pairs = [
            self.infinitive,
            self.present,
            self.past_simple,
            self.past_participle,
            self.imperative,
        ]
        self.word_list = [wp for wp in word_pairs if wp is not None]
