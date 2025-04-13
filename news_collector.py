#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# news_collector.py

import feedparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def fetch_rss_news(feed_url):
    feed = feedparser.parse(feed_url)
    news_items = []
    for entry in feed.entries:
        news_items.append({
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary if 'summary' in entry else '',
            'published': entry.published if 'published' in entry else ''
        })
    return news_items

def fetch_digiato_news():
    # راه‌اندازی WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://digiato.com/")
    
    news_items = []
    
    # فرض می‌کنیم لینک‌های خبرها توی بخش خاصی از صفحه هستند
    headlines = driver.find_elements(By.CSS_SELECTOR, 'h2.entry-title a')
    
    for headline in headlines:
        title = headline.text
        link = headline.get_attribute('href')
        news_items.append({'title': title, 'link': link})
    
    driver.quit()
    return news_items

