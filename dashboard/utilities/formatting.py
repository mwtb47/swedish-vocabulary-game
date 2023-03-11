"""Module with functions to format text.

Functions:
    split_title: Split text to show whitespace between words.
    format_enums:
    format_percentage:
"""

import re


def split_title(title: str) -> str:
    """Introduce whitespaces to strings with concatenated words.

    E.g. the string 'GraphTitle' would be converted to 'Graph Title'.

    Args:
        title: String to format.

    Returns:
        String split into individual words.
    """
    return " ".join(re.findall("[A-Z][a-z]*", title)).replace("I D", "ID")


def format_enums(enum: str) -> str:
    """Format enum value to be displayed in graph.

    '_'s are replaced by spaces and then the string formatted using
    Pascal case. The enum 'NA' is not formatted.

    Args:
        enum: Enum's string value.

    Returns:
        The formatted enum string value.
    """
    if enum == "NA":
        return enum
    return enum.replace("_", " ").capitalize()


def format_percentage(value: float) -> str:
    """Convert a decimal value to a percentage string.

    Converts a decimal value, e.g. 0.38, to a string representing
    it as a percentage, e.g. 38%.

    Args:
        value: The decimal value to convert to a percentage.

    Returns:
        The value as a percentage string.
    """
    return f"{value * 100:.1f}%"
