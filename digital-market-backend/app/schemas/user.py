"""Pydantic schemas for User - defines what data looks like in API requests/responses."""
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """What the client sends when creating a new user."""
    email: EmailStr
    password: str
    full_name: str | None = None


class UserOut(BaseModel):
    """What we send back to the client (never include the password)."""
    id: int
    email: EmailStr
    full_name: str | None = None
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Lets Pydantic read from SQLAlchemy models