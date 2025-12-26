from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Замените на ваш токен от @BotFather
TOKEN = "8031944253:AAFg4BC1BgsRVymsBFQkENDf6ynSrsed0Ws"
# Замените на вашу ссылку от Render
APP_URL = "https://balvaniy.onrender.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🚀 Открыть Gemini AI",
            web_app=WebAppInfo(url=APP_URL)
        )]
    ])
    await update.message.reply_text(
        "Привет! Нажми на кнопку ниже, чтобы запустить чат-бота Gemini прямо в Telegram.",
        reply_markup=kb
    )

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Бот запущен...")
    app.run_polling()
