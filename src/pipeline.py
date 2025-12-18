import logging
# Hints:
# - Keep imports minimal and specific to the steps below
from src.scrape.scraper import scraper              # Step 1: scrape
from src.db.connector import insert_raw_books, upsert_books  # Step 2 & 4: DB writes
from src.processing.clean import clean_row          # Step 3: cleaning

def run_pipeline(max_pages: int) -> dict:
    """
    Returns a summary dict for quick visibility.
    """
    # 1) SCRAPE
    scraped_rows = list(scraper(max_pages=max_pages))
    logging.info(f"Scraped {len(scraped_rows)} books")

    # 2) INSERT RAW
    raw_inserted = insert_raw_books(scraped_rows)
    logging.info(f"Inserted {raw_inserted} raw books")

    # 3) CLEAN
    cleaned_rows = []
    for r in scraped_rows:
        cleaned = clean_row({
            "title": r.get("title"),
            "price": r.get("price"),
            "rating": r.get("rating"),
            "availability": r.get("availability"),
            "product_page_url": r.get("product_page_url"),
        })
        if cleaned:
            cleaned_rows.append(cleaned)
    logging.info(f"Cleaned {len(cleaned_rows)} books")

    # 4) UPSERT CLEANED

    upserted = upsert_books(cleaned_rows)
    logging.info(f"Upserted {upserted} books into canonical table")

    return {
        "scraped": len(scraped_rows),
        "raw_inserted": raw_inserted,
        "cleaned": len(cleaned_rows),
        "upserted": upserted,
    }

if __name__ == "__main__":
    summary = run_pipeline(1)
    print(summary)