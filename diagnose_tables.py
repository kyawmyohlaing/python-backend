"""
Diagnostic script to check the current state of tables and their seats data
"""
import sys
import os
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
import json

# Add the parent directory to the Python path to import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try importing from app.module (local development)
    from app.database import Base
    from app.models.table import Table
except ImportError:
    # Try importing directly (Docker container)
    try:
        from database import Base
        from models.table import Table
    except ImportError:
        # If we can't import the modules, we'll work directly with SQLAlchemy
        Table = None

def diagnose_tables():
    """Diagnose the current state of tables and their seats data"""
    
    # Try to get database URL from environment or use default
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./app/dev.db')
    
    # Create engine and session
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print(f"Connected to database: {DATABASE_URL}")
        
        # If we have the Table model, use it
        if Table is not None:
            # Get all tables
            all_tables = db.query(Table).all()
            
            print(f"Found {len(all_tables)} tables in the database")
            
            # Show details for each table
            for table in all_tables:
                print(f"\nTable #{table.table_number} (ID: {table.id})")
                print(f"  Capacity: {table.capacity}")
                print(f"  Status: {table.status}")
                print(f"  Occupied: {table.is_occupied}")
                print(f"  Current Order ID: {table.current_order_id}")
                print(f"  Seats data type: {type(table.seats)}")
                print(f"  Seats data: {table.seats}")
                
                # Check if seats is None or empty
                if table.seats is None:
                    print("  WARNING: Seats is None!")
                elif isinstance(table.seats, list):
                    print(f"  Number of seats: {len(table.seats)}")
                    for i, seat in enumerate(table.seats):
                        print(f"    Seat {i+1}: {seat}")
                else:
                    print(f"  WARNING: Seats is not a list! Type: {type(table.seats)}")
        else:
            # Work directly with SQL
            print("Working directly with SQL...")
            
            # Get all tables
            result = db.execute(text("SELECT id, table_number, capacity, status, is_occupied, current_order_id, seats FROM tables"))
            all_tables = result.fetchall()
            
            print(f"Found {len(all_tables)} tables in the database")
            
            # Show details for each table
            for row in all_tables:
                table_id = row[0]
                table_number = row[1]
                capacity = row[2]
                status = row[3]
                is_occupied = row[4]
                current_order_id = row[5]
                seats = row[6]
                
                print(f"\nTable #{table_number} (ID: {table_id})")
                print(f"  Capacity: {capacity}")
                print(f"  Status: {status}")
                print(f"  Occupied: {is_occupied}")
                print(f"  Current Order ID: {current_order_id}")
                print(f"  Seats data type: {type(seats)}")
                print(f"  Seats data: {seats}")
                
                # Try to parse JSON if it's a string
                if isinstance(seats, str):
                    try:
                        seats_data = json.loads(seats)
                        print(f"  Parsed seats data: {seats_data}")
                        print(f"  Number of seats: {len(seats_data)}")
                    except json.JSONDecodeError:
                        print("  WARNING: Could not parse seats as JSON!")
                elif seats is None:
                    print("  WARNING: Seats is None!")
                elif isinstance(seats, list):
                    print(f"  Number of seats: {len(seats)}")
                    for i, seat in enumerate(seats):
                        print(f"    Seat {i+1}: {seat}")
        
    except Exception as e:
        print(f"Error diagnosing tables: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    diagnose_tables()