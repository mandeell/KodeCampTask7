from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from typing import Optional


class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    age: int
    is_admin: bool = False
    is_active: bool = True


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool