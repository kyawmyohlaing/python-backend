#!/usr/bin/env python3
"""
Debug authentication issues
"""

import requests
import json

def debug_auth():
    """Debug authentication issues"""
    print("Debugging authentication...")
    
    # Configuration
    BASE_URL = "http://localhost:8088"
    AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
    
    # Test different credential combinations
    test_credentials = [
        {"username": "admin", "password": "admin123"},
        {"username": "admin@example.com", "password": "admin123"},
        {"username": "manager", "password": "manager123"},
        {"username": "manager@example.com", "password": "manager123"},
    ]
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    for creds in test_credentials:
        print(f"\nTesting with username: {creds['username']}")
        try:
            response = requests.post(AUTH_ENDPOINT, data=creds, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    debug_auth()