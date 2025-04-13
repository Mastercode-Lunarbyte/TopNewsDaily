import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from news_collector import fetch_rss_news, fetch_digiato_news
from collections.abc import Sequence

from summarizer import summarize_text
from classifier import classify_topic
from config import TELEGRAM_TOKEN

load_dotenv()

def start(update, context):
    update.message.reply_text("سلام! برای مشاهده اخبار روزانه، دستور /news را وارد کنید.")

def send_news(update, context):
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

        update.message.reply_text(f"{title}\nموضوع: {topic}\n{link}", reply_markup=reply_markup)

def button_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=query.data)

def main():
    PORT = int(os.environ.get('PORT', 8443))
    APP_NAME = os.environ.get('APP_NAME')  # در Railway مقدار بده

    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("news", send_news))
    dp.add_handler(CallbackQueryHandler(button_handler))

    # Webhook setup
    webhook_url = f"https://{APP_NAME}.railway.app/{TELEGRAM_TOKEN}"
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN
    )
    updater.bot.set_webhook(webhook_url)

    updater.idle()

if __name__ == '__main__':
    main()
