import logging
import os
from pathlib import Path

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from configs import *
from utils import highlight_ranked

TOKEN = os.getenv('TG_BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8443)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_text = '🥳 Welcome to NLPaper!\n' \
                   'With the bot, you can easily ' \
                   'find the most important information in ' \
                   'any research paper. Simply ' \
                   'upload your paper and the bot will generate ' \
                   'a pdf file with the highlighted sections!'
    await message.reply(welcome_text)


@dp.message_handler(content_types=['document'])
async def document_handler(message: types.Message):
    if document := message.document:
        file_name = Path(document.file_name)
        if file_name.suffix == '.pdf':
            await message.reply('⏳ Please wait, your file is being processed')

            if not os.path.isdir(downloaded_path):
                os.makedirs(downloaded_path)
            await document.download(
                destination_file=downloaded_path / input_file_name
            )

            sentences = highlight_ranked(
                str(downloaded_path / input_file_name),
                str(downloaded_path / output_file_name),
                limit_sentences=limit_sentences)
            sentences_text = "\n 👉 ".join([''] + sentences)
            text = f'🔥 Top {limit_sentences} most important sentences in ' \
                   f'the text:\n{sentences_text}'
            await message.reply(text)

            doc = open(downloaded_path / output_file_name, 'rb')
            await message.reply_document(doc)

        else:
            await message.reply('☹️ We can process PDF files only.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    # executor.start_polling(dp, skip_updates=True)
