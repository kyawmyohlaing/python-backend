#!/usr/bin/env python3
"""
Create Sample Orders Script
This script creates sample orders and kitchen orders for testing
"""

import os
import sys
import json
from datetime import datetime

# Set the database URL to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./dev.db'

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def create_sample_orders():
    """Create sample orders and kitchen orders"""
    db = None
    try:
        # Import the database and models
        from app.database import get_db
        from app.models.order import Order, OrderType, PaymentType
        from app.models.kitchen import KitchenOrder, KitchenOrderStatus
        from app.models.user import User
        
        print("Creating sample orders...")
        
        # Get database session
        db = next(get_db())
        
        # Get the manager user (assuming it exists)
        manager_user = db.query(User).filter(User.username == "manager").first()
        if not manager_user:
            print("❌ Manager user not found")
            return False
            
        print(f"Using user: {manager_user.username} (ID: {manager_user.id})")
        
        # Create a sample order
        order_data = json.dumps([
            {
                "name": "Burger",
                "price": 8.99,
                "category": "food",
                "modifiers": []
            },
            {
                "name": "Beer",
                "price": 5.99,
                "category": "alcohol",
                "modifiers": []
            }
        ])
        
        sample_order = Order(
            total=14.98,
            order_data=order_data,
            table_number=1,
            order_type=OrderType.DINE_IN,
            customer_count=2,
            customer_name="",
            customer_phone="",
            delivery_address="",
            modifiers=json.dumps([]),
            assigned_seats=json.dumps([]),
            payment_type=PaymentType.CASH,
            created_by=manager_user.id
        )
        
        db.add(sample_order)
        db.commit()
        db.refresh(sample_order)
        
        print(f"✅ Created sample order (ID: {sample_order.id})")
        
        # Create a kitchen order for this order
        kitchen_order = KitchenOrder(
            order_id=sample_order.id,
            table_number=sample_order.table_number,
            order_type="dine_in",
            status=KitchenOrderStatus.PENDING.value
        )
        
        db.add(kitchen_order)
        db.commit()
        db.refresh(kitchen_order)
        
        print(f"✅ Created kitchen order (ID: {kitchen_order.id}) for order {sample_order.id}")
        
        # Create another sample order with only drink items (for bar)
        order_data_2 = json.dumps([
            {
                "name": "Wine",
                "price": 7.99,
                "category": "alcohol",
                "modifiers": []
            },
            {
                "name": "Soda",
                "price": 2.99,
                "category": "drink",
                "modifiers": []
            }
        ])
        
        sample_order_2 = Order(
            total=10.98,
            order_data=order_data_2,
            table_number=2,
            order_type=OrderType.DINE_IN,
            customer_count=2,
            customer_name="",
            customer_phone="",
            delivery_address="",
            modifiers=json.dumps([]),
            assigned_seats=json.dumps([]),
            payment_type=PaymentType.CASH,
            created_by=manager_user.id
        )
        
        db.add(sample_order_2)
        db.commit()
        db.refresh(sample_order_2)
        
        print(f"✅ Created sample order (ID: {sample_order_2.id}) with drink items")
        
        # Create a kitchen order for this order (for bar)
        kitchen_order_2 = KitchenOrder(
            order_id=sample_order_2.id,
            table_number=sample_order_2.table_number,
            order_type="dine_in",
            status=KitchenOrderStatus.PENDING.value
        )
        
        db.add(kitchen_order_2)
        db.commit()
        db.refresh(kitchen_order_2)
        
        print(f"✅ Created kitchen order (ID: {kitchen_order_2.id}) for order {sample_order_2.id}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample orders: {e}")
        if db:
            db.rollback()
        return False
    finally:
        if db:
            try:
                db.close()
            except:
                pass

if __name__ == "__main__":
    success = create_sample_orders()
    sys.exit(0 if success else 1)