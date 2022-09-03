"""Script to send a reminder if daily answer quota not reached.

This script will send a message via a Telegram bot if fewer
than 80 answers have been recorded during the current day. This
script is run at 8pm each day using cron and the output is written
to the log file telegram_reminder.log.

Fuctions:
    send_message: Send a message via the Telegram bot.
    check_status: Check the status of the send message request.
    main: Send message if daily answer quota not reached.
"""

from datetime import datetime
import requests

from config import API_KEY, CHAT_ID
from answers import count_answers


timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def send_message(day: int, week: int) -> requests.Response:
    """Send message from bot.

    Args:
        day: The number of answers today.
        week: The number of answers in the current week.

    Returns:
        A response object.
    """
    text = f"You need to do more translations!\nDay: {day}/80\nWeek: {week}/560"
    url = f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={CHAT_ID}&text={text}"
    return requests.get(url)


def check_status(response: requests.Response) -> None:
    """Check the status of the response.

    Args:
        response: Response object.
    """
    if response.status_code == 200:
        print(f"{timestamp} - Message sent succesfully.")
    else:
        print(f"{timestamp} - Sending failed. Error {response.status_code}")


def main() -> None:
    """Main function to check answers and send reminder."""
    day_count, week_count = count_answers()
    if day_count < 80:
        response = send_message(day_count, week_count)
        check_status(response)
    else:
        print(f"{timestamp} - Target already achieved.")


if __name__ == "__main__":
    main()
