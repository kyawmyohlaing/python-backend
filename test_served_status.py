#!/usr/bin/env python3
"""
Test script for the served status extension
This script tests the new served status functionality in the backend
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8088"

def test_served_status():
    """Test the served status functionality"""
    
    print("Testing served status extension...")
    
    # 1. Create a new order
    print("\n1. Creating a new order...")
    order_data = {
        "order": [
            {
                "name": "Test Burger",
                "price": 12.99,
                "category": "Main Course"
            }
        ],
        "total": 12.99,
        "order_type": "dine-in",
        "table_number": "5"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/orders/", json=order_data)
        if response.status_code == 200:
            order = response.json()
            order_id = order["id"]
            print(f"   Created order #{order_id}")
        else:
            print(f"   Failed to create order: {response.status_code}")
            return
    except Exception as e:
        print(f"   Error creating order: {e}")
        return
    
    # 2. Check that the order appears in the kitchen
    print("\n2. Checking kitchen orders...")
    try:
        response = requests.get(f"{BASE_URL}/api/kitchen/orders")
        if response.status_code == 200:
            kitchen_orders = response.json()
            kitchen_order = next((ko for ko in kitchen_orders if ko["order_id"] == order_id), None)
            if kitchen_order:
                print(f"   Order #{order_id} found in kitchen with status: {kitchen_order['status']}")
            else:
                print(f"   Order #{order_id} not found in kitchen")
                return
        else:
            print(f"   Failed to get kitchen orders: {response.status_code}")
            return
    except Exception as e:
        print(f"   Error checking kitchen orders: {e}")
        return
    
    # 3. Test updating status to served via kitchen API
    print("\n3. Updating order status to 'served' via kitchen API...")
    try:
        response = requests.put(
            f"{BASE_URL}/api/kitchen/orders/{order_id}",
            json={"status": "served"}
        )
        if response.status_code == 200:
            updated_order = response.json()
            print(f"   Order status updated to: {updated_order['status']}")
        else:
            print(f"   Failed to update order status: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   Error updating order status: {e}")
        return
    
    # 4. Test the mark-served endpoint
    print("\n4. Testing mark-served endpoint...")
    try:
        # First create another order to test with
        response = requests.post(f"{BASE_URL}/api/orders/", json=order_data)
        if response.status_code == 200:
            order2 = response.json()
            order2_id = order2["id"]
            print(f"   Created second order #{order2_id}")
            
            # Now mark it as served
            response = requests.post(f"{BASE_URL}/api/kitchen/orders/{order2_id}/mark-served")
            if response.status_code == 200:
                result = response.json()
                print(f"   Marked order as served: {result}")
            else:
                print(f"   Failed to mark order as served: {response.status_code}")
        else:
            print(f"   Failed to create second order: {response.status_code}")
    except Exception as e:
        print(f"   Error testing mark-served endpoint: {e}")
    
    # 5. Test invalid status
    print("\n5. Testing invalid status...")
    try:
        response = requests.put(
            f"{BASE_URL}/api/kitchen/orders/{order_id}",
            json={"status": "invalid_status"}
        )
        if response.status_code == 400:
            print("   Correctly rejected invalid status")
        else:
            print(f"   Unexpected response for invalid status: {response.status_code}")
    except Exception as e:
        print(f"   Error testing invalid status: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_served_status()