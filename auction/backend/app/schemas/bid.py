"""
Pydantic schemas for Bid model validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BidBase(BaseModel):
    """Base bid schema."""
    amount: float = Field(..., gt=0)
    item_id: int


class BidCreate(BidBase):
    """Schema for creating a new bid."""
    pass


class Bid(BidBase):
    """Schema for bid responses."""
    id: int
    bidder_id: int
    timestamp: datetime

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class BidWithDetails(Bid):
    """Schema for bid with bidder details."""
    bidder_username: str
    item_title: str

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class BidSummary(BaseModel):
    """Schema for bid summary."""
    amount: float
    bidder_username: str
    timestamp: datetime

    class Config:
        """Pydantic configuration."""
        from_attributes = True
