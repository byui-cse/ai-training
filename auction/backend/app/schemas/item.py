"""
Pydantic schemas for Item model validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Base schemas
class ItemBase(BaseModel):
    """Base item schema with common fields."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    starting_price: float = Field(..., gt=0)
    reserve_price: Optional[float] = Field(None, gt=0)
    buy_now_price: Optional[float] = Field(None, gt=0)
    auction_end: datetime
    category_id: Optional[int] = None


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating item information."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    reserve_price: Optional[float] = Field(None, gt=0)
    buy_now_price: Optional[float] = Field(None, gt=0)
    auction_end: Optional[datetime] = None
    category_id: Optional[int] = None


# Response schemas
class Item(ItemBase):
    """Schema for item responses."""
    id: int
    current_price: float
    seller_id: int
    is_active: bool
    is_sold: bool
    winner_id: Optional[int]
    auction_start: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ItemWithDetails(Item):
    """Schema for item with seller and category details."""
    seller_username: str
    category_name: Optional[str]
    bid_count: int = 0
    highest_bidder_username: Optional[str]

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ItemSummary(BaseModel):
    """Schema for item summary in listings."""
    id: int
    title: str
    current_price: float
    auction_end: datetime
    seller_username: str
    category_name: Optional[str]
    bid_count: int = 0
    is_auction_active: bool

    class Config:
        """Pydantic configuration."""
        from_attributes = True
