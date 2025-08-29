from pydantic import BaseModel
from typing import Optional



class ProductCreate(BaseModel):
    name: str
    stock: int
    price: float


class ProductUpdate(BaseModel):
    name: Optional[str]
    stock: Optional[int]
    price: Optional[float]


class ProductResponse(BaseModel):
    id: int
    name: str
    stock: int
    price: float