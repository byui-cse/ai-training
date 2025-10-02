from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import authenticate_user, create_access_token, get_user_by_username
from app.schemas.auth import Token, LoginRequest
from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login user and return access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register(
    user_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Register a new user (simplified - just for testing)."""
    # In a real app, you'd have proper user registration with email verification
    from app.services import create_user, get_user_by_username
    from app.schemas.user import UserCreate, UserRole

    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Create user with default role
    user_create = UserCreate(
        email=f"{user_data.username}@example.com",  # Simplified
        username=user_data.username,
        password=user_data.password,
        role=UserRole.BUYER
    )

    user = create_user(db, user_create)
    return {"message": "User created successfully", "user_id": user.id}


# Dependency to get current user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current authenticated user."""
    from app.services import verify_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception

    return user
