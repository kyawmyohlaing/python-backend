import requests
import json

# Test the menu endpoint
def test_menu_endpoint():
    print("Testing menu endpoint...")
    try:
        response = requests.get("http://localhost:8088/api/menu")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test the orders endpoint
def test_orders_endpoint():
    print("Testing orders endpoint...")
    try:
        # First get existing orders
        response = requests.get("http://localhost:8088/api/orders")
        print(f"GET Orders Status Code: {response.status_code}")
        
        # Then test creating an order
        order_data = {
            "order": [
                {
                    "name": "Test Item",
                    "price": 5.99,
                    "category": "Test Category"
                }
            ],
            "total": 5.99
        }
        
        response = requests.post(
            "http://localhost:8088/api/orders",
            headers={"Content-Type": "application/json"},
            data=json.dumps(order_data)
        )
        print(f"POST Orders Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Running integration tests...")
    
    menu_success = test_menu_endpoint()
    orders_success = test_orders_endpoint()
    
    if menu_success and orders_success:
        print("All tests passed!")
    else:
        print("Some tests failed.")