#!/usr/bin/env python3
"""
Test script to verify hash verification with the specific hash we're using
"""

from passlib.context import CryptContext

def test_hash_verification():
    """Test hash verification with our specific hash"""
    try:
        print("Testing hash verification...")
        
        # Create a password context
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Test password
        password = "manager123"
        print(f"Original password: {password}")
        
        # Our specific hash
        hash_to_test = "$2b$12$YljZqlQHihFUg5UuFya5VuNWMrvVvAcgk14hoq9j7DRHbqaZNggKe"
        print(f"Hash to test: {hash_to_test}")
        
        # Verify the password against the hash
        print("Verifying password against hash...")
        is_valid = pwd_context.verify(password, hash_to_test)
        print(f"Password verification result: {is_valid}")
        
        print("✅ Hash verification test completed!")
        
    except Exception as e:
        print(f"❌ Error during hash verification: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_hash_verification()