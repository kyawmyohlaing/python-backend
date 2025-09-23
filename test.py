#!/usr/bin/env python3
"""
Simple API test script for the FastAPI backend.
This script tests the main API endpoints with basic logging.
"""

import requests
import json

# Note: Make sure the FastAPI server is running on http://localhost:8088
BASE_URL = "http://localhost:8088"
API_PREFIX = ""

# Test user data
TEST_USER = {
    "name": "API Test User",
    "email": "api_test@example.com",
    "password": "secure_test_password_123"
}

def print_section_header(section_name):
    """Print a section header"""
    print(f"\n{'='*50}")
    print(f"  {section_name}")
    print(f"{'='*50}")

def print_result(test_name, status, details=""):
    """Print a test result"""
    print(f"  {status}: {test_name}" + (f" - {details}" if details else ""))

def test_health_check():
    """Test the health check endpoint"""
    print_section_header("Health Check Test")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print_result("GET /health", "PASS")
                return True
            else:
                print_result("GET /health", "FAIL", f"Unexpected response: {data}")
                return False
        else:
            print_result("GET /health", "FAIL", f"Status code: {response.status_code}")
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
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/users/register",
            json=TEST_USER
        )
        
        if response.status_code == 200:
            data = response.json()
            if (data.get("name") == TEST_USER["name"] and 
                data.get("email") == TEST_USER["email"]):
                print_result("POST /users/register", "PASS")
                return True
            else:
                print_result("POST /users/register", "FAIL", f"Data mismatch: {data}")
                return False
        elif response.status_code == 400:
            # User might already exist
            print_result("POST /users/register", "SKIP", "User may already exist")
            return True
        else:
            print_result("POST /users/register", "FAIL", f"Status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_result("POST /users/register", "FAIL", "Connection refused")
        return False
    except Exception as e:
        print_result("POST /users/register", "FAIL", f"Error: {str(e)}")
        return False

def test_login_user():
    """Test user login endpoint"""
    print_section_header("User Login Test")
    
    try:
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/users/login",
            json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if ("access_token" in data and 
                data.get("token_type") == "bearer"):
                print_result("POST /users/login", "PASS")
                return data["access_token"]
            else:
                print_result("POST /users/login", "FAIL", f"Invalid token response: {data}")
                return None
        else:
            print_result("POST /users/login", "FAIL", f"Status code: {response.status_code}")
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
            f"{BASE_URL}{API_PREFIX}/users/me",
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
            print_result("GET /users/me", "FAIL", f"Status code: {response.status_code}")
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
            f"{BASE_URL}{API_PREFIX}/users/",
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
            print_result("GET /users/", "FAIL", f"Status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_result("GET /users/", "FAIL", "Connection refused")
        return False
    except Exception as e:
        print_result("GET /users/", "FAIL", f"Error: {str(e)}")
        return False

def main():
    """Run all API tests"""
    print("🚀 Starting Simple API Tests")
    print(f"   Target: {BASE_URL}")
    
    # Test health check
    if not test_health_check():
        return False
    
    # Test user registration
    if not test_register_user():
        return False
    
    # Test user login
    token = test_login_user()
    if not token:
        return False
    
    # Test get current user
    if not test_get_current_user(token):
        return False
    
    # Test list users
    if not test_list_users(token):
        return False
    
    print(f"\n{'='*50}")
    print("  🎉 All tests passed!")
    print(f"{'='*50}")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)