import requests
import json

# Test the login endpoint
url = "http://localhost:8088/api/auth/login"

# Test data - using form data instead of JSON
# Try with the manager user
payload = {
    "username": "manager@example.com",
    "password": "manager123"
}

# Use form-encoded data (not JSON)
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

try:
    response = requests.post(url, data=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        print("✅ Login successful!")
        token_data = response.json()
        print(f"Access Token: {token_data.get('access_token')}")
    else:
        print("❌ Login failed")
except Exception as e:
    print(f"Error: {e}")