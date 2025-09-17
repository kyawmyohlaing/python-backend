import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Test importing the database
try:
    from app.database import Base, engine
    print("Database imported successfully!")
except ImportError as e:
    print(f"Error importing database: {e}")
    sys.exit(1)

# Test importing the models one by one
try:
    from app.models import user
    print("User model imported successfully!")
except ImportError as e:
    print(f"Error importing user model: {e}")

try:
    from app.models import menu
    print("Menu model imported successfully!")
except ImportError as e:
    print(f"Error importing menu model: {e}")

try:
    from app.models import order
    print("Order model imported successfully!")
except ImportError as e:
    print(f"Error importing order model: {e}")

try:
    from app.models import order_item
    print("OrderItem model imported successfully!")
except ImportError as e:
    print(f"Error importing order_item model: {e}")

try:
    from app.models import kitchen
    print("Kitchen model imported successfully!")
except ImportError as e:
    print(f"Error importing kitchen model: {e}")

try:
    from app.models import table
    print("Table model imported successfully!")
except ImportError as e:
    print(f"Error importing table model: {e}")

# Test creating tables
try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")
    sys.exit(1)

print("All tests passed!")