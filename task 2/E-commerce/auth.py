from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .models.user import User
from .utils import get_session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)

def get_user(username: str, db: Session) -> Optional[User]:
    """Get user from database by username"""
    user = db.query(User).filter(User.username == username).first()
    return user  # Return None if not found, don't raise exception here

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain password matches  the hashed password.

    Args:
        plain_password: The password to verify.
        hashed_password: The stored Hashed password.
    Returns:
        True if the password matches else False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    """
    Authenticate a user by username and password.
    """
    user = get_user(username, db)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    password_valid = verify_password(password, user.hashed_password)

    if not password_valid:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user.")

    return user


def create_access_token(data: dict) -> str:
    """
    Create a JWT  access token.

     Args:
        data: Dictionary containing token payload (e.g., username).

    Returns:
        Encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    """
    Validate JWT token and return the current user.

    Args:
        token: JWT token from the Authorization header.
        db: Database session.

    Returns:
        User object if token is valid.

    Raises:
        HTTPException: If token is invalid or user not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user(username, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user.")
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure current user is admin"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail=" User not an admin")
    return current_user

