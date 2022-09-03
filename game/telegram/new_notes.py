"""Module with functions to add notes from Telegram bot.

A new note can be added to game/new_words/notes.txt by sending a message in
the following format:

    #note text to add as note

Functions:
    read: Read the game/new_words/notes.txt file as a string.
    add_notes: Add notes to the string.
    write: Write the string back to game/new_words/notes.txt.
"""


def read() -> str:
    """Read and return the notes files as a string.

    Returns:
        Notes file as a string.
    """
    with open("game/new_words/notes.txt", "r", encoding="utf-8") as file_handle:
        return file_handle.read()


def write(note_file: str) -> None:
    """Write string back to the notes file.

    Args:
        note_file: String to write to txt file.
    """
    with open("game/new_words/notes.txt", "w", encoding="utf-8") as file_handle:
        file_handle.write(note_file)


def add(new_notes: list[str]) -> None:
    """Add the new notes to the text file string.

    Args:
        new_notes: List of messages containing new notes.
    """
    note_file = read()
    note_file += "\n".join([f"- {s.replace('#note ', '')}" for s in new_notes]) + "\n"
    write(note_file)
    print(f"Number of new notes added: {len(new_notes)}")