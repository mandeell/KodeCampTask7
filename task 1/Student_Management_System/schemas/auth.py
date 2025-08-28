from typing import Optional
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr
    is_active: bool

class TokenData(BaseModel):
    username: Optional[str]
