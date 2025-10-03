#!/usr/bin/env python3
"""
Test script for payment summary endpoint
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8088"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
PAYMENTS_ENDPOINT = f"{BASE_URL}/api/payments/"

def main():
    print("Payment Summary Test")
    print("=" * 25)
    
    # Authenticate
    print("1. Authenticating...")
    login_data = {
        "username": "manager@example.com",
        "password": "manager123"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(AUTH_ENDPOINT, data=login_data, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Authentication failed: {response.text}")
        return
    
    token_data = response.json()
    access_token = token_data.get("access_token")
    print("✅ Authentication successful")
    
    # Test payment summary
    print("\n2. Testing payment summary...")
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test without date filters
    response = requests.post(f"{PAYMENTS_ENDPOINT}summary", json={}, headers=auth_headers)
    
    if response.status_code == 200:
        summary = response.json()
        print("✅ Payment summary retrieved successfully")
        print(f"   Total Revenue: ${summary['total_revenue']:.2f}")
        print(f"   Total Transactions: {summary['total_transactions']}")
        print("   Payment Type Breakdown:")
        for payment_type, data in summary['payment_type_breakdown'].items():
            print(f"     - {payment_type}: {data['count']} transactions, ${data['amount']:.2f}")
    else:
        print(f"❌ Failed to get payment summary: {response.text}")
        return
    
    # Test payment methods
    print("\n3. Testing payment methods...")
    response = requests.get(f"{PAYMENTS_ENDPOINT}methods", headers=auth_headers)
    
    if response.status_code == 200:
        methods = response.json()
        print("✅ Payment methods retrieved successfully")
        for method, info in methods.items():
            print(f"   - {info['name']} ({method})")
    else:
        print(f"❌ Failed to get payment methods: {response.text}")
        return
    
    print("\n🎉 Payment summary test completed successfully!")

if __name__ == "__main__":
    main()