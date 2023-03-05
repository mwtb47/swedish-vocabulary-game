"""Module with classes containing ids for dashboard components.

Classes:
    AnswersIds: Component ids for answers page.
    DatabaseIds: Component ids for database page.
    PerformanceIds: Component ids for performance page.
"""


class AnswerIds:
    """Component ids for Answers Summary page.

    Attributes:
        ANSWER_COUNT_TODAY: Bullet chart with today's answer count.
        ANSWER_COUNT_WEEKLY: Bullet chart with weekly answer count.
        ANSWERS_OVER_TIME: Line chart showing answer count over time.
        TIME_PERIOD_INPUT: Time period selector for ANSWERS_OVER_TIME.
        ANSWERS_OVER_TIME_TITLE: Chart title for ANSWERS_OVER_TIME.
        ENGLISH_TO_SWEDISH: Bullet chart showing Eng/Swe answer ratio.
    """

    ANSWER_COUNT_TODAY = "answer-count-today"
    ANSWER_COUNT_WEEKLY = "answer-count-weekly"
    ANSWERS_OVER_TIME = "answers-over-time"
    TIME_PERIOD_INPUT = "time-period-input"
    ANSWERS_OVER_TIME_TITLE = "answers-over-time-title"
    ENGLISH_TO_SWEDISH = "english-to-swedish"


class DatabaseIds:
    """Component ids for Database Summary page.

    Attributes:
        GRAMMAR_CATEGORY_BAR_CHART: Bar chart for grammar categories.
        GRAMMAR_CATEGORY_BAR_CHART_TITLE: Grammar categories title.
        ID_GROUP_SELECTOR: WordID or WordGroup selector for bar charts.
        PART_OF_SPEECH_BAR_CHART: Bar chart for parts of speech.
        PART_OF_SPEECH_BAR_CHART_TITLE: Parts of speech title.
        WORD_CATEGORY_BAR_CHART: Bar chart for word categories.
        WORD_CATEGORY_BAR_CHART_TITLE: Word categories title.
    """

    GRAMMAR_CATEGORY_BAR_CHART = "grammar-category-bar-chart"
    GRAMMAR_CATEGORY_BAR_CHART_TITLE = "grammar-category-bar-chart-title"
    ID_GROUP_SELECTOR = "id-word-selector"
    PART_OF_SPEECH_BAR_CHART = "part-of-speech-bar-chart"
    PART_OF_SPEECH_BAR_CHART_TITLE = "part-of-speech-bar-chart-title"
    WORD_CATEGORY_BAR_CHART = "word-category-bar-chart"
    WORD_CATEGORY_BAR_CHART_TITLE = "word-category-bar-chart-title"


class PerformanceIds:
    """Component ids for Performance Summary page.

    Attributes:
        CUMULATIVE_AVERAGE: Cumulative average line chart.
    """

    CUMULATIVE_AVERAGE = "cumulative-average"
