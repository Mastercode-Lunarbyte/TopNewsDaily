import requests
from bs4 import BeautifulSoup
import logging

BASE_URL = "https://www.rokna.net"

def fetch_rokna_news():
    url = f'{BASE_URL}/%D8%A8%D8%AE%D8%B4-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%DB%8C-65'

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        news_links = soup.select('div.col-sm-12.col-xs-12 > a.item')[:10]  # حداکثر 10 خبر

        news_items = []
        for link in news_links:
            href = link.get('href')
            full_url = BASE_URL + href if href else None
            title = link.select_one('p.lead[itemprop="description"]')
            if full_url and title:
                news_items.append({
                    'title': title.get_text(strip=True),
                    'link': full_url
                })

        if not news_items:
            logging.warning("هیچ خبری از سایت رکنا دریافت نشد.")
        
        return news_items

    except requests.exceptions.RequestException as e:
        logging.error(f"خطا در دریافت اخبار: {e}")
        return []

def fetch_full_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('div', class_='col-sm-12 col-xs-12 description').get_text(strip=True)
        return article

    except Exception as e:
        logging.error(f"خطا در بارگذاری متن کامل خبر: {e}")
        return "متن کامل خبر در حال حاضر در دسترس نیست."

# فقط برای تست مستقیم
if __name__ == "__main__":
    news_list = fetch_rokna_news()
    for news in news_list:
        print(f"{news['title']} - {news['link']}")
        content = fetch_full_article(news['link'])
        print("------ متن کامل ------")
        print(content[:300])
