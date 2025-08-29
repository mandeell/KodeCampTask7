from pydantic import BaseModel
from pydantic import ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    stock: int
    price: float