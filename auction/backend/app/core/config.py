from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "sqlite:///./auction.db"

    # Security settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # App settings
    app_name: str = "Auction Website"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
