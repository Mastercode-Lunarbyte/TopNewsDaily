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
        self.url = f"https://www.rokna.net/{category_url}"

    def fetch_news(self):
        response = requests.get(self.url)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("div.news-content > a")

        news_list = []
        for article in articles:
            title = article.get("title")
            link = article.get("href")
            if title and link:
                news_list.append({
                    "title": title.strip(),
                    "link": "https://www.rokna.net" + link
                })

        return news_list


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
