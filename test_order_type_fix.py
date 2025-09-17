import requests
import json

# Test creating an order with the correct order_type
order_data = {
    "order": [
        {"name": "Soda", "price": 2.99, "category": "drink"}
    ],
    "total": 2.99,
    "order_type": "dine_in",  # Using the correct enum value
    "table_number": "3"
}

try:
    response = requests.post("http://localhost:8088/api/orders", json=order_data)
    print("Create order response:", response.status_code)
    if response.status_code == 200:
        print("Order created successfully!")
        print("Response body:", response.json())
    else:
        print("Failed to create order:")
        print("Response body:", response.text)
except Exception as e:
    print("Error creating order:", str(e))