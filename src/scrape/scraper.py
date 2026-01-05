from bs4 import BeautifulSoup, Tag
import requests
import time
import random
from typing import List, Dict, Optional
from urllib.parse import urljoin

import re
from decimal import Decimal, InvalidOperation
import logging


BASE = 'https://books.toscrape.com/'

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

def make_session() -> requests.Session:
    """
    Create and configure a requests Session with custom User-Agent.
    
    Returns:
        requests.Session: Configured session object for HTTP requests
    """
    session = requests.Session()
    session.headers.update({"User-Agent": "MiniDataPipelineBot/1.0 (lakatosbalint1029@gmail.com)"})
    return session 


def fetch(session: requests.Session, url: str, timeout: float = 10.0) -> str:
    """
    Fetch HTML content from a URL with retry logic and exponential backoff.
    
    Args:
        session: requests.Session for HTTP requests
        url: Target URL to fetch
        timeout: Request timeout in seconds (default: 10.0)
    
    Returns:
        str: HTML content as text
    
    Raises:
        requests.RequestException: If all retry attempts fail
    """
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            logging.warning(f"Fetch failed (attempt {attempt}/{retries}) for {url}: {exc}")

            if attempt == retries:
                logging.exception(f"Failed to fetch {url} after {retries} attempts")
                raise
            # exponential backoff
            time.sleep(2 ** attempt)

def parse_book_card(card: Tag, session: requests.Session) -> Dict[str, Optional[str]]:
    """
    Parse a book card element and extract book details including category from product page.
    
    Args:
        card: BeautifulSoup Tag representing a single book card
        session: requests.Session for fetching the product page
    
    Returns:
        Dict containing title, price, availability, rating, product_page_url, and category
    """
    title_el = card.select_one("h3 a")
    title = title_el.get("title", "").strip() if title_el else ""
    href = title_el.get("href") if title_el else None
    product_page_url = urljoin(BASE, href) if href else None

    price_el = card.select_one(".price_color")
    price_text = price_el.get_text(strip=True) if price_el else ""
    price = price_text.lstrip("£") if price_text else ""

    rating_el = card.select_one("p.star-rating")
    rating = None

    category, availability = fetch_product_details(session, product_page_url)

    if rating_el:
        classes = rating_el.get("class", [])
        rating_word = next((c for c in classes if c != "star-rating"), None)
        rating = RATING_MAP.get(rating_word)

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating,
        "product_page_url": product_page_url,
        "category" : category
    }


def scraper(start_path="index.html", max_pages=1):
    """
    Scrape book information from books.toscrape.com with pagination support.
    
    Args:
        start_path: Starting path for scraping (default: "index.html")
        max_pages: Maximum number of pages to scrape (default: 1)
    
    Yields:
        Dict: Book information including title, price, rating, availability, url, and category
    """
    session = make_session()
    url = urljoin(BASE, start_path.lstrip("/"))
    pages = 0

    while url and pages < max_pages:
        html = fetch(session, url)
        soup = BeautifulSoup(html, "html.parser")

        for card in soup.select("article.product_pod"):
            yield parse_book_card(card, session)

        next_url = soup.select_one("li.next a")
        url = urljoin(url, next_url["href"]) if next_url else None
        pages += 1
        time.sleep(1 + random.random())

        
def fetch_product_details(session: requests.Session, product_url: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Fetch the product page and extract category and availability.
    
    The category is extracted from the breadcrumb structure:
    Home > Books > [Category] > Book Title
    
    The availability is extracted from the product information table.
    
    Args:
        session: requests.Session for HTTP requests
        product_url: Full URL to the book's product page
    
    Returns:
        Tuple of (category, availability) where:
        - category: e.g., "Travel", "Mystery", or None
        - availability: e.g., "In stock (22 available)", or None
    """
    if not product_url:
        return None, None
    
    try:
        html = fetch(session, product_url)
        soup = BeautifulSoup(html, "html.parser")
        
        breadcrumb_links = soup.select("ul.breadcrumb li a")
        category = breadcrumb_links[2].get_text(strip=True) if len(breadcrumb_links) > 2 else None
        
        availability_el = soup.select_one("p.availability")
        availability = availability_el.get_text(strip=True) if availability_el else None
        
        return category, availability
    
    except Exception as e:
        logging.warning(f"Could not fetch product details for {product_url}: {e}")
        return None, None
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        books = list(scraper(max_pages=1))
        logging.info(f"Scraped {len(books)} books")
        print(books[:5])
    except Exception as e:
        logging.error(f"Scraper failed: {e}")