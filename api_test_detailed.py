#!/usr/bin/env python3
"""
Detailed API Testing Script for FastAPI Backend Template

This script provides comprehensive testing of all API endpoints with detailed output.
It includes tests for:
1. Health check endpoint
2. User registration
3. User login
4. Get current user
5. List all users

Usage:
    python api_test_detailed.py

Requirements:
    - requests library (pip install requests)
    - Running FastAPI server on http://localhost:8000

Author: Assistant
"""

import requests
import json
import time
from typing import Optional, Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/users"
TIMEOUT = 10  # seconds

# Test data
TEST_USER = {
    "name": "API Test User",
    "email": "api_test@example.com",
    "password": "secure_test_password_123"
}

class APITester:
    """API Testing class for FastAPI Backend Template"""
    
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.test_results = []
    
    def add_result(self, test_name: str, status: str, details: str = ""):
        """Add test result to results list"""
        self.test_results.append({
            "test": test_name,
            "status": status,
            "details": details
        })
    
    def print_results(self):
        """Print all test results"""
        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)
        
        passed = 0
        failed = 0
        
        for result in self.test_results:
            status_icon = "✓" if result["status"] == "PASS" else "✗"
            print(f"{status_icon} {result['test']:<35} {result['status']}")
            if result["details"]:
                print(f"   └─ {result['details']}")
            print()
            
            if result["status"] == "PASS":
                passed += 1
            else:
                failed += 1
        
        print("-"*60)
        print(f"Total: {len(self.test_results)} | Passed: {passed} | Failed: {failed}")
        print("="*60)
    
    def test_health_check(self) -> bool:
        """Test the health check endpoint"""
        try:
            response = self.session.get(
                f"{BASE_URL}/health",
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.add_result("Health Check", "PASS")
                    return True
                else:
                    self.add_result("Health Check", "FAIL", f"Unexpected response: {data}")
                    return False
            else:
                self.add_result("Health Check", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("Health Check", "FAIL", "Connection refused - is the server running?")
            return False
        except requests.exceptions.Timeout:
            self.add_result("Health Check", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("Health Check", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_register_user(self) -> bool:
        """Test user registration endpoint"""
        try:
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/register",
                json=TEST_USER,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if (data.get("email") == TEST_USER["email"] and 
                    data.get("name") == TEST_USER["name"] and
                    "id" in data):
                    self.user_id = data["id"]
                    self.add_result("User Registration", "PASS")
                    return True
                else:
                    self.add_result("User Registration", "FAIL", f"Unexpected response data: {data}")
                    return False
            elif response.status_code == 400:
                # User might already exist
                self.add_result("User Registration", "SKIP", "User may already exist")
                return True
            else:
                self.add_result("User Registration", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("User Registration", "FAIL", "Connection refused")
            return False
        except requests.exceptions.Timeout:
            self.add_result("User Registration", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("User Registration", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_login_user(self) -> bool:
        """Test user login endpoint"""
        try:
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/login",
                json={
                    "email": TEST_USER["email"],
                    "password": TEST_USER["password"]
                },
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if ("access_token" in data and 
                    data.get("token_type") == "bearer"):
                    self.token = data["access_token"]
                    self.add_result("User Login", "PASS")
                    return True
                else:
                    self.add_result("User Login", "FAIL", f"Invalid token response: {data}")
                    return False
            else:
                self.add_result("User Login", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("User Login", "FAIL", "Connection refused")
            return False
        except requests.exceptions.Timeout:
            self.add_result("User Login", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("User Login", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_get_current_user(self) -> bool:
        """Test get current user endpoint"""
        if not self.token:
            self.add_result("Get Current User", "SKIP", "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(
                f"{BASE_URL}{API_PREFIX}/me",
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("email") == TEST_USER["email"]:
                    self.add_result("Get Current User", "PASS")
                    return True
                else:
                    self.add_result("Get Current User", "FAIL", f"User data mismatch: {data}")
                    return False
            else:
                self.add_result("Get Current User", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("Get Current User", "FAIL", "Connection refused")
            return False
        except requests.exceptions.Timeout:
            self.add_result("Get Current User", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("Get Current User", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_list_users(self) -> bool:
        """Test list users endpoint"""
        if not self.token:
            self.add_result("List Users", "SKIP", "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(
                f"{BASE_URL}{API_PREFIX}/",
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.add_result("List Users", "PASS", f"Found {len(data)} users")
                    return True
                else:
                    self.add_result("List Users", "FAIL", "Response is not a list")
                    return False
            else:
                self.add_result("List Users", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("List Users", "FAIL", "Connection refused")
            return False
        except requests.exceptions.Timeout:
            self.add_result("List Users", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("List Users", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("FastAPI Backend Template - Detailed API Testing")
        print("=" * 50)
        print(f"Base URL: {BASE_URL}")
        print(f"Testing started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Test health check
        print("\n1. Testing Health Check...")
        if not self.test_health_check():
            print("⚠️  Health check failed. Make sure the server is running.")
            self.print_results()
            return
        
        # Test user registration
        print("\n2. Testing User Registration...")
        if not self.test_register_user():
            print("⚠️  User registration failed.")
        
        # Small delay to ensure server processing
        time.sleep(1)
        
        # Test user login
        print("\n3. Testing User Login...")
        if not self.test_login_user():
            print("⚠️  User login failed.")
        
        # Small delay to ensure server processing
        time.sleep(1)
        
        # Test get current user
        print("\n4. Testing Get Current User...")
        if not self.test_get_current_user():
            print("⚠️  Get current user test failed.")
        
        # Small delay to ensure server processing
        time.sleep(1)
        
        # Test list users
        print("\n5. Testing List Users...")
        if not self.test_list_users():
            print("⚠️  List users test failed.")
        
        # Print results
        self.print_results()
        
        print(f"\nTesting completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main function"""
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()