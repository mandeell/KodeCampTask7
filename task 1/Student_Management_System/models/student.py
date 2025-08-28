from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional, List
from sqlalchemy import JSON, Column


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    email: EmailStr = Field(unique=True)
    grades: List[float] = Field(default_factory=list, sa_column=Column(JSON))

