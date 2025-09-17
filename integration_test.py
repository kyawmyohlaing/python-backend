#!/usr/bin/env python3
"""
Integration test to verify that the application components work together correctly
"""

import sys
import os

# Add the current directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_application_startup():
    """Test that the application can start without errors"""
    try:
        print("Testing application startup...")
        
        # Import all the necessary components
        from app.models import order, kitchen, table, menu, invoice
        print("✓ All models imported successfully")
        
        from app.database import engine, SessionLocal, Base
        print("✓ Database components imported successfully")
        
        # Test creating all tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
        
        from app.routes import user_router, menu_router, order_router, table_router, invoice_router
        from app.routes.kitchen_routes_db import router as kitchen_router
        print("✓ All routes imported successfully")
        
        from app.services.kot_service_simple import kot_service
        print("✓ KOT service imported successfully")
        
        # Test creating the FastAPI app
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(title="FastAPI Backend Skeleton")
        
        # Add routers to app
        app.include_router(user_router)
        app.include_router(menu_router)
        app.include_router(order_router)
        app.include_router(kitchen_router)
        app.include_router(table_router)
        app.include_router(invoice_router)
        
        print("✓ FastAPI application created successfully")
        print("✓ All routers included successfully")
        
        print("\n🎉 Application startup test passed!")
        print("The application should work correctly with database storage.")
        return True
        
    except Exception as e:
        print(f"✗ Application startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_application_startup()
    sys.exit(0 if success else 1)
