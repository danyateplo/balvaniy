from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8031944253:AAFg4BC1BgsRVymsBFQkENDf6ynSrsed0Ws"
APP_URL = "https://balvaniy.onrender.com" # Проверь, что ссылка такая!

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🚀 Gemini AI Premium", web_app=WebAppInfo(url=APP_URL))
    ]])
    await update.message.reply_text("Нажми кнопку, чтобы открыть чат:", reply_markup=kb)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
