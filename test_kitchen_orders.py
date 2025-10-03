#!/usr/bin/env python3
"""
Test Kitchen Orders Script
This script tests if kitchen orders can be retrieved from the database
"""

import os
import sys

# Set the database URL to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./dev.db'

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_kitchen_orders():
    """Test if kitchen orders can be retrieved"""
    db = None
    try:
        # Import the database and models
        from app.database import get_db
        from app.models.kitchen import KitchenOrder
        from app.models.order import Order
        
        print("Testing kitchen orders retrieval...")
        
        # Get database session
        db = next(get_db())
        
        # Try to query kitchen orders
        kitchen_orders = db.query(KitchenOrder).all()
        
        print(f"Found {len(kitchen_orders)} kitchen orders:")
        for order in kitchen_orders:
            print(f"  - ID: {order.id}, Order ID: {order.order_id}, Status: {order.status}")
            
        # Try to query regular orders
        orders = db.query(Order).all()
        
        print(f"\nFound {len(orders)} regular orders:")
        for order in orders:
            print(f"  - ID: {order.id}, Total: {order.total}, Status: {order.status}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing kitchen orders: {e}")
        return False
    finally:
        if db:
            try:
                db.close()
            except:
                pass

if __name__ == "__main__":
    success = test_kitchen_orders()
    sys.exit(0 if success else 1)