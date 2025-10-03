#!/usr/bin/env python3
"""
Authentication Backend Test Script
This script tests the backend authentication and order submission endpoints directly
"""

import requests
import json
import sys
from typing import Dict, Any

class AuthBackendTester:
    def __init__(self, base_url: str = "http://localhost:8088"):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with a timestamp"""
        print(f"[{level}] {message}")
        
    def test_health_check(self) -> bool:
        """Test if the backend is running"""
        try:
            response = self.session.get(f"{self.base_url}/api/menu")
            if response.status_code == 200:
                self.log("✅ Backend is running")
                return True
            else:
                self.log(f"❌ Backend health check failed: {response.status_code}", "ERROR")
                return False
        except requests.exceptions.ConnectionError:
            self.log("❌ Cannot connect to backend. Is it running?", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Health check error: {e}", "ERROR")
            return False
    
    def test_login(self, username: str, password: str) -> bool:
        """Test user login"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                data={
                    "username": username,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.log(f"✅ Login successful. Token: {self.token[:20]}...")
                return True
            else:
                self.log(f"❌ Login failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Login error: {e}", "ERROR")
            return False
    
    def test_authenticated_request(self) -> bool:
        """Test an authenticated request"""
        if not self.token:
            self.log("❌ No token available for authenticated request", "ERROR")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(f"{self.base_url}/api/menu", headers=headers)
            
            if response.status_code == 200:
                self.log("✅ Authenticated request successful")
                return True
            elif response.status_code == 401:
                self.log("❌ Authenticated request failed: 401 Unauthorized", "ERROR")
                return False
            else:
                self.log(f"❌ Authenticated request failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Authenticated request error: {e}", "ERROR")
            return False
    
    def test_order_submission(self) -> bool:
        """Test order submission"""
        if not self.token:
            self.log("❌ No token available for order submission", "ERROR")
            return False
            
        # Sample order data
        order_data = {
            "order": [{
                "name": "Test Beer",
                "price": 5.99,
                "category": "alcohol",
                "id": 12345,
                "modifiers": []
            }],
            "total": 5.99,
            "order_type": "dine_in",
            "table_number": "1",
            "customer_name": "",
            "customer_phone": "",
            "delivery_address": ""
        }
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            response = self.session.post(
                f"{self.base_url}/api/orders",
                headers=headers,
                json=order_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Order submission successful. Order ID: {data.get('id')}")
                return True
            elif response.status_code == 401:
                self.log("❌ Order submission failed: 401 Unauthorized", "ERROR")
                return False
            else:
                self.log(f"❌ Order submission failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Order submission error: {e}", "ERROR")
            return False
    
    def run_full_test(self, username: str = "test", password: str = "test123") -> Dict[str, Any]:
        """Run the complete authentication and order test"""
        self.log("=== Starting Full Authentication and Order Test ===")
        
        results = {
            "health_check": False,
            "login": False,
            "authenticated_request": False,
            "order_submission": False,
            "overall_success": False
        }
        
        # Test 1: Health check
        self.log("\n1. Testing backend health...")
        results["health_check"] = self.test_health_check()
        
        if not results["health_check"]:
            self.log("❌ Backend is not running. Cannot continue tests.", "ERROR")
            return results
        
        # Test 2: Login
        self.log("\n2. Testing login...")
        results["login"] = self.test_login(username, password)
        
        if not results["login"]:
            self.log("❌ Login failed. Cannot continue tests.", "ERROR")
            return results
        
        # Test 3: Authenticated request
        self.log("\n3. Testing authenticated request...")
        results["authenticated_request"] = self.test_authenticated_request()
        
        # Test 4: Order submission
        self.log("\n4. Testing order submission...")
        results["order_submission"] = self.test_order_submission()
        
        # Overall result
        results["overall_success"] = all([
            results["health_check"],
            results["login"],
            results["authenticated_request"],
            results["order_submission"]
        ])
        
        self.log("\n=== Test Results ===")
        for test, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            self.log(f"{test}: {status}")
        
        if results["overall_success"]:
            self.log("\n🎉 All tests passed! Authentication and order submission are working correctly.", "SUCCESS")
        else:
            self.log("\n💥 Some tests failed. There may be an authentication issue.", "ERROR")
        
        return results

def main():
    """Main function to run the tests"""
    tester = AuthBackendTester()
    
    # Default credentials (you can modify these)
    username = "test"
    password = "test123"
    
    # Check if credentials were provided as arguments
    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
        print(f"Using provided credentials: {username}/***")
    else:
        print(f"Using default credentials: {username}/***")
        print("To use different credentials, run: python test_auth_backend.py <username> <password>")
    
    # Run the tests
    results = tester.run_full_test(username, password)
    
    # Exit with appropriate code
    if results["overall_success"]:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()