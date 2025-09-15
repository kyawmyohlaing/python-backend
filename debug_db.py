#!/usr/bin/env python3
"""
Debug script to check database connection and order table
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy import text
from app.database import engine
from app.models.order import Order
from app.models import Base

def debug_database():
    """Debug database connection and order table"""
    print("Debugging database connection...")
    
    try:
        # Test database connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful")
            
            # Check if orders table exists
            inspector = connection.dialect.inspector(engine)
            tables = inspector.get_table_names()
            print(f"Database tables: {tables}")
            
            if 'orders' in tables:
                print("Orders table exists")
                # Get table info
                columns = inspector.get_columns('orders')
                print("Orders table columns:")
                for column in columns:
                    print(f"  - {column['name']}: {column['type']}")
            else:
                print("Orders table does not exist")
                
    except Exception as e:
        print(f"Database connection error: {e}")
        
    # Check Order model
    print(f"\nOrder model table name: {Order.__tablename__}")
    print(f"Order model columns: {Order.__table__.columns.keys()}")

if __name__ == "__main__":
    debug_database()