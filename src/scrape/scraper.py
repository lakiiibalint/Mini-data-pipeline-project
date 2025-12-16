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

#a függvény egy Session objektumot ad vissza, 

def make_session() -> requests.Session:
    #nyitok egy böngészőt, és azon belül több oldalt töltök be
    session = requests.Session()
    #Alapértelmezett HTTP header beállítása, a szerver látja, ki küldi a kérést
    session.headers.update({"User-Agent" : "MiniDataPipelineBot/1.0 (lakatosbalint1029@gmail.com)"})
    #minden .get() automatikusan tartalmazza a User-Agent-et
    return session 

#biztonságosan letölt egy URL-t
def fetch (session : requests.Session, url : str, timeout : float = 10.0) -> str:
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            logging.warning(
                "Fetch failed (attempt %s/%s) for %s: %s",
                attempt, retries, url, exc
            )

            if attempt == retries:
                logging.exception(
                    "Failed to fetch %s after %s attempts",
                    url, retries
                )
                raise
            # exponential backoff
            time.sleep(2 ** attempt)

def parse_book_card(card: Tag) -> Dict[str, Optional[str]]:
    title_el = card.select_one("h3 a")
    title = title_el.get("title", "").strip() if title_el else ""

    price_el = card.select_one(".price_color")
    price = price_el.text[2:].strip() if price_el else ""

    avail_el = card.select_one("p.availability")
    availability = avail_el.text.strip() if avail_el else None

    rating_el = card.select_one("p.star-rating")
    rating = None
    if rating_el:
        classes = rating_el.get("class", [])
        #next() pulls the first value from the generator
        rating_word = next((c for c in classes if c != "star-rating"), None)
        rating = RATING_MAP.get(rating_word)

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating
    }


def scraper(start_path="index.html", max_pages=1):
    session = make_session()
    url = urljoin(BASE, start_path.lstrip("/"))
    pages = 0

    while url and pages < max_pages:
        html = fetch(session, url)
        soup = BeautifulSoup(html, "html.parser")

        for card in soup.select("article.product_pod"):
            yield parse_book_card(card)

        next_url = soup.select_one("li.next a")
        url = urljoin(url, next_url["href"]) if next_url else None
        pages += 1
        time.sleep(1 + random.random())
            
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        books = list(scraper(max_pages=1))
        logging.info("Scraped %d books", len(books))
        for b in books[:5]:
            logging.info(b)
    except Exception as e:
        logging.error("Scraper failed: %s", e)









