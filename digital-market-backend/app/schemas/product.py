"""Pydantic schemas for Product."""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    """What the client sends when creating a product."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)  # Greater than or equal to 0


class ProductOut(BaseModel):
    """What we return when fetching a product."""
    id: int
    title: str
    description: Optional[str] = None
    price: Decimal
    file_name: Optional[str] = None
    is_published: bool
    seller_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True