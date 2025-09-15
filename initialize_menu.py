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
from sqlalchemy.exc import IntegrityError
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
            # Add sample menu items with more variety
            sample_items = [
                # Myanmar Food
                MenuItem(name="Shan Noodles", price=2.5, category="Myanmar Food"),
                MenuItem(name="Mohinga", price=2.0, category="Myanmar Food"),
                MenuItem(name="Tea Leaf Salad", price=3.0, category="Myanmar Food"),
                MenuItem(name="Chicken Curry", price=4.5, category="Myanmar Food"),
                MenuItem(name="Lahpet Thoke", price=3.5, category="Myanmar Food"),
                
                # Western Food
                MenuItem(name="Cheeseburger", price=5.0, category="Western Food"),
                MenuItem(name="Caesar Salad", price=4.0, category="Western Food"),
                MenuItem(name="Grilled Chicken Sandwich", price=6.0, category="Western Food"),
                MenuItem(name="Fish and Chips", price=7.0, category="Western Food"),
                
                # Beverages
                MenuItem(name="Milk Tea", price=1.5, category="Beverages"),
                MenuItem(name="Coffee", price=2.0, category="Beverages"),
                MenuItem(name="Fresh Juice", price=2.5, category="Beverages"),
                MenuItem(name="Mineral Water", price=1.0, category="Beverages"),
                
                # Desserts
                MenuItem(name="Chocolate Cake", price=3.5, category="Desserts"),
                MenuItem(name="Ice Cream", price=2.5, category="Desserts"),
                MenuItem(name="Fruit Salad", price=3.0, category="Desserts"),
            ]
            
            added_count = 0
            for item in sample_items:
                try:
                    db.add(item)
                    db.flush()  # Flush to catch any integrity errors early
                    added_count += 1
                except IntegrityError as e:
                    print(f"Warning: Could not add {item.name}: {e}")
                    db.rollback()
            
            db.commit()
            print(f"Added {added_count} sample menu items successfully!")
        else:
            print("Menu items already exist in the database.")
    except Exception as e:
        print(f"Error initializing menu: {e}")
        db.rollback()
    finally:
        db.close()

def add_menu_item(name: str, price: float, category: str):
    """Add a single menu item to the database"""
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if item already exists
        existing_item = db.query(MenuItem).filter(MenuItem.name == name).first()
        if existing_item:
            print(f"Menu item '{name}' already exists.")
            return False
        
        # Add new item
        new_item = MenuItem(name=name, price=price, category=category)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        print(f"Added menu item: {name} - ${price} ({category})")
        return True
    except Exception as e:
        print(f"Error adding menu item '{name}': {e}")
        db.rollback()
        return False
    finally:
        db.close()

def update_menu_item(item_id: int, name: str = None, price: float = None, category: str = None):
    """Update a menu item in the database"""
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Find the item
        db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if db_item is None:
            print(f"Menu item with ID {item_id} not found.")
            return False
        
        # Update fields if provided
        if name is not None:
            db_item.name = name
        if price is not None:
            db_item.price = price
        if category is not None:
            db_item.category = category
            
        db.commit()
        db.refresh(db_item)
        print(f"Updated menu item ID {item_id}: {db_item.name} - ${db_item.price} ({db_item.category})")
        return True
    except Exception as e:
        print(f"Error updating menu item ID {item_id}: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    # If arguments are provided, treat as command line tool
    if len(sys.argv) > 1:
        if sys.argv[1] == "add" and len(sys.argv) == 5:
            # Add a new menu item: python initialize_menu.py add "Name" price "Category"
            name = sys.argv[2]
            price = float(sys.argv[3])
            category = sys.argv[4]
            add_menu_item(name, price, category)
        elif sys.argv[1] == "update" and len(sys.argv) >= 4:
            # Update a menu item: python initialize_menu.py update item_id [name] [price] [category]
            item_id = int(sys.argv[2])
            name = None
            price = None
            category = None
            
            # Parse optional arguments
            for i in range(3, len(sys.argv)):
                arg = sys.argv[i]
                if arg.startswith("name="):
                    name = arg[5:]
                elif arg.startswith("price="):
                    price = float(arg[6:])
                elif arg.startswith("category="):
                    category = arg[9:]
            
            update_menu_item(item_id, name, price, category)
        else:
            print("Usage:")
            print("  python initialize_menu.py              # Initialize with sample data")
            print("  python initialize_menu.py add \"Name\" price \"Category\"  # Add a new item")
            print("  python initialize_menu.py update item_id [name=Name] [price=Price] [category=Category]  # Update an item")
    else:
        # Default behavior: initialize with sample data
        initialize_menu()