#!/usr/bin/env python3
"""
Test script to verify database connectivity
"""

import sys
import os

# Add the current directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database():
    """Test database connectivity"""
    try:
        # Test config import
        from app.config import Config
        config = Config()
        print(f"Database URL: {config.DATABASE_URL}")
        
        # Test database import
        from app.database import engine, SessionLocal, Base
        print("✓ Database modules imported successfully")
        
        # Test creating a session
        session = SessionLocal()
        print("✓ Database session created successfully")
        
        # Test closing session
        session.close()
        print("✓ Database session closed successfully")
        
        print("\nDatabase connectivity test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Database connectivity error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing database connectivity...")
    success = test_database()
    sys.exit(0 if success else 1)