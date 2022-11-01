"""Script to fetch updates from Telegram bot chat.

The script fetches all updates from the Telegram bot chat (updates are
only available for the past 24 hours). New notes are added to the notes
file game/new_words/notes.txt and new words are added to the database.

This script is run on the hour, every hour, between 7pm and 11pm every
day using cron and the output is written to the log file
telegram_fetch.log.

Functions:
    get_updates: Fetch updates from Telegram bot chat.
    extract_messages: Extract messages from updates.
    parse_messages: Parse messages to word object.
    get_message_ids: Read message ids csv file.
    update_message_ids: Update message ids csv file.
    main: Main function to run script.
"""
from datetime import datetime, timedelta
import os
import requests
import sys

import pandas as pd

from game.telegram.config import API_KEY
import new_notes
import new_words


def print_message(message: str = None) -> None:
    """Print the current time followed by a message.

    Args:
        message: The message to print after timestamp. Defaults to none.
    """
    print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
    if message:
        print(f"{message}\n")


def get_updates() -> requests.Response:
    """Get updates from the Telegram bot chat.

    Returns:
        A response object.
    """
    url = f"https://api.telegram.org/bot{API_KEY}/getUpdates"
    return requests.get(url)


def extract_messages(
    response: requests.Response, committed_ids: pd.Series
) -> tuple[list[str], list[dict[str, datetime | int]]]:
    """Extract text, id and date data from messages.

    Args:
        response: Response object from get_updates request.
        committed_ids: Pandas series with message ids already committed
            to notes or database.

    Returns:
        Tuple, the first element being a list of messages, the second a
        list of dictionaries containing message ids and dates.
    """
    results = response.json()["result"]
    if not response.ok:
        print_message(f"Connection failed.\n{response.reason}")
        sys.exit()
    elif not results:
        print_message("No messages in past 24 hours.")
        sys.exit()
    else:
        messages = []
        ids = []
        for result in results:
            if result["update_id"] not in list(committed_ids):
                messages.append(result["message"]["text"])
                ids.append(
                    {
                        "Date": datetime.fromtimestamp(result["message"]["date"]),
                        "Id": result["update_id"],
                    }
                )
        return messages, ids


def parse_messages(messages: str) -> dict[str, list[str]]:
    """Identify and return new notes and new words messages.

    Args:
        messages: List of messages.

    Returns:
        Dictionary containing one list of messages with new notes and
        one list of messages with new words.
    """
    return {
        "notes": [line for line in messages if line.startswith("#note")],
        "new_words": [line for line in messages if line.startswith("#newword")],
    }


def get_message_ids() -> pd.DataFrame:
    """Add message ids to csv.

    Add the message ids of the parsed messages to a csv file along with
    the timestamp. This is so that notes and new words are not added
    multiple times. Message ids which are more than 48 hours old are
    deleted as updates are only available for 24 hours.

    Returns:
        DataFrame with message ids and their date.
    """
    csv_path = "game/telegram/message_ids.csv"
    if not os.path.exists(csv_path):
        ids = pd.DataFrame(columns=["Date", "Id"])
        ids.to_csv(csv_path, index=False)
        return ids
    else:
        return pd.read_csv("game/telegram/message_ids.csv", parse_dates=["Date"])


def update_message_ids(
    ids: pd.DataFrame, new_ids: list[dict[str, datetime | int]]
) -> None:
    """Remove message ids older than 48 hours and add new ids.

    Args:
        ids: DataFrame with message ids from past 48 hours.
        new_ids: List of dictionaries containing message id and date for
            all messages not already in the DataFrame.
    """
    ids = ids[ids.Date > datetime.today() - timedelta(days=2)]
    pd.concat([ids, pd.DataFrame(new_ids)]).to_csv(
        "game/telegram/message_ids.csv", index=False
    )


def main() -> None:
    """Main function to run script."""
    message_ids = get_message_ids()
    response = get_updates()
    messages, new_ids = extract_messages(response, message_ids.Id)
    update_message_ids(message_ids, new_ids)
    data = parse_messages(messages)
    print_message()
    new_notes.add(data["notes"])
    new_words.add(data["new_words"])
    print("\n")


if __name__ == "__main__":
    main()
