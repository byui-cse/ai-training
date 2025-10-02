#!/usr/bin/env python3
"""Database initialization script."""

from app.db.session import engine, Base

def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
