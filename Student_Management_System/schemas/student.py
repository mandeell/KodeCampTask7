import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List


class StudentCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    grades: Optional[List[float]] = []

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    grades: Optional[List[float]] = None

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    grades: List[float]