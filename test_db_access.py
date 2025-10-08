import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules
try:
    from app.database import get_db
    from app.models.user import User
    print("Successfully imported modules")
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def test_database_access():
    print("Testing database access...")
    
    try:
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        print("Database session created")
        
        # Test querying users
        print("\n1. Querying all users...")
        users = db.query(User).all()
        print(f"Found {len(users)} users")
        for user in users:
            print(f"  - {user.username} ({user.email}) - {user.role}")
            
        # Test querying specific user
        print("\n2. Querying manager user...")
        manager = db.query(User).filter(User.username == "manager").first()
        if manager:
            print(f"Manager found: {manager.username} ({manager.email}) - {manager.role}")
            print(f"Role type: {type(manager.role)}")
            print(f"Role value: {manager.role.value}")
        else:
            print("Manager not found")
            
        # Close database session
        try:
            next(db_gen)
        except StopIteration:
            pass
            
    except Exception as e:
        print(f"Error during database access test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_access()