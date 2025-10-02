from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.api.auth import get_current_user
from app.models.user import User as UserModel
from app.schemas.item import Item, ItemCreate, ItemUpdate, ItemWithBids
from app.services import (
    get_item_by_id, get_items, get_active_items, get_user_items,
    create_item, update_item, activate_item, get_item_with_bid_count
)

router = APIRouter()


@router.get("/", response_model=List[Item])
async def get_items_endpoint(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all items or active items only."""
    if active_only:
        items = get_active_items(db, skip=skip, limit=limit)
    else:
        items = get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get item by ID."""
    item = get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


@router.get("/{item_id}/details")
async def get_item_details(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get item with bid count."""
    item_details = get_item_with_bid_count(db, item_id)
    if not item_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item_details


@router.post("/", response_model=Item)
async def create_item_endpoint(
    item: ItemCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new auction item."""
    return create_item(db, item, current_user.id)


@router.put("/{item_id}", response_model=Item)
async def update_item_endpoint(
    item_id: int,
    item_update: ItemUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an auction item (seller only)."""
    updated_item = update_item(db, item_id, item_update, current_user.id)
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or not authorized"
        )
    return updated_item


@router.post("/{item_id}/activate", response_model=Item)
async def activate_item_endpoint(
    item_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activate an auction item (seller only)."""
    activated_item = activate_item(db, item_id, current_user.id)
    if not activated_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot activate item (not found, not owned, or invalid timing)"
        )
    return activated_item


@router.get("/user/me", response_model=List[Item])
async def get_my_items(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's auction items."""
    return get_user_items(db, current_user.id)
