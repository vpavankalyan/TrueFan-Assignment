from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import product_services
from common.database import get_db
from interfaces import product_interface

router = APIRouter()

@router.post("/",summary="Create a New Product", description="Creates a new product in the database using the provided product data.")
def create_product(product: product_interface.ProductCreate, db: Session = Depends(get_db)):
    return product_services.create_product(db=db, product=product)

@router.get("/{product_id}", response_model=product_interface.Product, summary="Get a Product", description="Retrieves a product by its ID. Returns a single product if found.")
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_services.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get("/", response_model=list[product_interface.Product], summary="List All Products", description="Retrieves a list of all products available in the database.")
def read_all_products(db: Session = Depends(get_db)):
    all_products = product_services.get_all_products(db)
    return all_products

@router.put("/{product_id}", response_model=product_interface.Product, summary="Update a Product", description="Updates the details of an existing product by its ID. Only fields provided in the request will be updated.")
def update_product(product_id: int, product: product_interface.ProductUpdate, db: Session = Depends(get_db)):
    return product_services.update_product(db, product_id, product)

@router.delete("/{product_id}", summary="Delete a Product", description="Deletes a product from the database by its ID.")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_services.delete_product(db, product_id)
