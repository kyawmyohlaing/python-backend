#!/usr/bin/env python3
"""
Debug script for the complete status flow
This script tests the complete status flow: pending → preparing → ready → served
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8088"

def debug_status_flow():
    """Test the complete status flow"""
    
    print("Debugging complete status flow...")
    
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
        "table_number": "7"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/orders/", json=order_data)
        if response.status_code == 200:
            order = response.json()
            order_id = order["id"]
            print(f"   Created order #{order_id}")
        else:
            print(f"   Failed to create order: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   Error creating order: {e}")
        return
    
    # Wait a moment for the kitchen order to be created
    time.sleep(1)
    
    # 2. Check initial status
    print("\n2. Checking initial kitchen order status...")
    try:
        response = requests.get(f"{BASE_URL}/api/kitchen/orders")
        if response.status_code == 200:
            kitchen_orders = response.json()
            kitchen_order = next((ko for ko in kitchen_orders if ko["order_id"] == order_id), None)
            if kitchen_order:
                print(f"   Order #{order_id} found in kitchen with status: {kitchen_order['status']}")
                if kitchen_order['status'] != 'pending':
                    print(f"   WARNING: Expected 'pending' but got '{kitchen_order['status']}'")
            else:
                print(f"   Order #{order_id} not found in kitchen")
                return
        else:
            print(f"   Failed to get kitchen orders: {response.status_code}")
            return
    except Exception as e:
        print(f"   Error checking kitchen orders: {e}")
        return
    
    # 3. Test status flow: pending → preparing
    print("\n3. Updating status: pending → preparing...")
    try:
        response = requests.put(
            f"{BASE_URL}/api/kitchen/orders/{order_id}",
            json={"status": "preparing"}
        )
        if response.status_code == 200:
            updated_order = response.json()
            print(f"   Order status updated to: {updated_order['status']}")
            if updated_order['status'] != 'preparing':
                print(f"   WARNING: Expected 'preparing' but got '{updated_order['status']}'")
        else:
            print(f"   Failed to update order status: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   Error updating order status: {e}")
        return
    
    # 4. Test status flow: preparing → ready
    print("\n4. Updating status: preparing → ready...")
    try:
        response = requests.put(
            f"{BASE_URL}/api/kitchen/orders/{order_id}",
            json={"status": "ready"}
        )
        if response.status_code == 200:
            updated_order = response.json()
            print(f"   Order status updated to: {updated_order['status']}")
            if updated_order['status'] != 'ready':
                print(f"   WARNING: Expected 'ready' but got '{updated_order['status']}'")
        else:
            print(f"   Failed to update order status: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   Error updating order status: {e}")
        return
    
    # 5. Test status flow: ready → served
    print("\n5. Updating status: ready → served...")
    try:
        response = requests.put(
            f"{BASE_URL}/api/kitchen/orders/{order_id}",
            json={"status": "served"}
        )
        if response.status_code == 200:
            updated_order = response.json()
            print(f"   Order status updated to: {updated_order['status']}")
            if updated_order['status'] != 'served':
                print(f"   WARNING: Expected 'served' but got '{updated_order['status']}'")
        else:
            print(f"   Failed to update order status: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   Error updating order status: {e}")
        return
    
    # 6. Verify final status
    print("\n6. Verifying final status...")
    try:
        response = requests.get(f"{BASE_URL}/api/kitchen/orders")
        if response.status_code == 200:
            kitchen_orders = response.json()
            kitchen_order = next((ko for ko in kitchen_orders if ko["order_id"] == order_id), None)
            if kitchen_order:
                print(f"   Order #{order_id} final status in kitchen: {kitchen_order['status']}")
                if kitchen_order['status'] != 'served':
                    print(f"   WARNING: Expected 'served' but got '{kitchen_order['status']}'")
            else:
                print(f"   Order #{order_id} not found in kitchen (might have been removed)")
        else:
            print(f"   Failed to get kitchen orders: {response.status_code}")
    except Exception as e:
        print(f"   Error checking final kitchen orders: {e}")
    
    # 7. Test alternative method: mark-served endpoint
    print("\n7. Testing alternative method: mark-served endpoint...")
    # Create another order for this test
    try:
        response = requests.post(f"{BASE_URL}/api/orders/", json=order_data)
        if response.status_code == 200:
            order2 = response.json()
            order2_id = order2["id"]
            print(f"   Created second order #{order2_id}")
            
            # Mark it as served using the alternative endpoint
            response = requests.post(f"{BASE_URL}/api/kitchen/orders/{order2_id}/mark-served")
            if response.status_code == 200:
                result = response.json()
                print(f"   Marked order as served: {result}")
            else:
                print(f"   Failed to mark order as served: {response.status_code}")
                print(f"   Response: {response.text}")
        else:
            print(f"   Failed to create second order: {response.status_code}")
    except Exception as e:
        print(f"   Error testing mark-served endpoint: {e}")
    
    print("\nDebug completed!")

if __name__ == "__main__":
    debug_status_flow()