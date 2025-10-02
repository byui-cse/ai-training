from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .common import AuctionStatus


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    starting_price: float
    reserve_price: Optional[float] = None
    start_time: datetime
    end_time: datetime
    image_url: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    starting_price: Optional[float] = None
    reserve_price: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[AuctionStatus] = None
    image_url: Optional[str] = None


class ItemInDBBase(ItemBase):
    id: int
    seller_id: int
    current_price: float
    status: AuctionStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Item(ItemInDBBase):
    pass


class ItemWithBids(Item):
    bids_count: int = 0
