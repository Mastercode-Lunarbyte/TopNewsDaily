import os
import logging
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

# ارسال لیست اخبار برای انتخاب
async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال دریافت اخبار... لطفاً صبر کنید 📰")

    try:
        news_items = fetch_digiato_news() + fetch_tabnak_news()

        keyboard = []
        # ایجاد دکمه برای هر عنوان خبری
        for i, news in enumerate(news_items):
            title = news['title']
            link = news['link']
            keyboard.append([InlineKeyboardButton(title[:30], callback_data=f"news_{i}")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("لطفاً یک خبر را انتخاب کنید:", reply_markup=reply_markup)

    except Exception as e:
        logging.error("خطا در دریافت اخبار:", exc_info=True)
        await update.message.reply_text("متأسفم، مشکلی در دریافت اخبار به‌وجود آمده 😞")

# نمایش خلاصه وقتی کاربر دکمه را انتخاب کرد
async def handle_summary_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # دریافت شماره خبر از callback_data
    news_index = int(query.data.split("_")[1])

    # دوباره دریافت اخبار
    news_items = fetch_digiato_news() + fetch_tabnak_news()
    news = news_items[news_index]
    title = news['title']
    link = news['link']
    summary = summarize_text(title)  # برای سادگی خلاصه‌ی عنوان

    # ارسال خلاصه‌ی خبر
    await query.edit_message_text(f"🗞️ {title}\n🔗 {link}\n\n✂️ خلاصه:\n\n{summary}")

def main():
    PORT = int(os.environ.get('PORT', 8443))
    APP_NAME = os.environ.get('APP_NAME')
    WEBHOOK_URL = f"https://{APP_NAME}.railway.app/{TELEGRAM_TOKEN}"

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", send_news))
    application.add_handler(CallbackQueryHandler(handle_summary_button))  # تغییر نام به `handle_summary_button`

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == '__main__':
    main()
