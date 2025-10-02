#!/usr/bin/env python3
"""Add sample data to the auction database for testing."""

from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.models.item import Item, AuctionStatus
from app.models.bid import Bid
from app.services.auth import get_password_hash
from datetime import datetime, timedelta
import random

def add_sample_data():
    """Add sample users, items, and bids to the database."""
    db = SessionLocal()

    try:
        # Create sample users
        users_data = [
            {
                "email": "alice@example.com",
                "username": "alice_smith",
                "hashed_password": get_password_hash("pass"),
                "role": UserRole.SELLER,
                "full_name": "Alice Smith"
            },
            {
                "email": "bob@example.com",
                "username": "bob_johnson",
                "hashed_password": get_password_hash("pass"),
                "role": UserRole.BUYER,
                "full_name": "Bob Johnson"
            },
            {
                "email": "carol@example.com",
                "username": "carol_williams",
                "hashed_password": get_password_hash("pass"),
                "role": UserRole.SELLER,
                "full_name": "Carol Williams"
            },
            {
                "email": "dave@example.com",
                "username": "dave_brown",
                "hashed_password": get_password_hash("pass"),
                "role": UserRole.BUYER,
                "full_name": "Dave Brown"
            }
        ]

        users = []
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
            users.append(user)

        db.commit()

        # Create sample items
        items_data = [
            {
                "title": "Vintage Mechanical Watch",
                "description": "Beautiful vintage mechanical watch from the 1950s. Fully restored and in excellent working condition.",
                "starting_price": 150.00,
                "reserve_price": 200.00,
                "seller_id": users[0].id,  # Alice
                "start_time": datetime.utcnow() - timedelta(hours=1),
                "end_time": datetime.utcnow() + timedelta(days=2),
                "status": AuctionStatus.ACTIVE
            },
            {
                "title": "Antique Ceramic Vase",
                "description": "Rare Ming dynasty ceramic vase. Perfect condition with authentic markings.",
                "starting_price": 300.00,
                "reserve_price": 500.00,
                "seller_id": users[0].id,  # Alice
                "start_time": datetime.utcnow() - timedelta(hours=2),
                "end_time": datetime.utcnow() + timedelta(days=1),
                "status": AuctionStatus.ACTIVE
            },
            {
                "title": "Gaming Laptop RTX 4080",
                "description": "High-performance gaming laptop with RTX 4080 GPU, 32GB RAM, 1TB SSD. Like new condition.",
                "starting_price": 1200.00,
                "reserve_price": 1500.00,
                "seller_id": users[2].id,  # Carol
                "start_time": datetime.utcnow() - timedelta(hours=3),
                "end_time": datetime.utcnow() + timedelta(days=3),
                "status": AuctionStatus.ACTIVE
            },
            {
                "title": "Vintage Vinyl Record Collection",
                "description": "Collection of 50 vintage vinyl records from the 1960s and 1970s. All in excellent condition.",
                "starting_price": 75.00,
                "reserve_price": 150.00,
                "seller_id": users[2].id,  # Carol
                "start_time": datetime.utcnow() - timedelta(hours=4),
                "end_time": datetime.utcnow() + timedelta(days=4),
                "status": AuctionStatus.ACTIVE
            },
            {
                "title": "Designer Handbag",
                "description": "Authentic designer handbag. Gently used, comes with dust bag and authenticity card.",
                "starting_price": 250.00,
                "reserve_price": 350.00,
                "seller_id": users[0].id,  # Alice
                "start_time": datetime.utcnow() - timedelta(days=1),
                "end_time": datetime.utcnow() - timedelta(hours=1),
                "status": AuctionStatus.ENDED
            }
        ]

        items = []
        for item_data in items_data:
            item = Item(**item_data)
            item.current_price = item.starting_price
            db.add(item)
            items.append(item)

        db.commit()

        # Create sample bids
        bids_data = [
            {
                "item_id": items[0].id,
                "bidder_id": users[1].id,  # Bob
                "amount": 160.00
            },
            {
                "item_id": items[0].id,
                "bidder_id": users[3].id,  # Dave
                "amount": 180.00
            },
            {
                "item_id": items[1].id,
                "bidder_id": users[1].id,  # Bob
                "amount": 350.00
            },
            {
                "item_id": items[2].id,
                "bidder_id": users[3].id,  # Dave
                "amount": 1300.00
            },
            {
                "item_id": items[4].id,  # Ended auction
                "bidder_id": users[1].id,  # Bob
                "amount": 280.00
            }
        ]

        for bid_data in bids_data:
            bid = Bid(**bid_data)
            db.add(bid)

            # Update item current price
            item = db.query(Item).filter(Item.id == bid.item_id).first()
            if item and bid.amount > item.current_price:
                item.current_price = bid.amount

        db.commit()

        print("Sample data added successfully!")
        print(f"Created {len(users)} users, {len(items)} items, and {len(bids_data)} bids")

    except Exception as e:
        print(f"Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()
