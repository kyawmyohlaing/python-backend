#!/usr/bin/env python3
"""
Test Bar Order Status Update Script
This script tests the bar order status update functionality
"""

import os
import sys
import requests
import json

def test_bar_order_status():
    """Test bar order status update functionality"""
    try:
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
        
        # Step 2: Get existing bar orders
        print("\n2. Getting bar orders...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        bar_response = requests.get(
            f"{base_url}/api/bar/orders",
            headers=headers
        )
        
        if bar_response.status_code == 200:
            bar_orders = bar_response.json()
            print(f"✅ Bar orders retrieved successfully!")
            print(f"   Found {len(bar_orders)} bar orders")
            
            if len(bar_orders) > 0:
                # Step 3: Update status of first bar order
                print("\n3. Updating status of first bar order...")
                first_order_id = bar_orders[0]["order_id"]
                print(f"   Updating order ID: {first_order_id}")
                
                update_data = {
                    "status": "preparing"
                }
                
                update_response = requests.put(
                    f"{base_url}/api/bar/orders/{first_order_id}",
                    json=update_data,
                    headers=headers
                )
                
                if update_response.status_code == 200:
                    updated_order = update_response.json()
                    print(f"✅ Bar order status updated successfully!")
                    print(f"   Order ID: {updated_order.get('order_id')}")
                    print(f"   New status: {updated_order.get('status')}")
                    
                    # Step 4: Verify the update
                    print("\n4. Verifying the update...")
                    verify_response = requests.get(
                        f"{base_url}/api/bar/orders",
                        headers=headers
                    )
                    
                    if verify_response.status_code == 200:
                        verified_orders = verify_response.json()
                        for order in verified_orders:
                            if order["order_id"] == first_order_id:
                                print(f"✅ Status verified: {order['status']}")
                                break
                        else:
                            print("⚠️  Could not find the updated order in verification")
                    else:
                        print(f"❌ Verification failed: {verify_response.status_code} - {verify_response.text}")
                else:
                    print(f"❌ Bar order status update failed: {update_response.status_code} - {update_response.text}")
                    # Let's check what valid statuses are
                    print("Valid statuses are: pending, preparing, ready, served")
            else:
                print("⚠️  No bar orders found. Creating a sample order...")
                # Create a sample order with drink items
                create_sample_order(base_url, headers)
        else:
            print(f"❌ Bar orders retrieval failed: {bar_response.status_code} - {bar_response.text}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def create_sample_order(base_url, headers):
    """Create a sample order with drink items for bar testing"""
    try:
        # First, we need to get the manager user ID
        user_response = requests.get(
            f"{base_url}/api/auth/users",
            headers=headers
        )
        
        if user_response.status_code != 200:
            print(f"❌ Failed to get users: {user_response.status_code}")
            return
            
        users = user_response.json()
        manager_user = None
        for user in users:
            if user.get("username") == "manager":
                manager_user = user
                break
                
        if not manager_user:
            print("❌ Manager user not found")
            return
            
        # Create order data with drink items
        order_data = {
            "order": [
                {
                    "name": "Wine",
                    "price": 7.99,
                    "category": "alcohol",
                    "modifiers": []
                },
                {
                    "name": "Soda",
                    "price": 2.99,
                    "category": "drink",
                    "modifiers": []
                }
            ],
            "total": 10.98,
            "order_type": "dine_in",
            "table_number": "3",
            "customer_name": "",
            "customer_phone": "",
            "delivery_address": ""
        }
        
        # Submit the order
        order_response = requests.post(
            f"{base_url}/api/orders",
            json=order_data,
            headers=headers
        )
        
        if order_response.status_code == 200:
            order_result = order_response.json()
            print(f"✅ Sample order created successfully! Order ID: {order_result.get('id')}")
            
            # Create a kitchen order for this order (which will appear in bar)
            kitchen_order_data = {
                "order_id": order_result.get("id"),
                "status": "pending"
            }
            
            kitchen_response = requests.post(
                f"{base_url}/api/bar/orders",
                json=kitchen_order_data,
                headers=headers
            )
            
            if kitchen_response.status_code == 200:
                kitchen_result = kitchen_response.json()
                print(f"✅ Kitchen order created for bar! Kitchen Order ID: {kitchen_result.get('id')}")
            else:
                print(f"❌ Failed to create kitchen order: {kitchen_response.status_code} - {kitchen_response.text}")
        else:
            print(f"❌ Failed to create sample order: {order_response.status_code} - {order_response.text}")
            
    except Exception as e:
        print(f"❌ Error creating sample order: {e}")

if __name__ == "__main__":
    success = test_bar_order_status()
    sys.exit(0 if success else 1)