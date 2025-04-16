import requests
from bs4 import BeautifulSoup
import logging

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
        for i, paragraph in enumerate(news_paragraphs[:10]):  # محدود کردن به 10 خبر اول
            news_items.append({
                'title': paragraph.get_text(strip=True),
                'link': paragraph.find_parent('a')['href'] if paragraph.find_parent('a') else None
            })

        if not news_items:
            logging.warning("هیچ خبری از سایت رکنا دریافت نشد.")
        
        return news_items

    except requests.exceptions.RequestException as e:
        logging.error(f"خطا در دریافت اخبار: {e}")
        return []

# دریافت اخبار از سایت رکنا
if __name__ == "__main__":
    rokna_news = fetch_rokna_news()

    # نمایش تیترهای اخبار
    if not rokna_news:
        print("مشکلی در دریافت اخبار پیش آمد.")
    else:
        for i, news in enumerate(rokna_news, start=1):
            print(f"{i}. {news['title']} - {news['link']}")
