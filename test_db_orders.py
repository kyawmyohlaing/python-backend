#!/usr/bin/env python3
"""
Test script to verify database order storage functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models.order import Order
import json
from datetime import datetime

def test_database_order_storage():
    """Test that orders can be stored in the database"""
    print("Testing database order storage...")
    
    # Create a test order
    test_order_data = [
        {
            "name": "Pizza",
            "price": 12.99,
            "category": "food",
            "modifiers": ["extra cheese"]
        },
        {
            "name": "Soda",
            "price": 2.99,
            "category": "drink",
            "modifiers": []
        }
    ]
    
    # Get database session
    db_generator = get_db()
    db = next(db_generator)
    
    try:
        # Create order in database
        db_order = Order(
            total=15.98,
            order_data=json.dumps(test_order_data),
            table_id=1,
            customer_count=2,
            special_requests="No onions",
            assigned_seats=json.dumps([1, 2]),
            order_type="dine-in",
            table_number="1",
            customer_name="John Doe",
            customer_phone="555-1234",
            delivery_address=None,
            modifiers=json.dumps(["extra napkins"])
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        print(f"Successfully created order with ID: {db_order.id}")
        
        # Retrieve the order
        retrieved_order = db.query(Order).filter(Order.id == db_order.id).first()
        if retrieved_order:
            print(f"Successfully retrieved order with ID: {retrieved_order.id}")
            print(f"Order total: {retrieved_order.total}")
            print(f"Order data: {retrieved_order.order_data}")
        else:
            print("Failed to retrieve order")
            
        # Clean up - delete the test order
        db.delete(db_order)
        db.commit()
        print("Cleaned up test order")
        
    except Exception as e:
        print(f"Error during test: {e}")
        db.rollback()
    finally:
        # Close database connection
        try:
            next(db_generator)
        except StopIteration:
            pass

if __name__ == "__main__":
    test_database_order_storage()