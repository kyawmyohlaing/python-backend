# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.routes.user_routes import router as user_router
    from app.routes.menu_routes import router as menu_router
    from app.routes.order_routes import router as order_router
    from app.routes.kitchen_routes_db import router as kitchen_router
    from app.routes.table_routes import router as table_router
    from app.routes.invoice_routes import router as invoice_router
except ImportError:
    # Try importing directly (Docker container)
    from routes.user_routes import router as user_router
    from routes.menu_routes import router as menu_router
    from routes.order_routes import router as order_router
    from routes.kitchen_routes_db import router as kitchen_router
    from routes.table_routes import router as table_router
    from routes.invoice_routes import router as invoice_router