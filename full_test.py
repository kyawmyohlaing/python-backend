from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules
try:
    # Import models first to ensure they are registered with the Base
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
    print("Successfully imported modules")
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
config = Config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - the routers already have their prefixes defined
app.include_router(user_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(kitchen_router)
app.include_router(bar_router)
app.include_router(table_router)
app.include_router(invoice_router)
app.include_router(stock_router)
app.include_router(analytics_router)  # Include analytics router
app.include_router(payment_router)  # Include payment router

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8093, log_level="debug")