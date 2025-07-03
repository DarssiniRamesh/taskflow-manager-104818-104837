"""Database utility setup for SQLAlchemy with SQLite.

This module configures the SQLAlchemy engine, session, and the base declarative class.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"  # Use relative path for local dev

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# PUBLIC_INTERFACE
def get_db():
    """Provides a transaction-scoped database session.

    Yields:
        SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
