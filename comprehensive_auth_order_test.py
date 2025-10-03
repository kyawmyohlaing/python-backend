#!/usr/bin/env python3
"""
Comprehensive test script demonstrating proper authentication and order submission flow.
This script handles token expiration and refresh automatically.
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration for Docker environment
BASE_URL = "http://localhost:8088"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
ORDERS_ENDPOINT = f"{BASE_URL}/api/orders"
ME_ENDPOINT = f"{BASE_URL}/api/auth/me"

# Test user credentials
TEST_CREDENTIALS = {
    "username": "manager@example.com",
    "password": "manager123"
}

class APIClient:
    def __init__(self):
        self.access_token = None
        self.token_expires_at = None
    
    def authenticate(self):
        """Authenticate and get a new access token"""
        print("=== Authenticating ===")
        
        login_data = {
            "username": TEST_CREDENTIALS["username"],
            "password": TEST_CREDENTIALS["password"]
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            response = requests.post(AUTH_ENDPOINT, data=login_data, headers=headers)
            print(f"Login Status: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                # Token expires in 60 minutes (3600 seconds)
                self.token_expires_at = datetime.now() + timedelta(seconds=3600)
                
                print("✅ Authentication successful!")
                return True
            else:
                print(f"❌ Authentication failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def is_token_valid(self):
        """Check if the current token is still valid"""
        if not self.access_token or not self.token_expires_at:
            return False
        return datetime.now() < self.token_expires_at
    
    def get_valid_token(self):
        """Get a valid token, refreshing if necessary"""
        if not self.is_token_valid():
            print("Token expired or invalid, getting new token...")
            if not self.authenticate():
                return None
        return self.access_token
    
    def submit_order(self, order_data):
        """Submit an order with automatic token handling"""
        token = self.get_valid_token()
        if not token:
            return None
            
        print("\n=== Submitting Order ===")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(ORDERS_ENDPOINT, json=order_data, headers=headers)
            print(f"Order Submission Status: {response.status_code}")
            
            if response.status_code == 200:
                order_response = response.json()
                print("✅ Order submitted successfully!")
                return order_response
            else:
                print(f"❌ Failed to submit order: {response.text}")
                # If it's an auth error, try once more with a fresh token
                if response.status_code == 401:
                    print("Retrying with fresh token...")
                    if self.authenticate():
                        token = self.access_token
                        headers["Authorization"] = f"Bearer {token}"
                        response = requests.post(ORDERS_ENDPOINT, json=order_data, headers=headers)
                        if response.status_code == 200:
                            order_response = response.json()
                            print("✅ Order submitted successfully on retry!")
                            return order_response
                        else:
                            print(f"❌ Still failed after retry: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error submitting order: {e}")
            return None
    
    def get_current_user(self):
        """Get current user information"""
        token = self.get_valid_token()
        if not token:
            return None
            
        print("\n=== Getting Current User ===")
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        try:
            response = requests.get(ME_ENDPOINT, headers=headers)
            print(f"User Info Status: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                print("✅ Retrieved user information!")
                print(f"User: {user_data['username']} ({user_data['email']})")
                print(f"Role: {user_data['role']}")
                return user_data
            else:
                print(f"❌ Failed to get user info: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting user info: {e}")
            return None
    
    def get_orders(self):
        """Get all orders"""
        token = self.get_valid_token()
        if not token:
            return None
            
        print("\n=== Retrieving Orders ===")
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        try:
            response = requests.get(ORDERS_ENDPOINT, headers=headers)
            print(f"Orders Retrieval Status: {response.status_code}")
            
            if response.status_code == 200:
                orders = response.json()
                print(f"✅ Retrieved {len(orders)} orders!")
                return orders
            else:
                print(f"❌ Failed to retrieve orders: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving orders: {e}")
            return None

def main():
    """Main test function"""
    print("FastAPI Comprehensive Authentication and Order Test")
    print("=" * 60)
    
    # Create API client
    client = APIClient()
    
    # Authenticate
    if not client.authenticate():
        print("❌ Failed to authenticate. Exiting.")
        return
    
    # Get user info
    user = client.get_current_user()
    if not user:
        print("❌ Failed to get user information.")
        return
    
    # Submit an order
    order_data = {
        "order": [
            {
                "name": "Pizza",
                "price": 12.99,
                "category": "Main Course",
                "modifiers": ["extra cheese", "pepperoni"]
            },
            {
                "name": "Soda",
                "price": 2.99,
                "category": "Drinks"
            }
        ],
        "total": 15.98,
        "customer_name": "Jane Smith",
        "payment_type": "card"
    }
    
    order = client.submit_order(order_data)
    
    # Get orders
    orders = client.get_orders()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Authentication: {'✅ Success' if client.access_token else '❌ Failed'}")
    print(f"User Info: {'✅ Retrieved' if user else '❌ Failed'}")
    print(f"Order Submission: {'✅ Success' if order else '❌ Failed'}")
    print(f"Orders Retrieval: {'✅ Success' if orders is not None else '❌ Failed'}")
    
    if order:
        print(f"\nSubmitted Order ID: {order['id']}")
    
    if orders is not None:
        print(f"Total Orders: {len(orders)}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()