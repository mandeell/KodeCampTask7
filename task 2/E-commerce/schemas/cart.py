from pydantic import BaseModel



class CartAdd(BaseModel):
    product_id: int
    quantity: int

class CartResponse(BaseModel):
    product_id: int
    user_id: str
    quantity: int
    total_price: float

