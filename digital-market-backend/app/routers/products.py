"""Product endpoints: create, list, get one."""
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductOut
from app.core.deps import get_current_user
from app.config import settings


router = APIRouter(prefix="/products", tags=["products"])


# Ensure upload directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=ProductOut, status_code=201)
async def create_product(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new product. Requires authentication.
    
    This is a multipart/form-data endpoint because we're uploading a file.
    """
    # Validate price
    if price < 0:
        raise HTTPException(status_code=400, detail="Price must be positive")
    
    # Handle file upload (if provided)
    file_path = None
    file_name = None
    if file:
        # Generate unique filename to prevent collisions
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        file_name = file.filename
    
    # Create the product
    new_product = Product(
        title=title,
        description=description,
        price=price,
        file_path=file_path,
        file_name=file_name,
        seller_id=current_user.id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.get("/", response_model=list[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all published products. Requires authentication."""
    products = (
        db.query(Product)
        .filter(Product.is_published == 1)
        .order_by(Product.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return products


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single product by ID. Requires authentication."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product