import psycopg2
import sqlite3

# Connect to the database
conn = sqlite3.connect('app/dev.db')
cursor = conn.cursor()

# Check if settings table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings';")
result = cursor.fetchall()
print('Settings table exists:', len(result) > 0)

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('All tables:')
for table in tables:
    print(f"  - {table[0]}")

# Close connection
conn.close()

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "mydb"
DB_USER = "postgres"
DB_PASS = "password"
DB_PORT = "5432"

try:
    # Connect to the database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    
    cursor = conn.cursor()
    
    # Check users table
    cursor.execute("SELECT COUNT(*) FROM users;")
    user_count = cursor.fetchone()[0]
    print(f"Number of users in database: {user_count}")
    
    # Check orders table
    cursor.execute("SELECT COUNT(*) FROM orders;")
    order_count = cursor.fetchone()[0]
    print(f"Number of orders in database: {order_count}")
    
    # List users
    cursor.execute("SELECT id, username, email, role FROM users;")
    users = cursor.fetchall()
    print("\nUsers in database:")
    for user in users:
        print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error connecting to database: {e}")