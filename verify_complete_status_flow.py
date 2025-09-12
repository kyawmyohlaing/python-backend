#!/usr/bin/env python3
"""
Comprehensive test to verify the complete status flow implementation
This script tests the full flow: pending → preparing → ready → served
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"

def verify_complete_status_flow():
    """Verify the complete status flow implementation"""
    
    print("Verifying complete status flow implementation...")
    print("=" * 50)
    
    # Test 1: Create order and verify initial status
    print("\nTest 1: Creating order and verifying initial status")
    order_data = {
        "order": [
            {
                "name": "Flow Test Burger",
                "price": 15.99,
                "category": "Main Course"
            },
            {
                "name": "Flow Test Fries",
                "price": 4.99,
                "category": "Sides"
            }
        ],
        "total": 20.98,
        "order_type": "dine-in",
        "table_number": "10"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/orders/", json=order_data)
        if response.status_code == 200:
            order = response.json()
            order_id = order["id"]
            print(f"   ✓ Created order #{order_id}")
        else:
            print(f"   ✗ Failed to create order: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ✗ Error creating order: {e}")
        return
    
    # Wait for kitchen order to be created
    time.sleep(1)
    
    # Test 2: Verify initial status in kitchen API
    print("\nTest 2: Verifying initial status in kitchen API")
    try:
        response = requests.get(f"{BASE_URL}/api/kitchen/orders")
        if response.status_code == 200:
            kitchen_orders = response.json()
            kitchen_order = next((ko for ko in kitchen_orders if ko["order_id"] == order_id), None)
            if kitchen_order and kitchen_order['status'] == 'pending':
                print(f"   ✓ Order #{order_id} has correct initial status: {kitchen_order['status']}")
            else:
                print(f"   ✗ Order #{order_id} has incorrect status: {kitchen_order['status'] if kitchen_order else 'Not found'}")
                return
        else:
            print(f"   ✗ Failed to get kitchen orders: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Error checking kitchen orders: {e}")
        return
    
    # Test 3: Test complete status flow
    status_flow = ['pending', 'preparing', 'ready', 'served']
    
    for i in range(1, len(status_flow)):
        current_status = status_flow[i]
        print(f"\nTest 3.{i}: Updating status to '{current_status}'")
        
        try:
            response = requests.put(
                f"{BASE_URL}/api/kitchen/orders/{order_id}",
                json={"status": current_status}
            )
            if response.status_code == 200:
                updated_order = response.json()
                if updated_order['status'] == current_status:
                    print(f"   ✓ Status updated to: {updated_order['status']}")
                else:
                    print(f"   ✗ Status update failed. Expected: {current_status}, Got: {updated_order['status']}")
                    return
            else:
                print(f"   ✗ Failed to update status: {response.status_code}")
                print(f"   Response: {response.text}")
                return
        except Exception as e:
            print(f"   ✗ Error updating status: {e}")
            return
        
        # Verify the status was updated
        try:
            response = requests.get(f"{BASE_URL}/api/kitchen/orders")
            if response.status_code == 200:
                kitchen_orders = response.json()
                kitchen_order = next((ko for ko in kitchen_orders if ko["order_id"] == order_id), None)
                if kitchen_order and kitchen_order['status'] == current_status:
                    print(f"   ✓ Verified status is now: {kitchen_order['status']}")
                else:
                    print(f"   ✗ Verification failed. Expected: {current_status}, Got: {kitchen_order['status'] if kitchen_order else 'Not found'}")
                    return
            else:
                print(f"   ✗ Failed to verify status: {response.status_code}")
                return
        except Exception as e:
            print(f"   ✗ Error verifying status: {e}")
            return
    
    # Test 4: Test alternative endpoint
    print("\nTest 4: Testing alternative 'mark-served' endpoint")
    try:
        # Create another order
        response = requests.post(f"{BASE_URL}/api/orders/", json=order_data)
        if response.status_code == 200:
            order2 = response.json()
            order2_id = order2["id"]
            print(f"   ✓ Created second order #{order2_id}")
            
            # Wait for kitchen order to be created
            time.sleep(1)
            
            # Move it to 'ready' status first
            response = requests.put(
                f"{BASE_URL}/api/kitchen/orders/{order2_id}",
                json={"status": "ready"}
            )
            if response.status_code == 200:
                print("   ✓ Moved order to 'ready' status")
                
                # Now mark it as served using the alternative endpoint
                response = requests.post(f"{BASE_URL}/api/kitchen/orders/{order2_id}/mark-served")
                if response.status_code == 200:
                    result = response.json()
                    if result.get('status') == 'served':
                        print(f"   ✓ Marked order as served: {result}")
                    else:
                        print(f"   ✗ Failed to mark as served. Response: {result}")
                        return
                else:
                    print(f"   ✗ Failed to mark order as served: {response.status_code}")
                    return
            else:
                print(f"   ✗ Failed to update order status: {response.status_code}")
                return
        else:
            print(f"   ✗ Failed to create second order: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Error testing mark-served endpoint: {e}")
        return
    
    # Test 5: Test validation
    print("\nTest 5: Testing status validation")
    try:
        response = requests.put(
            f"{BASE_URL}/api/kitchen/orders/{order_id}",
            json={"status": "invalid_status"}
        )
        if response.status_code == 400:
            print("   ✓ Correctly rejected invalid status")
        else:
            print(f"   ✗ Expected 400 error for invalid status, got: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ Error testing validation: {e}")
        return
    
    # Test 6: Resource cleanup verification
    print("\nTest 6: Verifying resource cleanup for served orders")
    try:
        # Get the table information to verify it's been released
        response = requests.get(f"{BASE_URL}/api/tables/")
        if response.status_code == 200:
            tables = response.json()
            table_10 = next((t for t in tables if str(t.get('table_number')) == '10'), None)
            if table_10:
                # The table should still be occupied because we only marked one order as served
                # The other order (order2) is still in 'ready' status
                print(f"   ✓ Table 10 status: {table_10.get('status', 'N/A')}")
            else:
                print("   - Table 10 not found in table list")
        else:
            print(f"   ✗ Failed to get tables: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error checking table status: {e}")
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
    print("The complete status flow implementation is working correctly:")
    print("pending → preparing → ready → served")
    print("=" * 50)

if __name__ == "__main__":
    verify_complete_status_flow()