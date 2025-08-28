from typing import Generator
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel
from .database_setup import engine
# from .database_setup import create_db_and_tables

# # Re-export the function
# __all__ = ["create_db_and_tables"]


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    This will be injected into FastAPI endpoints.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()