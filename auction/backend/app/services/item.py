from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from datetime import datetime
from app.models.item import Item, AuctionStatus
from app.models.bid import Bid
from app.schemas.item import ItemCreate, ItemUpdate


def get_item_by_id(db: Session, item_id: int) -> Optional[Item]:
    """Get item by ID."""
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """Get all items with pagination."""
    return db.query(Item).offset(skip).limit(limit).all()


def get_active_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """Get active auction items."""
    now = datetime.utcnow()
    return db.query(Item).filter(
        and_(Item.status == AuctionStatus.ACTIVE,
             Item.start_time <= now,
             Item.end_time > now)
    ).offset(skip).limit(limit).all()


def get_user_items(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
    """Get items for a specific user."""
    return db.query(Item).filter(Item.seller_id == user_id).offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate, seller_id: int) -> Item:
    """Create a new auction item."""
    db_item = Item(
        **item.dict(),
        seller_id=seller_id,
        current_price=item.starting_price,
        status=AuctionStatus.DRAFT
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_update: ItemUpdate, seller_id: int) -> Optional[Item]:
    """Update an auction item (only by seller)."""
    db_item = db.query(Item).filter(
        and_(Item.id == item_id, Item.seller_id == seller_id)
    ).first()

    if not db_item:
        return None

    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def activate_item(db: Session, item_id: int, seller_id: int) -> Optional[Item]:
    """Activate an auction item."""
    db_item = db.query(Item).filter(
        and_(Item.id == item_id, Item.seller_id == seller_id, Item.status == AuctionStatus.DRAFT)
    ).first()

    if not db_item:
        return None

    now = datetime.utcnow()
    if db_item.start_time <= now < db_item.end_time:
        db_item.status = AuctionStatus.ACTIVE
        db.commit()
        db.refresh(db_item)

    return db_item


def end_expired_auctions(db: Session) -> int:
    """End auctions that have passed their end time. Returns count of ended auctions."""
    now = datetime.utcnow()
    result = db.query(Item).filter(
        and_(Item.status == AuctionStatus.ACTIVE, Item.end_time <= now)
    ).update({"status": AuctionStatus.ENDED})

    db.commit()
    return result


def get_item_with_bid_count(db: Session, item_id: int):
    """Get item with bid count."""
    from sqlalchemy import func
    result = db.query(Item, func.count(Bid.id).label('bids_count')).outerjoin(Bid).filter(
        Item.id == item_id
    ).first()

    if result:
        item, bids_count = result
        return {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "starting_price": item.starting_price,
            "current_price": item.current_price,
            "reserve_price": item.reserve_price,
            "seller_id": item.seller_id,
            "start_time": item.start_time,
            "end_time": item.end_time,
            "status": item.status,
            "image_url": item.image_url,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
            "bids_count": bids_count or 0
        }
    return None
