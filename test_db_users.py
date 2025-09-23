from app.database import engine
from sqlalchemy import text

def test_users_table():
    try:
        with engine.connect() as conn:
            # Check if users table exists
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'users'"))
            tables = result.fetchall()
            print(f"Users table exists: {len(tables) > 0}")
            
            if len(tables) > 0:
                # Check table structure
                result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users'"))
                columns = result.fetchall()
                print("Users table columns:")
                for column in columns:
                    print(f"  - {column[0]}: {column[1]}")
                
                # Check if there are any users
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                count = result.fetchone()[0]
                print(f"Number of users in database: {count}")
                
                if count > 0:
                    # Show first user (without password)
                    result = conn.execute(text("SELECT id, username, email, role FROM users LIMIT 1"))
                    user = result.fetchone()
                    print(f"Sample user: {user}")
            else:
                print("Users table does not exist")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_users_table()