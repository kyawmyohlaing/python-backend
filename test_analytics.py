#!/usr/bin/env python3
"""
Test script for analytics functionality
"""

import os
import sys
import requests
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_analytics_endpoints():
    """Test the analytics endpoints"""
    base_url = "http://localhost:8088"
    api_prefix = "/api"
    
    print("Testing Analytics Endpoints")
    print("=" * 40)
    
    # First, we need to login to get a token
    print("1. Testing login...")
    try:
        # Send form data instead of JSON
        login_response = requests.post(
            f"{base_url}{api_prefix}/auth/login",
            data={
                "username": "manager",
                "password": "manager123"
            }
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            print(f"   Login successful. Token: {token[:10]}...")
        else:
            print(f"   Login failed with status code: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            return
    except Exception as e:
        print(f"   Login failed with error: {str(e)}")
        return
    
    # Set up headers with the token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test sales by employee endpoint
    print("2. Testing sales by employee endpoint...")
    try:
        response = requests.get(
            f"{base_url}{api_prefix}/analytics/sales-by-employee",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Success! Retrieved {len(data)} employee records")
            if data:
                print(f"   Sample record: {data[0]}")
        else:
            print(f"   Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Failed with error: {str(e)}")
    
    # Test tips by employee endpoint
    print("3. Testing tips by employee endpoint...")
    try:
        response = requests.get(
            f"{base_url}{api_prefix}/analytics/tips-by-employee",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Success! Retrieved {len(data)} employee records")
        else:
            print(f"   Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Failed with error: {str(e)}")
    
    # Test upselling performance endpoint
    print("4. Testing upselling performance endpoint...")
    try:
        response = requests.get(
            f"{base_url}{api_prefix}/analytics/upselling-performance",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Success! Retrieved {len(data)} employee records")
        else:
            print(f"   Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Failed with error: {str(e)}")
    
    print("\nAnalytics testing completed!")

if __name__ == "__main__":
    test_analytics_endpoints()