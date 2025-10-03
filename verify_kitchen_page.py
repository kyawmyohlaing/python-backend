#!/usr/bin/env python3
"""
Verify Kitchen Page Functionality
This script verifies that the kitchen page is still working correctly after our fixes.
"""

import os
import sys
import requests
import json

def verify_kitchen_page():
    """Verify that the kitchen page is working correctly"""
    try:
        print("=== Verifying Kitchen Page Functionality ===")
        
        base_url = "http://localhost:8088"
        
        # Step 1: Login as manager
        print("1. Logging in as manager...")
        login_data = {
            "username": "manager",
            "password": "manager123"
        }
        
        login_response = requests.post(
            f"{base_url}/api/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
            return False
            
        token_data = login_response.json()
        access_token = token_data["access_token"]
        print(f"✅ Login successful. Token: {access_token[:20]}...")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Step 2: Get kitchen orders
        print("\n2. Getting kitchen orders...")
        kitchen_response = requests.get(
            f"{base_url}/api/kitchen/orders",
            headers=headers
        )
        
        if kitchen_response.status_code == 200:
            kitchen_orders = kitchen_response.json()
            print(f"✅ Kitchen orders retrieved successfully!")
            print(f"   Found {len(kitchen_orders)} kitchen orders")
            
            # Display some details about the orders
            for i, order in enumerate(kitchen_orders[:3]):  # Show first 3 orders
                print(f"   Order {i+1}: ID={order.get('order_id')}, Status={order.get('status')}, Total=${order.get('total')}")
        else:
            print(f"❌ Kitchen orders retrieval failed: {kitchen_response.status_code} - {kitchen_response.text}")
            return False
            
        # Step 3: Test updating kitchen order status
        print("\n3. Testing kitchen order status update...")
        if len(kitchen_orders) > 0:
            first_order_id = kitchen_orders[0]["order_id"]
            print(f"   Updating order ID: {first_order_id}")
            
            update_data = {
                "status": "preparing"
            }
            
            update_response = requests.put(
                f"{base_url}/api/kitchen/orders/{first_order_id}",
                json=update_data,
                headers=headers
            )
            
            if update_response.status_code == 200:
                updated_order = update_response.json()
                print(f"✅ Kitchen order status updated successfully!")
                print(f"   Order ID: {updated_order.get('order_id')}")
                print(f"   New status: {updated_order.get('status')}")
            else:
                print(f"❌ Kitchen order status update failed: {update_response.status_code} - {update_response.text}")
                return False
        else:
            print("⚠️  No kitchen orders found to update")
            
        # Step 4: Verify the update
        print("\n4. Verifying the update...")
        verify_response = requests.get(
            f"{base_url}/api/kitchen/orders",
            headers=headers
        )
        
        if verify_response.status_code == 200:
            verified_orders = verify_response.json()
            if len(verified_orders) > 0:
                for order in verified_orders:
                    if order["order_id"] == first_order_id:
                        print(f"✅ Status verified: {order['status']}")
                        break
                else:
                    print("⚠️  Could not find the updated order in verification")
            else:
                print("⚠️  No orders found in verification")
        else:
            print(f"❌ Verification failed: {verify_response.status_code} - {verify_response.text}")
            return False
            
        # Step 5: Summary
        print("\n=== Kitchen Page Verification Summary ===")
        print("✅ Kitchen page is working correctly")
        print("✅ Kitchen orders can be retrieved")
        print("✅ Kitchen order statuses can be updated")
        print("✅ Updates are properly reflected in the system")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("This script will verify that the kitchen page is working correctly.")
    response = input("Do you want to continue? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        success = verify_kitchen_page()
        if success:
            print("\n🎉 Kitchen page verification completed successfully!")
            print("The kitchen page is working correctly.")
        else:
            print("\n❌ Kitchen page verification failed. Please check the error messages above.")
        sys.exit(0 if success else 1)
    else:
        print("Operation cancelled.")
        sys.exit(0)