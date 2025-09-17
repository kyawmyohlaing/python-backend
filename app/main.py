from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import models first to ensure they are registered with the Base
# Import models in correct order to avoid circular dependencies
# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.models import user, menu, order, order_item, invoice, kitchen, table
    from app.routes import user_router, menu_router, order_router, table_router, invoice_router
    from app.routes.kitchen_routes_db import router as kitchen_router
    from app.database import Base, engine
    from app.config import Config
except ImportError:
    # Try importing directly (Docker container)
    try:
        from models import user, menu, order, order_item, invoice, kitchen, table
        from routes import user_router, menu_router, order_router, table_router, invoice_router
        from routes.kitchen_routes_db import router as kitchen_router
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

app.include_router(user_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(kitchen_router)
app.include_router(table_router)
app.include_router(invoice_router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Backend with Postgres, JWT & Alembic!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}