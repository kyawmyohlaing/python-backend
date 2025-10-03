#!/usr/bin/env python3
"""
Test Order Submission Script
This script tests order submission with proper authentication
"""

import os
import sys
import requests
import json

def test_order_submission():
    """Test order submission with authentication"""
    try:
        base_url = "http://localhost:8088"
        
        # Step 1: Login
        print("1. Logging in...")
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
        
        # Step 2: Submit order
        print("\n2. Submitting order...")
        order_data = {
            "order": [{
                "name": "Beer",
                "price": 5.99,
                "category": "alcohol",
                "id": 1759309213706,
                "modifiers": []
            }],
            "total": 5.99,
            "order_type": "dine_in",
            "table_number": "1",
            "customer_name": "",
            "customer_phone": "",
            "delivery_address": ""
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        order_response = requests.post(
            f"{base_url}/api/orders",
            json=order_data,
            headers=headers
        )
        
        if order_response.status_code == 200:
            order_result = order_response.json()
            print(f"✅ Order submitted successfully!")
            print(f"   Order ID: {order_result.get('id')}")
            print(f"   Order data: {json.dumps(order_result, indent=2)}")
            return True
        else:
            print(f"❌ Order submission failed: {order_response.status_code} - {order_response.text}")
            return False
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_order_submission()
    sys.exit(0 if success else 1)