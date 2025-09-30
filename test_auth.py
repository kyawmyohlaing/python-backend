import requests

# Test login with manager credentials
url = "http://localhost:8088/api/auth/login"
payload = {
    "username": "manager@example.com",
    "password": "manager123"
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

try:
    response = requests.post(url, data=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        token_data = response.json()
        print("Login successful!")
        print(f"Access Token: {token_data.get('access_token')}")
        
        # Now test accessing the orders endpoint with the token
        orders_url = "http://localhost:8088/api/orders"
        orders_headers = {
            "Authorization": f"Bearer {token_data.get('access_token')}"
        }
        
        orders_response = requests.get(orders_url, headers=orders_headers)
        print(f"\nOrders Status Code: {orders_response.status_code}")
        print(f"Orders Response: {orders_response.text}")
    else:
        print("Login failed")
except Exception as e:
    print(f"Error: {e}")