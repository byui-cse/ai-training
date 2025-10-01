"""
Items API endpoints for auction item management.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.api.endpoints.auth import get_current_user
from app.db.session import get_db
from app.services.item import (
    create_item,
    delete_item,
    get_ending_soon_items,
    get_item,
    get_item_with_bid_stats,
    get_items,
    get_popular_items,
    update_item,
)

router = APIRouter()


@router.get("/", response_model=List[schemas.ItemSummary])
async def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    category_id: int = Query(None),
    search: str = Query(None, min_length=1),
    active_only: bool = True,
    seller_id: int = Query(None),
) -> Any:
    """
    Retrieve auction items with optional filtering.

    - **skip**: Number of items to skip (pagination)
    - **limit**: Maximum number of items to return (max 100)
    - **category_id**: Filter by category ID
    - **search**: Search in item title and description
    - **active_only**: Only return active auctions (default: true)
    - **seller_id**: Filter by seller ID
    """
    items = get_items(
        db=db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        search=search,
        active_only=active_only,
        seller_id=seller_id,
    )

    # Convert to ItemSummary format
    result = []
    for item in items:
        bid_count = len(item.bids) if hasattr(item, 'bids') else 0
        highest_bidder = None
        if item.bids:
            # Find highest bid
            highest_bid = max(item.bids, key=lambda b: b.amount)
            highest_bidder = highest_bid.bidder.username

        result.append({
            "id": item.id,
            "title": item.title,
            "current_price": item.current_price,
            "auction_end": item.auction_end,
            "seller_username": item.seller.username if item.seller else "Unknown",
            "category_name": item.category.name if item.category else None,
            "bid_count": bid_count,
            "is_auction_active": item.is_auction_active,
        })

    return result


@router.post("/", response_model=schemas.Item)
async def create_new_item(
    item_in: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    """
    Create a new auction item.
    """
    item = create_item(db, item=item_in, seller_id=current_user.id)
    return item


@router.get("/ending-soon", response_model=List[schemas.ItemSummary])
async def read_ending_soon_items(
    hours: int = Query(default=24, ge=1, le=168),  # 1 hour to 1 week
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get items ending soon.

    - **hours**: Number of hours from now (default: 24, max: 168)
    - **limit**: Maximum number of items to return (max 50)
    """
    items = get_ending_soon_items(db, hours=hours, limit=limit)

    result = []
    for item in items:
        bid_count = len(item.bids) if hasattr(item, 'bids') else 0
        result.append({
            "id": item.id,
            "title": item.title,
            "current_price": item.current_price,
            "auction_end": item.auction_end,
            "seller_username": item.seller.username if item.seller else "Unknown",
            "category_name": item.category.name if item.category else None,
            "bid_count": bid_count,
            "is_auction_active": item.is_auction_active,
        })

    return result


@router.get("/popular", response_model=List[schemas.ItemSummary])
async def read_popular_items(
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get most popular items by bid count.

    - **limit**: Maximum number of items to return (max 50)
    """
    items = get_popular_items(db, limit=limit)

    result = []
    for item in items:
        bid_count = len(item.bids) if hasattr(item, 'bids') else 0
        result.append({
            "id": item.id,
            "title": item.title,
            "current_price": item.current_price,
            "auction_end": item.auction_end,
            "seller_username": item.seller.username if item.seller else "Unknown",
            "category_name": item.category.name if item.category else None,
            "bid_count": bid_count,
            "is_auction_active": item.is_auction_active,
        })

    return result


@router.get("/{item_id}", response_model=schemas.ItemWithDetails)
async def read_item(
    item_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get detailed information about a specific auction item.
    """
    item_stats = get_item_with_bid_stats(db, item_id)
    if not item_stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    item = item_stats["item"]
    bid_count = item_stats["bid_count"]
    highest_bid = item_stats["highest_bid"]
    last_bid_time = item_stats["last_bid_time"]

    # Find highest bidder
    highest_bidder_username = None
    if item.bids:
        highest_bid_obj = max(item.bids, key=lambda b: b.amount)
        highest_bidder_username = highest_bid_obj.bidder.username

    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "starting_price": item.starting_price,
        "current_price": item.current_price,
        "reserve_price": item.reserve_price,
        "buy_now_price": item.buy_now_price,
        "auction_start": item.auction_start,
        "auction_end": item.auction_end,
        "is_active": item.is_active,
        "is_sold": item.is_sold,
        "winner_id": item.winner_id,
        "seller_id": item.seller_id,
        "category_id": item.category_id,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
        "seller_username": item.seller.username if item.seller else "Unknown",
        "category_name": item.category.name if item.category else None,
        "bid_count": bid_count,
        "highest_bidder_username": highest_bidder_username,
    }


@router.put("/{item_id}", response_model=schemas.Item)
async def update_item_endpoint(
    item_id: int,
    item_in: schemas.ItemUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    """
    Update an auction item (only by the seller).
    """
    item = update_item(db, item_id=item_id, item_update=item_in, seller_id=current_user.id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or you don't have permission to update it",
        )

    return item


@router.delete("/{item_id}")
async def delete_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    """
    Delete an auction item (only by the seller, only if no bids).
    """
    success = delete_item(db, item_id=item_id, seller_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found, you don't have permission, or item has bids",
        )

    return {"message": "Item deleted successfully"}
