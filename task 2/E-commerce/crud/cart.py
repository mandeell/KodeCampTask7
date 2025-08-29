from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..models.cart import Cart
from sqlalchemy.orm import Session

def create_cart(cart: Cart, db: Session) -> Cart:
    """Create a new cart item in the database."""
    db.add(cart)
    try:
        db.commit()
        db.refresh(cart)
        return cart
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error adding item to cart")

def get_user_cart(user_id: int, db: Session) -> List[Cart]:
    """Get all cart items for a user"""
    return db.query(Cart).filter(Cart.user_id == user_id).all()

def clear_user_cart(user_id: int, db: Session) -> None:
    """Clear all items from user's cart"""
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()


# Helper functions (you'll need to implement these in crud/cart.py)
from datetime import datetime
import json
import os
from fastapi import HTTPException


def save_order_to_json(order_data: dict):
    """Save order to orders.json file"""
    orders_file = "orders.json"

    # Load existing orders
    if os.path.exists(orders_file):
        with open(orders_file, "r") as f:
            orders = json.load(f)
    else:
        orders = []

    # Add new order
    orders.append(order_data)

    # Save back to file
    with open(orders_file, "w") as f:
        json.dump(orders, f, indent=2)