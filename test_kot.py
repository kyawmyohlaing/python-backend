"""
Test script for Kitchen Order Ticket (KOT) functionality
"""

import os
import sys
from datetime import datetime
from typing import List

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Set environment variables for testing
os.environ["ENVIRONMENT"] = "testing"

def test_kot_generation():
    """Test KOT generation functionality"""
    print("Testing KOT Generation...")
    
    # Import KOT service after setting up environment
    from app.services.kot_service import KOTService
    from app.models.menu import MenuItemBase
    
    # Create a test kitchen order using the correct MenuItemBase
    test_items = [
        MenuItemBase(name="Burger", price=8.99, category="Main Course"),
        MenuItemBase(name="Fries", price=3.99, category="Sides"),
        MenuItemBase(name="Soda", price=2.99, category="Beverages"),
        MenuItemBase(name="Ice Cream", price=4.99, category="Desserts")
    ]
    
    # Simple class to mimic KitchenOrderDetail for testing
    class KitchenOrderDetail:
        def __init__(self, id: int, order_id: int, status: str, created_at: datetime, 
                     updated_at: datetime, order_items: List, total: float,
                     order_type: str = "dine-in", table_number: str = None, customer_name: str = None):
            self.id = id
            self.order_id = order_id
            self.status = status
            self.created_at = created_at
            self.updated_at = updated_at
            self.order_items = order_items
            self.total = total
            self.order_type = order_type
            self.table_number = table_number
            self.customer_name = customer_name
            # Add optional attributes
            self.modifiers = {}
            self.special_requests = ""
    
    kitchen_order = KitchenOrderDetail(
        id=1,
        order_id=101,
        status="pending",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        order_items=test_items,
        total=20.96,
        order_type="dine-in",
        table_number="5",
        customer_name="John Doe"
    )
    
    # Add modifiers and special requests
    kitchen_order.modifiers = {
        "Burger": ["Extra Cheese", "No Onion"],
        "Soda": ["Extra Ice"]
    }
    kitchen_order.special_requests = "All food well done, please"
    
    # Create KOT service
    kot_service = KOTService()
    
    # Test KOT content generation
    kot_content = kot_service.generate_kot_content(kitchen_order)
    print("Generated KOT Content:")
    print(kot_content)
    
    # Test sending to printer
    print("\nTesting Printer Integration...")
    result = kot_service.send_to_printer(kitchen_order, "main_kitchen")
    print(f"Printer result: {result}")
    
    # Test getting printer information
    print("\nTesting Printer Information...")
    print("Available printers:", kot_service.printers)
    
    print("\nKOT Testing Complete!")

if __name__ == "__main__":
    test_kot_generation()