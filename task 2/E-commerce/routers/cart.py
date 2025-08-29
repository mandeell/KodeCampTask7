from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..utils import get_session
from ..crud.cart import create_cart, get_user_cart, clear_user_cart, save_order_to_json
from ..schemas.cart import CartAdd, CartResponse
from ..models import Cart, User
from ..auth import get_current_user
from ..crud.product import get_product

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add/", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart_endpoint(
        cart_item: CartAdd,
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    """Add item to cart"""
    # Calculate total price (you'll need to get product price)
    product = get_product(cart_item.product_id, db)
    total_price = product.price * cart_item.quantity
    
    db_cart = Cart(
        user_id=current_user.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        total_price=total_price
    )
    return create_cart(db_cart, db)

@router.post("/checkout/", status_code=status.HTTP_200_OK)
async def checkout_endpoint(
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    """Checkout cart and create order"""
    # Get user's cart items
    cart_items = get_user_cart(current_user.id, db)
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total order amount
    total_amount = sum(item.total_price for item in cart_items)
    
    # Create order data
    order_data = {
        "user_id": current_user.id,
        "username": current_user.username,
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.total_price
            }
            for item in cart_items
        ],
        "total_amount": total_amount,
        "order_date": datetime.now().isoformat()
    }
    
    # Save order to orders.json (requirement)
    save_order_to_json(order_data)
    
    # Clear user's cart after successful checkout
    clear_user_cart(current_user.id, db)
    
    return {"message": "Order placed successfully", "order_total": total_amount}

