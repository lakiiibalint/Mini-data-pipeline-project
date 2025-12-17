"""
Create database tables once from SQLAlchemy models,
basically create tables if they don’t exist.

Run:
	python -m src.db.init_db
"""
import logging
from sqlalchemy import create_engine
from src.config import DATABASE_URL
from src.db.models import Base

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_tables():
		"""Create all tables defined in src.db.models."""
		engine = create_engine(DATABASE_URL, echo=False)
		#base.metadata "goes through" the created tables 
		Base.metadata.create_all(engine)
		logger.info("Tables created successfully")
		engine.dispose()


if __name__ == "__main__":
		create_tables()
