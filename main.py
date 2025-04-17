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

from news_collector import fetch_rokna_news, fetch_full_article  # تغییر این خط

from summarizer import summarize_text
from config import TELEGRAM_TOKEN

load_dotenv()

news_cache = []
current_category = None

CATEGORY_URLS = {
    "اقتصادی": "اقتصادی",
    "فرهنگی": "فرهنگی"
}

# ✅ کلاس جدید برای یکپارچه‌سازی با ساختار قبلی
class NewsFetcher:
    def __init__(self, category):
        self.category = category

    def fetch_news(self):
        return fetch_rokna_news(self.category)

    @staticmethod
    def fetch_full_article(url):
        return fetch_full_article(url)

# ✅ دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! به ربات اخبار خوش اومدی 🎉\n"
        "برای دریافت اخبار جدید، دستور /news رو وارد کن."
    )

# دستور /news: انتخاب دسته‌بندی
async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧮 اقتصادی", callback_data="category_اقتصادی")],
        [InlineKeyboardButton("🎭 فرهنگی", callback_data="category_فرهنگی")]
    ]
    await update.message.reply_text(
        "دسته‌بندی مورد نظر خود را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# مرحله بعدی: گرفتن لیست خبر بعد از انتخاب دسته‌بندی
async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.split("_")[1]
    global current_category, news_cache
    current_category = category
    fetcher = NewsFetcher(category)
    news_cache = fetcher.fetch_news()

    if not news_cache:
        await query.edit_message_text("❌ خبری یافت نشد.")
        return

    keyboard = [
        [InlineKeyboardButton(news['title'][:60], callback_data=f"news_{i}")]
        for i, news in enumerate(news_cache)
    ]

    await query.edit_message_text(
        f"📚 اخبار {category}:\nیکی را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# نمایش خلاصه خبر
async def handle_summary_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    news_index = int(query.data.split("_")[1])
    news = news_cache[news_index]
    full_text = NewsFetcher.fetch_full_article(news['link'])

    if not full_text:
        await query.edit_message_text("❌ متن کامل خبر قابل دریافت نیست.")
        return

    summary = summarize_text(full_text)
    await query.edit_message_text(
        f"🗞️ {news['title']}\n"
        f"🔗 [مشاهده خبر]({news['link']})\n\n"
        f"✂️ خلاصه:\n\n{summary}",
        parse_mode='Markdown'
    )

# تابع main
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", send_news))
    application.add_handler(CallbackQueryHandler(handle_category_selection, pattern="^category_"))
    application.add_handler(CallbackQueryHandler(handle_summary_button, pattern="^news_"))

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 8443)),
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://{os.environ.get('APP_NAME')}.railway.app/{TELEGRAM_TOKEN}"
    )

if __name__ == '__main__':
    main()
