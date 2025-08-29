from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..models.user import User
from sqlalchemy.orm import Session
from ..auth import hash_password

def create_user(user: User, db: Session) -> User:
    """ Create  a new  user  in the database.

    Args:
        user: user object with name, username, password, email, and age.
        db: Database session.

    Returns:
        The created user object.

    Raises:
        HTTPException: if the user already exists.
        """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User registration failed")
