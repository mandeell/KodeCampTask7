from pydantic import BaseModel, EmailStr
from typing import Optional


class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    name: str
    username: str
    email:EmailStr
    password: str
    age: int
    is_admin: bool


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool