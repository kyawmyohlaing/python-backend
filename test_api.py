#!/usr/bin/env python3
"""
Test script for the FastAPI backend API endpoints.
This script tests the /register, /login, and /me endpoints.
"""

import requests
import json

# Test the health endpoint
response = requests.get("http://localhost:8088/health")
print(f"Health check: {response.status_code} - {response.json()}")

# Test getting all tables (should be empty initially)
response = requests.get("http://localhost:8088/api/tables/")
print(f"Get tables: {response.status_code} - {response.json()}")

# Test creating a table
table_data = {
    "table_number": 1,
    "capacity": 4
}

response = requests.post(
    "http://localhost:8088/api/tables/",
    headers={"Content-Type": "application/json"},
    data=json.dumps(table_data)
)

print(f"Create table: {response.status_code} - {response.json()}")

# Test getting all tables again (should now have one table)
response = requests.get("http://localhost:8088/api/tables/")
print(f"Get tables after creation: {response.status_code} - {response.json()}")

# Test creating an order
order_data = {
    "order": [
        {"name": "Burger", "price": 8.99, "category": "Main Course"},
        {"name": "Fries", "price": 3.99, "category": "Sides"},
        {"name": "Soda", "price": 2.99, "category": "Beverages"}
    ],
    "total": 15.97,
    "order_type": "dine-in",
    "table_number": "5",
    "customer_name": "John Doe"
}

# Create order
response = requests.post("http://localhost:8088/api/orders/", json=order_data)
print("Create Order Response:")
print(response.status_code)
print(json.dumps(response.json(), indent=2))

# Get kitchen orders
response = requests.get("http://localhost:8088/api/kitchen/orders")
print("\nKitchen Orders Response:")
print(response.status_code)
print(json.dumps(response.json(), indent=2))

# Test printers endpoint
response = requests.get("http://localhost:8088/api/kitchen/printers")
print("\nPrinters Response:")
print(response.status_code)
print(json.dumps(response.json(), indent=2))

# Test printing KOT for the last order (the one we just created)
if response.status_code == 200:
    response = requests.get("http://localhost:8088/api/kitchen/orders")
    if response.status_code == 200:
        kitchen_orders = response.json()
        if len(kitchen_orders) > 0:
            # Get the last order (the one we just created)
            order_id = kitchen_orders[-1]["order_id"]
            response = requests.post(f"http://localhost:8088/api/kitchen/orders/{order_id}/print-kot")
            print(f"\nPrint KOT Response for order {order_id}:")
            print(response.status_code)
            print(json.dumps(response.json(), indent=2))

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
    main()