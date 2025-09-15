#!/usr/bin/env python3
"""
Script to update database schema to match model definitions
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Set environment variables for testing
os.environ["SECRET_KEY"] = "test-secret-key"

def update_database_schema():
    """Update database schema to match model definitions"""
    try:
        print("Updating database schema...")
        
        from app.database import Base, engine
        from app.models import order, table, menu, kitchen, invoice, user
        
        # This will create any missing tables or columns
        print("Creating tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database schema updated successfully!")
        
        # Verify the tables exist
        from sqlalchemy import text
        with engine.connect() as conn:
            inspector = conn.dialect.inspector(engine)
            tables = inspector.get_table_names()
            print(f"📊 Database tables: {tables}")
            
            if 'orders' in tables:
                columns = inspector.get_columns('orders')
                print("📋 Orders table columns:")
                for col in columns:
                    print(f"   - {col['name']}: {col['type']}")
            
        return True
    except Exception as e:
        print(f"❌ Database schema update failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = update_database_schema()
    if success:
        print("\n🎉 Database schema updated successfully!")
        print("You can now try submitting orders again.")
    else:
        print("\n💥 Database schema update failed!")
        print("Please check the error above and try again.")