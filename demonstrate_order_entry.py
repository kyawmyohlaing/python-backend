"""
Demonstration script for Order Entry functionality
This script shows how to create different types of orders with modifiers
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8088/api"

def get_menu_items():
    """Get all menu items"""
    response = requests.get(f"{BASE_URL}/menu")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting menu items: {response.status_code}")
        return []

def create_order(order_data):
    """Create a new order"""
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating order: {response.status_code}")
        print(response.text)
        return None

def demonstrate_dine_in_order():
    """Demonstrate creating a dine-in order with modifiers"""
    print("=== Creating Dine-in Order ===")
    
    # Get menu items
    menu_items = get_menu_items()
    if not menu_items:
        print("No menu items found")
        return
    
    # Create a dine-in order with modifiers
    order_data = {
        "order": [
            {
                "name": menu_items[0]["name"],
                "price": menu_items[0]["price"],
                "category": menu_items[0]["category"],
                "modifiers": ["no onions", "extra cheese"]
            }
        ],
        "total": menu_items[0]["price"],
        "order_type": "dine-in",
        "table_number": "5",
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890"
    }
    
    print("Order data:")
    print(json.dumps(order_data, indent=2))
    
    result = create_order(order_data)
    if result:
        print("Order created successfully:")
        print(json.dumps(result, indent=2))
    else:
        print("Failed to create order")

def demonstrate_takeaway_order():
    """Demonstrate creating a takeaway order with modifiers"""
    print("\n=== Creating Takeaway Order ===")
    
    # Get menu items
    menu_items = get_menu_items()
    if not menu_items:
        print("No menu items found")
        return
    
    # Create a takeaway order with modifiers
    order_data = {
        "order": [
            {
                "name": menu_items[1]["name"],
                "price": menu_items[1]["price"],
                "category": menu_items[1]["category"],
                "modifiers": ["extra spicy"]
            },
            {
                "name": menu_items[2]["name"],
                "price": menu_items[2]["price"],
                "category": menu_items[2]["category"],
                "modifiers": ["no peanuts"]
            }
        ],
        "total": menu_items[1]["price"] + menu_items[2]["price"],
        "order_type": "takeaway",
        "customer_name": "Jane Smith",
        "customer_phone": "987-654-3210"
    }
    
    print("Order data:")
    print(json.dumps(order_data, indent=2))
    
    result = create_order(order_data)
    if result:
        print("Order created successfully:")
        print(json.dumps(result, indent=2))
    else:
        print("Failed to create order")

def demonstrate_delivery_order():
    """Demonstrate creating a delivery order with modifiers"""
    print("\n=== Creating Delivery Order ===")
    
    # Get menu items
    menu_items = get_menu_items()
    if not menu_items:
        print("No menu items found")
        return
    
    # Create a delivery order with modifiers
    order_data = {
        "order": [
            {
                "name": menu_items[0]["name"],
                "price": menu_items[0]["price"],
                "category": menu_items[0]["category"],
                "modifiers": ["no onions"]
            },
            {
                "name": menu_items[3]["name"],
                "price": menu_items[3]["price"],
                "category": menu_items[3]["category"],
                "modifiers": ["extra cheese", "well done"]
            }
        ],
        "total": menu_items[0]["price"] + menu_items[3]["price"],
        "order_type": "delivery",
        "customer_name": "Bob Johnson",
        "customer_phone": "555-123-4567",
        "delivery_address": "123 Main St, City, State 12345"
    }
    
    print("Order data:")
    print(json.dumps(order_data, indent=2))
    
    result = create_order(order_data)
    if result:
        print("Order created successfully:")
        print(json.dumps(result, indent=2))
    else:
        print("Failed to create order")

def main():
    """Main function to demonstrate all order types"""
    print("Order Entry Demonstration")
    print("========================")
    
    # Demonstrate each order type
    demonstrate_dine_in_order()
    demonstrate_takeaway_order()
    demonstrate_delivery_order()
    
    print("\nDemonstration complete!")

if __name__ == "__main__":
    main()