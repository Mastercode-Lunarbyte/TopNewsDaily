import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from news_collector import fetch_rss_news, fetch_digiato_news
from summarizer import summarize_text
from classifier import classify_topic
from config import TELEGRAM_TOKEN  # حالا این همون "TELEGRAM_TOKEN_NEWSBOT" رو از .env می‌خونه

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای مشاهده اخبار روزانه، دستور /news را وارد کنید.")

async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_items = []

    news_items += fetch_rss_news("https://www.isna.ir/rss")
    news_items += fetch_rss_news("https://www.rokna.ir/rss")
    news_items += fetch_digiato_news()

    for news in news_items:
        title = news['title']
        link = news['link']
        topic = classify_topic(title)
        summary = summarize_text(news['summary'] if news['summary'] else "")

        keyboard = [[InlineKeyboardButton("نمایش خلاصه", callback_data=summary)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(f"{title}\nموضوع: {topic}\n{link}", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=query.data)

def main():
    PORT = int(os.environ.get('PORT', 8443))
    APP_NAME = os.environ.get('APP_NAME')
    WEBHOOK_URL = f"https://{APP_NAME}.railway.app/{TELEGRAM_TOKEN}"

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", send_news))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == '__main__':
    main()
