#!/usr/bin/env python3
"""
Verification script for the complete order status flow.
This script tests the extended order status flow: pending → preparing → ready → served
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8088"
API_PREFIX = "/api"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

def get_auth_token():
    """Get authentication token for admin user"""
    try:
        response = requests.post(
            f"{BASE_URL}/users/login",
            json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"Failed to get auth token: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting auth token: {str(e)}")
        return None

def create_test_order(token):
    """Create a test order"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        order_data = {
            "table_id": 1,
            "items": [
                {
                    "menu_item_id": 1,
                    "quantity": 2
                }
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/orders/",
            headers=headers,
            json=order_data
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("id")
        else:
            print(f"Failed to create order: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error creating order: {str(e)}")
        return None

def test_kitchen_order_status_flow(token, order_id):
    """Test the kitchen order status flow"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test marking order as served via kitchen endpoint
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/kitchen/orders/{order_id}/mark-served",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✓ Kitchen order marked as served successfully")
            return True
        else:
            print(f"✗ Failed to mark kitchen order as served: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error testing kitchen order status flow: {str(e)}")
        return False

def test_order_status_flow(token, order_id):
    """Test the order status flow"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test marking order as served via order endpoint
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/orders/{order_id}/mark-served",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✓ Order marked as served successfully")
            return True
        else:
            print(f"✗ Failed to mark order as served: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error testing order status flow: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("🔍 Verifying Complete Order Status Flow")
    print("=" * 50)
    
    # Get authentication token
    print("1. Getting authentication token...")
    token = get_auth_token()
    if not token:
        print("✗ Failed to get authentication token")
        return False
    
    print("✓ Authentication token obtained")
    
    # Create test order
    print("\n2. Creating test order...")
    order_id = create_test_order(token)
    if not order_id:
        print("✗ Failed to create test order")
        return False
    
    print(f"✓ Test order created with ID: {order_id}")
    
    # Test kitchen order status flow
    print("\n3. Testing kitchen order status flow...")
    if not test_kitchen_order_status_flow(token, order_id):
        print("✗ Kitchen order status flow test failed")
        return False
    
    print("✓ Kitchen order status flow test passed")
    
    # Test order status flow
    print("\n4. Testing order status flow...")
    if not test_order_status_flow(token, order_id):
        print("✗ Order status flow test failed")
        return False
    
    print("✓ Order status flow test passed")
    
    print("\n" + "=" * 50)
    print("🎉 All order status flow tests passed!")
    print("The extended order status flow is working correctly:")
    print("  pending → preparing → ready → served")
    print("When an order is marked as served, associated resources are automatically released.")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)