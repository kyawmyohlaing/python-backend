import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8088"

def test_kitchen_api():
    print("Testing Kitchen API...")
    
    # First, create an order
    print("\n1. Creating an order...")
    order_data = {
        "order": [
            {
                "name": "Shan Noodles",
                "price": 2.5,
                "category": "Myanmar Food"
            },
            {
                "name": "Mohinga",
                "price": 2.0,
                "category": "Myanmar Food"
            }
        ],
        "total": 4.5
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/orders",
            headers={"Content-Type": "application/json"},
            data=json.dumps(order_data)
        )
        print(f"Create order status: {response.status_code}")
        if response.status_code == 200:
            order = response.json()
            order_id = order["id"]
            print(f"Created order with ID: {order_id}")
        else:
            print(f"Failed to create order: {response.text}")
            return
    except Exception as e:
        print(f"Error creating order: {e}")
        return
    
    # Get kitchen orders
    print("\n2. Getting kitchen orders...")
    try:
        response = requests.get(f"{BASE_URL}/api/kitchen/orders")
        print(f"Get kitchen orders status: {response.status_code}")
        if response.status_code == 200:
            kitchen_orders = response.json()
            print(f"Found {len(kitchen_orders)} kitchen orders")
            for order in kitchen_orders:
                print(f"  - Order {order['order_id']}: {order['status']}")
        else:
            print(f"Failed to get kitchen orders: {response.text}")
    except Exception as e:
        print(f"Error getting kitchen orders: {e}")
    
    # Update order status to "preparing"
    print("\n3. Updating order status to 'preparing'...")
    try:
        update_data = {"status": "preparing"}
        response = requests.put(
            f"{BASE_URL}/api/kitchen/orders/{order_id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(update_data)
        )
        print(f"Update status status: {response.status_code}")
        if response.status_code == 200:
            updated_order = response.json()
            print(f"Updated order status to: {updated_order['status']}")
        else:
            print(f"Failed to update order status: {response.text}")
    except Exception as e:
        print(f"Error updating order status: {e}")
    
    # Get kitchen orders again to verify the update
    print("\n4. Verifying updated status...")
    try:
        response = requests.get(f"{BASE_URL}/api/kitchen/orders")
        if response.status_code == 200:
            kitchen_orders = response.json()
            for order in kitchen_orders:
                if order['order_id'] == order_id:
                    print(f"Verified order {order_id} status: {order['status']}")
                    break
    except Exception as e:
        print(f"Error verifying update: {e}")
    
    # Update order status to "ready"
    print("\n5. Updating order status to 'ready'...")
    try:
        update_data = {"status": "ready"}
        response = requests.put(
            f"{BASE_URL}/api/kitchen/orders/{order_id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(update_data)
        )
        print(f"Update status status: {response.status_code}")
        if response.status_code == 200:
            updated_order = response.json()
            print(f"Updated order status to: {updated_order['status']}")
        else:
            print(f"Failed to update order status: {response.text}")
    except Exception as e:
        print(f"Error updating order status: {e}")
    
    # Remove order from kitchen
    print("\n6. Removing order from kitchen...")
    try:
        response = requests.delete(f"{BASE_URL}/api/kitchen/orders/{order_id}")
        print(f"Remove order status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Remove result: {result['message']}")
        else:
            print(f"Failed to remove order: {response.text}")
    except Exception as e:
        print(f"Error removing order: {e}")
    
    # Get kitchen orders one final time
    print("\n7. Verifying order removal...")
    try:
        response = requests.get(f"{BASE_URL}/api/kitchen/orders")
        if response.status_code == 200:
            kitchen_orders = response.json()
            order_found = False
            for order in kitchen_orders:
                if order['order_id'] == order_id:
                    order_found = True
                    break
            if order_found:
                print(f"Order {order_id} still found in kitchen orders")
            else:
                print(f"Verified order {order_id} removed from kitchen orders")
        else:
            print(f"Failed to get kitchen orders: {response.text}")
    except Exception as e:
        print(f"Error verifying removal: {e}")

if __name__ == "__main__":
    test_kitchen_api()