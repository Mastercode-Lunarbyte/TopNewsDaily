import requests
from bs4 import BeautifulSoup

def fetch_rokna_news():
    # آدرس صفحه اقتصادی سایت رکنا
    url = 'https://www.rokna.net/%D8%A8%D8%AE%D8%B4-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%DB%8C-65'

    try:
        # ارسال درخواست به سایت و دریافت محتوای صفحه
        response = requests.get(url)
        response.raise_for_status()  # در صورت بروز مشکل، خطا می‌دهد

        # استفاده از BeautifulSoup برای پردازش HTML صفحه
        soup = BeautifulSoup(response.text, 'html.parser')

        # استخراج تمامی تیترهای خبری با المنت مورد نظر
        news_paragraphs = soup.find_all('p', class_='lead', itemprop='description')

        # جمع‌آوری تیترهای خبری در یک لیست
        news_items = []
        for i, paragraph in enumerate(news_paragraphs[:10]):
            news_items.append(paragraph.get_text(strip=True))

        return news_items

    except requests.exceptions.RequestException as e:
        # مدیریت خطاهای درخواست (مثل قطع ارتباط با اینترنت)
        print(f"Error fetching news: {e}")
        return []

# دریافت اخبار از سایت رکنا
rokna_news = fetch_rokna_news()

# نمایش تیترهای اخبار
for i, news in enumerate(rokna_news, start=1):
    print(f"{i}. {news}")
