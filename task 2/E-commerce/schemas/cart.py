from pydantic import BaseModel
from pydantic import ConfigDict, conint


class CartAdd(BaseModel):
    product_id: int
    quantity: conint(gt=0)

class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    user_id: int
    quantity: int
    total_price: float

