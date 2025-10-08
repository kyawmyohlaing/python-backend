#!/usr/bin/env python3
"""
Full route test to simulate the exact FastAPI route call
"""

import sys
import os
from fastapi import Form, Depends
from sqlalchemy.orm import Session

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules
try:
    from app.database import get_db, engine, Base
    from app.models.user import User
    from app.services.user_service import UserService
    from app.security import create_access_token
    from app.routes.user_routes import login_user
    from sqlalchemy.orm import sessionmaker
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def full_route_test():
    try:
        print("Full route test...")
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test the login function exactly as FastAPI would call it
        print("\n--- Testing login_user function as FastAPI would call it ---")
        try:
            # This simulates what the FastAPI route does
            # The function signature is: login_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db))
            # We need to pass the parameters as they would be received by FastAPI
            result = login_user("manager", "manager123", db)
            print(f"✅ Full route test successful: {result}")
        except Exception as e:
            print(f"❌ Full route test failed: {e}")
            import traceback
            traceback.print_exc()
        
        db.close()
        
    except Exception as e:
        print(f"Error in full route test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    full_route_test()