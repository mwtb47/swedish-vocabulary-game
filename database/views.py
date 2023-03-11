"""Module with database views and 'stored procedures'."""


answers = """
    SELECT
        W.WordID,
        W.PartOfSpeechID,
        W.English,
        W.Swedish,
        W.WordGroup,
        P.PartOfSpeech,
        C.WordCategory,
        A.Mark,
        A.TranslationDirectionID,
        A.Timestamp,
        G.GrammarCategory,
        H.Hint,
        L.WiktionaryLink,
        D.TranslationDirection
    FROM
        Answer A
    JOIN Word W
        ON W.WordID = A.WordID
    JOIN PartOfSpeech P
        ON W.PartOfSpeechID = P.PartOfSpeechID
    JOIN WordCategory C
        ON W.WordCategoryID = C.WordCategoryID
    JOIN GrammarCategory G
        ON W.GrammarCategoryID = G.GrammarCategoryID
    LEFT JOIN Hint H
        ON W.WordGroup = H.WordGroup
    LEFT JOIN Link L
        ON W.WordGroup = L.WiktionaryLink
    LEFT JOIN TranslationDirection D
        ON A.TranslationDirectionID == D.TranslationDirectionID
"""


checkboxes = """
    SELECT
        W.WordID,
        P.PartOfSpeech,
        C.WordCategory
    FROM
        Word W
    JOIN PartOfSpeech P
        ON W.PartOfSpeechID = P.PartOfSpeechID
    JOIN WordCategory C
        ON W.WordCategoryID = C.WordCategoryID
"""


game_words = """
    SELECT
        W.WordID,
        W.PartOfSpeechID,
        W.English,
        W.Swedish,
        W.WordGroup,
        A.Mark,
        A.Timestamp,
        G.GrammarCategory,
        H.Hint,
        L.WiktionaryLink
    FROM
        Word W
    LEFT OUTER JOIN Answer A
        ON W.WordID = A.WordID
    JOIN PartOfSpeech P
        ON W.PartOfSpeechID = P.PartOfSpeechID
    JOIN WordCategory C
        ON W.WordCategoryID = C.WordCategoryID
    JOIN GrammarCategory G
        ON W.GrammarCategoryID = G.GrammarCategoryID
    LEFT JOIN Hint H
        ON W.WordGroup = H.WordGroup
    LEFT JOIN Link L
        ON W.WordGroup = L.WiktionaryLink
    WHERE
        P.PartOfSpeech IN ({parts_of_speech})
        AND C.WordCategory IN ({word_categories})
"""


words_info = """
    SELECT
        W.WordID,
        W.PartOfSpeechID,
        W.English,
        W.Swedish,
        W.WordGroup,
        C.WordCategory,
        P.PartOfSpeech,
        G.GrammarCategory,
        H.Hint,
        L.WiktionaryLink
    FROM
        Word W
    JOIN PartOfSpeech P
        ON W.PartOfSpeechID = P.PartOfSpeechID
    JOIN WordCategory C
        ON W.WordCategoryID = C.WordCategoryID
    JOIN GrammarCategory G
        ON W.GrammarCategoryID = G.GrammarCategoryID
    LEFT JOIN Hint H
        ON W.WordGroup = H.WordGroup
    LEFT JOIN Link L
        ON W.WordGroup = L.WiktionaryLink
"""
