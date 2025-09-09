#!/usr/bin/env python3
"""
API Testing Script for FastAPI Backend Template

This script tests the main API endpoints:
1. User registration
2. User login
3. Get current user
4. List all users

Usage:
    python test.py

Note: Make sure the FastAPI server is running on http://localhost:8000
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/users"

# Test data
TEST_USER = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpassword123"
}

UPDATED_USER = {
    "name": "Updated Test User"
}

def print_section_header(title):
    """Print a section header"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")

def print_result(endpoint, status, details=""):
    """Print test result"""
    status_icon = "✓" if status == "PASS" else "✗"
    print(f"{status_icon} {endpoint:<30} {status} {details}")

def test_health_check():
    """Test the health check endpoint"""
    print_section_header("Health Check Test")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print_result("GET /health", "PASS")
            return True
        else:
            print_result("GET /health", "FAIL", f"Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_result("GET /health", "FAIL", "Connection refused")
        return False
    except Exception as e:
        print_result("GET /health", "FAIL", f"Error: {str(e)}")
        return False

def test_register_user():
    """Test user registration endpoint"""
    print_section_header("User Registration Test")
    
    try:
        # First, try to delete the test user if it exists
        # (This is just for demo purposes - a real API wouldn't have this)
        
        # Register a new user
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/register",
            json=TEST_USER
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("email") == TEST_USER["email"] and data.get("name") == TEST_USER["name"]:
                print_result("POST /users/register", "PASS")
                return data  # Return user data including ID
            else:
                print_result("POST /users/register", "FAIL", "Unexpected response data")
                return None
        elif response.status_code == 400:
            # User might already exist
            print_result("POST /users/register", "SKIP", "User may already exist")
            return {"id": 0, "email": TEST_USER["email"], "name": TEST_USER["name"]}
        else:
            print_result("POST /users/register", "FAIL", f"Status: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print_result("POST /users/register", "FAIL", "Connection refused")
        return None
    except Exception as e:
        print_result("POST /users/register", "FAIL", f"Error: {str(e)}")
        return None

def test_login_user():
    """Test user login endpoint"""
    print_section_header("User Login Test")
    
    try:
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/login",
            json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data and data.get("token_type") == "bearer":
                print_result("POST /users/login", "PASS")
                return data["access_token"]
            else:
                print_result("POST /users/login", "FAIL", "Invalid token response")
                return None
        else:
            print_result("POST /users/login", "FAIL", f"Status: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print_result("POST /users/login", "FAIL", "Connection refused")
        return None
    except Exception as e:
        print_result("POST /users/login", "FAIL", f"Error: {str(e)}")
        return None

def test_get_current_user(token):
    """Test get current user endpoint"""
    print_section_header("Get Current User Test")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/me",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("email") == TEST_USER["email"]:
                print_result("GET /users/me", "PASS")
                return True
            else:
                print_result("GET /users/me", "FAIL", "User data mismatch")
                return False
        else:
            print_result("GET /users/me", "FAIL", f"Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_result("GET /users/me", "FAIL", "Connection refused")
        return False
    except Exception as e:
        print_result("GET /users/me", "FAIL", f"Error: {str(e)}")
        return False

def test_list_users(token):
    """Test list users endpoint"""
    print_section_header("List Users Test")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print_result("GET /users/", "PASS")
                return True
            else:
                print_result("GET /users/", "FAIL", "Response is not a list")
                return False
        else:
            print_result("GET /users/", "FAIL", f"Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_result("GET /users/", "FAIL", "Connection refused")
        return False
    except Exception as e:
        print_result("GET /users/", "FAIL", f"Error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("FastAPI Backend Template - API Testing Script")
    print("=" * 50)
    
    # Test health check
    if not test_health_check():
        print("\n⚠️  Health check failed. Make sure the server is running.")
        return
    
    # Test user registration
    user_data = test_register_user()
    if not user_data:
        print("\n⚠️  User registration failed. Cannot proceed with other tests.")
        return
    
    # Give the server a moment to process
    time.sleep(1)
    
    # Test user login
    token = test_login_user()
    if not token:
        print("\n⚠️  User login failed. Cannot proceed with authenticated tests.")
        return
    
    # Give the server a moment to process
    time.sleep(1)
    
    # Test get current user
    if not test_get_current_user(token):
        print("\n⚠️  Get current user test failed.")
    
    # Give the server a moment to process
    time.sleep(1)
    
    # Test list users
    if not test_list_users(token):
        print("\n⚠️  List users test failed.")
    
    print("\n" + "=" * 50)
    print("API Testing Complete")
    print("=" * 50)

if __name__ == "__main__":
    main()