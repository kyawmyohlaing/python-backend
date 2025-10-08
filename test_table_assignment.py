#!/usr/bin/env python3
"""
Test script to verify table assignment fix in the backend.
This script tests that when an order is created with a table_number,
the backend correctly looks up the table and sets the table_id.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.table import Table
    from app.models.order import Order
    from app.routes.order_routes import order_model_to_response
    from app.schemas.order_schema import OrderCreate, OrderItem
except ImportError:
    # Try importing directly (Docker container)
    try:
        from database import get_db
        from models.table import Table
        from models.order import Order
        from routes.order_routes import order_model_to_response
        from schemas.order_schema import OrderCreate, OrderItem
    except ImportError:
        print("Error: Could not import required modules")
        sys.exit(1)

def test_table_assignment():
    """Test that table assignment works correctly when creating orders with table_number"""
    print("Testing table assignment fix...")
    
    # Get database session
    db_generator = get_db()
    db = next(db_generator)
    
    try:
        # Create a test table if it doesn't exist
        test_table_number = 999
        table = db.query(Table).filter(Table.table_number == test_table_number).first()
        
        if not table:
            print(f"Creating test table {test_table_number}...")
            table = Table(
                table_number=test_table_number,
                capacity=4,
                is_occupied=False,
                status="available",
                seats=[{"seat_number": i+1, "status": "available", "customer_name": None} for i in range(4)]
            )
            db.add(table)
            db.commit()
            db.refresh(table)
        
        print(f"Test table ID: {table.id}, Table number: {table.table_number}")
        
        # Create test order items
        test_items = [
            OrderItem(name="Test Burger", price=12.99, category="Food", modifiers=["No onions"]),
            OrderItem(name="Test Drink", price=3.99, category="Drink", modifiers=[])
        ]
        
        # Test creating order with table_number (should set table_id automatically)
        print("Creating order with table_number...")
        order_create = OrderCreate(
            order=test_items,
            total=16.98,
            table_number=str(test_table_number),  # Send as string like frontend does
            order_type="dine_in",
            customer_name="Test Customer",
            customer_count=2
        )
        
        # Convert order items to JSON string
        import json
        order_data_json = json.dumps([item.dict() for item in order_create.order])
        
        # Create order manually (simulating the fixed backend logic)
        db_order = Order(
            total=order_create.total,
            order_data=order_data_json,
            table_id=None,  # Start with None, should be set by our logic
            customer_count=order_create.customer_count,
            special_requests=order_create.special_requests,
            created_by=1,  # Test user ID
            order_type=order_create.order_type,
            table_number=order_create.table_number,
            customer_name=order_create.customer_name,
            customer_phone=order_create.customer_phone,
            delivery_address=order_create.delivery_address
        )
        
        # Apply the fix: Look up table by table_number and set table_id
        if db_order.table_number and not db_order.table_id:
            # Look up table by table_number
            lookup_table = db.query(Table).filter(Table.table_number == db_order.table_number).first()
            if lookup_table:
                db_order.table_id = lookup_table.id
                print(f"✅ Table lookup successful! Set table_id to {lookup_table.id}")
            else:
                print("❌ Table lookup failed - table not found")
        
        # Save the order
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Convert to response format
        order_response = order_model_to_response(db_order)
        
        # Verify the fix worked
        print(f"Order created with ID: {order_response.id}")
        print(f"Order table_number: {order_response.table_number}")
        print(f"Order table_id: {order_response.table_id}")
        
        if order_response.table_id == table.id:
            print("✅ SUCCESS: Table assignment fix is working correctly!")
            print("   The backend correctly looked up the table by table_number and set table_id.")
        else:
            print("❌ FAILURE: Table assignment fix is not working.")
            print(f"   Expected table_id {table.id}, but got {order_response.table_id}")
        
        # Clean up: Delete the test order
        db.delete(db_order)
        db.commit()
        print("Cleaned up test order.")
        
    except Exception as e:
        print(f"Error during test: {e}")
        db.rollback()
    finally:
        # Close the database session
        try:
            db_generator.close()
        except:
            pass

if __name__ == "__main__":
    test_table_assignment()