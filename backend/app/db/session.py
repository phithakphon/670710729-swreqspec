import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def init_db() -> None:
    """รองรับ CON-TECH-01, DOM-PDPA-01, IF-HIS-01"""
    Base.metadata.create_all(bind=engine)
