from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..utils import get_session
from ..crud.product import (
    create_product,
    get_product,
    get_products
)
from ..schemas.product import ProductUpdate,ProductResponse, ProductCreate
from ..models import Product, User
from ..auth import get_current_admin_user


# Create two routers - one for admin, one for public
admin_router = APIRouter(prefix="/admin", tags=["admin"])
public_router = APIRouter(prefix="/products", tags=["products"])


@admin_router.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(
        product: ProductCreate,
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_admin_user)
):
    """Create a new product (admin only)"""
    db_product = Product(**product.model_dump())
    return create_product(db_product, db)

@public_router.get("/", response_model=List[ProductResponse])
async def get_products_endpoint(
        db: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 10
):
    """Get all products (public endpoint)"""
    return get_products(db, skip, limit)

@public_router.get("/{product_id}", response_model=ProductResponse)
async def get_product_endpoint(product_id: int, db: Session = Depends(get_session)):
    """Get a product by ID (public endpoint)"""
    return get_product(product_id, db)