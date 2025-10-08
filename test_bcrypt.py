#!/usr/bin/env python3
"""
Simple test script to verify bcrypt functionality
"""

from passlib.context import CryptContext

def test_bcrypt():
    """Test bcrypt functionality"""
    try:
        print("Testing bcrypt functionality...")
        
        # Create a password context
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Test password
        password = "manager123"
        print(f"Original password: {password}")
        print(f"Password length: {len(password)}")
        
        # Hash the password
        print("Hashing password...")
        hashed = pwd_context.hash(password)
        print(f"Hashed password: {hashed}")
        
        # Verify the password
        print("Verifying password...")
        is_valid = pwd_context.verify(password, hashed)
        print(f"Password verification result: {is_valid}")
        
        print("✅ Bcrypt test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing bcrypt: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bcrypt()