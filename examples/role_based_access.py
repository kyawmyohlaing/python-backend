"""
Example script demonstrating role-based access control in the FastAPI backend.
This script shows how to create users with different roles and how to protect endpoints based on roles.
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8088"

def register_user(name, email, password, role):
    """Register a new user with a specific role"""
    try:
        response = requests.post(f"{BASE_URL}/users/register", json={
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }, timeout=10)
        return response
    except Exception as e:
        print(f"Error registering user {name}: {e}")
        return None

def login_user(email, password):
    """Login and get access token"""
    try:
        response = requests.post(f"{BASE_URL}/users/login", json={
            "email": email,
            "password": password
        }, timeout=10)
        return response
    except Exception as e:
        print(f"Error logging in user {email}: {e}")
        return None

def get_current_user(token):
    """Get current user information"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers, timeout=10)
        return response
    except Exception as e:
        print(f"Error getting current user: {e}")
        return None

def list_all_users(token):
    """List all users (requires admin role in a real implementation)"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/", headers=headers, timeout=10)
        return response
    except Exception as e:
        print(f"Error listing users: {e}")
        return None

# Example usage
if __name__ == "__main__":
    print("=== Role-Based Access Control Example ===\n")
    
    # Register users with different roles
    print("1. Registering users with different roles:")
    
    users = [
        {"name": "Admin User", "email": "admin@example.com", "password": "admin123", "role": "admin"},
        {"name": "Waiter User", "email": "waiter@example.com", "password": "waiter123", "role": "waiter"},
        {"name": "Cashier User", "email": "cashier@example.com", "password": "cashier123", "role": "cashier"},
        {"name": "Manager User", "email": "manager@example.com", "password": "manager123", "role": "manager"},
        {"name": "Chef User", "email": "chef@example.com", "password": "chef123", "role": "chef"},
    ]
    
    registered_users = []
    
    for user in users:
        response = register_user(user["name"], user["email"], user["password"], user["role"])
        if response and response.status_code == 200:
            print(f"   ✓ Registered {user['name']} with role {user['role']}")
            registered_users.append(user)
        else:
            error_msg = response.text if response else "No response"
            print(f"   ✗ Failed to register {user['name']}: {error_msg}")
    
    print("\n2. Logging in as different users:")
    
    # Login as waiter
    waiter_token = None
    if len(registered_users) > 1:  # Waiter user
        waiter_user = registered_users[1]
        login_response = login_user(waiter_user["email"], waiter_user["password"])
        if login_response and login_response.status_code == 200:
            waiter_token = login_response.json()["access_token"]
            print("   ✓ Waiter logged in successfully")
            
            # Get waiter info
            user_response = get_current_user(waiter_token)
            if user_response and user_response.status_code == 200:
                user_data = user_response.json()
                print(f"   ✓ Current user: {user_data['username']} (Role: {user_data['role']})")
        else:
            error_msg = login_response.text if login_response else "No response"
            print(f"   ✗ Waiter login failed: {error_msg}")
    
    # Login as manager
    manager_token = None
    if len(registered_users) > 3:  # Manager user
        manager_user = registered_users[3]
        login_response = login_user(manager_user["email"], manager_user["password"])
        if login_response and login_response.status_code == 200:
            manager_token = login_response.json()["access_token"]
            print("   ✓ Manager logged in successfully")
            
            # Get manager info
            user_response = get_current_user(manager_token)
            if user_response and user_response.status_code == 200:
                user_data = user_response.json()
                print(f"   ✓ Current user: {user_data['username']} (Role: {user_data['role']})")
        else:
            error_msg = login_response.text if login_response else "No response"
            print(f"   ✗ Manager login failed: {error_msg}")
    
    print("\n3. Accessing protected resources:")
    
    # Manager can list all users (in a full implementation, we would add role checks to endpoints)
    if manager_token:
        users_response = list_all_users(manager_token)
        if users_response and users_response.status_code == 200:
            users_data = users_response.json()
            print(f"   ✓ Manager can access user list ({len(users_data)} users found)")
        else:
            error_msg = users_response.text if users_response else "No response"
            print(f"   ✗ Manager cannot access user list: {error_msg}")
    else:
        print("   ✗ Manager token not available")
    
    print("\n=== End of Example ===")