import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.rokna.net'

class NewsFetcher:
    def __init__(self, category_url):
        self.url = f"{BASE_URL}/{category_url}"

    def fetch_news(self):
        try:
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
                        "link": BASE_URL + link
                    })

            return news_list
        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در دریافت اطلاعات: {e}")
            return []

    @staticmethod
    def fetch_full_article(url):
        try:
            response = requests.get(url)
            response.encoding = 'utf-8'
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.select("div.body > p")
            full_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            return full_text or None
        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در دریافت مقاله کامل: {e}")
            return None
