import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.rokna.net'
URL = f'{BASE_URL}/%D8%A8%D8%AE%D8%B4-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%DB%8C-65'

def fetch_rokna_news(limit=10):
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = []

    articles = soup.find_all('div', class_='item')

    for article in articles[:limit]:
        title_tag = article.find('p', class_='lead', itemprop='description')
        link_tag = article.find('a', itemprop='url')

        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = BASE_URL + link_tag.get('href')
            news_items.append({'title': title, 'link': link})  # ← dict استفاده از

    return news_items

def fetch_full_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # محتوای کامل خبر را از تگ مربوطه بگیر
        content_div = soup.find('div', itemprop='articleBody')
        if not content_div:
            return "محتوایی یافت نشد."

        paragraphs = content_div.find_all('p')
        full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

        return full_text

    except Exception as e:
        return "خطا در دریافت محتوای کامل خبر."

if __name__ == "__main__":
    for i, item in enumerate(fetch_rokna_news(), 1):
        print(f"{i}. {item['title']}")
        print(f"   لینک: {item['link']}")
        print("-" * 60)
