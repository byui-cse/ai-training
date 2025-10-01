"""
Item model for auction items.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Item(Base):
    """Item database model."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    starting_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)  # Updated with bids
    reserve_price = Column(Float, nullable=True)   # Minimum price for sale
    buy_now_price = Column(Float, nullable=True)   # Optional instant purchase price

    # Auction timing
    auction_start = Column(DateTime, default=datetime.utcnow)
    auction_end = Column(DateTime, nullable=False)

    # Status
    is_active = Column(Boolean, default=True)
    is_sold = Column(Boolean, default=False)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Foreign keys
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    seller = relationship("User", back_populates="items", foreign_keys=[seller_id])
    category = relationship("Category", back_populates="items")
    bids = relationship("Bid", back_populates="item", cascade="all, delete-orphan")
    winner = relationship("User", foreign_keys=[winner_id])

    @property
    def is_auction_active(self) -> bool:
        """Check if auction is currently active."""
        now = datetime.utcnow()
        return self.is_active and self.auction_start <= now < self.auction_end

    @property
    def time_remaining(self) -> Optional[float]:
        """Get remaining time in seconds until auction ends."""
        if not self.is_auction_active:
            return None
        return (self.auction_end - datetime.utcnow()).total_seconds()

    def __repr__(self):
        """String representation of Item."""
        return f"<Item(id={self.id}, title={self.title}, current_price={self.current_price})>"
