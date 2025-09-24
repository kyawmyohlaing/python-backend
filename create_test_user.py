#!/usr/bin/env python3
"""
Script to create a test admin user for analytics testing
"""

import os
import sys
import requests

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def create_test_user():
    """Create a test admin user"""
    base_url = "http://localhost:8088"
    api_prefix = "/api"
    
    print("Creating test admin user...")
    
    # First, try to login as manager to see if we can create a user
    print("1. Testing login as manager...")
    try:
        # Send form data instead of JSON
        login_response = requests.post(
            f"{base_url}{api_prefix}/auth/login",
            data={
                "username": "admin",
                "password": "admin123"
            }
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            print(f"   Manager login successful. Token: {token[:10]}...")
        else:
            print(f"   Manager login failed with status code: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            
            # Try to register a new admin user
            print("2. Trying to register a new admin user...")
            try:
                register_response = requests.post(
                    f"{base_url}{api_prefix}/auth/register",
                    json={
                        "username": "testadmin",
                        "email": "testadmin@example.com",
                        "password": "testpassword123",
                        "role": "admin",
                        "full_name": "Test Administrator"
                    }
                )
                
                if register_response.status_code == 200:
                    print("   User registration successful!")
                    user_data = register_response.json()
                    print(f"   Created user: {user_data}")
                    
                    # Now try to login with the new user
                    print("3. Testing login with new admin user...")
                    login_response = requests.post(
                        f"{base_url}{api_prefix}/auth/login",
                        data={
                            "username": "testadmin",
                            "password": "testpassword123"
                        }
                    )
                    
                    if login_response.status_code == 200:
                        token_data = login_response.json()
                        token = token_data.get("access_token")
                        print(f"   Login successful. Token: {token[:10]}...")
                        return token
                    else:
                        print(f"   Login failed with status code: {login_response.status_code}")
                        print(f"   Response: {login_response.text}")
                        return None
                else:
                    print(f"   Registration failed with status code: {register_response.status_code}")
                    print(f"   Response: {register_response.text}")
                    return None
            except Exception as e:
                print(f"   Registration failed with error: {str(e)}")
                return None
    except Exception as e:
        print(f"   Login failed with error: {str(e)}")
        return None

if __name__ == "__main__":
    token = create_test_user()
    if token:
        print(f"\nTest user created successfully! Use this token for analytics testing:")
        print(f"Authorization: Bearer {token}")
    else:
        print("\nFailed to create test user.")