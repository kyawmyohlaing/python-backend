"""
Simple test script to verify the role-based access fixes
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8088"

def test_user_registration():
    """Test user registration with role"""
    print("Testing user registration with role...")
    
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "waiter"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register", json=user_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            print("✓ User registration successful")
            return data.get("id"), data.get("email")
        else:
            print(f"✗ User registration failed: {response.text}")
            return None, None
    except Exception as e:
        print(f"✗ Error during user registration: {e}")
        return None, None

def test_user_login(email):
    """Test user login"""
    print("\nTesting user login...")
    
    login_data = {
        "email": email,
        "password": "testpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            print("✓ User login successful")
            return data.get("access_token")
        else:
            print(f"✗ User login failed: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error during user login: {e}")
        return None

def test_get_current_user(token):
    """Test getting current user info"""
    print("\nTesting get current user...")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            print("✓ Get current user successful")
            return True
        else:
            print(f"✗ Get current user failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error during get current user: {e}")
        return False

def main():
    print("=== Testing Role-Based Access Fixes ===\n")
    
    # Test user registration
    user_id, email = test_user_registration()
    if not email:
        print("Failed to register user. Exiting.")
        return
    
    # Test user login
    token = test_user_login(email)
    if not token:
        print("Failed to login user. Exiting.")
        return
    
    # Test getting current user
    success = test_get_current_user(token)
    if not success:
        print("Failed to get current user. Exiting.")
        return
    
    print("\n=== All tests passed! ===")

if __name__ == "__main__":
    main()