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
        M.Mark,
        M.TranslationDirectionID,
        M.Timestamp,
        G.GrammarCategory,
        H.Hint,
        L.WiktionaryLink,
        D.TranslationDirection
    FROM
        Marks M
    JOIN Words W
        ON W.WordID = M.WordID
    JOIN PartsOfSpeech P
        ON W.PartOfSpeechID = P.PartOfSpeechID
    JOIN WordCategories C
        ON W.WordCategoryID = C.WordCategoryID
    JOIN GrammarCategories G
        ON W.GrammarCategoryID = G.GrammarCategoryID
    LEFT JOIN Hints H
        ON W.WordGroup = H.WordGroup
    LEFT JOIN Links L
        ON W.WordGroup = L.WiktionaryLink
    LEFT JOIN TranslationDirections D
        ON M.TranslationDirectionID == D.TranslationDirectionID
"""


checkboxes = """
    SELECT
        W.WordID,
        P.PartOfSpeech,
        C.WordCategory
    FROM
        Words W
    JOIN PartsOfSpeech P
        ON W.PartOfSpeechID = P.PartOfSpeechID
    JOIN WordCategories C
        ON W.WordCategoryID = C.WordCategoryID
"""


game_words = """
    SELECT
        W.WordID,
        W.PartOfSpeechID,
        W.English,
        W.Swedish,
        W.WordGroup,
        M.Mark,
        M.Timestamp,
        G.GrammarCategory,
        H.Hint,
        L.WiktionaryLink
    FROM
        Words W
    LEFT OUTER JOIN Marks M
        ON W.WordID = M.WordID
    JOIN PartsOfSpeech P
        ON W.PartOfSpeechID = P.PartOfSpeechID
    JOIN WordCategories C
        ON W.WordCategoryID = C.WordCategoryID
    JOIN GrammarCategories G
        ON W.GrammarCategoryID = G.GrammarCategoryID
    LEFT JOIN Hints H
        ON W.WordGroup = H.WordGroup
    LEFT JOIN Links L
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
        Words W
    JOIN PartsOfSpeech P
        ON W.PartOfSpeechID = P.PartOfSpeechID
    JOIN WordCategories C
        ON W.WordCategoryID = C.WordCategoryID
    JOIN GrammarCategories G
        ON W.GrammarCategoryID = G.GrammarCategoryID
    LEFT JOIN Hints H
        ON W.WordGroup = H.WordGroup
    LEFT JOIN Links L
        ON W.WordGroup = L.WiktionaryLink
"""
