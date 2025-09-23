#!/usr/bin/env python3
"""
Test script to check imports
"""

print("Testing imports...")

try:
    from app.schemas.user_schema import UserUpdate
    print("✓ UserUpdate imported successfully")
except Exception as e:
    print(f"✗ Failed to import UserUpdate: {e}")

try:
    from app.routes.user_routes import router
    print("✓ User routes imported successfully")
except Exception as e:
    print(f"✗ Failed to import user routes: {e}")

print("Import test completed.")