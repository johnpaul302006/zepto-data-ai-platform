import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = "https://books.toscrape.com/catalogue/"
NUM_PAGES = 5


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


session = requests.Session()
session.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/131.0 Safari/537.36"
        )
    }
)


def get_soup(url):
    """Download a web page and return its BeautifulSoup object."""
    response = session.get(url, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_book(book_card):
    """Extract book information from one product card."""
    try:
        title_tag = book_card.select_one("h3 a")
        price_tag = book_card.select_one("p.price_color")
        rating_tag = book_card.select_one("p.star-rating")
        availability_tag = book_card.select_one("p.instock.availability")

        if not all([title_tag, price_tag, rating_tag, availability_tag]):
            return None

        title = title_tag.get("title") or title_tag.get_text(strip=True)

        price_text = price_tag.get_text(strip=True)

        rating_classes = rating_tag.get("class", [])
        rating_text = next(
            (item for item in rating_classes if item in RATING_MAP),
            None,
        )

        availability = availability_tag.get_text(" ", strip=True)

        relative_url = title_tag.get("href")
        detail_url = urljoin(CATALOGUE_URL, relative_url)

        # Open the individual book page to get the category.
        detail_soup = get_soup(detail_url)

        breadcrumb_items = detail_soup.select("ul.breadcrumb li")

        if len(breadcrumb_items) >= 2:
            category = breadcrumb_items[-2].get_text(strip=True)
        else:
            category = None

        return {
            "title": title,
            "price": price_text,
            "star_rating": rating_text,
            "availability": availability,
            "category": category,
        }

    except (requests.RequestException, AttributeError, IndexError) as exc:
        print(f"Skipping a book because of an error: {exc}")
        return None


def scrape_books():
    """Scrape books from the first five catalogue pages."""
    books = []

    for page_number in range(1, NUM_PAGES + 1):
        page_url = f"{CATALOGUE_URL}page-{page_number}.html"

        print(f"\nScraping page {page_number}: {page_url}")

        try:
            soup = get_soup(page_url)
        except requests.RequestException as exc:
            print(f"Could not load page {page_number}: {exc}")
            continue

        book_cards = soup.select("article.product_pod")

        print(f"Found {len(book_cards)} books on this page.")

        for book_card in book_cards:
            book = scrape_book(book_card)

            if book is not None:
                books.append(book)

            # Small delay between requests.
            time.sleep(0.2)

    return books


if __name__ == "__main__":
    records = scrape_books()

    df = pd.DataFrame(records)

    print("\n========== SCRAPING COMPLETE ==========")
    print("Total books scraped:", len(df))

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nColumns:")
    print(df.columns.tolist())

    df.to_csv("data_pipeline/raw_books.csv", index=False)

    print("\nSaved to:")
    print("data_pipeline/raw_books.csv")