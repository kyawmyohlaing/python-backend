import requests
import json

def test_auth_and_orders():
    # Test login
    print("Testing login with manager credentials...")
    login_url = "http://localhost:8088/api/auth/login"
    login_data = {
        "username": "manager@example.com",
        "password": "manager123"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        login_response = requests.post(login_url, data=login_data, headers=headers)
        print(f"Login Status Code: {login_response.status_code}")
        print(f"Login Response: {login_response.text}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"Access Token: {access_token}")
            
            # Test accessing orders with the token
            print("\nTesting orders access with token...")
            orders_url = "http://localhost:8088/api/orders"
            orders_headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            orders_response = requests.get(orders_url, headers=orders_headers)
            print(f"Orders Status Code: {orders_response.status_code}")
            print(f"Orders Response: {orders_response.text}")
            
            # Test accessing orders without token (should fail)
            print("\nTesting orders access without token (should fail)...")
            orders_response_no_auth = requests.get(orders_url)
            print(f"Orders No Auth Status Code: {orders_response_no_auth.status_code}")
            print(f"Orders No Auth Response: {orders_response_no_auth.text}")
        else:
            print("Login failed, cannot test orders access")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_auth_and_orders()