"""
Test script for tax rate functionality
"""
import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8088/api"

def test_tax_rate_functionality():
    """Test the tax rate functionality"""
    
    print("Testing tax rate functionality...")
    
    # Test 1: Get current tax rate
    print("\n1. Testing GET /analytics/tax-rate")
    try:
        response = requests.get(f"{BASE_URL}/analytics/tax-rate")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            tax_rate = response.json()
            print(f"Current tax rate: {tax_rate}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Update tax rate
    print("\n2. Testing POST /analytics/tax-rate")
    try:
        new_tax_rate = 8.5  # 8.5%
        response = requests.post(
            f"{BASE_URL}/analytics/tax-rate",
            json=new_tax_rate,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Update result: {result}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Verify updated tax rate
    print("\n3. Testing GET /analytics/tax-rate (after update)")
    try:
        response = requests.get(f"{BASE_URL}/analytics/tax-rate")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            tax_rate = response.json()
            print(f"Updated tax rate: {tax_rate}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Test tax summary report with custom tax rate
    print("\n4. Testing GET /analytics/reports/tax-summary")
    try:
        response = requests.get(f"{BASE_URL}/analytics/reports/tax-summary")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            summary = response.json()
            print(f"Tax summary report generated successfully")
            print(f"Tax rate in report: {summary.get('tax_rate')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_tax_rate_functionality()