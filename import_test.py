import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Testing imports...")

# Test the first import block
try:
    # Try importing from app.module (local development)
    from app.models import User, MenuItem, Order, OrderItem, Invoice, KitchenOrder, Table, Ingredient, StockTransaction
    # Import the updated router
    from app.routes.user_routes import router as user_router
    from app.routes.menu_routes import router as menu_router
    from app.routes.order_routes import router as order_router
    from app.routes.table_routes import router as table_router
    from app.routes.invoice_routes import router as invoice_router
    from app.routes.kitchen_routes_db import router as kitchen_router
    from app.routes.bar_routes import router as bar_router
    from app.routes.stock_routes import router as stock_router
    from app.routes.analytics_routes import router as analytics_router  # Add analytics router
    from app.routes.payment_routes import router as payment_router  # Add payment router
    from app.database import Base, engine
    from app.config import Config
    print("First import block successful")
except ImportError as e:
    print(f"First import block failed: {e}")
    import traceback
    traceback.print_exc()

# Test the second import block
try:
    # Try importing directly (Docker container)
    from models import User, MenuItem, Order, OrderItem, Invoice, KitchenOrder, Table, Ingredient, StockTransaction
    from routes.user_routes import router as user_router
    from routes.menu_routes import router as menu_router
    from routes.order_routes import router as order_router
    from routes.table_routes import router as table_router
    from routes.invoice_routes import router as invoice_router
    from routes.kitchen_routes_db import router as kitchen_router
    from routes.bar_routes import router as bar_router
    from routes.stock_routes import router as stock_router
    from routes.analytics_routes import router as analytics_router  # Add analytics router
    from routes.payment_routes import router as payment_router  # Add payment router
    from database import Base, engine
    from config import Config
    print("Second import block successful")
except ImportError as e:
    print(f"Second import block failed: {e}")
    import traceback
    traceback.print_exc()

print("Import test complete")