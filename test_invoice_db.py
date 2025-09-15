#!/usr/bin/env python3

"""
Test script to verify invoice database functionality
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.database import Base, engine, get_db
from app.models.invoice import Invoice
from app.models.order import Order
from sqlalchemy.orm import Session

def test_database_connection():
    """Test database connection and table existence"""
    print("Testing database connection and invoice table...")
    
    try:
        # Test if we can connect to the database
        with engine.connect() as connection:
            print("✓ Database connection successful")
            
        # Test if invoices table exists
        if engine.dialect.has_table(engine.connect(), "invoices"):
            print("✓ Invoices table exists")
        else:
            print("✗ Invoices table does not exist")
            
        # Test if orders table exists
        if engine.dialect.has_table(engine.connect(), "orders"):
            print("✓ Orders table exists")
        else:
            print("✗ Orders table does not exist")
            
        # Test querying invoices
        db_generator = get_db()
        db = next(db_generator)
        try:
            # Try to query invoices
            invoices = db.query(Invoice).all()
            print(f"✓ Successfully queried invoices table, found {len(invoices)} records")
            
            # Try to query orders
            orders = db.query(Order).all()
            print(f"✓ Successfully queried orders table, found {len(orders)} records")
            
        except Exception as e:
            print(f"✗ Error querying tables: {e}")
        finally:
            # Close the database connection
            try:
                db_generator.close()
            except:
                pass
                
    except Exception as e:
        print(f"✗ Database connection failed: {e}")

if __name__ == "__main__":
    test_database_connection()