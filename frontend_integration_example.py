#!/usr/bin/env python3
"""
Example script demonstrating proper frontend integration with authentication
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8088"
MENU_ENDPOINT = f"{BASE_URL}/api/menu/"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
ORDERS_ENDPOINT = f"{BASE_URL}/api/orders/"

class RestaurantAPIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.access_token = None
        self.session = requests.Session()
    
    def authenticate(self, username, password):
        """Authenticate with the API and store the token"""
        login_data = {
            "username": username,
            "password": password
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = self.session.post(
            AUTH_ENDPOINT, 
            data=login_data, 
            headers=headers
        )
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            # Set default headers for authenticated requests
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}"
            })
            print("✅ Authentication successful")
            return True
        else:
            print(f"❌ Authentication failed: {response.text}")
            return False
    
    def get_menu(self):
        """Get menu items (no authentication required)"""
        response = self.session.get(MENU_ENDPOINT)
        if response.status_code == 200:
            menu_items = response.json()
            print(f"✅ Retrieved {len(menu_items)} menu items")
            return menu_items
        else:
            print(f"❌ Failed to get menu: {response.text}")
            return None
    
    def submit_order(self, order_data):
        """Submit an order (authentication required)"""
        # Ensure we have a valid token
        if not self.access_token:
            print("❌ Not authenticated. Please authenticate first.")
            return None
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.post(
            ORDERS_ENDPOINT,
            json=order_data,
            headers=headers
        )
        
        if response.status_code == 200:
            order = response.json()
            print(f"✅ Order submitted successfully. Order ID: {order['id']}")
            return order
        else:
            print(f"❌ Failed to submit order: {response.text}")
            return None

def main():
    """Demonstrate proper frontend integration"""
    print("Restaurant API Frontend Integration Example")
    print("=" * 50)
    
    # Create API client
    client = RestaurantAPIClient()
    
    # 1. Get menu (no authentication needed)
    print("\n1. Fetching menu items...")
    menu = client.get_menu()
    
    if menu:
        print("Sample menu items:")
        for item in menu[:3]:  # Show first 3 items
            print(f"  - {item['name']}: ${item['price']}")
    
    # 2. Authenticate (required for order submission)
    print("\n2. Authenticating...")
    if not client.authenticate("manager@example.com", "manager123"):
        print("❌ Authentication failed. Cannot proceed.")
        return
    
    # 3. Submit order (authentication required)
    print("\n3. Submitting order...")
    order_data = {
        "order": [
            {
                "name": "Burger",
                "price": 8.99,
                "category": "Main Course",
                "modifiers": ["extra cheese"]
            },
            {
                "name": "Fries",
                "price": 3.99,
                "category": "Sides"
            }
        ],
        "total": 12.98,
        "customer_name": "John Doe",
        "payment_type": "cash"
    }
    
    order = client.submit_order(order_data)
    
    if order:
        print("\n🎉 Integration test completed successfully!")
    else:
        print("\n❌ Integration test failed!")

if __name__ == "__main__":
    main()