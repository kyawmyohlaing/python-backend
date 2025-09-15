#!/usr/bin/env python3
"""
Integration test for order and invoice system with database storage
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Set environment variables for testing
os.environ["DATABASE_URL"] = "postgresql://postgres:password@localhost:5432/mydb"
os.environ["SECRET_KEY"] = "test-secret-key"

def test_order_and_invoice_system():
    """Test the complete order and invoice system with database storage"""
    print("Testing order and invoice system with database storage...")
    
    try:
        from sqlalchemy.orm import Session
        from app.database import get_db
        from app.models.order import Order
        from app.models.invoice import Invoice
        import json
        from datetime import datetime
        
        # Get database session
        db_generator = get_db()
        db = next(db_generator)
        
        # Test 1: Create an order in the database
        print("\n1. Creating test order in database...")
        
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
        
        print(f"   Successfully created order with ID: {db_order.id}")
        
        # Test 2: Retrieve the order
        print("\n2. Retrieving order from database...")
        
        retrieved_order = db.query(Order).filter(Order.id == db_order.id).first()
        if retrieved_order:
            print(f"   Successfully retrieved order with ID: {retrieved_order.id}")
            print(f"   Order total: {retrieved_order.total}")
        else:
            print("   Failed to retrieve order")
            return False
            
        # Test 3: Create an invoice for the order
        print("\n3. Creating invoice for the order...")
        
        # Generate invoice number
        now = datetime.now()
        year_month = now.strftime("%Y%m")
        invoice_count = db.query(Invoice).filter(
            Invoice.invoice_number.like(f"INV-{year_month}%")
        ).count()
        invoice_number = f"INV-{year_month}-{invoice_count + 1:04d}"
        
        # Prepare invoice items from order data
        order_items = json.loads(retrieved_order.order_data) if retrieved_order.order_data else []
        invoice_items = [
            {
                "name": item["name"],
                "category": item["category"],
                "price": item["price"],
                "quantity": 1
            }
            for item in order_items
        ]
        
        # Create invoice
        db_invoice = Invoice(
            invoice_number=invoice_number,
            order_id=retrieved_order.id,
            customer_name=retrieved_order.customer_name,
            customer_phone=retrieved_order.customer_phone,
            customer_address=retrieved_order.delivery_address,
            order_type=retrieved_order.order_type,
            table_number=retrieved_order.table_number,
            subtotal=15.98,
            tax=1.60,  # 10% tax
            total=17.58,
            invoice_data=json.dumps(invoice_items)
        )
        
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        
        print(f"   Successfully created invoice with number: {db_invoice.invoice_number}")
        
        # Test 4: Retrieve the invoice
        print("\n4. Retrieving invoice from database...")
        
        retrieved_invoice = db.query(Invoice).filter(Invoice.id == db_invoice.id).first()
        if retrieved_invoice:
            print(f"   Successfully retrieved invoice with number: {retrieved_invoice.invoice_number}")
            print(f"   Invoice total: {retrieved_invoice.total}")
        else:
            print("   Failed to retrieve invoice")
            return False
            
        # Test 5: Verify invoice can be retrieved by order ID
        print("\n5. Retrieving invoice by order ID...")
        
        invoice_by_order = db.query(Invoice).filter(Invoice.order_id == retrieved_order.id).first()
        if invoice_by_order:
            print(f"   Successfully retrieved invoice by order ID: {invoice_by_order.invoice_number}")
        else:
            print("   Failed to retrieve invoice by order ID")
            return False
            
        # Clean up - delete test data
        print("\n6. Cleaning up test data...")
        db.delete(db_invoice)
        db.delete(db_order)
        db.commit()
        print("   Test data cleaned up successfully")
        
        # Close database connection
        try:
            next(db_generator)
        except StopIteration:
            pass
            
        print("\nAll tests passed! Order and invoice system is working correctly with database storage.")
        return True
        
    except Exception as e:
        print(f"\nError during test: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to close database connection
        try:
            next(db_generator)
        except:
            pass
            
        return False

if __name__ == "__main__":
    success = test_order_and_invoice_system()
    if success:
        print("\nIntegration test completed successfully!")
    else:
        print("\nIntegration test failed!")
        sys.exit(1)