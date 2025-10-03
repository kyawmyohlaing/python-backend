#!/usr/bin/env python3
"""
Complete workflow test simulating menu.page user experience
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8088"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
MENU_ENDPOINT = f"{BASE_URL}/api/menu/"
ORDERS_ENDPOINT = f"{BASE_URL}/api/orders/"
PAYMENTS_ENDPOINT = f"{BASE_URL}/api/payments/"

class MenuPageWorkflow:
    def __init__(self):
        self.access_token = None
        self.session = requests.Session()
    
    def authenticate(self, username="manager@example.com", password="manager123"):
        """Authenticate with the API"""
        print("🔐 Authenticating with backend...")
        
        login_data = {
            "username": username,
            "password": password
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
    
    def load_menu(self):
        """Load menu items from backend"""
        print("\n📋 Loading menu items...")
        
        response = self.session.get(MENU_ENDPOINT)
        
        if response.status_code == 200:
            menu_items = response.json()
            print(f"✅ Loaded {len(menu_items)} menu items")
            return menu_items
        else:
            print(f"❌ Failed to load menu: {response.text}")
            return None
    
    def add_to_cart(self, menu_items, selections):
        """Simulate adding items to cart"""
        print("\n🛒 Adding items to cart...")
        cart = []
        
        for selection in selections:
            item_id = selection["item_id"]
            quantity = selection["quantity"]
            modifiers = selection.get("modifiers", [])
            
            # Find item in menu
            item = next((item for item in menu_items if item["id"] == item_id), None)
            if item:
                cart_item = {
                    "name": item["name"],
                    "price": item["price"],
                    "category": item["category"],
                    "quantity": quantity,
                    "modifiers": modifiers
                }
                cart.append(cart_item)
                print(f"   Added {quantity}x {item['name']} to cart")
            else:
                print(f"   ❌ Item with ID {item_id} not found")
        
        return cart
    
    def checkout(self, cart, customer_info):
        """Process checkout with order submission and payment"""
        print("\n💳 Processing checkout...")
        
        # Calculate total
        total = sum(item["price"] * item["quantity"] for item in cart)
        
        # Prepare order data
        order_data = {
            "order": [
                {
                    "name": item["name"],
                    "price": item["price"],
                    "category": item["category"],
                    "modifiers": item["modifiers"]
                } for item in cart
            ],
            "total": total,
            "customer_name": customer_info["name"],
            "customer_phone": customer_info.get("phone", ""),
            "payment_type": customer_info.get("payment_type", "cash")
        }
        
        # Submit order
        print("   Submitting order...")
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.post(ORDERS_ENDPOINT, json=order_data, headers=headers)
        
        if response.status_code == 200:
            order = response.json()
            order_id = order["id"]
            print(f"   ✅ Order #{order_id} submitted successfully")
            
            # Process payment
            print("   Processing payment...")
            payment_data = {
                "order_id": order_id,
                "payment_type": customer_info.get("payment_type", "cash"),
                "amount": total,
                "payment_details": {
                    "timestamp": datetime.now().isoformat(),
                    "reference": f"txn_{int(datetime.now().timestamp())}"
                }
            }
            
            response = self.session.post(f"{PAYMENTS_ENDPOINT}process", json=payment_data, headers=headers)
            
            if response.status_code == 200:
                payment_result = response.json()
                print(f"   ✅ Payment processed successfully")
                print(f"      Invoice ID: {payment_result.get('invoice_id', 'N/A')}")
                return order
            else:
                print(f"   ❌ Payment processing failed: {response.text}")
                return None
        else:
            print(f"   ❌ Order submission failed: {response.text}")
            return None
    
    def get_order_status(self, order_id):
        """Get order status"""
        print(f"\n📊 Checking status for order #{order_id}...")
        
        response = self.session.get(f"{ORDERS_ENDPOINT}{order_id}")
        
        if response.status_code == 200:
            order = response.json()
            print(f"   Order #{order['id']} - Total: ${order['total']}")
            print(f"   Customer: {order['customer_name']}")
            print(f"   Payment Type: {order['payment_type']}")
            return order
        else:
            print(f"   ❌ Failed to get order status: {response.text}")
            return None

def main():
    """Complete menu.page workflow simulation"""
    print("🍽️  Menu.Page Complete Workflow Simulation")
    print("=" * 50)
    
    # Create workflow instance
    workflow = MenuPageWorkflow()
    
    # Step 1: Authenticate
    if not workflow.authenticate():
        print("❌ Workflow failed at authentication step")
        return
    
    # Step 2: Load menu
    menu_items = workflow.load_menu()
    if not menu_items:
        print("❌ Workflow failed at menu loading step")
        return
    
    # Display available menu items
    print("\n📋 Available Menu Items:")
    for i, item in enumerate(menu_items[:5]):  # Show first 5 items
        print(f"   {item['id']}. {item['name']} - ${item['price']}")
    
    # Step 3: Simulate user selections
    print("\n👤 Simulating user selections...")
    selections = [
        {"item_id": menu_items[0]["id"], "quantity": 1, "modifiers": ["extra cheese"]},
        {"item_id": menu_items[1]["id"], "quantity": 2, "modifiers": []},
        {"item_id": menu_items[2]["id"], "quantity": 1, "modifiers": ["no onions"]}
    ]
    
    # Step 4: Add items to cart
    cart = workflow.add_to_cart(menu_items, selections)
    if not cart:
        print("❌ Workflow failed at cart creation step")
        return
    
    # Show cart contents
    print("\n🛒 Cart Contents:")
    cart_total = 0
    for item in cart:
        item_total = item["price"] * item["quantity"]
        cart_total += item_total
        print(f"   {item['quantity']}x {item['name']} - ${item_total:.2f}")
        if item["modifiers"]:
            print(f"      Modifiers: {', '.join(item['modifiers'])}")
    print(f"   Total: ${cart_total:.2f}")
    
    # Step 5: Checkout
    customer_info = {
        "name": "Jane Doe",
        "phone": "555-9876",
        "payment_type": "card"
    }
    
    order = workflow.checkout(cart, customer_info)
    if not order:
        print("❌ Workflow failed at checkout step")
        return
    
    # Step 6: Check order status
    workflow.get_order_status(order["id"])
    
    print("\n🎉 Complete menu.page workflow simulation finished successfully!")
    print(f"Order #{order['id']} has been placed and paid for.")

if __name__ == "__main__":
    main()