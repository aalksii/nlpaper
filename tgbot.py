import logging
import os
from pathlib import Path

from telegram.ext import ApplicationBuilder, CommandHandler, \
    MessageHandler, filters

from configs import *
from utils import highlight_ranked

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


PORT = int(os.environ.get('PORT', 5000))

async def downloader(update, context):
    file = await context.bot.get_file(update.message.document)
    path = Path(file.file_path)
    if path.suffix == '.pdf':
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='⏳ Please wait, your file '
                                            'is being processed')

        if not os.path.isdir(downloaded_path):
            os.makedirs(downloaded_path)
        await file.download_to_drive(downloaded_path / input_file_name)

        sentences = highlight_ranked(str(downloaded_path / input_file_name),
                                     str(downloaded_path / output_file_name),
                                     limit_sentences=limit_sentences)
        sentences_text = "\n 👉 ".join([''] + sentences)
        message = f'🔥 Top {limit_sentences} most important sentences in ' \
                  f'the text:\n{sentences_text}'
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=message)

        await send_document(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='☹️ Please send PDF file only')


async def send_document(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='✅ Here\'s your highlighted '
                                        'pdf file!')
    document = open(str(downloaded_path / output_file_name), 'rb')
    await context.bot.send_document(update.effective_chat.id,
                                    document)


async def start(update, context):
    welcome_text = '🥳 Welcome to NLPaper!\n' \
                   'With the bot, you can easily ' \
                   'find the most important information in ' \
                   'any research paper. Simply ' \
                   'upload your paper and the bot will generate ' \
                   'a pdf file with the highlighted sections!'
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=welcome_text)


if __name__ == '__main__':
    TOKEN = os.environ['TG_BOT_TOKEN']
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.ALL, downloader))
    app.run_webhook(listen='0.0.0.0',
                    port=PORT,
                    url_path=TOKEN,
                    webhook_url='https://nlpaper.herokuapp.com/' + TOKEN)

    # app.run_polling()
