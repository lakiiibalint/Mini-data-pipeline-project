from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"

DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

"""Database configuration.
Uses SQLite locally unless DB_HOST is set (Postgres).
"""

# If DB_HOST is provided (in Docker), use Postgres; otherwise SQLite for local dev
if os.getenv("DB_HOST"):
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "books")
    DB_USER = os.getenv("DB_USER", "appuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "app_password")
    DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"sqlite:///{DATA_DIR / 'books.db'}"

BASE_URL = "https://books.toscrape.com"

USER_AGENT = (
    "MiniDataPipelineBot/0.1 "
    "(+https://github.com/<lakiiibalint>/mini-data-pipeline)"
)
