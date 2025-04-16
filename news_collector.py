import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.rokna.net'
URL = f'{BASE_URL}/%D8%A8%D8%AE%D8%B4-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%DB%8C-65'

# تابع برای استخراج تیترهای خبری و لینک‌ها
def fetch_rokna_news(limit=10):
    try:
        response = requests.get(URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []

        # استفاده از CSS Selectors برای استخراج اخبار
        articles = soup.select('li.ostani-parted')  # به روز رسانی انتخاب کننده به 'li'

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
        print(f"خطا در دریافت اطلاعات: {e}")
        return []

# تابع برای دریافت متن کامل مقاله
def fetch_full_article(link):
    try:
        response = requests.get(link)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='body')

        if not content_div:
            return "متن کامل خبر یافت نشد."

        paragraphs = content_div.find_all('p')
        full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return full_text

    except requests.exceptions.RequestException as e:
        return f"خطا در دریافت مقاله: {e}"

# تابع اصلی برای نمایش اخبار
def news_collector():
    news = fetch_rokna_news()

    if news:
        for i, item in enumerate(news):
            print(f"{i + 1}. عنوان: {item['title']}")
            print(f"   توضیحات: {item['description']}")
            print(f"   لینک: {item['link']}\n")

            # برای دریافت متن کامل خبر
            full_article = fetch_full_article(item['link'])
            print(f"   متن کامل:\n{full_article}\n")
    else:
        print("هیچ خبری برای نمایش یافت نشد.")

# اجرای جمع‌آوری اخبار
news_collector()
