#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# main.py
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from news_collector import fetch_rss_news, fetch_digiato_news
from summarizer import summarize_text
from classifier import classify_topic
from config import TELEGRAM_TOKEN
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_NEWSBOT')


def start(update, context):
    update.message.reply_text("سلام! برای مشاهده اخبار روزانه، دستور /news را وارد کنید.")

def send_news(update, context):
    # اخبار از سایت‌ها
    news_items = []
    
    # اخبار ایسنا و رکنا
    news_items += fetch_rss_news("https://www.isna.ir/rss")
    news_items += fetch_rss_news("https://www.rokna.ir/rss")
    
    # اخبار دیجیاتو
    news_items += fetch_digiato_news()
    
    # ارسال اخبار به کاربر
    for news in news_items:
        title = news['title']
        link = news['link']
        topic = classify_topic(title)
        
        # خلاصه خبر
        summary = summarize_text(news['summary'] if news['summary'] else "")
        
        # دکمه‌های تلگرام
        keyboard = [[InlineKeyboardButton("نمایش خلاصه", callback_data=summary)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # ارسال خبر به کاربر
        update.message.reply_text(f"{title}\nموضوع: {topic}\n{link}", reply_markup=reply_markup)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("news", send_news))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

