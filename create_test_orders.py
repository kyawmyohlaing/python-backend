#!/usr/bin/env python3
"""
Script to create test orders for analytics testing
"""

import os
import sys
import requests
import json

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def create_test_orders():
    """Create test orders to populate analytics data"""
    base_url = "http://localhost:8088"
    api_prefix = "/api"
    
    print("Creating test orders for analytics...")
    
    # First, login as testadmin to create orders
    print("1. Logging in as testadmin...")
    try:
        login_response = requests.post(
            f"{base_url}{api_prefix}/auth/login",
            data={
                "username": "testadmin",
                "password": "testpassword123"
            }
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            print(f"   Login successful. Token: {token[:10]}...")
        else:
            print(f"   Login failed with status code: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            return
    except Exception as e:
        print(f"   Login failed with error: {str(e)}")
        return
    
    # Set up headers with the token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create some test orders
    test_orders = [
        {
            "table_number": 1,
            "order_type": "dine_in",
            "order_items": [
                {"menu_item_id": 1, "quantity": 2, "price": 8.99},
                {"menu_item_id": 4, "quantity": 1, "price": 2.99}
            ],
            "total": 20.97
        },
        {
            "table_number": 2,
            "order_type": "takeaway",
            "order_items": [
                {"menu_item_id": 2, "quantity": 1, "price": 12.99},
                {"menu_item_id": 5, "quantity": 1, "price": 3.99}
            ],
            "total": 16.98
        },
        {
            "table_number": 3,
            "order_type": "dine_in",
            "order_items": [
                {"menu_item_id": 3, "quantity": 1, "price": 7.99},
                {"menu_item_id": 6, "quantity": 2, "price": 7.99}
            ],
            "total": 23.97
        }
    ]
    
    print("2. Creating test orders...")
    for i, order_data in enumerate(test_orders, 1):
        try:
            response = requests.post(
                f"{base_url}{api_prefix}/orders",
                headers=headers,
                json=order_data
            )
            
            if response.status_code == 200:
                order_result = response.json()
                print(f"   Order {i} created successfully. ID: {order_result.get('id')}")
            else:
                print(f"   Failed to create order {i} with status code: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   Failed to create order {i} with error: {str(e)}")
    
    print("\nTest orders creation completed!")

if __name__ == "__main__":
    create_test_orders()