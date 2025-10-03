#!/usr/bin/env python3
"""
Test Kitchen and Bar APIs Script
This script tests the kitchen and bar API endpoints
"""

import os
import sys
import requests
import json

def test_kitchen_bar_apis():
    """Test kitchen and bar API endpoints"""
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
        
        # Step 2: Test kitchen orders endpoint
        print("\n2. Testing kitchen orders endpoint...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        kitchen_response = requests.get(
            f"{base_url}/api/kitchen/orders",
            headers=headers
        )
        
        if kitchen_response.status_code == 200:
            kitchen_orders = kitchen_response.json()
            print(f"✅ Kitchen orders retrieved successfully!")
            print(f"   Found {len(kitchen_orders)} kitchen orders")
            if len(kitchen_orders) > 0:
                print(f"   First order ID: {kitchen_orders[0].get('id')}")
                print(f"   First order status: {kitchen_orders[0].get('status')}")
        else:
            print(f"❌ Kitchen orders retrieval failed: {kitchen_response.status_code} - {kitchen_response.text}")
            
        # Step 3: Test bar orders endpoint
        print("\n3. Testing bar orders endpoint...")
        bar_response = requests.get(
            f"{base_url}/api/bar/orders",
            headers=headers
        )
        
        if bar_response.status_code == 200:
            bar_orders = bar_response.json()
            print(f"✅ Bar orders retrieved successfully!")
            print(f"   Found {len(bar_orders)} bar orders")
            if len(bar_orders) > 0:
                print(f"   First order ID: {bar_orders[0].get('id')}")
                print(f"   First order status: {bar_orders[0].get('status')}")
        else:
            print(f"❌ Bar orders retrieval failed: {bar_response.status_code} - {bar_response.text}")
            
        # Step 4: Test updating kitchen order status
        print("\n4. Testing kitchen order status update...")
        if kitchen_response.status_code == 200 and len(kitchen_response.json()) > 0:
            first_kitchen_order_id = kitchen_response.json()[0]["order_id"]
            update_data = {
                "status": "preparing"
            }
            
            update_response = requests.put(
                f"{base_url}/api/kitchen/orders/{first_kitchen_order_id}",
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
        else:
            print("⚠️  Skipping kitchen order update test (no orders found)")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_kitchen_bar_apis()
    sys.exit(0 if success else 1)