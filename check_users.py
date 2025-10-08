import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'app', 'dev.db')
print(f"Database path: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print("Users table exists")
        # Get all users
        cursor.execute("SELECT id, username, email, role FROM users;")
        users = cursor.fetchall()
        
        if users:
            print("Existing users:")
            for user in users:
                print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
        else:
            print("No users found in the database")
    else:
        print("Users table does not exist")
        
    conn.close()
    
except Exception as e:
    print(f"Error accessing database: {e}")