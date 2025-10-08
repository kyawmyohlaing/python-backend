import requests
import time

def test_admin_login():
    # Wait a moment for the server to fully start
    time.sleep(2)
    
    print("Testing admin login endpoint...")
    
    # Test data for the admin user
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8088/api/auth/login",
            data=login_data
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("Admin login successful!")
            print(f"Access Token: {response_data.get('access_token')}")
            print(f"Token Type: {response_data.get('token_type')}")
            return True
        else:
            print(f"Admin login failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error during admin login test: {e}")
        return False

if __name__ == "__main__":
    success = test_admin_login()
    if success:
        print("\n✓ Admin login test passed!")
    else:
        print("\n✗ Admin login test failed!")