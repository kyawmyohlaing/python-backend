#!/usr/bin/env python3
"""
Verification script to ensure payment API endpoints are properly integrated
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def verify_payment_api_integration():
    """Verify that payment API is properly integrated"""
    try:
        # Import the main app
        from app.main import app
        
        # Check if payment routes are included
        payment_routes = [route for route in app.routes if route.path.startswith("/api/payments")]
        
        if len(payment_routes) > 0:
            print("✓ Payment routes are properly integrated into the main app")
            print(f"✓ Found {len(payment_routes)} payment API endpoints:")
            for route in payment_routes:
                print(f"  - {route.methods} {route.path}")
            return True
        else:
            print("✗ No payment routes found in the main app")
            return False
            
    except Exception as e:
        print(f"✗ Error verifying payment API integration: {e}")
        return False

def verify_payment_service_functionality():
    """Verify payment service functionality"""
    try:
        from app.services.payment_service import payment_service
        
        # Test payment method validation
        assert payment_service.validate_payment_type("cash") == True
        assert payment_service.validate_payment_type("card") == True
        assert payment_service.validate_payment_type("invalid") == False
        
        # Test payment method info retrieval
        cash_info = payment_service.get_payment_method_info("cash")
        assert "name" in cash_info
        assert "requires_processing" in cash_info
        
        print("✓ Payment service functionality verified")
        return True
        
    except Exception as e:
        print(f"✗ Error verifying payment service functionality: {e}")
        return False

def verify_payment_schemas():
    """Verify payment schemas"""
    try:
        from app.schemas.payment_schema import (
            PaymentProcessRequest, 
            PaymentProcessResponse,
            RefundProcessRequest,
            RefundProcessResponse
        )
        
        # Test schema instantiation
        request = PaymentProcessRequest(
            order_id=1,
            payment_type="cash",
            amount=10.0
        )
        
        response = PaymentProcessResponse(
            success=True,
            order_id=1,
            payment_type="cash",
            amount=10.0,
            timestamp="2025-10-01T10:00:00"
        )
        
        print("✓ Payment schemas verified")
        return True
        
    except Exception as e:
        print(f"✗ Error verifying payment schemas: {e}")
        return False

def main():
    """Main verification function"""
    print("Verifying Payment API Implementation")
    print("=" * 40)
    
    tests = [
        verify_payment_api_integration,
        verify_payment_service_functionality,
        verify_payment_schemas
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
    print(f"Verification Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All verifications passed! Payment API is properly implemented and integrated.")
        return 0
    else:
        print("❌ Some verifications failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())