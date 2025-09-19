import sqlite3
import json
from datetime import datetime

def debug_order_31_db():
    # Connect to the database
    conn = sqlite3.connect('dev.db')
    cursor = conn.cursor()
    
    # Get order #31
    cursor.execute("SELECT * FROM orders WHERE id = ?", (31,))
    order = cursor.fetchone()
    
    # Get column names
    column_names = [description[0] for description in cursor.description]
    
    if order:
        print("Order #31 Details from Database:")
        print("-" * 50)
        for i, (column, value) in enumerate(zip(column_names, order)):
            print(f"{column}: {value}")
    else:
        print("Order #31 not found in database")
    
    conn.close()

if __name__ == "__main__":
    debug_order_31_db()