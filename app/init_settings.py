"""
Initialize default settings in the database
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

def init_default_settings():
    """Initialize default settings in the database"""
    try:
        db_generator = get_db()
        db = next(db_generator)
    except Exception as e:
        print(f"Error getting database connection: {e}")
        return
    
    try:
        # Check if tax_rate setting already exists
        existing_setting = db.query(Setting).filter(Setting.key == "tax_rate").first()
        
        if not existing_setting:
            # Create default tax rate setting (8%)
            tax_rate_setting = Setting(
                key="tax_rate",
                value="0.08",
                description="Default tax rate (8%)"
            )
            db.add(tax_rate_setting)
            db.commit()
            print("Default tax rate setting (8%) initialized successfully")
        else:
            print("Tax rate setting already exists")
            
    except Exception as e:
        print(f"Error initializing default settings: {e}")
        db.rollback()
    finally:
        # Close the database session
        db.close()

if __name__ == "__main__":
    init_default_settings()