import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.rokna.net'

CATEGORIES = {
    'اقتصادی': '/بخش-اقتصادی-65',
    'فرهنگی': '/بخش-فرهنگی-9',
    'سبک زندگی': '/بخش-%D8%B3%D8%A8%DA%A9-%D8%B2%D9%86%D8%AF%DA%AF%DB%8C-261',
    'اجتماعی': '/بخش-اخبار-اجتماعی-95',
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

        # استفاده از سلکتور مناسب برای هر دسته
        if category in ["اقتصادی", "اجتماعی"]:
            articles = soup.select('li.ostani-parted')
        elif category in ["فرهنگی", "سبک زندگی"]:
            articles = soup.select('div.l-landing-list')
        else:
            articles = []

        for article in articles[:limit]:
            title_tag = article.find('h3', class_='title')
            description_tag = article.find('p', class_='lead', itemprop='description')
            link_tag = article.find('a', href=True)

            if title_tag and link_tag:
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

        # برای فرهنگی و سبک زندگی
        if 'فرهنگی' in url or 'سبک-زندگی' in url:
            content_div = soup.find('div', id='echo_detail')
            if content_div:
                paragraphs = content_div.find_all('p')
                return '\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        # برای اقتصادی و اجتماعی
        content_div = soup.find('div', class_='body')
        if content_div:
            paragraphs = content_div.find_all('p')
            return '\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        # تلاش با تمام تگ‌های p
        all_paragraphs = soup.find_all('p')
        article_text = '\n'.join(p.get_text(strip=True) for p in all_paragraphs if p.get_text(strip=True))
        return article_text if article_text.strip() else ""

    except Exception as e:
        print(f"❌ خطا در دریافت متن کامل خبر: {e}")
        return ""
