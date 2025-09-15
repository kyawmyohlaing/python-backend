#!/usr/bin/env python3

"""
Debug script to identify invoice creation issues
"""

import sys
import os
import json
from datetime import datetime

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import the necessary modules
from app.database import Base, engine, get_db
from app.models.invoice import Invoice, InvoiceItem
from app.models.order import Order
from sqlalchemy.orm import Session

def debug_database():
    """Debug database connection and table structure"""
    print("=== Database Debug Information ===")
    
    try:
        # Test database connection
        print("1. Testing database connection...")
        with engine.connect() as conn:
            print("   ✓ Connection successful")
            
            # Check if tables exist
            print("\n2. Checking table existence...")
            tables = ['invoices', 'orders']
            for table in tables:
                exists = engine.dialect.has_table(conn, table)
                print(f"   {'✓' if exists else '✗'} {table} table: {'Exists' if exists else 'Missing'}")
                
            # Show table structure
            print("\n3. Showing invoices table structure...")
            try:
                result = conn.execute("PRAGMA table_info(invoices)")
                columns = result.fetchall()
                if columns:
                    for col in columns:
                        print(f"   - {col[1]} ({col[2]}) {'PRIMARY KEY' if col[5] == 1 else ''}")
                else:
                    print("   No columns found or table doesn't exist")
            except Exception as e:
                print(f"   Error getting table info: {e}")
                
    except Exception as e:
        print(f"   ✗ Connection failed: {e}")

def debug_invoice_creation():
    """Debug invoice creation process"""
    print("\n=== Invoice Creation Debug ===")
    
    try:
        # Get database session
        db_generator = get_db()
        db = next(db_generator)
        
        try:
            print("1. Checking if we can query orders...")
            orders = db.query(Order).all()
            print(f"   Found {len(orders)} orders")
            if orders:
                print(f"   Sample order ID: {orders[0].id if hasattr(orders[0], 'id') else 'No ID'}")
            
            # Try to create a minimal invoice
            print("\n2. Attempting to create test invoice...")
            
            # Create test invoice data
            test_invoice_data = {
                'invoice_number': 'INV-DEBUG-001',
                'order_id': 1,  # Assuming order 1 exists
                'customer_name': 'Debug Customer',
                'order_type': 'dine-in',
                'subtotal': 10.0,
                'tax': 0.0,
                'total': 10.0,
                'invoice_data': json.dumps([
                    {
                        'name': 'Test Item',
                        'category': 'Test',
                        'price': 10.0,
                        'quantity': 1
                    }
                ])
            }
            
            print("   Creating invoice with data:")
            for key, value in test_invoice_data.items():
                print(f"     {key}: {value}")
            
            # Try to insert directly
            try:
                invoice = Invoice(**test_invoice_data)
                db.add(invoice)
                db.commit()
                print("   ✓ Direct insert successful")
                db.refresh(invoice)
                print(f"   Created invoice ID: {invoice.id}")
                
                # Clean up
                db.delete(invoice)
                db.commit()
                print("   ✓ Cleaned up test invoice")
                
            except Exception as e:
                print(f"   ✗ Direct insert failed: {e}")
                db.rollback()
            
        except Exception as e:
            print(f"   ✗ Error during invoice creation test: {e}")
            db.rollback()
        finally:
            try:
                db_generator.close()
            except:
                pass
                
    except Exception as e:
        print(f"   ✗ Failed to get database session: {e}")

def check_models():
    """Check model definitions"""
    print("\n=== Model Definition Check ===")
    
    print("1. Invoice model fields:")
    try:
        invoice_columns = Invoice.__table__.columns
        for column in invoice_columns:
            print(f"   - {column.name}: {column.type} {'(nullable)' if column.nullable else '(required)'}")
    except Exception as e:
        print(f"   Error getting invoice columns: {e}")
        
    print("\n2. Order model fields:")
    try:
        order_columns = Order.__table__.columns
        for column in order_columns:
            print(f"   - {column.name}: {column.type} {'(nullable)' if column.nullable else '(required)'}")
    except Exception as e:
        print(f"   Error getting order columns: {e}")

if __name__ == "__main__":
    print("Starting invoice debugging...")
    debug_database()
    check_models()
    debug_invoice_creation()
    print("\nDebugging complete.")