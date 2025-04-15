#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# news_collector.py

# news_collector.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def fetch_digiato_news():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://digiato.com/")

    news_items = []
    headlines = driver.find_elements(By.CSS_SELECTOR, 'h2.entry-title a')

    for headline in headlines[:10]:
        title = headline.text
        link = headline.get_attribute('href')
        news_items.append({'title': title, 'link': link, 'summary': '', 'published': ''})

    driver.quit()
    return news_items

def fetch_tabnak_news():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.tabnak.ir/")

    news_items = []
    headlines = driver.find_elements(By.CSS_SELECTOR, '.title a')

    for headline in headlines[:10]:
        title = headline.text
        link = headline.get_attribute('href')
        news_items.append({'title': title, 'link': link, 'summary': '', 'published': ''})

    driver.quit()
    return news_items
