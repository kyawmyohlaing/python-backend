#!/usr/bin/env python3
"""
Test script to verify consistent authentication between GET and POST requests.
This script tests both menu and order endpoints to ensure authentication works the same way.
"""

import requests
import json
import os
from typing import Dict, Any

# Configuration
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8088")
LOGIN_ENDPOINT = f"{BASE_URL}/api/auth/login"
MENU_ENDPOINT = f"{BASE_URL}/api/menu"
ORDER_ENDPOINT = f"{BASE_URL}/api/orders"

def login_user(username: str, password: str) -> str:
    """Login and return access token"""
    try:
        response = requests.post(
            LOGIN_ENDPOINT,
            data={"username": username, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def test_get_request_without_auth(endpoint: str) -> bool:
    """Test GET request without authentication"""
    try:
        response = requests.get(endpoint)
        # Should fail with 401
        return response.status_code == 401
    except Exception as e:
        print(f"GET request without auth failed: {e}")
        return False

def test_post_request_without_auth(endpoint: str, data: Dict[Any, Any]) -> bool:
    """Test POST request without authentication"""
    try:
        response = requests.post(endpoint, json=data)
        # Should fail with 401
        return response.status_code == 401
    except Exception as e:
        print(f"POST request without auth failed: {e}")
        return False

def test_get_request_with_auth(endpoint: str, token: str) -> bool:
    """Test GET request with authentication"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(endpoint, headers=headers)
        # Should succeed (200 or other success status)
        return response.status_code < 400
    except Exception as e:
        print(f"GET request with auth failed: {e}")
        return False

def test_post_request_with_auth(endpoint: str, token: str, data: Dict[Any, Any]) -> bool:
    """Test POST request with authentication"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(endpoint, json=data, headers=headers)
        # Should succeed (200 or other success status, might be 400 for bad data which is still auth success)
        # We're checking that it's not a 401/403 auth error
        return response.status_code != 401 and response.status_code != 403
    except Exception as e:
        print(f"POST request with auth failed: {e}")
        return False

def run_auth_consistency_tests():
    """Run authentication consistency tests"""
    print("=== Authentication Consistency Test ===")
    
    # Test data
    test_menu_item = {
        "name": "Test Item",
        "price": 10.99,
        "category": "Test",
        "description": "Test item for authentication consistency"
    }
    
    test_order = {
        "order": [
            {
                "name": "Test Item",
                "price": 10.99,
                "category": "Test",
                "modifiers": []
            }
        ],
        "total": 10.99
    }
    
    # Login to get token
    print("1. Logging in...")
    token = login_user("admin", "adminpassword")
    if not token:
        print("FAILED: Could not login to get authentication token")
        return False
    print("SUCCESS: Logged in and obtained token")
    
    # Test Menu Endpoints
    print("\n2. Testing Menu Endpoints...")
    
    # Test GET without auth
    print("   Testing GET /api/menu without auth...")
    get_no_auth = test_get_request_without_auth(MENU_ENDPOINT)
    print(f"   Result: {'PASS' if get_no_auth else 'FAIL'} (expected 401)")
    
    # Test POST without auth
    print("   Testing POST /api/menu without auth...")
    post_no_auth = test_post_request_without_auth(MENU_ENDPOINT, test_menu_item)
    print(f"   Result: {'PASS' if post_no_auth else 'FAIL'} (expected 401)")
    
    # Test GET with auth
    print("   Testing GET /api/menu with auth...")
    get_with_auth = test_get_request_with_auth(MENU_ENDPOINT, token)
    print(f"   Result: {'PASS' if get_with_auth else 'FAIL'} (expected success)")
    
    # Test POST with auth
    print("   Testing POST /api/menu with auth...")
    post_with_auth = test_post_request_with_auth(MENU_ENDPOINT, token, test_menu_item)
    print(f"   Result: {'PASS' if post_with_auth else 'FAIL'} (expected success or 400 for bad data)")
    
    menu_tests_passed = get_no_auth and post_no_auth and get_with_auth and post_with_auth
    
    # Test Order Endpoints
    print("\n3. Testing Order Endpoints...")
    
    # Test GET without auth
    print("   Testing GET /api/orders without auth...")
    get_no_auth = test_get_request_without_auth(ORDER_ENDPOINT)
    print(f"   Result: {'PASS' if get_no_auth else 'FAIL'} (expected 401)")
    
    # Test POST without auth
    print("   Testing POST /api/orders without auth...")
    post_no_auth = test_post_request_without_auth(ORDER_ENDPOINT, test_order)
    print(f"   Result: {'PASS' if post_no_auth else 'FAIL'} (expected 401)")
    
    # Test GET with auth
    print("   Testing GET /api/orders with auth...")
    get_with_auth = test_get_request_with_auth(ORDER_ENDPOINT, token)
    print(f"   Result: {'PASS' if get_with_auth else 'FAIL'} (expected success)")
    
    # Test POST with auth
    print("   Testing POST /api/orders with auth...")
    post_with_auth = test_post_request_with_auth(ORDER_ENDPOINT, token, test_order)
    print(f"   Result: {'PASS' if post_with_auth else 'FAIL'} (expected success or 400 for bad data)")
    
    order_tests_passed = get_no_auth and post_no_auth and get_with_auth and post_with_auth
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Menu Tests: {'PASS' if menu_tests_passed else 'FAIL'}")
    print(f"Order Tests: {'PASS' if order_tests_passed else 'FAIL'}")
    print(f"Overall: {'PASS' if menu_tests_passed and order_tests_passed else 'FAIL'}")
    
    return menu_tests_passed and order_tests_passed

if __name__ == "__main__":
    success = run_auth_consistency_tests()
    exit(0 if success else 1)