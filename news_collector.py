import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.rokna.net'
URL = f'{BASE_URL}/%D8%A8%D8%AE%D8%B4-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%DB%8C-65'

def fetch_rokna_news():
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = []

    # هر خبر داخل div.item است
    articles = soup.find_all('div', class_='item')

    for article in articles[:10]:  # فقط 10 تای اول
        title_tag = article.find('p', class_='lead', itemprop='description')
        link_tag = article.find('a', itemprop='url')

        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = BASE_URL + link_tag.get('href')

            news_items.append((title, link))

    return news_items

# چاپ تستی
for i, (title, link) in enumerate(fetch_rokna_news(), 1):
    print(f"{i}. {title}")
    print(f"   لینک: {link}")
    print("-" * 60)
