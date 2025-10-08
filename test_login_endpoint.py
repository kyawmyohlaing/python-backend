import requests
import time

def test_login():
    # Wait a moment for the server to fully start
    time.sleep(2)
    
    print("Testing login endpoint...")
    
    # Test data for the manager user
    login_data = {
        "username": "manager",
        "password": "manager123"
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8088/api/auth/login",
            data=login_data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("Login successful!")
            print(f"Access Token: {response_data.get('access_token')}")
            print(f"Token Type: {response_data.get('token_type')}")
            return True
        else:
            print(f"Login failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error during login test: {e}")
        return False

if __name__ == "__main__":
    success = test_login()
    if success:
        print("\n✓ Login test passed!")
    else:
        print("\n✗ Login test failed!")