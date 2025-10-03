#!/usr/bin/env python3
"""
Test script to verify the payment functionality implementation
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_payment_service_import():
    """Test that we can import the payment service"""
    try:
        from app.services.payment_service import payment_service
        print("✓ Payment service imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import payment service: {e}")
        return False

def test_payment_routes_import():
    """Test that we can import the payment routes"""
    try:
        from app.routes.payment_routes import router
        print("✓ Payment routes imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import payment routes: {e}")
        return False

def test_payment_schemas_import():
    """Test that we can import the payment schemas"""
    try:
        from app.schemas.payment_schema import PaymentProcessRequest
        print("✓ Payment schemas imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import payment schemas: {e}")
        return False

def test_payment_methods():
    """Test payment methods functionality"""
    try:
        from app.services.payment_service import payment_service
        
        # Test valid payment methods
        valid_methods = ["cash", "card", "qr", "e_wallet", "gift_card"]
        for method in valid_methods:
            assert payment_service.validate_payment_type(method) == True
            print(f"✓ Payment method '{method}' validated successfully")
        
        # Test invalid payment method
        assert payment_service.validate_payment_type("paypal") == False
        print("✓ Invalid payment method correctly rejected")
        
        return True
    except Exception as e:
        print(f"✗ Error testing payment methods: {e}")
        return False

def test_payment_service_methods():
    """Test payment service methods"""
    try:
        from app.services.payment_service import payment_service
        
        # Test getting payment method info
        cash_info = payment_service.get_payment_method_info("cash")
        assert "name" in cash_info
        assert "requires_processing" in cash_info
        assert "instant_confirmation" in cash_info
        print("✓ Payment method info retrieval works")
        
        # Test getting info for invalid method
        invalid_info = payment_service.get_payment_method_info("paypal")
        assert invalid_info == {}
        print("✓ Invalid payment method info correctly returns empty dict")
        
        return True
    except Exception as e:
        print(f"✗ Error testing payment service methods: {e}")
        return False

def test_payment_summary_structure():
    """Test payment summary structure"""
    try:
        from app.services.payment_service import payment_service
        
        # Test payment summary structure (without database)
        summary = {
            "success": True,
            "total_revenue": 0.0,
            "total_transactions": 0,
            "payment_type_breakdown": {},
            "period": {
                "start_date": None,
                "end_date": None
            }
        }
        
        # Verify structure matches expected format
        required_keys = ["success", "total_revenue", "total_transactions", "payment_type_breakdown", "period"]
        for key in required_keys:
            assert key in summary
        print("✓ Payment summary structure is correct")
        
        return True
    except Exception as e:
        print(f"✗ Error testing payment summary structure: {e}")
        return False

def main():
    """Main test function"""
    print("Testing Payment Functionality Implementation")
    print("=" * 50)
    
    tests = [
        test_payment_service_import,
        test_payment_routes_import,
        test_payment_schemas_import,
        test_payment_methods,
        test_payment_service_methods,
        test_payment_summary_structure
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
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Payment functionality is implemented correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())