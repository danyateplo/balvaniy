from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8031944253:AAFg4BC1BgsRVymsBFQkENDf6ynSrsed0Ws"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "💬 Открыть чат с ИИ",
            web_app=WebAppInfo(url="https://balvaniy.onrender.com")
        )]
    ])
    await update.message.reply_text("Запусти Mini App:", reply_markup=kb)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()

