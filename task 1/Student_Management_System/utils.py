from typing import Generator
from fastapi import FastAPI, Request
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel
import logging
import time
from .database_setup import engine
from fastapi.middleware.cors import CORSMiddleware


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
    logging.FileHandler('requests.log'),
    logging.StreamHandler()
    ]
)


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
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def configure_logging_middleware(app: FastAPI) -> None:
    logger = logging.getLogger(__name__)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request {request.method} {request.url} {response.status_code} took {process_time:.2f} seconds")
        return response



