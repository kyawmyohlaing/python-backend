#!/usr/bin/env python3
"""
Script to initialize PostgreSQL database with tables and sample data.
This script creates the necessary tables and populates them with sample data.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, '/app')

# Import the models directly
from database import Base
from models.menu import MenuItem
from models.user import User

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

def init_database():
    """Initialize the database with tables and sample data."""
    try:
        # Use the database URL directly
        # When running inside Docker, we need to use the service name 'db' instead of 'localhost'
        DATABASE_URL = "postgresql://postgres:password@db:5432/mydb"
        
        # Create database engine
        engine = create_engine(DATABASE_URL)
        
        # Create all tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if we already have menu items
        existing_items = db.query(MenuItem).count()
        if existing_items == 0:
            print("Adding sample menu items...")
            # Add sample menu items
            sample_items = [
                MenuItem(name="Burger", price=8.99, category="food"),
                MenuItem(name="Pizza", price=12.99, category="food"),
                MenuItem(name="Salad", price=7.99, category="food"),
                MenuItem(name="Soda", price=2.99, category="drink"),
                MenuItem(name="Coffee", price=3.99, category="drink"),
                MenuItem(name="Tea Leaf Salad", price=6.99, category="food"),
                MenuItem(name="Chicken Curry", price=11.99, category="food"),
                MenuItem(name="Steak (Grill)", price=18.99, category="food"),
                MenuItem(name="Wine", price=7.99, category="alcohol"),
                MenuItem(name="Beer", price=5.99, category="alcohol"),
            ]
            
            for item in sample_items:
                db.add(item)
            
            db.commit()
            print("Sample menu items added successfully.")
        else:
            print(f"Database already contains {existing_items} menu items. Skipping sample data insertion.")
        
        # Check if we have any users
        existing_users = db.query(User).count()
        if existing_users == 0:
            print("Adding sample user...")
            # Add a sample user (in a real application, you'd want to hash the password)
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            sample_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=pwd_context.hash("admin123"),
                role="admin"
            )
            
            db.add(sample_user)
            db.commit()
            print("Sample user added successfully.")
        else:
            print(f"Database already contains {existing_users} users. Skipping user insertion.")
        
        db.close()
        print("Database initialization completed successfully.")
        
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()