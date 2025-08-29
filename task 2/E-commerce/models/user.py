from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    email: EmailStr = Field(unique=True)
    username: str = Field(unique=True)
    hashed_password: str
    is_active: bool
    is_admin: bool
