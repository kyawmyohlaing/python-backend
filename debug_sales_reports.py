#!/usr/bin/env python3
"""
Debug script for sales reports functionality
"""

import requests
import json
from datetime import datetime, timedelta

def test_sales_reports():
    """Test the sales report endpoints directly"""
    base_url = "http://localhost:8088"  # Assuming this is your backend port
    api_prefix = "/api"
    
    print("Debugging Sales Report Endpoints")
    print("=" * 40)
    
    # Test without authentication first to see what we get
    print("1. Testing endpoints without authentication...")
    
    endpoints = [
        "/analytics/reports/daily",
        "/analytics/reports/weekly", 
        "/analytics/reports/monthly"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{api_prefix}{endpoint}")
            print(f"   {endpoint}: Status {response.status_code}")
            if response.status_code == 401:
                print(f"      Expected - requires authentication")
            elif response.status_code == 200:
                data = response.json()
                print(f"      Success - Data: {json.dumps(data, indent=2)[:200]}...")
            else:
                print(f"      Unexpected response: {response.text[:200]}")
        except Exception as e:
            print(f"   {endpoint}: Error - {str(e)}")
    
    # Test with a very broad date range to see if we get data
    print("\n2. Testing daily report with broad date range...")
    try:
        # Use a very broad date range to capture all possible data
        start_date = (datetime.now() - timedelta(days=365)).isoformat()
        end_date = (datetime.now() + timedelta(days=1)).isoformat()
        
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        response = requests.get(
            f"{base_url}{api_prefix}/analytics/reports/daily",
            params=params
        )
        
        print(f"   Broad date range request: Status {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"      Success - Found {len(data.get('sales_data', []))} data points")
            print(f"      Total sales: {data.get('total_sales', 0)}")
            print(f"      Total orders: {data.get('total_orders', 0)}")
        else:
            print(f"      Response: {response.text[:300]}")
    except Exception as e:
        print(f"   Error: {str(e)}")

if __name__ == "__main__":
    test_sales_reports()