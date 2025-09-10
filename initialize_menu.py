#!/usr/bin/env python3
"""
Script to initialize the database with sample menu data.
This script can be run after the application starts to populate the menu with sample items.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.orm import sessionmaker
from app.database import engine, Base
from app.models.menu import MenuItem

def initialize_menu():
    """Initialize the database with sample menu items"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if menu items already exist
        existing_items = db.query(MenuItem).count()
        if existing_items == 0:
            # Add sample menu items
            sample_items = [
                MenuItem(name="Shan Noodles", price=2.5, category="Myanmar Food"),
                MenuItem(name="Mohinga", price=2.0, category="Myanmar Food"),
                MenuItem(name="Tea Leaf Salad", price=3.0, category="Myanmar Food"),
                MenuItem(name="Chicken Curry", price=4.5, category="Myanmar Food"),
            ]
            
            for item in sample_items:
                db.add(item)
            
            db.commit()
            print("Sample menu items added successfully!")
        else:
            print("Menu items already exist in the database.")
    except Exception as e:
        print(f"Error initializing menu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    initialize_menu()