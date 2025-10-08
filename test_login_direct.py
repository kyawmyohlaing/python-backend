import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules
try:
    from app.database import get_db
    from app.routes.user_routes import login_user
    from fastapi import Form
    print("Successfully imported modules")
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def test_login_direct():
    print("Testing login function directly...")
    
    try:
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        # Test the login function directly
        print("\n1. Calling login_user function directly...")
        result = login_user("manager", "manager123", db)
        print(f"Result: {result}")
        
        # Close database session
        try:
            next(db_gen)
        except StopIteration:
            pass
            
    except Exception as e:
        print(f"Error during direct login test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login_direct()