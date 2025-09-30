#!/usr/bin/env python3
"""
Example script demonstrating the use of payment types in the restaurant management system
"""

def demonstrate_payment_types():
    """Demonstrate creating orders with different payment types"""
    
    print("Payment Types Example")
    print("=" * 30)
    
    # Example order data with different payment types
    orders = [
        {
            "description": "Cash payment for dine-in order",
            "order": [
                {
                    "name": "Cheeseburger",
                    "price": 9.99,
                    "category": "Main Course",
                    "modifiers": ["extra cheese"]
                },
                {
                    "name": "Fries",
                    "price": 3.99,
                    "category": "Sides"
                }
            ],
            "total": 13.98,
            "order_type": "dine_in",
            "table_number": "12",
            "customer_name": "John Smith",
            "payment_type": "cash"
        },
        {
            "description": "Card payment for takeaway order",
            "order": [
                {
                    "name": "Chicken Sandwich",
                    "price": 8.99,
                    "category": "Main Course"
                },
                {
                    "name": "Soda",
                    "price": 2.50,
                    "category": "Drinks"
                }
            ],
            "total": 11.49,
            "order_type": "takeaway",
            "customer_name": "Jane Doe",
            "customer_phone": "555-1234",
            "payment_type": "card"
        },
        {
            "description": "QR code payment for delivery order",
            "order": [
                {
                    "name": "Pizza Margherita",
                    "price": 14.99,
                    "category": "Main Course"
                },
                {
                    "name": "Caesar Salad",
                    "price": 7.99,
                    "category": "Appetizers"
                },
                {
                    "name": "Beer",
                    "price": 4.50,
                    "category": "Drinks"
                }
            ],
            "total": 27.48,
            "order_type": "delivery",
            "customer_name": "Bob Johnson",
            "customer_phone": "555-5678",
            "delivery_address": "123 Main St, City, State 12345",
            "payment_type": "qr"
        },
        {
            "description": "E-wallet payment for dine-in order",
            "order": [
                {
                    "name": "Pasta Carbonara",
                    "price": 16.99,
                    "category": "Main Course",
                    "modifiers": ["extra bacon"]
                },
                {
                    "name": "Garlic Bread",
                    "price": 4.99,
                    "category": "Sides"
                },
                {
                    "name": "Wine",
                    "price": 8.50,
                    "category": "Drinks"
                }
            ],
            "total": 30.48,
            "order_type": "dine_in",
            "table_number": "5",
            "customer_name": "Alice Brown",
            "payment_type": "e_wallet"
        },
        {
            "description": "Gift card payment for takeaway order",
            "order": [
                {
                    "name": "Fish and Chips",
                    "price": 12.99,
                    "category": "Main Course"
                },
                {
                    "name": "Apple Pie",
                    "price": 5.99,
                    "category": "Desserts"
                }
            ],
            "total": 18.98,
            "order_type": "takeaway",
            "customer_name": "Charlie Wilson",
            "customer_phone": "555-9012",
            "payment_type": "gift_card"
        }
    ]
    
    # Print each order example
    for i, order in enumerate(orders, 1):
        print(f"\n{i}. {order['description']}")
        print(f"   Payment Type: {order['payment_type']}")
        print(f"   Order Type: {order['order_type']}")
        print(f"   Total: ${order['total']:.2f}")
        print("   Items:")
        for item in order['order']:
            print(f"     - {item['name']}: ${item['price']:.2f}")
        print(f"   Customer: {order['customer_name']}")
        
        if 'table_number' in order:
            print(f"   Table: {order['table_number']}")
        if 'customer_phone' in order:
            print(f"   Phone: {order['customer_phone']}")
        if 'delivery_address' in order:
            print(f"   Delivery Address: {order['delivery_address']}")

def demonstrate_payment_type_validation():
    """Demonstrate payment type validation"""
    
    print("\n\nPayment Type Validation")
    print("=" * 30)
    
    # Valid payment types
    valid_payment_types = ["cash", "card", "qr", "e_wallet", "gift_card"]
    print("Valid payment types:")
    for payment_type in valid_payment_types:
        print(f"  - {payment_type}")
    
    # Invalid payment type that will default to cash
    print("\nInvalid payment type example:")
    print("  Payment type: 'paypal' (invalid)")
    print("  Result: Defaults to 'cash'")

def demonstrate_invoice_payment_types():
    """Demonstrate invoice creation with payment types"""
    
    print("\n\nInvoice Payment Types")
    print("=" * 30)
    
    invoice_example = {
        "order_id": 123,
        "customer_name": "John Smith",
        "order_type": "dine_in",
        "table_number": "12",
        "subtotal": 13.98,
        "tax": 1.12,
        "total": 15.10,
        "payment_type": "card",
        "invoice_items": [
            {
                "name": "Cheeseburger",
                "category": "Main Course",
                "price": 9.99,
                "quantity": 1
            },
            {
                "name": "Fries",
                "category": "Sides",
                "price": 3.99,
                "quantity": 1
            }
        ]
    }
    
    print("Invoice example with payment type:")
    print(f"  Customer: {invoice_example['customer_name']}")
    print(f"  Order ID: {invoice_example['order_id']}")
    print(f"  Payment Type: {invoice_example['payment_type']}")
    print(f"  Subtotal: ${invoice_example['subtotal']:.2f}")
    print(f"  Tax: ${invoice_example['tax']:.2f}")
    print(f"  Total: ${invoice_example['total']:.2f}")
    print("  Items:")
    for item in invoice_example['invoice_items']:
        print(f"    - {item['name']}: ${item['price']:.2f} x {item['quantity']}")

if __name__ == "__main__":
    demonstrate_payment_types()
    demonstrate_payment_type_validation()
    demonstrate_invoice_payment_types()
    
    print("\n\n🎉 Payment types feature is ready for use!")
    print("The system supports cash, card, QR code, e-wallet, and gift card payments.")