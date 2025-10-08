#!/usr/bin/env python3
"""
Script to check users in the PostgreSQL database directly
"""

import psycopg2
import sys

def check_users():
    """Check users in the PostgreSQL database directly"""
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="mydb",
            user="postgres",
            password="password"
        )
        
        cursor = conn.cursor()
        
        # Get all users
        cursor.execute("SELECT id, username, email, role, hashed_password FROM users;")
        users = cursor.fetchall()
        
        print("Users in PostgreSQL database:")
        print("=============================")
        for user in users:
            user_id, username, email, role, hashed_password = user
            print(f"ID: {user_id}")
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Role: {role}")
            print(f"Password hash: {hashed_password}")
            print(f"Password hash length: {len(hashed_password) if hashed_password else 0}")
            print("---")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error checking users: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_users()