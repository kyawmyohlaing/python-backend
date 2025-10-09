"""
Create settings table in the database
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import Base, engine
    from app.models.settings import Setting
except ImportError:
    # Try importing directly (Docker container)
    try:
        from database import Base, engine
        from models.settings import Setting
    except ImportError:
        print("Could not import required modules. Please check your installation.")
        sys.exit(1)

def create_settings_table():
    """Create the settings table in the database"""
    try:
        # Create the settings table
        Setting.__table__.create(bind=engine, checkfirst=True)
        print("Settings table created successfully")
        
        # Verify the table was created
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='settings';"))
            tables = result.fetchall()
            if len(tables) > 0:
                print("Settings table verified in database")
            else:
                print("Warning: Settings table may not have been created properly")
                
    except Exception as e:
        print(f"Error creating settings table: {e}")

if __name__ == "__main__":
    create_settings_table()