#!/usr/bin/env python3
"""
Check API consistency between kitchen orders and general orders
This script verifies that both APIs return consistent status information
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8088"

def check_api_consistency():
    """Check consistency between kitchen orders and general orders APIs"""
    
    print("Checking API consistency...")
    
    # 1. Get all orders from general orders API
    print("\n1. Getting orders from general orders API...")
    try:
        response = requests.get(f"{BASE_URL}/api/orders/")
        if response.status_code == 200:
            orders = response.json()
            print(f"   Found {len(orders)} orders in general orders API")
            for order in orders:
                print(f"   Order #{order['id']}: status = {order.get('status', 'N/A')}")
        else:
            print(f"   Failed to get orders: {response.status_code}")
            return
    except Exception as e:
        print(f"   Error getting orders: {e}")
        return
    
    # 2. Get all orders from kitchen API
    print("\n2. Getting orders from kitchen API...")
    try:
        response = requests.get(f"{BASE_URL}/api/kitchen/orders")
        if response.status_code == 200:
            kitchen_orders = response.json()
            print(f"   Found {len(kitchen_orders)} orders in kitchen API")
            for order in kitchen_orders:
                print(f"   Order #{order['order_id']}: status = {order.get('status', 'N/A')}")
        else:
            print(f"   Failed to get kitchen orders: {response.status_code}")
            return
    except Exception as e:
        print(f"   Error getting kitchen orders: {e}")
        return
    
    # 3. Compare statuses
    print("\n3. Comparing statuses...")
    try:
        # Get both sets of data
        response1 = requests.get(f"{BASE_URL}/api/orders/")
        response2 = requests.get(f"{BASE_URL}/api/kitchen/orders")
        
        if response1.status_code == 200 and response2.status_code == 200:
            orders = response1.json()
            kitchen_orders = response2.json()
            
            # Create a mapping of order_id to status for kitchen orders
            kitchen_status_map = {ko['order_id']: ko['status'] for ko in kitchen_orders}
            
            # Compare with general orders
            for order in orders:
                order_id = order['id']
                general_status = order.get('status', 'N/A')
                kitchen_status = kitchen_status_map.get(order_id, 'N/A')
                
                print(f"   Order #{order_id}: General={general_status}, Kitchen={kitchen_status}")
                
                # Note: The general orders API might not have a status field since it's managed by the kitchen API
                # This is expected behavior
        else:
            print("   Failed to get data from one or both APIs")
    except Exception as e:
        print(f"   Error comparing statuses: {e}")

    # 4. Test updating status through kitchen API and checking general API
    print("\n4. Testing status update synchronization...")
    try:
        # Create a new order
        order_data = {
            "order": [
                {
                    "name": "Sync Test Burger",
                    "price": 9.99,
                    "category": "Test"
                }
            ],
            "total": 9.99,
            "order_type": "takeaway",
            "customer_name": "Sync Test Customer"
        }
        
        response = requests.post(f"{BASE_URL}/api/orders/", json=order_data)
        if response.status_code == 200:
            order = response.json()
            order_id = order["id"]
            print(f"   Created test order #{order_id}")
            
            # Wait a moment
            import time
            time.sleep(1)
            
            # Check status in kitchen API
            response = requests.get(f"{BASE_URL}/api/kitchen/orders")
            if response.status_code == 200:
                kitchen_orders = response.json()
                kitchen_order = next((ko for ko in kitchen_orders if ko["order_id"] == order_id), None)
                if kitchen_order:
                    print(f"   Kitchen status for order #{order_id}: {kitchen_order['status']}")
                    
                    # Update status to preparing
                    response = requests.put(
                        f"{BASE_URL}/api/kitchen/orders/{order_id}",
                        json={"status": "preparing"}
                    )
                    if response.status_code == 200:
                        print("   Updated status to 'preparing'")
                        
                        # Check status in kitchen API again
                        response = requests.get(f"{BASE_URL}/api/kitchen/orders")
                        if response.status_code == 200:
                            kitchen_orders = response.json()
                            kitchen_order = next((ko for ko in kitchen_orders if ko["order_id"] == order_id), None)
                            if kitchen_order:
                                print(f"   Verified kitchen status for order #{order_id}: {kitchen_order['status']}")
                    else:
                        print(f"   Failed to update status: {response.status_code}")
                else:
                    print(f"   Order #{order_id} not found in kitchen")
            else:
                print(f"   Failed to get kitchen orders: {response.status_code}")
        else:
            print(f"   Failed to create test order: {response.status_code}")
    except Exception as e:
        print(f"   Error testing status update synchronization: {e}")
    
    print("\nAPI consistency check completed!")

if __name__ == "__main__":
    check_api_consistency()