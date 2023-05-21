import logging
import os
from pathlib import Path

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

from configs.tgbot_config import (downloaded_path,
                                  input_file_name,
                                  output_file_name,
                                  limit_sentences,
                                  use_webhooks)
# from predict import fill_mask
from utils import highlight

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


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = '🥳 Welcome to NLPaper!\n' \
           'With the bot, you can easily ' \
           'find the most important information in ' \
           'any research paper (in English). Simply ' \
           'upload your paper and the bot will generate ' \
           'a pdf file with the highlighted sections!\n' \
           'Max file size is 3 MB. \n' \
           '❓ If you need help, just write the command /help.'
    await message.reply(text)


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    text = 'Q: How does it work?\n' \
           'A: The bot extracts the text from the pdf file, then it ' \
           'splits the text on sentences, which can be ranked after. ' \
           'Top n sentences are the most important, so the bot finds ' \
           'these strings in the pdf file and highlights it.'
    await message.reply(text)


@dp.message_handler(content_types=['document'])
async def document_handler(message: types.Message):
    if document := message.document:
        file_name = Path(document.file_name)
        if file_name.suffix == '.pdf':
            await message.reply('⏳ Please wait, your file is being processed.')

            user_id = message.from_user.id
            input_path = str(downloaded_path / (str(user_id) + '_'
                                                + str(input_file_name)))
            output_path = str(downloaded_path / (str(user_id) + '_'
                                                 + str(output_file_name)))

            if not os.path.isdir(downloaded_path):
                os.makedirs(downloaded_path)
            await document.download(
                destination_file=input_path
            )

            sentences = highlight(input_path,
                                  output_path,
                                  limit_sentences=limit_sentences)
            sentences_text = '\n 👉 '.join([''] + sentences)
            text = f'🔥 Top {limit_sentences} most important sentences in ' \
                   f'the text:\n{sentences_text}'
            await message.reply(text)

            doc = open(output_path, 'rb')
            await message.reply_document(doc)

            # delete this file:
            if os.path.exists(output_path):
                os.remove(output_path)

        else:
            await message.reply('☹️ We can process PDF files only.')


# @dp.message_handler()
# async def message_handler(message: types.Message):
#     # Send POST request to the server with a text user wants to summarize
#
#     await message.reply(fill_mask(message.text))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    if use_webhooks:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(dp, skip_updates=True)
