import logging
from pathlib import Path

from telegram.ext import ApplicationBuilder, CommandHandler, \
    MessageHandler, filters

from configs import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def downloader(update, context):
    file = await context.bot.get_file(update.message.document)
    path = Path(file.file_path)
    if path.suffix == ".pdf":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='⏳ Please wait, your file '
                                            'is being processed')
        await file.download_to_drive('paper.pdf')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='☹️ Please send PDF file')


async def send_document(update, context):
    chat_id = update.message.chat_id
    document = open('paper.pdf', 'rb')
    await context.bot.send_document(chat_id, document)


async def start(update, context):
    welcome_text = "🥳 Welcome to NLPaper!\n" \
                   "With our bot, you can quickly and easily " \
                   "highlight the most important information in " \
                   "any research paper. Simply " \
                   "upload your paper and our bot will generate " \
                   "a pdf file with the highlighted sections for " \
                   "you to download."
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=welcome_text)


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.ALL, downloader))
    app.add_handler(CommandHandler('send', send_document))

    app.run_polling()
