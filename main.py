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
from news_collector import fetch_rokna_news, fetch_full_article
from summarizer import summarize_text
from config import TELEGRAM_TOKEN

load_dotenv()

news_cache = []  # کش برای ذخیره اخبار

# شروع دستور
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای دریافت اخبار جدید دستور /news رو بزن 😊")

# دریافت اخبار و ارسال به کاربر
async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال دریافت اخبار... لطفاً صبر کنید 📰")

    try:
        global news_cache
        news_cache = fetch_rokna_news()  # دریافت اخبار جدید

        if not news_cache:
            await update.message.reply_text("متأسفانه، خبری یافت نشد.")
            return

        keyboard = []
        for i, news in enumerate(news_cache):
            title = news['title']
            keyboard.append([InlineKeyboardButton(title[:30], callback_data=f"news_{i}")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("لطفاً یک خبر را انتخاب کنید:", reply_markup=reply_markup)

    except Exception as e:
        logging.error("خطا در دریافت اخبار:", exc_info=True)
        await update.message.reply_text("متأسفم، مشکلی در دریافت اخبار به‌وجود آمده 😞")

# ارسال خلاصه خبر پس از انتخاب توسط کاربر
async def handle_summary_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    news_index = int(query.data.split("_")[1])
    news = news_cache[news_index]
    title = news['title']
    link = news['link']
    full_text = fetch_full_article(link)  # دریافت متن کامل خبر
    summary = summarize_text(full_text)  # خلاصه کردن متن

    await query.edit_message_text(
        f"🗞️ {title}\n"
        f"🔗 [مشاهده خبر]({link})\n\n"
        f"✂️ خلاصه:\n{item['summary']}\n",
        parse_mode='Markdown'
    )

# اجرای اصلی بات تلگرام
def main():
    PORT = int(os.environ.get('PORT', 8443))
    APP_NAME = os.environ.get('APP_NAME')
    WEBHOOK_URL = f"https://{APP_NAME}.railway.app/{TELEGRAM_TOKEN}"

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", send_news))
    application.add_handler(CallbackQueryHandler(handle_summary_button))

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == '__main__':
    main()
