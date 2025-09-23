import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    # Try to import the database
    from app.database import engine
    from sqlalchemy import text
    
    print("✅ Database engine imported successfully")
    
    # Try to connect to the database
    with engine.connect() as conn:
        # Check if users table exists
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'users'"))
        tables = result.fetchall()
        if tables:
            print("✅ Users table exists")
            # Try to query the users table structure
            result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users'"))
            columns = result.fetchall()
            print("Users table columns:")
            for column in columns:
                print(f"  - {column[0]}: {column[1]}")
        else:
            print("❌ Users table does not exist")
            
        # Check if there are any users
        try:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            row = result.fetchone()
            if row is not None:
                count = row[0]
                print(f"Number of users in database: {count}")
            else:
                print("No result from COUNT query")
        except Exception as e:
            print(f"Could not query users table: {e}")
            
except Exception as e:
    print(f"❌ Error connecting to database: {e}")
    import traceback
    traceback.print_exc()