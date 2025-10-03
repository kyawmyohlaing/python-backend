#!/usr/bin/env python3
"""
Test script for authentication in Docker environment
"""

import requests
import json

# Configuration for Docker environment
BASE_URL = "http://localhost:8088"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
ORDERS_ENDPOINT = f"{BASE_URL}/api/orders"
ME_ENDPOINT = f"{BASE_URL}/api/auth/me"

# Test user credentials (from the existing database)
TEST_CREDENTIALS = {
    "username": "testadmin@example.com",  # Using existing user
    "password": "admin123"
}

def test_authentication():
    """
    Test the authentication flow and return the access token if successful.
    """
    print("=== Testing Authentication Flow ===")
    
    # Prepare the login request
    # Note: The login endpoint expects form data, not JSON
    login_data = {
        "username": TEST_CREDENTIALS["username"],
        "password": TEST_CREDENTIALS["password"]
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        # Attempt to login
        print(f"Attempting to login with username: {TEST_CREDENTIALS['username']}")
        response = requests.post(AUTH_ENDPOINT, data=login_data, headers=headers)
        
        print(f"Login Status Code: {response.status_code}")
        print(f"Login Response: {response.text}")
        
        if response.status_code == 200:
            # Parse the response to get the access token
            token_data = response.json()
            access_token = token_data.get("access_token")
            
            if access_token:
                print("✅ Authentication successful!")
                print(f"Access Token: {access_token}")
                print(f"Token Type: {token_data.get('token_type', 'bearer')}")
                return access_token
            else:
                print("❌ Authentication failed: No access token in response")
                return None
        else:
            print("❌ Authentication failed with status code:", response.status_code)
            print("Response:", response.text)
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Could not connect to the server")
        print("Make sure the FastAPI server is running on localhost:8088")
        return None
    except Exception as e:
        print(f"❌ Unexpected error during authentication: {e}")
        return None

def test_submit_order(access_token):
    """
    Test submitting an order using the access token.
    """
    print("\n=== Testing Order Submission ===")
    
    # Sample order data
    order_data = {
        "order": [
            {
                "name": "Burger",
                "price": 8.99,
                "category": "Main Course",
                "modifiers": ["extra cheese"]
            },
            {
                "name": "Fries",
                "price": 3.99,
                "category": "Sides"
            }
        ],
        "total": 12.98,
        "customer_name": "John Doe",
        "payment_type": "cash"
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(ORDERS_ENDPOINT, json=order_data, headers=headers)
        print(f"Order Submission Status Code: {response.status_code}")
        
        if response.status_code == 200:
            order_response = response.json()
            print("✅ Order submitted successfully!")
            print("Order Details:")
            print(json.dumps(order_response, indent=2))
            return order_response.get("id")
        else:
            print("❌ Failed to submit order")
            print("Response:", response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error submitting order: {e}")
        return None

def main():
    """
    Main function to run authentication and order submission tests.
    """
    print("FastAPI Authentication and Order Submission Test (Docker)")
    print("=" * 60)
    
    # Test authentication
    access_token = test_authentication()
    
    if not access_token:
        print("\n❌ Authentication failed. Cannot proceed with order tests.")
        return
    
    # Test order submission
    order_id = test_submit_order(access_token)
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("1. Authentication Flow: Complete" if access_token else "1. Authentication Flow: Failed")
    print("2. Order Submission: Complete" if order_id else "2. Order Submission: Failed")
    print("=" * 60)

if __name__ == "__main__":
    main()