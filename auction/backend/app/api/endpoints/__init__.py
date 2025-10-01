"""
API endpoints package.
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .items import router as items_router
from .users import router as users_router

# Main API router
router = APIRouter()

# Include sub-routers
router.include_router(auth_router, prefix="/auth", tags=["authentication"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(items_router, prefix="/items", tags=["items"])

# TODO: Add more routers as implemented
# router.include_router(bids_router, prefix="/bids", tags=["bids"])
# router.include_router(categories_router, prefix="/categories", tags=["categories"])
