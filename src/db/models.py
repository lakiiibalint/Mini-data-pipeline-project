"""
SQLAlchemy ORM models for the books database,
defines how does the DB look like
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

# Base class all ORM models inherit from
Base = declarative_base()


class RawBook(Base):
    __tablename__ = "raw_books"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    price_raw = Column(String, nullable=True)
    rating_raw = Column(String, nullable=True)
    availability_raw = Column(String, nullable=True)
    product_page_url = Column(String, nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<RawBook(title={self.title!r}, url={self.product_page_url!r})>"