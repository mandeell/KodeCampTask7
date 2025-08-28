import json, os
from datetime import timedelta, datetime
from typing import List, Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from .models.user import User
from passlib.context import  CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def load_user() -> List[User]:
    """
    Load users from a JSON file.
    Return:
        List of User objects.
    Raises:
        FileNotFoundError: If the user.json does not exist.
        JSONDecodeError: If the JSON file is not malformed.
    """
    file_path = os.path.join(os.path.dirname(__file__), "users.json")
    try:
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as file:
            data = json.load(file)
        return [User(**user_data) for user_data in data]
    except json.JSONDecoderError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in users.json")

def get_user(username: str) -> Optional[User]:
    """
    Find a user by username.

    Args:
    username: Username to search for.

    Returns:
    """
    users = load_user()
    for user in users:
        if user.username == username:
            return user
    return None

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


def authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by username and password.
    """
    user = get_user(username)

    if not user:
        print("DEBUG: User not found")
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

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Validate JWT  toekn and return the current user.

    Args:
        token: JWT token from the Authorization header.

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
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user.")
    return user
