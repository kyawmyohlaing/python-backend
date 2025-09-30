import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import models first to ensure they are registered with the Base
# Import models in correct order to avoid circular dependencies
# Handle imports for both local development and Docker container environments
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
    from app.database import Base, engine
    from app.config import Config
except ImportError:
    # Try importing directly (Docker container)
    try:
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
        from database import Base, engine
        from config import Config
    except ImportError:
        # This should not happen, but let's have a clear error message
        raise ImportError("Could not import required modules. Please check your installation.")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Backend Skeleton")

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

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Backend with Postgres, JWT & Alembic!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Get port from environment variable or default to 8088
    port = int(os.getenv("PORT", 8088))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )