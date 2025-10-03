#!/usr/bin/env python3
"""
Test script for manager authentication
"""

import requests

# Configuration for Docker environment
BASE_URL = "http://localhost:8088"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"

# Test manager credentials
TEST_CREDENTIALS = {
    "username": "manager@example.com",
    "password": "manager123"
}

def test_authentication():
    """
    Test the authentication flow with manager credentials
    """
    print("=== Testing Manager Authentication Flow ===")
    
    # Prepare the login request
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
        return None
    except Exception as e:
        print(f"❌ Unexpected error during authentication: {e}")
        return None

if __name__ == "__main__":
    test_authentication()