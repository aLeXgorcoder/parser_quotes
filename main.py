import requests
from bs4 import BeautifulSoup
import json

URL = "https://quotes.toscrape.com/"
quotes_data = []


def get_quotes(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

        quotes_data.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    next_button = soup.find("li", class_="next")
    if next_button:
        next_page = URL + next_button.find("a")["href"]
        get_quotes(next_page)


get_quotes(URL)
"""Запуск парсинга"""

with open("quotes.json", "w", encoding="utf-8") as f:
    """Сохранение в JSON"""
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)