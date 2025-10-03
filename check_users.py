#!/usr/bin/env python3
"""
Script to check existing users in the database with the correct schema
"""

import sqlite3
import os

def check_users():
    """Check existing users in the database"""
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('app/dev.db')
        cursor = conn.cursor()
        
        # Get all users (using the new schema)
        cursor.execute('SELECT id, username, email, role FROM users')
        users = cursor.fetchall()
        
        print(f"Found {len(users)} users in the database:")
        
        for user in users:
            print(f"  - ID: {user[0]}")
            print(f"    Username: {user[1]}")
            print(f"    Email: {user[2]}")
            print(f"    Role: {user[3]}")
            print()
            
        conn.close()
                
    except Exception as e:
        print(f"Error connecting to database: {e}")

if __name__ == "__main__":
    check_users()