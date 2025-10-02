from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.items import router as items_router
from app.api.bids import router as bids_router
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    openapi_url=f"/openapi.json",
    debug=settings.debug
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["authentication"]
)

app.include_router(
    users_router,
    prefix="/users",
    tags=["users"]
)

app.include_router(
    items_router,
    prefix="/items",
    tags=["items"]
)

app.include_router(
    bids_router,
    prefix="/bids",
    tags=["bids"]
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Auction API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
