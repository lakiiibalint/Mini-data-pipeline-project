

---

## 🧩 Architecture & Flow

This is how the pipeline components interact end-to-end.

### Components
- [src/pipeline.py](src/pipeline.py): Orchestrates the whole run.
- [src/scrape/scraper.py](src/scrape/scraper.py): Scrapes book cards and yields dicts.
- [src/processing/clean.py](src/processing/clean.py): Cleans one row (`clean_row`) using helpers (`to_price`, `to_rating`, `to_availability`).
- [src/db/connector.py](src/db/connector.py): Database operations (`insert_raw_books`, `upsert_books`) and session management.
- [src/db/models.py](src/db/models.py): SQLAlchemy ORM models (`RawBook`, `Book`).
- [src/db/init_db.py](src/db/init_db.py): Creates tables from models.
- [src/config.py](src/config.py): Switches DB between SQLite (local) and Postgres (Docker) via env vars.

### Data Models
- `RawBook` (append-only audit): `title`, `price_raw`, `rating_raw`, `availability_raw`, `product_page_url`, `timestamp`.
- `Book` (clean canonical): `title`, `price` (float), `rating` (int), `availability` (int), `product_page_url` (unique), `timestamp`.

### Call Flow (Sequence)

```
CLI: python -m src.pipeline
	 → pipeline.run_pipeline(max_pages)
			1) scraper.scraper(max_pages) → [{title, price, rating, availability, product_page_url}, ...]
			2) connector.insert_raw_books(rows) → writes to raw_books
			3) For each row: clean.clean_row(row) → {title, price:float, rating:int, availability:int, url}
			4) connector.upsert_books(cleaned_rows) → INSERT/UPDATE books by product_page_url
			5) Summary printed: {scraped, raw_inserted, cleaned, upserted}
```

### DB Switching
- Local default: SQLite at `data/books.db`.
- With env var `DB_HOST` set: Postgres via `postgresql+psycopg`.
	- Example (Docker Postgres on host port 5433):

```powershell
$env:DB_HOST="localhost"; $env:DB_PORT="5433"; $env:DB_NAME="books"; $env:DB_USER="appuser"; $env:DB_PASSWORD="app_password"
python -m src.db.init_db
python -m src.pipeline