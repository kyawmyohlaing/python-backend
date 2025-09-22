#!/usr/bin/env python3
"""
Script to debug the invoice endpoint by directly calling the FastAPI route.
"""

import sys
import os
import time

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# Set the environment to development
os.environ["ENVIRONMENT"] = "development"

from main import app
from fastapi.testclient import TestClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_invoice_creation_sequence():
    """Debug the exact sequence that might be causing the issue."""
    try:
        # Create a test client
        client = TestClient(app)
        
        # First, let's pick an order that doesn't have an invoice yet
        logger.info("🔍 Finding an order without an invoice...")
        
        # Get all orders
        from database import get_db
        from models.order import Order
        from models.invoice import Invoice
        db_generator = get_db()
        db = next(db_generator)
        
        # Get all orders
        orders = db.query(Order).all()
        # Get all invoice order IDs
        invoice_order_ids = [i.order_id for i in db.query(Invoice).all()]
        # Find orders without invoices
        orders_without_invoices = [o for o in orders if o.id not in invoice_order_ids]
        
        if not orders_without_invoices:
            logger.error("❌ No orders without invoices found!")
            return False
            
        order = orders_without_invoices[0]
        order_id = order.id
        logger.info(f"✅ Found order {order_id} without invoice")
        
        # Parse order data to create invoice items
        import json
        try:
            # Access the actual value of the column, not the column object
            order_data_value = getattr(order, 'order_data', None)
            order_data_str = str(order_data_value) if order_data_value else ''
            order_items_data = json.loads(order_data_str) if order_data_str else []
        except (json.JSONDecodeError, Exception):
            order_items_data = []
            
        # Create invoice items
        invoice_items = []
        for item_data in order_items_data:
            invoice_items.append({
                'name': item_data.get('name', ''),
                'category': item_data.get('category', ''),
                'price': item_data.get('price', 0.0)
            })
            
        # Prepare invoice data
        invoice_data = {
            'order_id': order_id,
            'customer_name': str(getattr(order, 'customer_name', None)) if getattr(order, 'customer_name', None) else 'N/A',
            'customer_phone': str(getattr(order, 'customer_phone', None)) if getattr(order, 'customer_phone', None) else None,
            'customer_address': str(getattr(order, 'delivery_address', None)) if getattr(order, 'delivery_address', None) else None,
            'order_type': str(getattr(order, 'order_type', 'dine-in')),
            'table_number': str(getattr(order, 'table_number', None)) if getattr(order, 'table_number', None) else None,
            'subtotal': float(getattr(order, 'total', 0.0)) if getattr(order, 'total', None) else 0.0,
            'tax': 0.0,
            'total': float(getattr(order, 'total', 0.0)) if getattr(order, 'total', None) else 0.0,
            'invoice_items': invoice_items
        }
        
        logger.info(f"🔍 Creating invoice for order {order_id}...")
        response = client.post("/api/invoices/", json=invoice_data)
        logger.info(f"Create invoice status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"❌ Failed to create invoice: {response.text}")
            return False
            
        created_invoice = response.json()
        invoice_id = created_invoice.get('id')
        logger.info(f"✅ Created invoice {invoice_id} for order {order_id}")
        
        # Now immediately try to fetch the invoice by order ID
        logger.info(f"🔍 Fetching invoice by order ID {order_id}...")
        response = client.get(f"/api/invoices/order/{order_id}")
        logger.info(f"Fetch invoice status: {response.status_code}")
        
        if response.status_code == 200:
            fetched_invoice = response.json()
            logger.info(f"✅ Successfully fetched invoice {fetched_invoice.get('id')} for order {order_id}")
            return True
        else:
            logger.error(f"❌ Failed to fetch invoice by order ID: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to test invoice creation sequence: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_invoice_endpoint():
    """Debug the invoice endpoint by making a direct call."""
    try:
        # Create a test client
        client = TestClient(app)
        
        # Try to get all invoices
        logger.info("🔍 Testing invoices endpoint...")
        response = client.get("/api/invoices/")
        
        logger.info(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            logger.info("✅ Invoices endpoint working!")
            invoices = response.json()
            logger.info(f"Invoices count: {len(invoices) if isinstance(invoices, list) else 'N/A'}")
        else:
            logger.error("❌ Invoices endpoint failed!")
            return False
            
        # Try to get an invoice by order ID (one that exists)
        logger.info("\n🔍 Testing get invoice by order ID (existing invoice)...")
        response = client.get("/api/invoices/order/1")
        logger.info(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            logger.info("✅ Get invoice by order ID (existing) working!")
            invoice = response.json()
            logger.info(f"Invoice ID: {invoice.get('id')}, Order ID: {invoice.get('order_id')}")
        else:
            logger.error("❌ Get invoice by order ID (existing) failed!")
            logger.error(f"Response: {response.text}")
            return False
            
        # Try to get an invoice by order ID (one that doesn't exist)
        logger.info("\n🔍 Testing get invoice by order ID (non-existing invoice)...")
        response = client.get("/api/invoices/order/999")
        logger.info(f"Status Code: {response.status_code}")
        if response.status_code == 404:
            logger.info("✅ Get invoice by order ID (non-existing) correctly returns 404!")
        else:
            logger.error("❌ Get invoice by order ID (non-existing) should return 404!")
            logger.error(f"Response: {response.text}")
            return False
            
        # Try to create a new invoice
        logger.info("\n🔍 Testing create invoice...")
        invoice_data = {
            "order_id": 4,
            "customer_name": "Debug Customer",
            "order_type": "dine-in",
            "table_number": "10",
            "subtotal": 45.50,
            "tax": 0.0,
            "total": 45.50,
            "invoice_items": [
                {"name": "Pizza", "category": "Main Course", "price": 20.00},
                {"name": "Salad", "category": "Sides", "price": 10.00},
                {"name": "Wine", "category": "Drinks", "price": 15.50}
            ]
        }
        response = client.post("/api/invoices/", json=invoice_data)
        logger.info(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            logger.info("✅ Create invoice working!")
            invoice = response.json()
            invoice_id = invoice.get('id')
            order_id = invoice.get('order_id')
            logger.info(f"Created Invoice ID: {invoice_id}, Order ID: {order_id}")
            
            # Now try to fetch the invoice we just created
            logger.info("\n🔍 Testing fetch newly created invoice by order ID...")
            response = client.get(f"/api/invoices/order/{order_id}")
            logger.info(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                logger.info("✅ Fetch newly created invoice by order ID working!")
                fetched_invoice = response.json()
                logger.info(f"Fetched Invoice ID: {fetched_invoice.get('id')}, Order ID: {fetched_invoice.get('order_id')}")
            else:
                logger.error("❌ Fetch newly created invoice by order ID failed!")
                logger.error(f"Response: {response.text}")
                return False
        else:
            logger.error("❌ Create invoice failed!")
            logger.error(f"Response: {response.text}")
            return False
            
        return True
            
    except Exception as e:
        logger.error(f"Failed to test invoices endpoint: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Debugging invoice endpoint directly...")
    print()
    
    print("=== Testing basic invoice functionality ===")
    success1 = debug_invoice_endpoint()
    
    print("\n=== Testing invoice creation sequence ===")
    success2 = debug_invoice_creation_sequence()
    
    print()
    if success1 and success2:
        print("✅ All invoice endpoint tests completed successfully!")
    else:
        print("❌ Some invoice endpoint tests failed!")