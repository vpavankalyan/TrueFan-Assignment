from sqlalchemy.orm import Session
from common.models import Product
from interfaces import product_interface

def create_product(db: Session, product: Product):
    """
    Creates a new product in the database.

    Args:
    db (Session): The database session to use for the transaction.
    product (Product): The product instance containing data to store.

    Returns:
    Product: The newly created product object.
    """
    new_product = Product(
        name=product.name,
        category=product.category,
        price=product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product(db: Session, product_id: int):
    """
    Fetches product details from the database using Product ID.

    Args:
    db (Session): The database session to use for the transaction.
    product_id (Product): The ID of the product to be retrieved.

    Returns:
    Product: The product object with corresponding ID.
    """
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session):
    """
    Fetches all product details from the database.

    Args:
    db (Session): The database session to use for the transaction.

    Returns:
    Product: The product object with corresponding ID.
    """
    return db.query(Product).all()

def update_product(db: Session, product_id: int, updated_data: product_interface.ProductUpdate):
    """
    Updates product details from the database based on Product ID.

    Args:
    db (Session): The database session to use for the transaction.
    product_id (int): The ID of the product to be retrieved.
    updated_data (Product): The product data to which it has to be updated.

    Returns:
    Product: Updated details of the product.
    """
    print("updated_data::",type(updated_data))
    db_product = db.query(Product).filter(Product.id == product_id).first()

    # Check if product exists
    if db_product is None:
        raise ValueError("No product found with the provided ID.")

    # Check if there are updates to be made
    if not updated_data:
        raise ValueError("No update data provided.")

    # Update the product with new data, explicitly handling each field
    if updated_data.name:
        db_product.name = updated_data.name
    if updated_data.category:
        db_product.category = updated_data.category
    if updated_data.price:
        db_product.price = updated_data.price

    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    """
    Deletes product details from the database based on Product ID.

    Args:
    db (Session): The database session to use for the transaction.
    product_id (int): The ID of the product to be retrieved.

    Returns:
    Success and Message.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is not None:
        db.delete(db_product)
        db.commit()
    return {"staus": True, "message": f"Deleted product with  id {product_id} successfully"}
