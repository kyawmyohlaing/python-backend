#!/usr/bin/env python3
"""
Demonstration of the complete payment workflow in the restaurant system
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8088"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"
ORDERS_ENDPOINT = f"{BASE_URL}/api/orders/"
PAYMENTS_ENDPOINT = f"{BASE_URL}/api/payments/"
INVOICES_ENDPOINT = f"{BASE_URL}/api/invoices/"

class PaymentWorkflowDemo:
    def __init__(self):
        self.access_token = None
        self.session = requests.Session()
    
    def authenticate(self):
        """Authenticate with the API"""
        login_data = {
            "username": "manager@example.com",
            "password": "manager123"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = self.session.post(AUTH_ENDPOINT, data=login_data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}"
            })
            print("✅ Authentication successful")
            return True
        else:
            print(f"❌ Authentication failed: {response.text}")
            return False
    
    def create_order(self):
        """Create an order with a specific payment type"""
        order_data = {
            "order": [
                {
                    "name": "Grilled Salmon",
                    "price": 18.99,
                    "category": "Main Course",
                    "modifiers": ["lemon butter sauce"]
                },
                {
                    "name": "Caesar Salad",
                    "price": 9.99,
                    "category": "Appetizer"
                },
                {
                    "name": "Glass of Wine",
                    "price": 7.50,
                    "category": "Beverages"
                }
            ],
            "total": 36.48,
            "customer_name": "Jane Smith",
            "table_number": "5",
            "payment_type": "card"  # Specify payment type
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.post(ORDERS_ENDPOINT, json=order_data, headers=headers)
        
        if response.status_code == 200:
            order = response.json()
            print(f"✅ Order created successfully. Order ID: {order['id']}")
            return order
        else:
            print(f"❌ Failed to create order: {response.text}")
            return None
    
    def process_payment(self, order_id, amount):
        """Process payment for an order"""
        payment_data = {
            "order_id": order_id,
            "payment_type": "card",
            "amount": amount,
            "payment_details": {
                "card_type": "Visa",
                "last_four": "1234",
                "transaction_reference": f"txn_{int(datetime.now().timestamp())}"
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.post(f"{PAYMENTS_ENDPOINT}process", json=payment_data, headers=headers)
        
        if response.status_code == 200:
            payment_result = response.json()
            print(f"✅ Payment processed successfully.")
            print(f"   Order ID: {payment_result['order_id']}")
            print(f"   Payment Type: {payment_result['payment_type']}")
            print(f"   Amount: ${payment_result['amount']}")
            print(f"   Invoice ID: {payment_result.get('invoice_id', 'N/A')}")
            return payment_result
        else:
            print(f"❌ Failed to process payment: {response.text}")
            return None
    
    def get_order_payment_status(self, order_id):
        """Get payment status for an order"""
        response = self.session.get(f"{PAYMENTS_ENDPOINT}order/{order_id}")
        
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Payment status retrieved for order {order_id}")
            print(f"   Payment Status: {status['payment_status']}")
            print(f"   Payment Type: {status['payment_type']}")
            print(f"   Paid At: {status['paid_at']}")
            return status
        else:
            print(f"❌ Failed to get payment status: {response.text}")
            return None
    
    def get_payment_methods(self):
        """Get available payment methods"""
        response = self.session.get(f"{PAYMENTS_ENDPOINT}methods")
        
        if response.status_code == 200:
            methods = response.json()
            print("✅ Available payment methods:")
            for method, info in methods.items():
                print(f"   - {info['name']} ({method})")
            return methods
        else:
            print(f"❌ Failed to get payment methods: {response.text}")
            return None
    
    def get_payment_summary(self):
        """Get payment summary"""
        summary_data = {}  # No date filters for now
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.post(f"{PAYMENTS_ENDPOINT}summary", json=summary_data, headers=headers)
        
        if response.status_code == 200:
            summary = response.json()
            print("✅ Payment summary:")
            print(f"   Total Revenue: ${summary['total_revenue']:.2f}")
            print(f"   Total Transactions: {summary['total_transactions']}")
            print("   Payment Type Breakdown:")
            for payment_type, data in summary['payment_type_breakdown'].items():
                print(f"     - {payment_type}: {data['count']} transactions, ${data['amount']:.2f}")
            return summary
        else:
            print(f"❌ Failed to get payment summary: {response.text}")
            return None

def main():
    """Demonstrate the complete payment workflow"""
    print("Restaurant Payment Workflow Demo")
    print("=" * 40)
    
    # Create demo instance
    demo = PaymentWorkflowDemo()
    
    # Authenticate
    print("\n1. Authenticating...")
    if not demo.authenticate():
        print("❌ Authentication failed. Cannot proceed.")
        return
    
    # Show available payment methods
    print("\n2. Available Payment Methods:")
    demo.get_payment_methods()
    
    # Create an order
    print("\n3. Creating Order...")
    order = demo.create_order()
    if not order:
        print("❌ Failed to create order. Cannot proceed.")
        return
    
    order_id = order['id']
    order_total = order['total']
    
    # Process payment
    print("\n4. Processing Payment...")
    payment_result = demo.process_payment(order_id, order_total)
    if not payment_result:
        print("❌ Failed to process payment.")
        return
    
    # Check payment status
    print("\n5. Checking Payment Status...")
    demo.get_order_payment_status(order_id)
    
    # Show payment summary
    print("\n6. Payment Summary:")
    demo.get_payment_summary()
    
    print("\n🎉 Payment workflow demo completed successfully!")

if __name__ == "__main__":
    main()