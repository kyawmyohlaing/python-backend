#!/usr/bin/env python3
"""
Route test to isolate the issue
"""

import sys
import os

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

def route_test():
    try:
        print("Route test...")
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test the login function directly with the same parameters as the route
        print("\n--- Testing login_user route function directly ---")
        try:
            # This simulates what the FastAPI route does
            result = login_user("manager", "manager123", db)
            print(f"✅ Login route function successful: {result}")
        except Exception as e:
            print(f"❌ Login route function failed: {e}")
            import traceback
            traceback.print_exc()
        
        db.close()
        
    except Exception as e:
        print(f"Error in route test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    route_test()