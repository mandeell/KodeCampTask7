from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..utils import get_session
from ..auth import authenticate_user, create_access_token, hash_password
from ..schemas.auth import Token
from ..schemas.user import UserCreate, UserResponse
from ..crud.user import create_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    """Login endpoint to get access token"""
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_session)
):
    """Register a new user"""
    hashed_password = hash_password(user_data.password)
    db_user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        age=user_data.age,
        hashed_password=hashed_password,
        is_active=user_data.is_active,
        is_admin=user_data.is_admin  # Regular users are not admin by default
    )

    return create_user(db_user, db)