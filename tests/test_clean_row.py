from src.processing.clean import clean_row

print("=== Testing clean_row() ===")

# Scraper-shaped input
scraper_row = {
    "title": "A Light in the Attic",
    "price": "£51.77",
    "rating": "Three",
    "availability": "In stock (22 available)",
    "product_page_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
}

cleaned1 = clean_row(scraper_row)
print("Scraper-shaped cleaned:", cleaned1)

# DB-shaped raw input
db_row = {
    "title": "A Light in the Attic",
    "price_raw": "£51.77",
    "rating_raw": "Three",
    "availability_raw": "In stock",
    "product_page_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
}

cleaned2 = clean_row(db_row)
print("DB-shaped cleaned:", cleaned2)

# Missing critical field
bad_row = {
    "title": "",
    "price": "£10.00",
    "rating": "Two",
    "availability": "In stock",
    "product_page_url": "",
}

cleaned3 = clean_row(bad_row)
print("Missing critical fields -> should be None:", cleaned3)
