"""
Check the current tax rate in the database
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.settings import Setting
except ImportError:
    # Try importing directly (Docker container)
    try:
        from database import get_db
        from models.settings import Setting
    except ImportError:
        print("Could not import required modules. Please check your installation.")
        sys.exit(1)

def check_tax_rate():
    """Check the current tax rate in the database"""
    try:
        db_generator = get_db()
        db = next(db_generator)
    except Exception as e:
        print(f"Error getting database connection: {e}")
        return
    
    try:
        # Check if tax_rate setting exists
        tax_rate_setting = db.query(Setting).filter(Setting.key == "tax_rate").first()
        
        if tax_rate_setting:
            print(f"Tax rate setting found:")
            print(f"  Key: {tax_rate_setting.key}")
            print(f"  Value: {tax_rate_setting.value}")
            print(f"  Description: {tax_rate_setting.description}")
        else:
            print("No tax rate setting found in database")
            
    except Exception as e:
        print(f"Error checking tax rate: {e}")
    finally:
        # Close the database session
        db.close()

if __name__ == "__main__":
    check_tax_rate()