#!/usr/bin/env python3
"""
Debug script to test the sales reports API endpoints that the frontend would call
This can help identify if frontend issues are due to backend problems or frontend implementation
"""

import requests
import json
from datetime import datetime, timedelta

def test_sales_reports_api():
    """Test the sales reports API endpoints"""
    base_url = "http://localhost:8088"  # Default backend port
    api_prefix = "/api"
    
    print("Testing Sales Reports API Endpoints for Frontend Debugging")
    print("=" * 60)
    
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
            print(f"   ✓ Login successful. Token: {token[:20]}...")
        else:
            print(f"   ✗ Login failed with status code: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            return
    except Exception as e:
        print(f"   ✗ Login failed with error: {str(e)}")
        return
    
    # Set up headers with the token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test daily sales report endpoint
    print("\n2. Testing daily sales report endpoint...")
    try:
        response = requests.get(
            f"{base_url}{api_prefix}/analytics/reports/daily",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success! Retrieved daily sales report")
            print(f"   Period: {data.get('period')}")
            print(f"   Total sales: {data.get('total_sales')}")
            print(f"   Total orders: {data.get('total_orders')}")
            print(f"   Sales data points: {len(data.get('sales_data', []))}")
            print(f"   Full response keys: {list(data.keys())}")
        else:
            print(f"   ✗ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Failed with error: {str(e)}")
    
    # Test weekly sales report endpoint
    print("\n3. Testing weekly sales report endpoint...")
    try:
        response = requests.get(
            f"{base_url}{api_prefix}/analytics/reports/weekly",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success! Retrieved weekly sales report")
            print(f"   Period: {data.get('period')}")
            print(f"   Total sales: {data.get('total_sales')}")
            print(f"   Total orders: {data.get('total_orders')}")
            print(f"   Sales data points: {len(data.get('sales_data', []))}")
            print(f"   Full response keys: {list(data.keys())}")
        else:
            print(f"   ✗ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Failed with error: {str(e)}")
    
    # Test monthly sales report endpoint
    print("\n4. Testing monthly sales report endpoint...")
    try:
        response = requests.get(
            f"{base_url}{api_prefix}/analytics/reports/monthly",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success! Retrieved monthly sales report")
            print(f"   Period: {data.get('period')}")
            print(f"   Total sales: {data.get('total_sales')}")
            print(f"   Total orders: {data.get('total_orders')}")
            print(f"   Sales data points: {len(data.get('sales_data', []))}")
            print(f"   Full response keys: {list(data.keys())}")
        else:
            print(f"   ✗ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Failed with error: {str(e)}")
    
    # Test sales report endpoint with date filters
    print("\n5. Testing sales report endpoint with date filters...")
    try:
        # Calculate date range (last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        response = requests.get(
            f"{base_url}{api_prefix}/analytics/reports/daily",
            headers=headers,
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success! Retrieved filtered daily sales report")
            print(f"   Start date: {data.get('start_date')}")
            print(f"   End date: {data.get('end_date')}")
            print(f"   Sales data points: {len(data.get('sales_data', []))}")
        else:
            print(f"   ✗ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Failed with error: {str(e)}")
    
    print("\nAPI testing completed!")

if __name__ == "__main__":
    test_sales_reports_api()