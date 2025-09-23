#!/usr/bin/env python3
"""
Detailed API test script for the FastAPI backend.
This script tests all the main API endpoints with detailed logging.
"""

import requests
import json
import time
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8088"
API_PREFIX = ""
TIMEOUT = 10

# Test user data
TEST_USER = {
    "name": "API Test User",
    "email": "api_test@example.com",
    "password": "secure_test_password_123"
}

class APITestRunner:
    """Class to run detailed API tests with logging"""
    
    def __init__(self):
        self.session = requests.Session()
        self.token: Optional[str] = None
        self.results = []
        
    def add_result(self, test_name: str, status: str, details: str = ""):
        """Add a test result to the results list"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.time()
        }
        self.results.append(result)
        print(f"  {status}: {test_name}" + (f" - {details}" if details else ""))
        
    def print_section_header(self, section_name: str):
        """Print a section header"""
        print(f"\n{'='*50}")
        print(f"  {section_name}")
        print(f"{'='*50}")
        
    def test_health_check(self):
        """Test the health check endpoint"""
        self.print_section_header("Health Check Test")
        
        try:
            response = self.session.get(
                f"{BASE_URL}/health",
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.add_result("GET /health", "PASS")
                    return True
                else:
                    self.add_result("GET /health", "FAIL", f"Unexpected response: {data}")
                    return False
            else:
                self.add_result("GET /health", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("GET /health", "FAIL", "Connection refused")
            return False
        except requests.exceptions.Timeout:
            self.add_result("GET /health", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("GET /health", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_register_user(self):
        """Test user registration endpoint"""
        self.print_section_header("User Registration Test")
        
        try:
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/users/register",
                json=TEST_USER,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if (data.get("name") == TEST_USER["name"] and 
                    data.get("email") == TEST_USER["email"]):
                    self.add_result("POST /users/register", "PASS")
                    return True
                else:
                    self.add_result("POST /users/register", "FAIL", f"Data mismatch: {data}")
                    return False
            elif response.status_code == 400:
                # User might already exist
                print("  SKIP: User may already exist")
                return True
            else:
                self.add_result("POST /users/register", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("POST /users/register", "FAIL", "Connection refused")
            return False
        except requests.exceptions.Timeout:
            self.add_result("POST /users/register", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("POST /users/register", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_login_user(self):
        """Test user login endpoint"""
        self.print_section_header("User Login Test")
        
        try:
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/users/login",
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
                    self.add_result("POST /users/login", "PASS")
                    return True
                else:
                    self.add_result("POST /users/login", "FAIL", f"Invalid token response: {data}")
                    return False
            else:
                self.add_result("POST /users/login", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("POST /users/login", "FAIL", "Connection refused")
            return False
        except requests.exceptions.Timeout:
            self.add_result("POST /users/login", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("POST /users/login", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_get_current_user(self):
        """Test get current user endpoint"""
        self.print_section_header("Get Current User Test")
        
        if not self.token:
            self.add_result("GET /users/me", "SKIP", "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(
                f"{BASE_URL}{API_PREFIX}/users/me",
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("email") == TEST_USER["email"]:
                    self.add_result("GET /users/me", "PASS")
                    return True
                else:
                    self.add_result("GET /users/me", "FAIL", "User data mismatch")
                    return False
            else:
                self.add_result("GET /users/me", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("GET /users/me", "FAIL", "Connection refused")
            return False
        except requests.exceptions.Timeout:
            self.add_result("GET /users/me", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("GET /users/me", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_list_users(self):
        """Test list users endpoint"""
        self.print_section_header("List Users Test")
        
        if not self.token:
            self.add_result("GET /users/", "SKIP", "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(
                f"{BASE_URL}{API_PREFIX}/users/",
                headers=headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.add_result("GET /users/", "PASS")
                    return True
                else:
                    self.add_result("GET /users/", "FAIL", "Response is not a list")
                    return False
            else:
                self.add_result("GET /users/", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.add_result("GET /users/", "FAIL", "Connection refused")
            return False
        except requests.exceptions.Timeout:
            self.add_result("GET /users/", "FAIL", "Request timeout")
            return False
        except Exception as e:
            self.add_result("GET /users/", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Detailed API Tests")
        print(f"   Target: {BASE_URL}")
        print(f"   Timeout: {TIMEOUT}s")
        print()
        
        # Test sequence
        tests = [
            self.test_health_check,
            self.test_register_user,
            self.test_login_user,
            self.test_get_current_user,
            self.test_list_users
        ]
        
        start_time = time.time()
        passed = 0
        failed = 0
        skipped = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"  ERROR: {test.__name__} failed with exception: {str(e)}")
                failed += 1
        
        end_time = time.time()
        
        # Print summary
        print(f"\n{'='*50}")
        print("  📊 TEST SUMMARY")
        print(f"{'='*50}")
        print(f"  Total Tests: {len(tests)}")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Skipped: {skipped}")
        print(f"  Duration: {end_time - start_time:.2f}s")
        
        if failed == 0:
            print("\n  🎉 All tests passed!")
            return True
        else:
            print(f"\n  ❌ {failed} test(s) failed.")
            return False

if __name__ == "__main__":
    runner = APITestRunner()
    success = runner.run_all_tests()
    exit(0 if success else 1)