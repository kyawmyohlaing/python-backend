"""
Database migration script to create stock tracking tables.
This script can be used to manually create the tables if needed.
"""

from sqlalchemy import create_engine, MetaData
from app.models.stock import Base
from app.database import DATABASE_URL

def create_stock_tables():
    """Create stock tracking tables in the database"""
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    
    # Create all tables defined in the stock module
    Base.metadata.create_all(engine)
    
    print("Stock tracking tables created successfully!")

if __name__ == "__main__":
    create_stock_tables()