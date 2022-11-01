"""Module containing word object dataclasses.

Classes:
    WordPair: A dataclass to represent the English and Swedish version
        of a word or phrase.
    Word: Base class for all types of word objects.
    Adjective: A dataclass to represent adjectives.
    Adverb: A dataclass to represent adverbs.
    Generic: A dataclass to represent generic words or phrases.
    Noun: A dataclass to represent nouns.
    Verb: A dataclass to represent verbs.
"""

from abc import abstractproperty
from dataclasses import dataclass

from game.new_words.enums import GrammarCategory, PartOfSpeech, WordCategory


@dataclass
class WordPair:
    """Dataclass to represent a word or phrase pair.

    Attributes:
        en: Word or phrase in English.
        sv: Word of phrase in Swedish.
        grammar_id: See table_summaries.txt for grammar ids.
    """

    en: str
    sv: str
    grammar_id: GrammarCategory = GrammarCategory.NA


@dataclass(kw_only=True)
class Word:
    """Base class for a word object.

    Attributes:
        word_category: See table_summaries.txt for word categories.
        context_hint: Hint to be displayed under the question.
            Defaults to None.
        wiktionary_link: Link to wiktionary page. Defaults to
            None.
    """

    part_of_speech: PartOfSpeech
    word_category: WordCategory = WordCategory.GENERAL
    context_hint: str | None = None
    wiktionary_link: str | None = None

    @abstractproperty
    def word_list(self) -> list[WordPair]:
        pass


@dataclass
class Adjective(Word):
    """Dataclass to represent an adjective.

    Attributes:
        neutrum: WordPair object containing neutrum form of adjective.
            Defaults to None.
        utrum: WordPair object containing utrum form of adjective.
            Defaults to None.
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

    utrum: WordPair | None = None
    neutrum: WordPair | None = None
    plural: WordPair | None = None
    comparative: WordPair | None = None
    superlative: WordPair | None = None
    part_of_speech: PartOfSpeech = PartOfSpeech.ADJECTIVE

    def __post_init__(self) -> None:
        self.__assign_grammar_ids()

    def __assign_grammar_ids(self) -> None:
        """Assign grammar ids where WordPair has been set."""
        if self.utrum:
            self.utrum.grammar_id = GrammarCategory.ADJECTIVE_UTRUM
        if self.neutrum:
            self.neutrum.grammar_id = GrammarCategory.ADJECTIVE_NEUTRUM
        if self.plural:
            self.plural.grammar_id = GrammarCategory.ADJECTIVE_PLURAL
        if self.comparative:
            self.comparative.grammar_id = GrammarCategory.ADJECTIVE_COMPARATIVE
        if self.superlative:
            self.superlative.grammar_id = GrammarCategory.ADJECTIVE_SUPERLATIVE

    @property
    def word_list(self) -> list[WordPair]:
        """List of word pairs for specified grammatical categories."""
        word_pairs = [
            self.utrum,
            self.neutrum,
            self.plural,
            self.comparative,
            self.superlative,
        ]
        return [wp for wp in word_pairs if wp is not None]


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
        self.word.grammar_id = GrammarCategory.NA

    @property
    def word_list(self) -> list[WordPair]:
        """List containing the adverb word pair."""
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
    part_of_speech: PartOfSpeech = PartOfSpeech.CONJUNCTION

    def __post_init__(self) -> None:
        self.word.grammar_id = GrammarCategory.NA

    @property
    def word_list(self) -> list[WordPair]:
        """List containing the conjunction word pair."""
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

    @property
    def word_list(self) -> list[WordPair]:
        """List containing the generic word or phrase pair."""
        self.word_list = [self.word]


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
    part_of_speech: PartOfSpeech = PartOfSpeech.NOUN

    def __post_init__(self) -> None:
        self.__assign_grammar_ids()

    def __assign_grammar_ids(self) -> None:
        """Assign grammar ids where WordPair has been set."""
        if self.indefinite_singular:
            self.indefinite_singular.grammar_id = (
                GrammarCategory.NOUN_INDEFINITE_SINGULAR
            )
        if self.indefinite_plural:
            self.indefinite_plural.grammar_id = GrammarCategory.NOUN_INDEFINITE_PLURAL
        if self.definite_singular:
            self.definite_singular.grammar_id = GrammarCategory.NOUN_DEFINITE_SINGULAR
        if self.definite_plural:
            self.definite_plural.grammar_id = GrammarCategory.NOUN_DEFINITE_PLURAL

    @property
    def word_list(self) -> list[WordPair]:
        """List of word pairs for specified noun inflections."""
        word_pairs = [
            self.indefinite_singular,
            self.indefinite_plural,
            self.definite_singular,
            self.definite_plural,
        ]
        return [wp for wp in word_pairs if wp is not None]


@dataclass
class Verb(Word):
    """Dataclass to represent a verb.

    Attributes:
        infinitive: WordPair object containing verb in infinitive form.
            Defaults to None.
        present_simple: WordPair object containing verb in present tense
            form. Defaults to None.
        past_simple: WordPair object containing verb in past simple
            tense form. Defaults to None.
        present_perfect: WordPair object containing verb in present
            perfect tense form. Defaults to None.
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
    present_simple: WordPair | None = None
    past_simple: WordPair | None = None
    present_perfect: WordPair | None = None
    imperative: WordPair | None = None
    part_of_speech: PartOfSpeech = PartOfSpeech.VERB

    def __post_init__(self) -> None:
        self.__assign_grammar_ids()

    def __assign_grammar_ids(self) -> None:
        """Assign grammar ids where WordPair has been set."""
        if self.infinitive:
            self.infinitive.grammar_id = GrammarCategory.VERB_INFINITIVE
        if self.present_simple:
            self.present_simple.grammar_id = GrammarCategory.VERB_PRESENT_SIMPLE
        if self.past_simple:
            self.past_simple.grammar_id = GrammarCategory.VERB_PAST_SIMPLE
        if self.present_perfect:
            self.present_perfect.grammar_id = GrammarCategory.VERB_PRESENT_PERFECT
        if self.imperative:
            self.imperative.grammar_id = GrammarCategory.VERB_IMPERATIVE

    @property
    def word_list(self) -> list[WordPair]:
        """List of word pairs for specified verb inflections."""
        word_pairs = [
            self.infinitive,
            self.present_simple,
            self.past_simple,
            self.present_perfect,
            self.imperative,
        ]
        return [wp for wp in word_pairs if wp is not None]
