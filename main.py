import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from news_collector import fetch_digiato_news, fetch_tabnak_news

from summarizer import summarize_text
from classifier import classify_topic
from config import TELEGRAM_TOKEN  # حالا این همون "TELEGRAM_TOKEN_NEWSBOT" رو از .env می‌خونه

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای دریافت اخبار جدید دستور /news رو بزن 😊")

async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال دریافت اخبار... لطفاً صبر کنید 📰")

    try:
        news_items = fetch_digiato_news() + fetch_tabnak_news()

        for news in news_items:
            title = news['title']
            link = news['link']
            topic = classify_topic(title)
            summary = summarize_text(title)  # برای سادگی خلاصه‌ی عنوان

            keyboard = [[InlineKeyboardButton("📌 نمایش خلاصه", callback_data=summary[:1000])]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(f"🗞️ {title}\n🔗 {link}\n📚 موضوع: {topic}", reply_markup=reply_markup)

    except Exception as e:
        logging.error("خطا در دریافت اخبار:", exc_info=True)
        await update.message.reply_text("متأسفم، مشکلی در دریافت اخبار به‌وجود آمده 😞")

async def handle_summary_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"✂️ خلاصه:\n\n{query.data}")

    

   

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
