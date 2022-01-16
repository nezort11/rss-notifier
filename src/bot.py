import logging

import toml
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, Updater
from telegram.parsemode import ParseMode

config = toml.load("config.toml")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = config["bot"]["token"]
updater = Updater(BOT_TOKEN)
dispatcher: Dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=r"Hello, **World**\!",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

if __name__ == "__main__":
    updater.start_polling()
