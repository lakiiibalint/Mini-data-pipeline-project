"""Database connector using SQLAlchemy ORM
Used every run ro write/read data.
DB operations (insert/query"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import List, Dict, Any
from src.config import DATABASE_URL
from src.db.models import RawBook


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)  

#engine: connection configuration + driver.
#session : a “conversation” with the DB (transaction scope).
#Create a session when you want to write/read, then close it.

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
                product_page_url=r.get("product_page_url"),
            )
        )
    
    with get_session() as session:
        session.add_all(objects)
        
    return len(objects)


if __name__ == "__main__":
    # Demo test
    demo = [{
        "title": "Test Book",
        "price": "9.99",
        "rating": 3,
        "availability": "In stock",
        "product_page_url": "https://example.com/test-book",
    }]
    
    count = insert_raw_books(demo)
    print(f"Inserted {count} demo records")