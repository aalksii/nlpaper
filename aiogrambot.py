import io
import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

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


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


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
    file_in_io = io.BytesIO()
    if message.content_type == 'document':
        await message.document.download(destination_file=file_in_io)
    print(file_in_io)
    

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
