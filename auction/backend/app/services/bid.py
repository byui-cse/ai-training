from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from datetime import datetime
from app.models.bid import Bid
from app.models.item import Item, AuctionStatus
from app.schemas.bid import BidCreate


def get_bid_by_id(db: Session, bid_id: int) -> Optional[Bid]:
    """Get bid by ID."""
    return db.query(Bid).filter(Bid.id == bid_id).first()


def get_item_bids(db: Session, item_id: int, skip: int = 0, limit: int = 100) -> List[Bid]:
    """Get all bids for an item."""
    return db.query(Bid).filter(Bid.item_id == item_id).order_by(
        desc(Bid.amount)
    ).offset(skip).limit(limit).all()


def get_user_bids(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Bid]:
    """Get all bids by a user."""
    return db.query(Bid).filter(Bid.bidder_id == user_id).order_by(
        desc(Bid.created_at)
    ).offset(skip).limit(limit).all()


def get_highest_bid_for_item(db: Session, item_id: int) -> Optional[Bid]:
    """Get the highest bid for an item."""
    return db.query(Bid).filter(Bid.item_id == item_id).order_by(
        desc(Bid.amount)
    ).first()


def create_bid(db: Session, bid: BidCreate, bidder_id: int) -> Optional[Bid]:
    """Create a new bid if valid."""
    # Check if item exists and is active
    item = db.query(Item).filter(Item.id == bid.item_id).first()
    if not item:
        return None

    now = datetime.utcnow()
    if (item.status != AuctionStatus.ACTIVE or
        item.start_time > now or
        item.end_time <= now):
        return None

    # Check if bid is higher than current price
    if bid.amount <= item.current_price:
        return None

    # Create the bid
    db_bid = Bid(
        item_id=bid.item_id,
        bidder_id=bidder_id,
        amount=bid.amount
    )
    db.add(db_bid)

    # Update item's current price
    item.current_price = bid.amount
    item.updated_at = now

    db.commit()
    db.refresh(db_bid)
    return db_bid


def validate_bid_amount(db: Session, item_id: int, bid_amount: float) -> bool:
    """Validate if a bid amount is acceptable for the item."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return False

    # Must be higher than current price
    if bid_amount <= item.current_price:
        return False

    # Must be higher than starting price if no bids yet
    if item.current_price == item.starting_price and bid_amount <= item.starting_price:
        return False

    return True
