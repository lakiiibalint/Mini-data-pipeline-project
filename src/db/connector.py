"""Database connector using SQLAlchemy ORM
Used every run ro write/read data.
DB operations (insert/query"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import List, Dict, Any
from src.config import DATABASE_URL
from src.db.models import RawBook, Book


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)  

#engine: connection configuration + driver
#session : a conversation with the DB 
#Create a session when you want to write/read, then close it

"""1. SCRAPE:
   scraper() → [{title: "Book", price: "51.77", rating: "Three", ...}, ...]
                ↓
2. SAVE RAW:
   insert_raw_books(raw_rows) → saves to raw_books table
                ↓
3. CLEAN:
   cleaned_rows = [clean_row(r) for r in raw_rows]
   → [{title: "Book", price: 51.77, rating: 3, ...}, ...]  (typed!)
                ↓
4. UPSERT CLEANED:
   upsert_books(cleaned_rows) → saves to books table"""

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def get_session():
    """Context manager for DB sessions with auto commit/rollback."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Session error: {e}")
        raise
    finally:
        session.close()
#{'title': 'A Light in the Attic', 'price': '51.77', 'availability': 'In stock', 'rating': 3}

def insert_raw_books(rows: List[Dict[str, Any]]) -> int:
    """
    Insert a list/iterable of scraped raw book dicts into raw_books table.
    Returns number of inserted rows.
    """
    if not rows:
        return 0
    
    objects = []
    for r in rows:
        objects.append(
            RawBook(
                title=r.get("title"),
                price_raw=r.get("price"),  # Scraper returns 'price', not 'price_raw'
                rating_raw=str(r.get("rating")) if r.get("rating") is not None else None,
                availability_raw=r.get("availability"),
                category=r.get("category"),
                product_page_url=r.get("product_page_url"),
            )
        )
    
    with get_session() as session:
        session.add_all(objects)
        
    return len(objects)

def upsert_books(cleaned_rows: List[Dict[str, Any]]) -> int:
    """
    Insert or update cleaned books into the 'books' table.
    
    Logic:
    - If product_page_url already exists → UPDATE price, rating, availability
    - If product_page_url is new → INSERT as new row
    - Returns count of affected (inserted + updated) rows
    """
    if not cleaned_rows :
        return 0
    #{'title': 'A Light in the Attic', 'price': 'Â£51.77', 'availability':
    # 'In stock', 'rating': 3, 'product_page_url': 
    # 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'}
    with get_session() as session:
        count = 0
        for row in cleaned_rows:
            exists = session.query(Book).filter_by(product_page_url=row["product_page_url"]).first()

            if exists:
                # UPDATE path: modify existing record
                exists.title = row.get("title")
                exists.price = row.get("price")
                exists.rating = row.get("rating")
                exists.availability = row.get("availability")
                exists.category = row.get("category")
                logger.info(f"Updated book: {row['title']}")   
            else:
                # INSERT path: create new record
                new_book = Book(
                    title=row.get("title"),
                    price=row.get("price"),
                    rating=row.get("rating"),
                    availability=row.get("availability"),
                    category=row.get("category"),
                    product_page_url=row.get("product_page_url"),

                )
                session.add(new_book)
                logger.info(f"Inserted new book: {row['title']}")
            
            count += 1
    
    return count



if __name__ == "__main__":
    # Test INSERT path
    print("\n=== TEST 1: Insert new book ===")
    cleaned_demo = [{'title': 'A Light in the Attic', 'price': 50.2, 'availability':
     5, 'rating': 3, 'product_page_url': 
     'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'}]
    
    count = upsert_books(cleaned_demo)
    print(f"Affected {count} row(s)\n")
    
    # Test UPDATE path 
    print("=== TEST 2: Update existing book (same URL) ===")
    updated_demo = [{'title': 'A Light in the Attic (Updated!)', 'price': 99.99, 
     'availability': 1, 'rating': 5, 'product_page_url': 
     'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'}]  # SAME URL
    
    count = upsert_books(updated_demo)
    print(f"Affected {count} row(s)\n")
    print("Check database - should see updated price (99.99) and rating (5)!")