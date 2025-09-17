#!/usr/bin/env python3
"""
Test script to verify that all imports work correctly
"""

print("Testing imports...")

try:
    print("Importing app.main...")
    import app.main
    print("✓ app.main imported successfully")
except Exception as e:
    print(f"✗ Failed to import app.main: {e}")

try:
    print("Importing app.routes.table_routes...")
    import app.routes.table_routes
    print("✓ app.routes.table_routes imported successfully")
except Exception as e:
    print(f"✗ Failed to import app.routes.table_routes: {e}")

try:
    print("Importing app.schemas.table_schema...")
    import app.schemas.table_schema
    print("✓ app.schemas.table_schema imported successfully")
except Exception as e:
    print(f"✗ Failed to import app.schemas.table_schema: {e}")

try:
    print("Importing app.models.table...")
    import app.models.table
    print("✓ app.models.table imported successfully")
except Exception as e:
    print(f"✗ Failed to import app.models.table: {e}")

print("Import test completed.")