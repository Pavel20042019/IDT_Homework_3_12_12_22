from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    'Starts dialogue'
    await update.message.reply_text('Ок.')


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    'Answers a message'
    a, b = update.message.text.split()
    await update.message.reply_text(int(a)+int(b))

with open('token.txt') as f:
    token = str(*f)
application = Application.builder().token(token).build()
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(
    filters.TEXT & ~ filters.COMMAND, answer))
application.run_polling()
