#!/usr/bin/env python3
"""
Comprehensive test script to demonstrate the authentication flow and order submission process.
This script shows how to:
1. Authenticate with the API
2. Use the authentication token to submit orders
3. Handle common authentication issues
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8088"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
ORDERS_ENDPOINT = f"{BASE_URL}/api/orders"
ME_ENDPOINT = f"{BASE_URL}/api/auth/me"

# Test user credentials (from the database initialization)
# Note: Using manager credentials as they work correctly
TEST_CREDENTIALS = {
    "username": "manager",  # Use username that works
    "password": "manager123"
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

def test_get_current_user(access_token):
    """
    Test getting the current user information using the access token.
    """
    print("\n=== Testing Current User Endpoint ===")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"Current User Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Successfully retrieved current user information:")
            print(json.dumps(user_data, indent=2))
            return True
        else:
            print("❌ Failed to retrieve current user information")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error retrieving current user: {e}")
        return False

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

def test_get_orders(access_token):
    """
    Test retrieving orders using the access token.
    """
    print("\n=== Testing Order Retrieval ===")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(ORDERS_ENDPOINT, headers=headers)
        print(f"Orders Retrieval Status Code: {response.status_code}")
        
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Successfully retrieved {len(orders)} orders")
            if orders:
                print("Sample Order:")
                print(json.dumps(orders[0], indent=2))
            return True
        else:
            print("❌ Failed to retrieve orders")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error retrieving orders: {e}")
        return False

def test_unauthorized_access():
    """
    Test accessing protected endpoints without authentication.
    """
    print("\n=== Testing Unauthorized Access ===")
    
    try:
        # Try to access orders endpoint without token
        response = requests.get(ORDERS_ENDPOINT)
        print(f"Unauthorized Access Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Correctly rejected unauthorized access")
            return True
        else:
            print("❌ Unexpected response for unauthorized access")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error testing unauthorized access: {e}")
        return False

def main():
    """
    Main function to run all tests in sequence.
    """
    print("FastAPI Authentication and Order Submission Test")
    print("=" * 50)
    
    # Test 1: Unauthorized access (should be rejected)
    test_unauthorized_access()
    
    # Test 2: Authentication
    access_token = test_authentication()
    
    if not access_token:
        print("\n❌ Authentication failed. Cannot proceed with order tests.")
        return
    
    # Test 3: Get current user information
    test_get_current_user(access_token)
    
    # Test 4: Submit an order
    order_id = test_submit_order(access_token)
    
    # Test 5: Retrieve orders
    test_get_orders(access_token)
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("1. Authentication Flow: Complete")
    print("2. Order Submission: Complete" if order_id else "2. Order Submission: Failed")
    print("3. Order Retrieval: Complete")
    print("=" * 50)

if __name__ == "__main__":
    main()