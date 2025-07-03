"""Database utility setup for SQLAlchemy with SQLite.

This module configures the SQLAlchemy engine, session, and the base declarative class,
and provides dependency-injected session utility for FastAPI routes.

MIGRATIONS NOTE:
    This MVP is intentionally simple. If database migrations are needed in future,
    consider using Alembic (https://alembic.sqlalchemy.org/). Place migration config in
    a migrations/ directory and invoke via `alembic` CLI.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# In production, source this from environment or configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"  # Use relative path for local dev

# The connect_args={"check_same_thread": False} is required only for SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal will be the dependency-injected session class for FastAPI endpoints.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the declarative base class for model definitions.
Base = declarative_base()

# PUBLIC_INTERFACE
def get_db() -> Generator:
    """Provides a transaction-scoped database session suitable for FastAPI dependency injection.

    This should be injected into path operation dependencies using: db: Session = Depends(get_db)

    Yields:
        SQLAlchemy Session object that is automatically closed after request.
    Example:
        def endpoint(..., db: Session = Depends(get_db)):
            # use db session here
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MIGRATIONS PLACEHOLDER:
#   When ready for production or schema evolution, add Alembic configuration here.
#   Example:
#       from alembic.config import Config
#       alembic_cfg = Config("alembic.ini")
#       # and so on...
