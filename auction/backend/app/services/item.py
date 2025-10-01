"""
Item service for auction item management operations.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from app.models.item import Item
from app.models.bid import Bid
from app.schemas.item import ItemCreate, ItemUpdate


def get_item(db: Session, item_id: int) -> Optional[Item]:
    """
    Get item by ID with related data.

    Args:
        db: Database session
        item_id: Item ID

    Returns:
        Item object or None if not found
    """
    return (
        db.query(Item)
        .options(
            joinedload(Item.seller),
            joinedload(Item.category),
            joinedload(Item.bids).joinedload(Bid.bidder),
        )
        .filter(Item.id == item_id)
        .first()
    )


def get_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    active_only: bool = True,
    seller_id: Optional[int] = None,
) -> List[Item]:
    """
    Get list of items with optional filtering.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        category_id: Filter by category ID
        search: Search in title and description
        active_only: Only return active auctions
        seller_id: Filter by seller ID

    Returns:
        List of Item objects
    """
    query = db.query(Item).options(
        joinedload(Item.seller),
        joinedload(Item.category),
    )

    # Apply filters
    if active_only:
        query = query.filter(
            and_(
                Item.is_active == True,
                Item.auction_start <= datetime.utcnow(),
                Item.auction_end > datetime.utcnow(),
            )
        )

    if category_id:
        query = query.filter(Item.category_id == category_id)

    if seller_id:
        query = query.filter(Item.seller_id == seller_id)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Item.title.ilike(search_filter),
                Item.description.ilike(search_filter),
            )
        )

    return query.offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate, seller_id: int) -> Item:
    """
    Create a new auction item.

    Args:
        db: Database session
        item: Item creation data
        seller_id: ID of the seller creating the item

    Returns:
        Created Item object
    """
    db_item = Item(
        **item.model_dump(),
        seller_id=seller_id,
        current_price=item.starting_price,  # Initialize current price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(
    db: Session, item_id: int, item_update: ItemUpdate, seller_id: int
) -> Optional[Item]:
    """
    Update item information (only by seller).

    Args:
        db: Database session
        item_id: Item ID to update
        item_update: Item update data
        seller_id: ID of the seller (for authorization)

    Returns:
        Updated Item object or None if not found or not authorized
    """
    db_item = get_item(db, item_id)
    if not db_item or db_item.seller_id != seller_id:
        return None

    # Don't allow updates to items with bids or ended auctions
    if db_item.bids or not db_item.is_auction_active:
        return None

    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int, seller_id: int) -> bool:
    """
    Delete an item (only by seller, only if no bids).

    Args:
        db: Database session
        item_id: Item ID to delete
        seller_id: ID of the seller (for authorization)

    Returns:
        True if item was deleted, False otherwise
    """
    db_item = get_item(db, item_id)
    if not db_item or db_item.seller_id != seller_id:
        return False

    # Don't allow deletion of items with bids
    if db_item.bids:
        return False

    db.delete(db_item)
    db.commit()
    return True


def get_item_with_bid_stats(db: Session, item_id: int) -> Optional[dict]:
    """
    Get item with bidding statistics.

    Args:
        db: Database session
        item_id: Item ID

    Returns:
        Dictionary with item and bid statistics
    """
    item = get_item(db, item_id)
    if not item:
        return None

    # Get bid statistics
    bid_stats = (
        db.query(
            func.count(Bid.id).label("bid_count"),
            func.max(Bid.amount).label("highest_bid"),
            func.max(Bid.timestamp).label("last_bid_time"),
        )
        .filter(Bid.item_id == item_id)
        .first()
    )

    return {
        "item": item,
        "bid_count": bid_stats.bid_count or 0,
        "highest_bid": bid_stats.highest_bid or item.starting_price,
        "last_bid_time": bid_stats.last_bid_time,
    }


def get_ending_soon_items(db: Session, hours: int = 24, limit: int = 10) -> List[Item]:
    """
    Get items ending soon.

    Args:
        db: Database session
        hours: Number of hours from now
        limit: Maximum number of items to return

    Returns:
        List of Item objects ending soon
    """
    end_time = datetime.utcnow() + timedelta(hours=hours)

    return (
        db.query(Item)
        .options(joinedload(Item.seller), joinedload(Item.category))
        .filter(
            and_(
                Item.is_active == True,
                Item.auction_end <= end_time,
                Item.auction_end > datetime.utcnow(),
            )
        )
        .order_by(Item.auction_end)
        .limit(limit)
        .all()
    )


def get_popular_items(db: Session, limit: int = 10) -> List[Item]:
    """
    Get most popular items by bid count.

    Args:
        db: Database session
        limit: Maximum number of items to return

    Returns:
        List of popular Item objects
    """
    return (
        db.query(Item)
        .options(joinedload(Item.seller), joinedload(Item.category))
        .join(Bid, isouter=True)
        .filter(
            and_(
                Item.is_active == True,
                Item.auction_end > datetime.utcnow(),
            )
        )
        .group_by(Item.id)
        .order_by(func.count(Bid.id).desc())
        .limit(limit)
        .all()
    )
