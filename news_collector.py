def fetch_rokna_news():
    url = f'{BASE_URL}/%D8%A8%D8%AE%D8%B4-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%DB%8C-65'

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        titles = soup.find_all('p', class_='lead', itemprop='description')
        links = soup.find_all('a', itemprop='url')

        news_items = []
        for title, link in zip(titles, links):
            href = link.get('href')
            full_url = BASE_URL + href if href else None
            news_items.append({
                'title': title.get_text(strip=True),
                'link': full_url
            })

        if not news_items:
            logging.warning("هیچ خبری از سایت رکنا دریافت نشد.")
        
        return news_items[:10]  # حداکثر 10 خبر

    except requests.exceptions.RequestException as e:
        logging.error(f"خطا در دریافت اخبار: {e}")
        return []
