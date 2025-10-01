"""
Database initialization script.
Creates tables and populates with sample data.
"""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine
from app.models import Base
from app.services.user import create_user
from app.schemas.user import UserCreate


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


def create_sample_data():
    """Create sample data for development."""
    print("Creating sample data...")

    db = SessionLocal()

    try:
        # Create sample users
        users_data = [
            UserCreate(
                email="admin@example.com",
                username="admin",
                password="admin123",
                full_name="Admin User",
                is_superuser=True,
            ),
            UserCreate(
                email="john@example.com",
                username="john_doe",
                password="password123",
                full_name="John Doe",
            ),
            UserCreate(
                email="jane@example.com",
                username="jane_smith",
                password="password123",
                full_name="Jane Smith",
            ),
            UserCreate(
                email="bob@example.com",
                username="bob_wilson",
                password="password123",
                full_name="Bob Wilson",
            ),
        ]

        users = []
        for user_data in users_data:
            user = create_user(db, user_data)
            users.append(user)
            print(f"Created user: {user.username}")

        # Create sample categories
        from app.models.category import Category

        categories_data = [
            {"name": "Electronics", "description": "Electronic devices and gadgets"},
            {"name": "Books", "description": "Books and publications"},
            {"name": "Art", "description": "Artwork and collectibles"},
            {"name": "Sports", "description": "Sports equipment and memorabilia"},
            {"name": "Home & Garden", "description": "Home improvement and gardening items"},
        ]

        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            db.commit()
            db.refresh(category)
            categories.append(category)
            print(f"Created category: {category.name}")

        # Create sample items
        from app.models.item import Item

        items_data = [
            {
                "title": "Vintage Camera",
                "description": "A classic vintage camera in excellent condition",
                "starting_price": 50.0,
                "current_price": 50.0,
                "reserve_price": 100.0,
                "auction_end": datetime.utcnow() + timedelta(days=7),
                "seller_id": users[1].id,
                "category_id": categories[0].id,
            },
            {
                "title": "Rare First Edition Book",
                "description": "A rare first edition of a classic novel",
                "starting_price": 200.0,
                "current_price": 200.0,
                "reserve_price": 500.0,
                "auction_end": datetime.utcnow() + timedelta(days=5),
                "seller_id": users[2].id,
                "category_id": categories[1].id,
            },
            {
                "title": "Original Oil Painting",
                "description": "Beautiful landscape painting by local artist",
                "starting_price": 150.0,
                "current_price": 150.0,
                "auction_end": datetime.utcnow() + timedelta(days=10),
                "seller_id": users[3].id,
                "category_id": categories[2].id,
            },
            {
                "title": "Basketball Signed by Legend",
                "description": "Authentic basketball signed by a basketball legend",
                "starting_price": 300.0,
                "current_price": 300.0,
                "reserve_price": 800.0,
                "auction_end": datetime.utcnow() + timedelta(days=3),
                "seller_id": users[1].id,
                "category_id": categories[3].id,
            },
        ]

        items = []
        for item_data in items_data:
            item = Item(**item_data)
            db.add(item)
            db.commit()
            db.refresh(item)
            items.append(item)
            print(f"Created item: {item.title}")

        # Create sample bids
        from app.models.bid import Bid

        bids_data = [
            {"amount": 75.0, "item_id": items[0].id, "bidder_id": users[2].id},
            {"amount": 85.0, "item_id": items[0].id, "bidder_id": users[3].id},
            {"amount": 250.0, "item_id": items[1].id, "bidder_id": users[1].id},
            {"amount": 320.0, "item_id": items[3].id, "bidder_id": users[2].id},
            {"amount": 350.0, "item_id": items[3].id, "bidder_id": users[3].id},
        ]

        for bid_data in bids_data:
            bid = Bid(**bid_data)
            db.add(bid)
            # Update item current price
            item = db.query(Item).filter(Item.id == bid.item_id).first()
            if item and bid.amount > item.current_price:
                item.current_price = bid.amount
            print(f"Created bid: ${bid.amount} on {item.title if item else 'Unknown item'}")

        db.commit()
        print("Sample data created successfully!")

    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
    create_sample_data()
    print("Database initialization complete!")
