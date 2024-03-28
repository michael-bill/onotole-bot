from telegram import (
    BotCommand,
    Update
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    CallbackContext
)
import json
import random

with open('config.json', 'r') as f:
    config = json.loads(f.read())
with open('facts.txt', 'r') as f:
    facts = f.read().strip().split('\n')

async def start_handle(update: Update, context: CallbackContext):
    await update.message.reply_text(config["start_message"])

async def send_fact(update: Update, context: CallbackContext):
    random_fact = facts[random.randint(0, len(facts) - 1)]
    await update.message.reply_text(random_fact)

async def post_init(application: Application):
    await application.bot.set_my_commands(
        [
            BotCommand('/getfact', 'Новый факт про Анатолия Вассермана'),
        ]
    )

def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(config['tg_bot_token'])
        .concurrent_updates(True)
        .post_init(post_init)
        .build()
    )
    application.add_handler(CommandHandler("start", start_handle))
    application.add_handler(CommandHandler('getfact', send_fact))
    application.run_polling()

run_bot()