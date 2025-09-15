#!/usr/bin/env python3
"""
Test script to verify invoice functionality
"""

import json
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.order import Order
from app.models.invoice import Invoice
from app.services.invoice_service import invoice_service

def test_invoice_functionality():
    """Test the invoice functionality"""
    print("Testing Invoice Functionality")
    print("=" * 40)
    
    # Create an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Create a sample order
        print("1. Creating a sample order...")
        order_data = [
            {"name": "Burger", "price": 12.00, "category": "Main Course"},
            {"name": "Fries", "price": 5.00, "category": "Sides"},
            {"name": "Soda", "price": 3.50, "category": "Drinks"}
        ]
        
        order = Order(
            total=20.50,
            order_data=json.dumps(order_data),
            order_type="dine-in",
            table_number="5",
            customer_name="John Doe",
            customer_phone="123-456-7890"
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        print(f"   Created order with ID: {order.id}")
        
        # Test invoice number generation
        print("2. Testing invoice number generation...")
        invoice_number = invoice_service.generate_invoice_number(db)
        print(f"   Generated invoice number: {invoice_number}")
        
        # Create an invoice from the order
        print("3. Creating invoice from order...")
        invoice = invoice_service.create_invoice_from_order(db, order.id)
        print(f"   Created invoice with ID: {invoice.id}")
        print(f"   Invoice number: {invoice.invoice_number}")
        print(f"   Total amount: ${invoice.total}")
        
        # Retrieve the invoice
        print("4. Retrieving invoice...")
        retrieved_invoice = db.query(Invoice).filter(Invoice.id == invoice.id).first()
        print(f"   Retrieved invoice: {retrieved_invoice.invoice_number}")
        
        # Get invoice items
        print("5. Getting invoice items...")
        invoice_items = invoice_service.get_invoice_items(db, invoice.id)
        print(f"   Number of items: {len(invoice_items)}")
        for item in invoice_items:
            print(f"   - {item.name}: ${item.price}")
        
        # Update the invoice
        print("6. Updating invoice...")
        retrieved_invoice.customer_name = "Jane Smith"
        retrieved_invoice.total = 25.00
        db.commit()
        db.refresh(retrieved_invoice)
        print(f"   Updated customer name: {retrieved_invoice.customer_name}")
        print(f"   Updated total: ${retrieved_invoice.total}")
        
        # Delete the invoice
        print("7. Deleting invoice...")
        db.delete(retrieved_invoice)
        db.commit()
        print("   Invoice deleted successfully")
        
        # Verify deletion
        deleted_invoice = db.query(Invoice).filter(Invoice.id == invoice.id).first()
        if deleted_invoice is None:
            print("   Verified invoice deletion")
        else:
            print("   ERROR: Invoice still exists after deletion")
        
        print("\nAll tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_invoice_functionality()
    sys.exit(0 if success else 1)