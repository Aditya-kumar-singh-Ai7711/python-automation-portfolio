"""
Sample Python script for public web data extraction.

This script scrapes book titles and prices from a publicly
available website and exports the data into a CSV file.

Purpose:
- Demonstrates basic web scraping
- Shows structured data extraction
- Outputs clean, Excel-ready data

Website used: http://books.toscrape.com/
"""

import requests
from bs4 import BeautifulSoup
import csv
from requests.exceptions import RequestException


def fetch_page(url):
    """Fetch HTML content from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except RequestException as error:
        print(f"Error fetching page: {error}")
        return None


def parse_books(html):
    """Parse book titles and prices from HTML."""
    soup = BeautifulSoup(html, "lxml")
    books = []

    for article in soup.find_all("article", class_="product_pod"):
        title = article.h3.a.get("title", "").strip()
        price = article.find("p", class_="price_color").text.strip()

        books.append([title, price])

    return books


def save_to_csv(data, filename="output.csv"):
    """Save extracted data to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price"])
        writer.writerows(data)


def main():
    url = "http://books.toscrape.com/"
    html = fetch_page(url)

    if not html:
        print("Failed to retrieve data.")
        return

    book_data = parse_books(html)
    save_to_csv(book_data)

    print(f"Scraping completed. {len(book_data)} records saved.")


if __name__ == "__main__":
    main()
