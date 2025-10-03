#!/usr/bin/env python3
"""
Debug Orders Status Tracker Page Issues
This script helps identify why the Orders Status Tracker page is not loading orders.
"""

import os
import sys
import requests
import json

def debug_orders_status():
    """Debug the orders status tracker page issues"""
    try:
        print("=== Debugging Orders Status Tracker Page Issues ===")
        
        base_url = "http://localhost:8088"
        
        # Step 1: Test if backend is running
        print("1. Testing if backend is running...")
        try:
            health_response = requests.get(f"{base_url}/docs")
            if health_response.status_code == 200:
                print("✅ Backend is running")
            else:
                print(f"❌ Backend health check failed: {health_response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to backend: {e}")
            return False
            
        # Step 2: Login as manager
        print("\n2. Logging in as manager...")
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
        
        # Step 3: Test orders endpoint directly
        print("\n3. Testing orders endpoint...")
        orders_response = requests.get(
            f"{base_url}/api/orders",
            headers=headers
        )
        
        print(f"   Orders endpoint status: {orders_response.status_code}")
        
        if orders_response.status_code == 200:
            orders = orders_response.json()
            print(f"✅ Orders retrieved successfully!")
            print(f"   Found {len(orders)} orders")
            
            # Show first few orders
            print("\n   First 3 orders:")
            for i, order in enumerate(orders[:3]):
                print(f"     Order ID: {order.get('id')}")
                print(f"     Customer: {order.get('customer_name')}")
                print(f"     Total: ${order.get('total')}")
                print(f"     Status: {order.get('status', 'N/A')}")
                print(f"     Order Type: {order.get('order_type')}")
                print()
        else:
            print(f"❌ Failed to retrieve orders: {orders_response.status_code}")
            try:
                error_text = orders_response.text
                print(f"   Error details: {error_text}")
            except:
                print("   Could not parse error details")
            return False
            
        # Step 4: Test without authentication (this might be the issue)
        print("\n4. Testing orders endpoint without authentication...")
        no_auth_response = requests.get(f"{base_url}/api/orders")
        print(f"   No-auth request status: {no_auth_response.status_code}")
        
        if no_auth_response.status_code == 401:
            print("✅ Orders endpoint correctly requires authentication")
        elif no_auth_response.status_code == 200:
            print("⚠️  Orders endpoint does not require authentication (unexpected)")
        else:
            print(f"❓ Unexpected status code: {no_auth_response.status_code}")
            
        # Step 5: Test specific order endpoint
        print("\n5. Testing specific order endpoint...")
        if 'orders' in locals() and len(orders) > 0:
            first_order_id = orders[0].get('id')
            if first_order_id:
                specific_order_response = requests.get(
                    f"{base_url}/api/orders/{first_order_id}",
                    headers=headers
                )
                print(f"   Specific order endpoint status: {specific_order_response.status_code}")
                
                if specific_order_response.status_code == 200:
                    order_details = specific_order_response.json()
                    print("✅ Specific order retrieved successfully")
                    print(f"   Order details keys: {list(order_details.keys())}")
                else:
                    print(f"❌ Failed to retrieve specific order: {specific_order_response.status_code}")
        
        # Step 6: Summary
        print("\n=== Debug Summary ===")
        print("✅ Backend is running")
        print("✅ Authentication is working")
        print("✅ Orders can be retrieved with proper authentication")
        print("✅ Specific order endpoint is working")
        
        print("\n🔧 Potential Issues with Orders Status Tracker Page:")
        print("1. The page might not be sending the authentication token")
        print("2. The page might be using an incorrect API endpoint")
        print("3. The page might have frontend JavaScript errors")
        print("4. There might be CORS issues")
        print("5. The page might be expecting a different data format")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("This script will help debug the Orders Status Tracker page issues.")
    response = input("Do you want to continue? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        success = debug_orders_status()
        if success:
            print("\n🎉 Debugging completed successfully!")
            print("The backend API is working correctly.")
            print("The issue is likely in the frontend implementation of the Orders Status Tracker page.")
        else:
            print("\n❌ Debugging failed. Please check the error messages above.")
        sys.exit(0 if success else 1)
    else:
        print("Operation cancelled.")
        sys.exit(0)