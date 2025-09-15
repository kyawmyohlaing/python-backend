#!/usr/bin/env python3

"""
Debug script to check order-invoice relationship issues
"""

import sys
import os
import json

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import the necessary modules
from app.database import get_db
from app.models.invoice import Invoice
from app.models.order import Order
from app.data.shared_data import sample_orders

def debug_order_storage():
    """Debug how orders are stored"""
    print("=== Order Storage Debug ===")
    
    print("1. Checking sample_orders (in-memory storage):")
    print(f"   Number of sample orders: {len(sample_orders)}")
    if sample_orders:
        print(f"   Sample order IDs: {[order.id for order in sample_orders]}")
        print(f"   First order: {sample_orders[0] if sample_orders else 'None'}")
    
    print("\n2. Checking database orders:")
    try:
        db_generator = get_db()
        db = next(db_generator)
        try:
            db_orders = db.query(Order).all()
            print(f"   Number of database orders: {len(db_orders)}")
            if db_orders:
                print(f"   Database order IDs: {[order.id for order in db_orders]}")
            else:
                print("   No orders found in database")
        except Exception as e:
            print(f"   Error querying database orders: {e}")
        finally:
            try:
                db_generator.close()
            except:
                pass
    except Exception as e:
        print(f"   Error getting database session: {e}")

def debug_invoice_creation_with_sample_order():
    """Debug invoice creation with a sample order"""
    print("\n=== Invoice Creation with Sample Order ===")
    
    if not sample_orders:
        print("   No sample orders available")
        return
        
    # Try to create an invoice for the first sample order
    sample_order = sample_orders[0]
    print(f"1. Using sample order ID: {sample_order.id}")
    print(f"   Order data: {sample_order}")
    
    try:
        db_generator = get_db()
        db = next(db_generator)
        try:
            # Check if order exists in database
            db_order = db.query(Order).filter(Order.id == sample_order.id).first()
            if db_order:
                print("   ✓ Order exists in database")
            else:
                print("   ✗ Order does not exist in database")
                print("   This is likely the issue - invoices can only be created for database orders")
                
            # Try to create invoice
            print("\n2. Attempting to create invoice...")
            
            from app.routes.invoice_routes import generate_invoice_number
            from datetime import datetime
            import json
            
            # Generate invoice number
            invoice_number = generate_invoice_number(db)
            print(f"   Generated invoice number: {invoice_number}")
            
            # Prepare invoice data (matching what the API expects)
            invoice_items = []
            if hasattr(sample_order, 'order') and sample_order.order:
                for item in sample_order.order:
                    invoice_items.append({
                        'name': getattr(item, 'name', 'Unknown Item'),
                        'category': getattr(item, 'category', 'Unknown'),
                        'price': getattr(item, 'price', 0.0),
                        'quantity': 1
                    })
            
            print(f"   Invoice items: {invoice_items}")
            
            # Create invoice record
            invoice_data = {
                'invoice_number': invoice_number,
                'order_id': sample_order.id,
                'customer_name': getattr(sample_order, 'customer_name', 'N/A') or 'N/A',
                'customer_phone': getattr(sample_order, 'customer_phone', None),
                'customer_address': getattr(sample_order, 'delivery_address', None),
                'order_type': getattr(sample_order, 'order_type', 'dine-in'),
                'table_number': getattr(sample_order, 'table_number', None),
                'subtotal': getattr(sample_order, 'total', 0.0),
                'tax': 0.0,
                'total': getattr(sample_order, 'total', 0.0),
                'invoice_data': json.dumps(invoice_items)
            }
            
            print("   Creating invoice with data:")
            for key, value in invoice_data.items():
                print(f"     {key}: {value}")
            
            # Try to create the invoice
            invoice = Invoice(**invoice_data)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            print(f"   ✓ Invoice created successfully with ID: {invoice.id}")
            
            # Clean up
            db.delete(invoice)
            db.commit()
            print("   ✓ Cleaned up test invoice")
            
        except Exception as e:
            print(f"   ✗ Error during invoice creation: {e}")
            import traceback
            traceback.print_exc()
            db.rollback()
        finally:
            try:
                db_generator.close()
            except:
                pass
    except Exception as e:
        print(f"   ✗ Error getting database session: {e}")

if __name__ == "__main__":
    print("Starting order-invoice debugging...")
    debug_order_storage()
    debug_invoice_creation_with_sample_order()
    print("\nDebugging complete.")