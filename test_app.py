import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Test importing the models
try:
    from app.models import user, menu, order, order_item, invoice, kitchen, table
    print("All models imported successfully!")
except ImportError as e:
    print(f"Error importing models: {e}")
    sys.exit(1)

# Test importing the database
try:
    from app.database import Base, engine
    print("Database imported successfully!")
except ImportError as e:
    print(f"Error importing database: {e}")
    sys.exit(1)

# Test creating tables
try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")
    sys.exit(1)

print("All tests passed!")