#!/usr/bin/env python3
"""
Simple test script to verify payment type implementation
"""

def test_payment_type_imports():
    """Test that we can import the payment type enum"""
    try:
        # Try to import the payment type enum
        from app.models.order import PaymentType
        print("✓ PaymentType enum imported successfully")
        
        # Test enum values
        print(f"✓ PaymentType.CASH: {PaymentType.CASH}")
        print(f"✓ PaymentType.CARD: {PaymentType.CARD}")
        print(f"✓ PaymentType.QR: {PaymentType.QR}")
        print(f"✓ PaymentType.E_WALLET: {PaymentType.E_WALLET}")
        print(f"✓ PaymentType.GIFT_CARD: {PaymentType.GIFT_CARD}")
        
        # Test that all expected values are present
        expected_values = ["cash", "card", "qr", "e_wallet", "gift_card"]
        for value in expected_values:
            assert value in [item.value for item in PaymentType]
        print("✓ All expected payment types are present")
        
    except Exception as e:
        print(f"✗ Error importing PaymentType: {e}")
        return False
    
    return True

def test_order_model():
    """Test that the Order model has payment_type field"""
    try:
        # Try to import the Order model
        from app.models.order import Order
        print("✓ Order model imported successfully")
        
        # Check that payment_type field exists
        if hasattr(Order, 'payment_type'):
            print("✓ Order model has payment_type field")
        else:
            print("✗ Order model missing payment_type field")
            return False
            
    except Exception as e:
        print(f"✗ Error importing Order model: {e}")
        return False
    
    return True

def test_invoice_model():
    """Test that the Invoice model has payment_type field"""
    try:
        # Try to import the Invoice model
        from app.models.invoice import Invoice
        print("✓ Invoice model imported successfully")
        
        # Check that payment_type field exists
        if hasattr(Invoice, 'payment_type'):
            print("✓ Invoice model has payment_type field")
        else:
            print("✗ Invoice model missing payment_type field")
            return False
            
    except Exception as e:
        print(f"✗ Error importing Invoice model: {e}")
        return False
    
    return True

def test_order_schema():
    """Test that the Order schema has payment_type field"""
    try:
        # Try to import the OrderCreate schema
        from app.schemas.order_schema import OrderCreate
        print("✓ OrderCreate schema imported successfully")
        
        # Check that payment_type field exists in the schema
        # The field is defined in the base class, so we need to check the model fields
        if 'payment_type' in OrderCreate.model_fields:
            print("✓ OrderCreate schema has payment_type field")
        else:
            # Let's also check the base class
            from app.schemas.order_schema import OrderBase
            if 'payment_type' in OrderBase.model_fields:
                print("✓ OrderCreate schema has payment_type field (inherited from OrderBase)")
            else:
                print("✗ OrderCreate schema missing payment_type field")
                return False
            
    except Exception as e:
        print(f"✗ Error importing OrderCreate schema: {e}")
        return False
    
    return True

def test_invoice_schema():
    """Test that the Invoice schema has payment_type field"""
    try:
        # Try to import the InvoiceCreate schema
        from app.schemas.invoice_schema import InvoiceCreate
        print("✓ InvoiceCreate schema imported successfully")
        
        # Check that payment_type field exists in the schema
        # The field is defined in the base class, so we need to check the model fields
        if 'payment_type' in InvoiceCreate.model_fields:
            print("✓ InvoiceCreate schema has payment_type field")
        else:
            # Let's also check the base class
            from app.schemas.invoice_schema import InvoiceBase
            if 'payment_type' in InvoiceBase.model_fields:
                print("✓ InvoiceCreate schema has payment_type field (inherited from InvoiceBase)")
            else:
                print("✗ InvoiceCreate schema missing payment_type field")
                return False
            
    except Exception as e:
        print(f"✗ Error importing InvoiceCreate schema: {e}")
        return False
    
    return True

def test_order_schema_functionality():
    """Test that the Order schema actually works with payment_type"""
    try:
        # Try to import the OrderCreate schema
        from app.schemas.order_schema import OrderCreate
        from app.schemas.order_schema import OrderItem
        
        # Create an order with payment_type
        order_item = OrderItem(
            name="Test Item",
            price=10.99,
            category="Test"
        )
        
        order_data = OrderCreate(
            order=[order_item],
            total=10.99,
            payment_type="card"
        )
        
        print("✓ OrderCreate schema works with payment_type field")
        print(f"  Payment type: {order_data.payment_type}")
        
    except Exception as e:
        print(f"✗ Error testing OrderCreate schema with payment_type: {e}")
        return False
    
    return True

def test_invoice_schema_functionality():
    """Test that the Invoice schema actually works with payment_type"""
    try:
        # Try to import the InvoiceCreate schema
        from app.schemas.invoice_schema import InvoiceCreate, InvoiceItem
        
        # Create an invoice with payment_type
        invoice_item = InvoiceItem(
            name="Test Item",
            price=10.99,
            category="Test",
            quantity=1
        )
        
        invoice_data = InvoiceCreate(
            order_id=1,
            customer_name="Test Customer",
            order_type="dine_in",
            subtotal=10.99,
            tax=0.0,
            total=10.99,
            invoice_items=[invoice_item],
            payment_type="card"
        )
        
        print("✓ InvoiceCreate schema works with payment_type field")
        print(f"  Payment type: {invoice_data.payment_type}")
        
    except Exception as e:
        print(f"✗ Error testing InvoiceCreate schema with payment_type: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("Testing Payment Type Implementation")
    print("=" * 40)
    
    tests = [
        test_payment_type_imports,
        test_order_model,
        test_invoice_model,
        test_order_schema,
        test_invoice_schema,
        test_order_schema_functionality,
        test_invoice_schema_functionality
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    
    if failed == 0:
        print("🎉 All tests passed! Payment type implementation is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    exit(main())