from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.api.auth import get_current_user
from app.models.user import User as UserModel
from app.schemas.bid import Bid, BidCreate
from app.services import (
    get_item_bids, get_user_bids, create_bid, validate_bid_amount, get_item_by_id
)
from app.models.item import AuctionStatus

router = APIRouter()


@router.get("/item/{item_id}", response_model=List[Bid])
async def get_item_bids_endpoint(
    item_id: int,
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(get_db)
):
    """Get all bids for an item."""
    # Check if item exists
    item = get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    return get_item_bids(db, item_id, skip=skip, limit=limit)


@router.post("/", response_model=Bid)
async def create_bid_endpoint(
    bid: BidCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Place a bid on an item."""
    # Validate bid amount
    if not validate_bid_amount(db, bid.item_id, bid.amount):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid bid amount"
        )

    # Create the bid
    new_bid = create_bid(db, bid, current_user.id)
    if not new_bid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot place bid (auction not active or item not found)"
        )

    return new_bid


@router.get("/user/me", response_model=List[Bid])
async def get_my_bids(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's bids."""
    return get_user_bids(db, current_user.id)
