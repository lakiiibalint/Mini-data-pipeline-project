"""
Database connector utilities for PostgreSQL.
"""

from typing import Iterable, Dict

import psycopg #Python driver to talk to PostgreSQL.
from psycopg.rows import dict_row # makes query results come back as dicts instead of tuples.

from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

#Any code that wants to talk to the DB calls get_connection().
def get_connection() -> psycopg.Connection:
    """
    Return a Postgres connection to the project database.
    """
    conn = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        row_factory=dict_row,
    )
    return conn


def insert_books(records: Iterable[Dict]) -> None:
    """
    Insert a collection of raw book records into the 'raw_books' table.
    """
    records = list(records)
    if not records:
        return

    conn = get_connection()
    with conn:
        conn.executemany(
            """
            INSERT INTO raw_books
                (title, price_raw, rating_raw, availability_raw,
                 category_raw, product_page_url, timestamp)
            VALUES
                (%(title)s, %(price_raw)s, %(rating_raw)s, %(availability_raw)s,
                 %(category_raw)s, %(product_page_url)s, %(timestamp)s)
            """,
            records,
        )
    conn.close()
