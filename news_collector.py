import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.rokna.net'


class NewsFetcher:
    def __init__(self, category_url):
        self.category_url = f'{BASE_URL}/{category_url}'

    def fetch_news(self, limit=10):
        try:
            response = requests.get(self.category_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = []

            articles = soup.select('li.ostani-parted')

            for article in articles[:limit]:
                title_tag = article.find('h3', class_='title')
                description_tag = article.find('p', class_='lead', itemprop='description')
                link_tag = article.find('a', href=True)

                if title_tag and description_tag and link_tag:
                    title = title_tag.get_text(strip=True)
                    description = description_tag.get_text(strip=True)
                    link = BASE_URL + link_tag['href']
                    news_items.append({'title': title, 'description': description, 'link': link})

            return news_items

        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در دریافت اطلاعات: {e}")
            return []


class ArticleFetcher:
    @staticmethod
    def fetch_full_article(url):
        try:
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            possible_selectors = [
                {'name': 'div', 'class_': 'body'},
                {'name': 'div', 'class_': 'article-body'},
                {'name': 'div', 'class_': 'news-body'},
                {'name': 'div', 'class_': 'content'},
                {'name': 'div', 'id': 'content'},
            ]

            for selector in possible_selectors:
                content_div = soup.find(selector['name'], class_=selector.get('class_'), id=selector.get('id'))
                if content_div:
                    paragraphs = content_div.find_all(['p', 'div'])
                    article_text = '\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                    if article_text.strip():
                        return article_text

            all_paragraphs = soup.find_all('p')
            article_text = '\n'.join(p.get_text(strip=True) for p in all_paragraphs if p.get_text(strip=True))
            return article_text

        except Exception as e:
            print(f"❌ خطا در دریافت متن کامل خبر: {e}")
            return ""
