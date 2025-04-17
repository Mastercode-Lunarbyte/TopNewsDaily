import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.imna.ir'
CATEGORIES = {
    'اقتصادی': 'اقتصادی',
    'اجتماعی': 'اجتماعی',
    'سیاسی': 'سیاسی',
    'علمی': 'علمی-و-آموزشی',
    'فرهنگی': 'فرهنگی',
}

class NewsFetcher:
    def __init__(self, category_url):
        self.category_url = f'{BASE_URL}/{category_url}'

    def fetch_news(self, limit=10):
        try:
            response = requests.get(self.category_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = []

            # حالت ۱: ساختار کلاسیک (مانند اقتصادی)
            articles = soup.select('li.ostani-parted')
            if not articles:
                # حالت ۲: ساختار جدید (مانند فرهنگی)
                container = soup.find('div', class_='l-landing-list')
                if container:
                    articles = container.find_all('div', recursive=False)

            for article in articles[:limit]:
                title_tag = article.find('h3', class_='title')
                link_tag = title_tag.find('a', href=True) if title_tag else None
                description_tag = article.find('p', class_='lead')

                if title_tag and link_tag:
                    title = title_tag.get_text(strip=True)
                    link = BASE_URL + link_tag['href']
                    description = description_tag.get_text(strip=True) if description_tag else ""
                    news_items.append({
                        'title': title,
                        'description': description,
                        'link': link
                    })

            return news_items

        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در دریافت اطلاعات: {e}")
            return []

if __name__ == "__main__":
    for name, path in CATEGORIES.items():
        print(f"\n🗂 دسته‌بندی: {name}")
        fetcher = NewsFetcher(path)
        news_list = fetcher.fetch_news(limit=5)
        for news in news_list:
            print(f"📰 {news['title']}")
            print(f"🔗 {news['link']}")
            if news['description']:
                print(f"📄 {news['description']}")
            print('---')
