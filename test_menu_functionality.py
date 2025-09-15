#!/usr/bin/env python3
"""
Simple test script to verify menu functionality
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.orm import sessionmaker
from app.database import engine, Base
from app.models.menu import MenuItem
from initialize_menu import add_menu_item, update_menu_item

def test_menu_functionality():
    """Test the menu functionality"""
    print("Testing menu functionality...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Test adding a menu item
    print("\n1. Testing add_menu_item function:")
    success = add_menu_item("Test Burger", 5.99, "Test Category")
    if success:
        print("✓ Successfully added menu item")
    else:
        print("✗ Failed to add menu item")
    
    # Test adding a duplicate item (should fail)
    print("\n2. Testing duplicate prevention:")
    success = add_menu_item("Test Burger", 6.99, "Test Category")
    if not success:
        print("✓ Correctly prevented duplicate item")
    else:
        print("✗ Failed to prevent duplicate item")
    
    # Test updating a menu item
    print("\n3. Testing update_menu_item function:")
    # First, let's find the item we added
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        item = db.query(MenuItem).filter(MenuItem.name == "Test Burger").first()
        if item:
            success = update_menu_item(item.id, name="Updated Burger", price=7.99)
            if success:
                print("✓ Successfully updated menu item")
            else:
                print("✗ Failed to update menu item")
        else:
            print("✗ Could not find item to update")
    finally:
        db.close()
    
    print("\nMenu functionality test completed!")

if __name__ == "__main__":
    test_menu_functionality()