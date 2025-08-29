from typing import Optional
from sqlmodel import SQLModel, Field



class Cart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    quantity: int
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    total_price: float