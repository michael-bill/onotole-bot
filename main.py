from telegram import (
    BotCommand,
    Update
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters
)
import json
import random
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file_handler = RotatingFileHandler('main.log', maxBytes=20 * 1024 * 1024, backupCount=5)
log_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(log_file_handler)

with open('config.json', 'r') as f:
    config = json.loads(f.read())
with open('./data/onotole-facts.txt', 'r') as f:
    onotole_facts = f.read().strip().split('\n')
with open('./data/jason-quotes.txt', 'r') as f:
    jason_quotes = f.read().strip().split('\n')

async def start_handle(update: Update, context: CallbackContext):
    logger.info(f'@{update.message.from_user.username} : {update.message.text}')
    await update.message.reply_text(config['start_message'])

async def send_onotole_fact(update: Update, context: CallbackContext):
    logger.info(f'@{update.message.from_user.username} : {update.message.text}')
    random_fact = onotole_facts[random.randint(0, len(onotole_facts) - 1)]
    await update.message.reply_text(random_fact)

async def send_jason_quote(update: Update, context: CallbackContext):
    logger.info(f'@{update.message.from_user.username} : {update.message.text}')
    random_quote = jason_quotes[random.randint(0, len(jason_quotes) - 1)]
    await update.message.reply_text(random_quote)

async def post_init(application: Application):
    await application.bot.set_my_commands(
        [
            BotCommand('/start', 'Информация о боте'),
            BotCommand('/onotole_fact', 'Новый факт про Анатолия Вассермана'),
            BotCommand('/jason_quote', 'Цитата от Джейсона Стетхема'),
        ]
    )

async def log_message(update: Update, context: CallbackContext):
    logger.info(f'@{update.message.from_user.username} : {update.message.text}')

def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(config['tg_bot_token'])
        .concurrent_updates(True)
        .post_init(post_init)
        .build()
    )
    application.add_handler(CommandHandler('start', start_handle))
    application.add_handler(CommandHandler('onotole_fact', send_onotole_fact))
    application.add_handler(CommandHandler('jason_quote', send_jason_quote))
    application.add_handler(MessageHandler(filters.TEXT, log_message))
    application.run_polling()

run_bot()