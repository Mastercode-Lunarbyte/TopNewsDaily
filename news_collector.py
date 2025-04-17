import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.rokna.net'

CATEGORIES = {
    'اقتصادی': '/بخش-اقتصادی-65',
    'فرهنگی': '/بخش-فرهنگی-73'
}

# تابع برای استخراج تیترهای خبری و لینک‌ها
def fetch_rokna_news(category='اقتصادی', limit=10):
    try:
        category_path = CATEGORIES.get(category)
        if not category_path:
            print(f"دسته '{category}' موجود نیست.")
            return []

        url = f'{BASE_URL}{category_path}'
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []

        # استفاده از CSS Selectors برای استخراج اخبار
        articles = soup.select('li.ostani-parted')

        for article in articles[:limit]:
            title_tag = article.find('h3', class_='title')
            description_tag = article.find('p', class_='lead', itemprop='description')
            link_tag = article.find('a', href=True)

            if title_tag and description_tag and link_tag:
                title = title_tag.get_text(strip=True)
                description = description_tag.get_text(strip=True) if description_tag else 'خلاصه‌ای موجود نیست.'
                link = BASE_URL + link_tag['href']
                news_items.append({'title': title, 'description': description, 'link': link})

        return news_items

    except requests.exceptions.RequestException as e:
        print(f"❌ خطا در دریافت اطلاعات ({category}): {e}")
        return []

# تابع برای دریافت متن کامل مقاله
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

        # تلاش با تمام تگ‌های p
        all_paragraphs = soup.find_all('p')
        article_text = '\n'.join(p.get_text(strip=True) for p in all_paragraphs if p.get_text(strip=True))
        return article_text if article_text.strip() else ""

    except Exception as e:
        print(f"❌ خطا در دریافت متن کامل خبر: {e}")
        return ""

# تابع اصلی برای نمایش اخبار برای هر دسته
def news_collector():
    for category in CATEGORIES:
        print(f"\n📰 دسته: {category}")
        news = fetch_rokna_news(category)

        if news:
            for i, item in enumerate(news):
                print(f"{i + 1}. عنوان: {item['title']}")
                print(f"   توضیحات: {item['description']}")
                print(f"   لینک: {item['link']}\n")

                full_article = fetch_full_article(item['link'])
                print(f"   متن کامل:\n{full_article}\n")
        else:
            print("هیچ خبری برای نمایش یافت نشد.")

# اجرای جمع‌آوری اخبار
if __name__ == '__main__':
    news_collector()
