from fastapi import Depends
from sqlalchemy.orm import Session
from .utils import get_session


def get_db() -> Session:
    """
    Database dependency for FastAPI endpoints.
    Usage: db: Session = Depends(get_db)
    """
    return Depends(get_session)
