from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BidBase(BaseModel):
    item_id: int
    amount: float


class BidCreate(BidBase):
    pass


class BidUpdate(BaseModel):
    amount: Optional[float] = None


class BidInDBBase(BidBase):
    id: int
    bidder_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Bid(BidInDBBase):
    pass
