#!/bin/bash
set -e

# Debug information
echo "Starting start.sh script"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"

# Wait for Postgres using Python instead of pg_isready or netcat
echo "Waiting for Postgres..."
until python -c "import socket; socket.create_connection(('db', 5432), timeout=5)" 2>/dev/null; do
  sleep 1
done
echo "Postgres ready!"

# Run Alembic migrations
echo "Running Alembic migrations..."
cd /app  # Change to the app directory where migrations are located

# Run alembic from within the migrations directory
cd migrations
alembic -c alembic.ini upgrade head

# Change back to the app directory
cd /app

# Initialize database with sample data
echo "Initializing database with sample data..."
# Use Python directly to initialize the database
python -c "
import sys
sys.path.insert(0, '/app')
from database import Base
from models.menu import MenuItem
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use the database URL directly
DATABASE_URL = 'postgresql://postgres:password@db:5432/mydb'
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Check if we already have menu items
existing_items = db.query(MenuItem).count()
if existing_items == 0:
    print('Adding sample menu items...')
    # Add sample menu items
    sample_items = [
        MenuItem(name='Burger', price=8.99, category='food'),
        MenuItem(name='Pizza', price=12.99, category='food'),
        MenuItem(name='Salad', price=7.99, category='food'),
        MenuItem(name='Soda', price=2.99, category='drink'),
        MenuItem(name='Coffee', price=3.99, category='drink'),
        MenuItem(name='Tea Leaf Salad', price=6.99, category='food'),
        MenuItem(name='Chicken Curry', price=11.99, category='food'),
        MenuItem(name='Steak (Grill)', price=18.99, category='food'),
        MenuItem(name='Wine', price=7.99, category='alcohol'),
        MenuItem(name='Beer', price=5.99, category='alcohol'),
    ]
    
    for item in sample_items:
        db.add(item)
    
    db.commit()
    print('Sample menu items added successfully.')
else:
    print(f'Database already contains {existing_items} menu items. Skipping sample data insertion.')

# Check if we have any users
existing_users = db.query(User).count()
if existing_users == 0:
    print('Adding sample user...')
    # Add a sample user (in a real application, you'd want to hash the password)
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    
    sample_user = User(
        username='admin',
        email='admin@example.com',
        hashed_password=pwd_context.hash('admin123'),
        role='admin'
    )
    
    db.add(sample_user)
    db.commit()
    print('Sample user added successfully.')
else:
    print(f'Database already contains {existing_users} users. Skipping user insertion.')

db.close()
print('Database initialization completed successfully.')
"

# Start server
echo "Starting server..."
exec "$@"