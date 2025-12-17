import logging
from src.scrape.scraper import scraper
from src.db.connector import insert_raw_books

def run_pipeline (max_pages : int) -> int:
    rows = list(scraper(max_pages = max_pages))
    logging.info(f"Scraped {len(rows)} books")
    inserted = insert_raw_books (rows)
    logging.info(f"Inserted {inserted} raw books")
    return inserted

if __name__ == "__main__":
    run_pipeline(1)