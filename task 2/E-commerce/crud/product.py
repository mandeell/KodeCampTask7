from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..models.product import Product
from sqlalchemy.orm import Session




def create_product(product: Product, db: Session) -> Product:
    """ Create  a new  product  in the database.

    Args:
        product: product object with name, price, and stock.
        db: Database session.

    Returns:
        The created product object.

    Raises:
        HTTPException: if the product already exists.
        """
    db_product = Product(**product.model_dump())
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="product already exists")


def get_product(product_id: int, db: Session) -> Product:
    """
    Retrieve a product by ID.

    Args:
        product_id: ID of the product to retrieve.
        db: Database session.

    returns:
        The Product object if found.

    raises:
        HTTPException: if the product is not found.
    """

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    """
    retrieve a list of products with pagination.

    Args:
        db: Database session.
        skip: Number of product to skip.
        limit: Maximum number of records to return.

    Returns:
        List of Product objects.
    """

    return db.query(Product).offset(skip).limit(limit).all()