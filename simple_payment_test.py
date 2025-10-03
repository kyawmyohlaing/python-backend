#!/usr/bin/env python3
"""
Simple test script for payment workflow
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8088"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
ORDERS_ENDPOINT = f"{BASE_URL}/api/orders/"
PAYMENTS_ENDPOINT = f"{BASE_URL}/api/payments/"

def main():
    print("Testing Payment Workflow")
    print("=" * 30)
    
    # Authenticate
    print("\n1. Authenticating...")
    login_data = {
        "username": "manager@example.com",
        "password": "manager123"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(AUTH_ENDPOINT, data=login_data, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Authentication failed: {response.text}")
        return
    
    token_data = response.json()
    access_token = token_data.get("access_token")
    print("✅ Authentication successful")
    
    # Create an order
    print("\n2. Creating order...")
    order_data = {
        "order": [
            {
                "name": "Burger",
                "price": 8.99,
                "category": "Main Course"
            }
        ],
        "total": 8.99,
        "customer_name": "John Doe",
        "payment_type": "card"
    }
    
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(ORDERS_ENDPOINT, json=order_data, headers=auth_headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to create order: {response.text}")
        return
    
    order = response.json()
    order_id = order['id']
    print(f"✅ Order created successfully. Order ID: {order_id}")
    
    # Process payment
    print("\n3. Processing payment...")
    payment_data = {
        "order_id": order_id,
        "payment_type": "card",
        "amount": 8.99,
        "payment_details": {
            "card_type": "Visa",
            "last_four": "1234"
        }
    }
    
    response = requests.post(f"{PAYMENTS_ENDPOINT}process", json=payment_data, headers=auth_headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to process payment: {response.text}")
        return
    
    payment_result = response.json()
    print("✅ Payment processed successfully")
    print(f"   Invoice ID: {payment_result.get('invoice_id', 'N/A')}")
    
    # Get payment methods
    print("\n4. Getting payment methods...")
    response = requests.get(f"{PAYMENTS_ENDPOINT}methods", headers=auth_headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to get payment methods: {response.text}")
        return
    
    methods = response.json()
    print("✅ Available payment methods:")
    for method, info in methods.items():
        print(f"   - {info['name']} ({method})")
    
    print("\n🎉 Payment workflow test completed successfully!")

if __name__ == "__main__":
    main()