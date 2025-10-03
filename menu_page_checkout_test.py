#!/usr/bin/env python3
"""
Test script simulating menu.page checkout flow
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8088"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
ORDERS_ENDPOINT = f"{BASE_URL}/api/orders/"

class MenuPageCheckoutTester:
    def __init__(self):
        self.access_token = None
        self.session = requests.Session()
    
    def authenticate(self):
        """Authenticate with the API"""
        login_data = {
            "username": "manager@example.com",
            "password": "manager123"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = self.session.post(AUTH_ENDPOINT, data=login_data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}"
            })
            print("✅ Authentication successful")
            return True
        else:
            print(f"❌ Authentication failed: {response.text}")
            return False
    
    def simulate_menu_page_checkout(self, cart_items, customer_info):
        """Simulate the checkout flow from menu.page"""
        print("\n=== Simulating menu.page Checkout ===")
        
        # Step 1: Authenticate (if not already authenticated)
        if not self.access_token:
            if not self.authenticate():
                return None
        
        # Step 2: Prepare order data (as menu.page would)
        order_data = {
            "order": [
                {
                    "name": item["name"],
                    "price": item["price"],
                    "category": item.get("category", "food"),
                    "modifiers": item.get("modifiers", [])
                } for item in cart_items
            ],
            "total": sum(item["price"] * item.get("quantity", 1) for item in cart_items),
            "customer_name": customer_info.get("name", "Customer"),
            "customer_phone": customer_info.get("phone", ""),
            "payment_type": customer_info.get("payment_type", "cash")
        }
        
        # Step 3: Submit order with proper authentication
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.post(ORDERS_ENDPOINT, json=order_data, headers=headers)
        
        if response.status_code == 200:
            order = response.json()
            print("✅ Order submitted successfully!")
            print(f"   Order ID: {order['id']}")
            print(f"   Total: ${order['total']}")
            print(f"   Customer: {order['customer_name']}")
            print(f"   Payment Type: {order['payment_type']}")
            return order
        else:
            print(f"❌ Failed to submit order: {response.text}")
            return None

def main():
    """Test the menu.page checkout flow"""
    print("Menu.Page Checkout Test")
    print("=" * 30)
    
    # Create tester instance
    tester = MenuPageCheckoutTester()
    
    # Simulate cart items (as they would exist in menu.page)
    cart_items = [
        {
            "name": "Grilled Chicken Sandwich",
            "price": 12.99,
            "category": "Main Course",
            "modifiers": ["extra cheese", "avocado"],
            "quantity": 1
        },
        {
            "name": "French Fries",
            "price": 4.99,
            "category": "Sides",
            "modifiers": ["extra salt"],
            "quantity": 1
        },
        {
            "name": "Soft Drink",
            "price": 2.99,
            "category": "Beverages",
            "modifiers": [],
            "quantity": 2
        }
    ]
    
    # Simulate customer info (as collected during checkout)
    customer_info = {
        "name": "John Smith",
        "phone": "555-1234",
        "payment_type": "card"
    }
    
    # Perform checkout
    order = tester.simulate_menu_page_checkout(cart_items, customer_info)
    
    if order:
        print("\n🎉 Menu.page checkout test completed successfully!")
        print(f"Order #{order['id']} has been placed.")
    else:
        print("\n❌ Menu.page checkout test failed!")

if __name__ == "__main__":
    main()