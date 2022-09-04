# Telegram Bot

## Setting up bot

Set up a Telegram bot [here](https://core.telegram.org/bots/api). Add API key and chat id to config.py in the game/telegram directory.

## Running jobs

I use cron to run the fetch.py and reminder.py scripts. How I set up jobs (there may be a more streamlined way):
- Run `crontab -e`
- Use `cd` to navigate to swedish-translation-game directory
- Activate virtual environment which also sets PYTHONPATH
- Run script using python executable in virtual environment
- Write the output to a log file

Things to note about cron:
- The jobs are only triggered if the computer is awake.
- I have set my computer to wake at 8pm every day, however this only happens if the computer is plugged in.

I have looked into running them on GCP but the setup involved in running them, and how they interact with the files stores locally, was too much to be worth it right now. Perhaps something to revist in the future.

### fetch.py

I run this on the hour, every hour, between 7pm and 11pm. This is to try and ensure that it is run every day as chat updates are only available for the latest 24 hours.

### reminder.py

I run this at 8pm every day.