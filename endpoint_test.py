#!/usr/bin/env python3
"""
Endpoint test to directly call the login endpoint
"""

import sys
import os
import requests

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def endpoint_test():
    try:
        print("Endpoint test...")
        
        # Test the login endpoint directly
        print("\n--- Testing login endpoint directly ---")
        url = "http://localhost:8088/api/auth/login"
        data = {
            "username": "manager",
            "password": "manager123"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = requests.post(url, data=data, headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error in endpoint test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    endpoint_test()