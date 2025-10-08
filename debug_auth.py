import sqlite3
import os
from app.security import verify_password, hash_password

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'app', 'dev.db')
print(f"Database path: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get the manager user
    cursor.execute("SELECT id, username, email, hashed_password, role FROM users WHERE username = 'manager';")
    user = cursor.fetchone()
    
    if user:
        print("Manager user found:")
        print(f"  ID: {user[0]}")
        print(f"  Username: {user[1]}")
        print(f"  Email: {user[2]}")
        print(f"  Role: {user[4]}")
        print(f"  Hashed Password: {user[3]}")
        
        # Test password verification
        test_password = "manager123"
        print(f"\nTesting password verification with '{test_password}':")
        
        # Verify the password
        is_valid = verify_password(test_password, user[3])
        print(f"Password valid: {is_valid}")
        
        # Test hashing the same password
        hashed_test = hash_password(test_password)
        print(f"Hashed test password: {hashed_test}")
        
        # Verify with the new hash
        is_valid_new = verify_password(test_password, hashed_test)
        print(f"New hash verification: {is_valid_new}")
    else:
        print("Manager user not found")
        
    conn.close()
    
except Exception as e:
    print(f"Error accessing database: {e}")
    import traceback
    traceback.print_exc()