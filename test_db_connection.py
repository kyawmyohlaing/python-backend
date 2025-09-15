import psycopg2
from psycopg2 import sql

try:
    # Try to connect to the database
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="mydb",
        user="postgres",
        password="password",
        sslmode="disable"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"Successfully connected to PostgreSQL: {version[0]}")
    
    # Check if invoices table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'invoices'
        );
    """)
    table_exists = cursor.fetchone()[0]
    print(f"Invoices table exists: {table_exists}")
    
    if table_exists:
        # Get table schema
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'invoices'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        print("\nInvoices table schema:")
        for column in columns:
            print(f"  {column[0]}: {column[1]} ({'NULL' if column[2] == 'YES' else 'NOT NULL'})")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error connecting to database: {e}")