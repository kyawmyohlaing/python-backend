#!/usr/bin/env python3
"""
Test script for KOT service with physical printer
"""

import sys
import os
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_kot_with_physical_printer():
    """Test KOT generation and printing with physical printer"""
    
    # Import the KOT service
    try:
        from app.services.kot_service import KOTService
        # Import the correct MenuItem class
        from app.models.menu import MenuItemBase
        print("✓ KOT Service imported successfully")
    except Exception as e:
        print(f"✗ Failed to import KOT Service: {e}")
        return
    
    # Create KOT service instance
    kot_service = KOTService()
    
    # Create a test kitchen order using the correct MenuItemBase
    test_items = [
        MenuItemBase(name="Cheeseburger", price=8.99, category="Main Course"),
        MenuItemBase(name="French Fries", price=3.99, category="Sides"),
        MenuItemBase(name="Coca Cola", price=2.99, category="Beverages"),
        MenuItemBase(name="Apple Pie", price=4.99, category="Desserts")
    ]
    
    # Simple class to mimic KitchenOrderDetail for testing
    class KitchenOrderDetail:
        def __init__(self, id, order_id, status, created_at, updated_at, 
                     order_items, total, order_type="dine-in", 
                     table_number=None, customer_name=None):
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
    
    print("\n1. Testing KOT content generation...")
    try:
        kot_content = kot_service.generate_kot_content(kitchen_order)
        print("✓ KOT content generated successfully")
        print("\nGenerated KOT Content:")
        print(kot_content)
    except Exception as e:
        print(f"✗ Failed to generate KOT content: {e}")
        return
    
    print("\n2. Testing printer status...")
    try:
        status = kot_service.get_printer_status("main_kitchen")
        print(f"✓ Printer status check successful: {status}")
    except Exception as e:
        print(f"✗ Failed to check printer status: {e}")
    
    print("\n3. Testing KOT printing to main kitchen printer...")
    try:
        result = kot_service.send_to_printer(kitchen_order, "main_kitchen")
        if result.get("success"):
            print("✓ KOT sent to main kitchen printer successfully")
            if "content" in result:
                print("  Content was:")
                print(result["content"])
        else:
            print(f"✗ Failed to send KOT to main kitchen printer: {result.get('message')}")
    except Exception as e:
        print(f"✗ Error sending KOT to main kitchen printer: {e}")
    
    print("\n4. Testing KOT printing to beverage station (KDS)...")
    try:
        result = kot_service.send_to_printer(kitchen_order, "beverage_station")
        if result.get("success"):
            print("✓ KOT sent to beverage station (KDS) successfully")
            if "kds_data" in result:
                print("  KDS data was sent:")
                import json
                print(json.dumps(result["kds_data"], indent=2))
        else:
            print(f"✗ Failed to send KOT to beverage station: {result.get('message')}")
    except Exception as e:
        print(f"✗ Error sending KOT to beverage station: {e}")
    
    print("\n5. Testing printer connection simulation...")
    print("Since python-escpos is not installed, the system is simulating printer output.")
    print("To test with actual hardware, install python-escpos:")
    print("  pip install python-escpos")
    print("\nThen configure your printer details in the KOT service configuration.")

def main():
    """Main function"""
    print("KOT Service Physical Printer Test")
    print("=" * 40)
    
    test_kot_with_physical_printer()
    
    print("\nTest completed.")

if __name__ == "__main__":
    main()