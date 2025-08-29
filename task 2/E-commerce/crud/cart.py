import json
import os
from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..models.cart import Cart
from sqlalchemy.orm import Session
from ..models.product import Product
from ..crud.product import get_product

# Resolve orders.json path anchored to the Task 2 directory
ORDERS_FILE = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "orders.json"))

def create_cart(cart: Cart, db: Session) -> Cart:
    """Create a new cart item in the database with stock validation and deduction."""
     # Get the product to check stock
    product = get_product(cart.product_id, db)

    # check if enough stock is available
    if product.stock < cart.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"insufficient stock. Available: {product.stock}, "
                   f"Requested: {cart.quantity}")

    # Check if user already has the product in cart
    existing_cart_item = db.query(Cart).filter(
        Cart.user_id == cart.user_id,
        Cart.product_id == cart.product_id
    ).first()

    if existing_cart_item:
        # update existing cart item
        new_total_quantity = existing_cart_item.quantity + cart.quantity

        # check if total quantity exceeds stock
        if product.stock < new_total_quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock. Available: {product.stock}, Total requested: {new_total_quantity}"
            )

        # update existing cart item
        existing_cart_item.quantity = new_total_quantity
        existing_cart_item.total_price = product.price * new_total_quantity

        # reduce stock
        product.stock -= cart.quantity

        try:
            db.commit()
            db.refresh(existing_cart_item)
            db.refresh(product)
            return existing_cart_item
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error updating cart")

    else:
        # create new cart existing_cart_item
        # reduce stock
        product.stock -= cart.quantity

        db.add(cart)
        try:
            db.commit()
            db.refresh(cart)
            db.refresh(product)
            return cart
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error adding item to cart"
            )


def get_user_cart(user_id: int, db: Session) -> List[Cart]:
    """Get all cart items for a user"""
    return db.query(Cart).filter(Cart.user_id == user_id).all()

def clear_user_cart(user_id: int, db: Session) -> None:
    """Clear all items from user's cart"""
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

def save_order_to_json(order_data: dict):
    """Save order to orders.json file"""
    orders_file = ORDERS_FILE

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


def remove_from_cart(user_id: int, product_id: int, db: Session) -> None:
    """Remove item from cart and restore stock"""
    cart_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    # Restore stock
    from ..crud.product import get_product
    product = get_product(product_id, db)
    product.stock += cart_item.quantity

    # Remove cart item
    db.delete(cart_item)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error removing from cart")