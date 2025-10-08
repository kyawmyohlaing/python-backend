#!/usr/bin/env python3
"""
Test script to verify bcrypt functionality directly
"""

import bcrypt

def test_direct_bcrypt():
    """Test bcrypt functionality directly"""
    try:
        print("Testing direct bcrypt functionality...")
        
        # Test password
        password = "manager123"
        print(f"Original password: {password}")
        print(f"Password length: {len(password)}")
        
        # Hash the password
        print("Hashing password...")
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        print(f"Hashed password: {hashed}")
        
        # Verify the password
        print("Verifying password...")
        is_valid = bcrypt.checkpw(password_bytes, hashed)
        print(f"Password verification result: {is_valid}")
        
        print("✅ Direct bcrypt test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing direct bcrypt: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_bcrypt()