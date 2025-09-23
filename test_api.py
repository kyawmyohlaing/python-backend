#!/usr/bin/env python3
"""
Test script for the FastAPI backend API endpoints.
This script tests the /register, /login, and /me endpoints.
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8088"

def test_register_user():
    """Test registering a new user"""
    try:
        print("Testing user registration...")
        response = requests.post(f"{BASE_URL}/users/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword",
            "role": "waiter"
        }, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test creating an order
order_data = {
    "order": [
        {"name": "Burger", "price": 12.99, "category": "grill"},
        {"name": "Fries", "price": 4.99, "category": "sides"}
    ],
    "total": 17.98,
    "order_type": "dine_in"
}

response = requests.post("http://localhost:8088/api/orders", json=order_data)
print("Create order response:", response.status_code)
print("Response body:", response.json())

# Test getting all orders
response = requests.get("http://localhost:8088/api/orders")
print("Get orders response:", response.status_code)
print("Response body:", response.json())

# Test getting kitchen orders
response = requests.get("http://localhost:8088/api/kitchen/orders")
print("Get kitchen orders response:", response.status_code)
print("Response body:", response.json())

def test_register():
    """Test user registration"""
    print("Testing user registration...")
    
    # Test data
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register", json=user_data)
        if response.status_code == 200:
            print("✓ User registration successful")
            return response.json()
        else:
            print(f"✗ User registration failed with status code {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"✗ User registration failed with exception: {e}")
        return None

def test_login(email, password):
    """Test user login"""
    print("Testing user login...")
    
    # Login data
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        if response.status_code == 200:
            print("✓ User login successful")
            return response.json()
        else:
            print(f"✗ User login failed with status code {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"✗ User login failed with exception: {e}")
        return None

def test_get_current_user(token):
    """Test getting current user"""
    print("Testing get current user...")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        if response.status_code == 200:
            print("✓ Get current user successful")
            return response.json()
        else:
            print(f"✗ Get current user failed with status code {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"✗ Get current user failed with exception: {e}")
        return None

def main():
    """Test the API endpoints"""
    print("Testing FastAPI backend API endpoints...")
    print("=" * 50)
    
    # Test with the seeded example user
    print("Testing with seeded example user...")
    login_response = test_login("user@example.com", "password123")
    
    if login_response:
        token = login_response.get("access_token")
        if token:
            user_response = test_get_current_user(token)
            if user_response:
                print(f"Current user: {user_response}")
        else:
            print("Failed to get access token")
    else:
        print("Failed to login with example user")
    
    print("\n" + "=" * 50)
    
    # Test with a new user
    print("Testing with a new user...")
    register_response = test_register()
    
    if register_response:
        user_id = register_response.get("id")
        if user_id:
            login_response = test_login("test@example.com", "testpassword123")
            if login_response:
                token = login_response.get("access_token")
                if token:
                    user_response = test_get_current_user(token)
                    if user_response:
                        print(f"Current user: {user_response}")
                else:
                    print("Failed to get access token")
            else:
                print("Failed to login with new user")
        else:
            print("Failed to get user ID")
    else:
        print("Failed to register new user")

if __name__ == "__main__":
    test_register_user()
    main()