import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from tqdm import tqdm
import json
import os

init(autoreset=True)

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to fetch {url}")
        return None


def parse_books(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".product_pod")

    books = []

    for item in items:
        title = item.h3.a["title"]
        price = item.select_one(".price_color").text

        books.append({
            "title": title,
            "price": price
        })

    return books


def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open("data/books.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(Fore.GREEN + "\n[SAVED] Data saved to data/books.json")


def display_books(books):
    print(Fore.CYAN + "\n--- Sample Results ---\n")
    for book in books[:5]:
        print(Fore.YELLOW + f"Title: {book['title']}")
        print(Fore.GREEN + f"Price: {book['price']}")
        print("-" * 50)


def main():
    total_pages = 5
    all_books = []

    print(Fore.MAGENTA + "\nStarting Web Scraper...\n")

    for page in tqdm(range(1, total_pages + 1), desc="Scraping Pages"):
        url = BASE_URL.format(page)
        html = fetch_page(url)

        if html:
            books = parse_books(html)
            all_books.extend(books)

    print(Fore.BLUE + f"\nTotal Books Scraped: {len(all_books)}")

    display_books(all_books)
    save_data(all_books)


if __name__ == "__main__":
    main()