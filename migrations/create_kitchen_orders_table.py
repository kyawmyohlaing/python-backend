#!/usr/bin/env python3
"""
Migration script to create kitchen_orders table in the database.
This script can be run inside or outside of Docker containers.
"""

import os
import sys
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime

# Try to import database configuration from different possible locations
try:
    # Try direct import first (when running inside the app)
    from database import DATABASE_URL
    from models.kitchen import KitchenOrder
    from models.order import Order
except ImportError:
    try:
        # Try relative import (when running as script)
        # Add parent directory to path
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from database import DATABASE_URL
        from models.kitchen import KitchenOrder
        from models.order import Order
    except ImportError:
        # If we can't import, use default configuration
        DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://pos_user:pos_password@localhost:5432/mydb')

def create_kitchen_orders_table():
    """Create the kitchen_orders table in the database"""
    try:
        print(f"Connecting to database: {DATABASE_URL}")
        engine = create_engine(DATABASE_URL)
        
        # Create the kitchen_orders table
        # We'll define the table structure directly to avoid import issues
        metadata = MetaData()
        
        kitchen_orders_table = Table('kitchen_orders', metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('order_id', Integer, ForeignKey('orders.id')),
            Column('status', String, default='pending'),
            Column('created_at', TIMESTAMP, default=datetime.utcnow),
            Column('updated_at', TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
        )
        
        # Create the table
        metadata.create_all(engine)
        print("✅ Kitchen orders table created successfully!")
        
        # Verify the table was created
        with engine.connect() as conn:
            result = conn.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'kitchen_orders')")
            exists = result.fetchone()[0]
            if exists:
                print("✅ Table verification successful!")
                return True
            else:
                print("❌ Table verification failed!")
                return False
                
    except Exception as e:
        print(f"❌ Error creating kitchen orders table: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_database_connection():
    """Check if we can connect to the database"""
    try:
        print(f"Testing database connection to: {DATABASE_URL}")
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute("SELECT version()")
            version = result.fetchone()[0]
            print(f"✅ Database connection successful! PostgreSQL version: {version}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Kitchen Orders Table Migration ===")
    
    # Check database connection first
    if not check_database_connection():
        print("Cannot proceed without database connection")
        sys.exit(1)
    
    # Create the table
    success = create_kitchen_orders_table()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("You can now restart your application to use the database-backed kitchen orders system.")
    else:
        print("\n💥 Migration failed!")
        sys.exit(1)