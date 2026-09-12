"""Product database model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    """Product table - stores digital products for sale."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    file_path = Column(String, nullable=True)  # Path to file on disk
    file_name = Column(String, nullable=True)  # Original filename
    is_published = Column(Integer, default=1)  # 1 = published, 0 = draft
    
    # Foreign key to User
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship: a product belongs to a user
    # This lets us do product.seller to get the User object
    seller = relationship("User", back_populates="products")

    def __repr__(self):
        return f"<Product {self.id}: {self.title}>"