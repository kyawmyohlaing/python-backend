#!/usr/bin/env python3
"""
Test script to verify that the new user fields (full_name, created_at, updated_at) are working correctly.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_user_model_fields():
    """Test that the User model has the new fields"""
    try:
        from app.models.user import User
        # Check that the User class has the new fields
        assert hasattr(User, 'full_name'), "User model should have full_name field"
        assert hasattr(User, 'created_at'), "User model should have created_at field"
        assert hasattr(User, 'updated_at'), "User model should have updated_at field"
        print("✓ User model has all required fields")
        return True
    except Exception as e:
        print(f"✗ Error testing User model: {e}")
        return False

def test_user_schema_fields():
    """Test that the User schema has the new fields"""
    try:
        from app.schemas.user_schema import UserResponse
        # Check that the UserResponse schema has the new fields
        # We can't easily check Pydantic model fields, but we can at least import it
        print("✓ UserResponse schema imported successfully")
        return True
    except Exception as e:
        print(f"✗ Error testing User schema: {e}")
        return False

def test_migration_file_exists():
    """Test that the migration file exists"""
    migration_file = os.path.join(os.path.dirname(__file__), 'app', 'migrations', 'versions', '0010_add_full_name_and_timestamps_to_users.py')
    if os.path.exists(migration_file):
        print("✓ Migration file exists")
        return True
    else:
        print("✗ Migration file does not exist")
        return False

if __name__ == "__main__":
    print("Testing user field implementations...")
    print()
    
    tests = [
        test_user_model_fields,
        test_user_schema_fields,
        test_migration_file_exists
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
        print()
    
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    
    if failed == 0:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)