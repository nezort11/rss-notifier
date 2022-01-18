import json
import logging
from json import JSONDecodeError
from threading import Thread
from time import sleep

import sentry_sdk
import toml
from telegram import Update
from telegram.bot import Bot
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, Updater
from telegram.parsemode import ParseMode

from feed import poll_feed
from job import JobEntry

config = toml.load("config.toml")

sentry_sdk.init(config["sentry"]["key"], traces_sample_rate=1.0)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = config["bot"]["token"]


def get_subscribers():
    """
    Return bot subscribers.
    File may not exists (should be created empty) and file may be empty (JSON-invalid).
    """
    try:
        with open("subscribers.json", "r") as f:
            try:
                subscribers = json.load(f)
            except JSONDecodeError:
                subscribers = []
    except FileNotFoundError:
        subscribers = []

    return subscribers


def start(update: Update, context: CallbackContext):
    subscribers = get_subscribers()

    if update.effective_chat.id not in subscribers:
        with open("subscribers.json", "w") as f:
            subscribers.append(update.effective_chat.id)
            json.dump(subscribers, f)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=r"Hello, **World**\!",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


start_handler = CommandHandler("start", start)


def start_feed_polling():
    """
    Launch a thread for polling feed with config interval.
    On update integrate with telegram bot thread.
    Broadcast updates to all bot subscribers.
    """
    while True:
        subscribers = get_subscribers()
        # Broadcast notification to bot subscribers
        for update in poll_feed():
            job = JobEntry(update)
            logging.INFO(f"New job - {job.title}")

            for subscriber in subscribers:
                bot.send_message(subscriber, str(job))

        interval = config["notifier"]["interval"]
        sleep(interval)


if __name__ == "__main__":
    updater = Updater(BOT_TOKEN)
    dispatcher: Dispatcher = updater.dispatcher
    bot: Bot = updater.bot
    dispatcher.add_handler(start_handler)

    # Launch bot update poller + feed update poller (in separe threads)
    updater.start_polling()
    feed_poller = Thread(target=start_feed_polling)
    feed_poller.start()

    logging.debug("Updater and poller don't block main thread.")

    feed_poller.join()
