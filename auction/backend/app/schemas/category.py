"""
Pydantic schemas for Category model validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating category information."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class Category(CategoryBase):
    """Schema for category responses."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class CategoryWithStats(Category):
    """Schema for category with item statistics."""
    item_count: int = 0
    active_auctions: int = 0

    class Config:
        """Pydantic configuration."""
        from_attributes = True
