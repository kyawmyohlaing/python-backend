#!/usr/bin/env python3
"""
Integration test for payment types feature
"""

def test_payment_types_integration():
    """Test the complete payment types integration"""
    try:
        # Test importing all necessary components
        from app.models.order import Order, PaymentType
        from app.models.invoice import Invoice
        from app.schemas.order_schema import OrderCreate, OrderItem
        from app.schemas.invoice_schema import InvoiceCreate, InvoiceItem
        from app.services.invoice_service import invoice_service
        
        print("✓ All models and schemas imported successfully")
        
        # Test creating an order with payment type
        order_item = OrderItem(
            name="Burger",
            price=8.99,
            category="Main Course",
            modifiers=["extra cheese"]
        )
        
        order_schema = OrderCreate(
            order=[order_item],
            total=8.99,
            payment_type="card",
            order_type="dine_in",
            table_number="12",
            customer_name="John Doe"
        )
        
        print(f"✓ Order schema created with payment_type: {order_schema.payment_type}")
        
        # Test creating an invoice with payment type
        invoice_item = InvoiceItem(
            name="Burger",
            price=8.99,
            category="Main Course",
            quantity=1
        )
        
        invoice_schema = InvoiceCreate(
            order_id=1,
            customer_name="John Doe",
            order_type="dine_in",
            table_number="12",
            subtotal=8.99,
            tax=0.72,
            total=9.71,
            invoice_items=[invoice_item],
            payment_type="card"
        )
        
        print(f"✓ Invoice schema created with payment_type: {invoice_schema.payment_type}")
        
        # Test the PaymentType enum
        print(f"✓ PaymentType.CASH value: {PaymentType.CASH.value}")
        print(f"✓ PaymentType.CARD value: {PaymentType.CARD.value}")
        print(f"✓ PaymentType.QR value: {PaymentType.QR.value}")
        print(f"✓ PaymentType.E_WALLET value: {PaymentType.E_WALLET.value}")
        print(f"✓ PaymentType.GIFT_CARD value: {PaymentType.GIFT_CARD.value}")
        
        # Test that all expected payment types are in the enum
        expected_types = ["cash", "card", "qr", "e_wallet", "gift_card"]
        actual_types = [pt.value for pt in PaymentType]
        
        for expected in expected_types:
            if expected in actual_types:
                print(f"✓ Payment type '{expected}' found in enum")
            else:
                print(f"✗ Payment type '{expected}' missing from enum")
                return False
        
        print("✓ All payment types verified")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in integration test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the integration test"""
    print("Payment Types Integration Test")
    print("=" * 40)
    
    if test_payment_types_integration():
        print("\n🎉 Integration test passed! Payment types feature is working correctly.")
        return 0
    else:
        print("\n❌ Integration test failed.")
        return 1

if __name__ == "__main__":
    exit(main())