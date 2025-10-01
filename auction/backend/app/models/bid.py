"""
Bid model for auction bidding.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.session import Base


class Bid(Base):
    """Bid database model."""

    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Foreign keys
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    item = relationship("Item", back_populates="bids")
    bidder = relationship("User", back_populates="bids")

    def __repr__(self):
        """String representation of Bid."""
        return f"<Bid(id={self.id}, amount={self.amount}, item_id={self.item_id}, bidder_id={self.bidder_id})>"
