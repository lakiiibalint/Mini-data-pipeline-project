"""
SQLAlchemy ORM models for the books database,
defines how does the DB look like
"""

from sqlalchemy import Column, Integer, String, DateTime, func, Float
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
    category = Column(String, nullable=True)
    product_page_url = Column(String, nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Integer, nullable=True)
    availability = Column(Integer, nullable=True)
    category = Column(String, nullable=True)
    product_page_url = Column(String, nullable=False, unique=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)