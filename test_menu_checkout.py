#!/usr/bin/env python3
"""
Test Menu Page Checkout Script
This script tests the menu page checkout functionality
"""

import os
import sys
import requests
import json

def test_menu_checkout():
    """Test menu page checkout functionality"""
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
        
        # Step 2: Get menu items to simulate menu page
        print("\n2. Getting menu items...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        menu_response = requests.get(
            f"{base_url}/api/menu",
            headers=headers
        )
        
        if menu_response.status_code == 200:
            menu_items = menu_response.json()
            print(f"✅ Menu items retrieved successfully!")
            print(f"   Found {len(menu_items)} menu items")
            
            # Select some items for the order
            if len(menu_items) > 0:
                # Select first food item and first drink item
                food_item = None
                drink_item = None
                
                for item in menu_items:
                    if item.get("category") in ["food"] and food_item is None:
                        food_item = item
                    elif item.get("category") in ["drink", "alcohol"] and drink_item is None:
                        drink_item = item
                        
                order_items = []
                if food_item:
                    order_items.append({
                        "name": food_item["name"],
                        "price": food_item["price"],
                        "category": food_item["category"],
                        "id": food_item.get("id", 0),
                        "modifiers": []
                    })
                    
                if drink_item:
                    order_items.append({
                        "name": drink_item["name"],
                        "price": drink_item["price"],
                        "category": drink_item["category"],
                        "id": drink_item.get("id", 0),
                        "modifiers": []
                    })
                
                # Step 3: Submit order (simulate menu page checkout)
                print("\n3. Submitting order (simulating menu page checkout)...")
                order_data = {
                    "order": order_items,
                    "total": sum(item["price"] for item in order_items),
                    "orderType": "DINE-IN",
                    "tableNumber": "5",
                    "customerName": "",
                    "customerPhone": "",
                    "deliveryAddress": ""
                }
                
                print(f"   Order data: {json.dumps(order_data, indent=2)}")
                
                order_response = requests.post(
                    f"{base_url}/api/orders",
                    json=order_data,
                    headers=headers
                )
                
                if order_response.status_code == 200:
                    order_result = order_response.json()
                    print(f"✅ Order submitted successfully!")
                    print(f"   Order ID: {order_result.get('id')}")
                    print(f"   Total: ${order_result.get('total')}")
                    print(f"   Order type: {order_result.get('order_type')}")
                    print(f"   Table number: {order_result.get('table_number')}")
                    
                    # Step 4: Verify the order was created
                    print("\n4. Verifying order creation...")
                    verify_response = requests.get(
                        f"{base_url}/api/orders/{order_result.get('id')}",
                        headers=headers
                    )
                    
                    if verify_response.status_code == 200:
                        verified_order = verify_response.json()
                        print(f"✅ Order verified successfully!")
                        print(f"   Order ID: {verified_order.get('id')}")
                        print(f"   Total: ${verified_order.get('total')}")
                        print(f"   Status: {verified_order.get('status')}")
                        
                        # Step 5: Check if kitchen/bar orders were created
                        print("\n5. Checking kitchen/bar orders...")
                        
                        # Check kitchen orders
                        kitchen_response = requests.get(
                            f"{base_url}/api/kitchen/orders",
                            headers=headers
                        )
                        
                        if kitchen_response.status_code == 200:
                            kitchen_orders = kitchen_response.json()
                            kitchen_order_found = False
                            for k_order in kitchen_orders:
                                if k_order.get("order_id") == verified_order.get("id"):
                                    kitchen_order_found = True
                                    print(f"✅ Kitchen order created for order {verified_order.get('id')}")
                                    print(f"   Kitchen order status: {k_order.get('status')}")
                                    break
                                    
                            if not kitchen_order_found:
                                print("⚠️  Kitchen order not found for this order")
                        else:
                            print(f"❌ Failed to get kitchen orders: {kitchen_response.status_code}")
                            
                    else:
                        print(f"❌ Order verification failed: {verify_response.status_code} - {verify_response.text}")
                else:
                    print(f"❌ Order submission failed: {order_response.status_code} - {order_response.text}")
                    print(f"   Response: {order_response.text}")
            else:
                print("❌ No menu items found")
        else:
            print(f"❌ Menu items retrieval failed: {menu_response.status_code} - {menu_response.text}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_menu_checkout()
    sys.exit(0 if success else 1)