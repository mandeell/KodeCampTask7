from typing import Generator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .database_setup import engine
from sqlalchemy.orm import Session, sessionmaker

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


def configure_cors(app: FastAPI) -> None:
    """Configure CORS middleware for the FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )