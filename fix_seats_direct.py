"""
Direct script to fix tables with null seats values
This can be run directly without using alembic migrations
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

def fix_null_seats_direct():
    """Fix tables that have null seats values using direct database connection"""
    
    # Try to get database URL from environment or use default
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
    
    # Create engine and session
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # If we have the Table model, use it
        if Table is not None:
            # Find all tables with null seats
            tables_with_null_seats = db.query(Table).filter(Table.seats.is_(None)).all()
            
            print(f"Found {len(tables_with_null_seats)} tables with null seats")
            
            # Update each table to have an empty seats array
            for table in tables_with_null_seats:
                print(f"Fixing table {table.id} (Table #{table.table_number}) with capacity {table.capacity}")
                table.seats = []
                # Initialize seats based on capacity
                for i in range(table.capacity or 0):  # Handle None capacity
                    table.seats.append({
                        "seat_number": i + 1,
                        "status": "available",
                        "customer_name": None
                    })
            
            # Commit changes
            db.commit()
            print("Successfully fixed all tables with null seats using ORM")
        else:
            # Work directly with SQL
            print("Working directly with SQL...")
            
            # Find tables with null seats
            result = db.execute(text("SELECT id, table_number, capacity FROM tables WHERE seats IS NULL"))
            tables_with_null_seats = result.fetchall()
            
            print(f"Found {len(tables_with_null_seats)} tables with null seats")
            
            # Update each table
            for row in tables_with_null_seats:
                table_id = row[0]
                table_number = row[1]
                capacity = row[2] or 0  # Handle None capacity
                
                print(f"Fixing table {table_id} (Table #{table_number}) with capacity {capacity}")
                
                # Initialize seats based on capacity
                seats = []
                for i in range(capacity):
                    seats.append({
                        "seat_number": i + 1,
                        "status": "available",
                        "customer_name": None
                    })
                
                # Update the table record
                db.execute(
                    text("UPDATE tables SET seats = :seats WHERE id = :id"),
                    {"seats": json.dumps(seats), "id": table_id}
                )
            
            # Commit changes
            db.commit()
            print("Successfully fixed all tables with null seats using direct SQL")
        
    except Exception as e:
        print(f"Error fixing tables: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_null_seats_direct()