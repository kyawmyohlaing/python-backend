import sys
import os

# Add the app directory to the Python path
sys.path.append('/app')

try:
    # Try to import the main app
    from app.main import app
    print("✅ Main app imported successfully")
    print(f"App title: {getattr(app, 'title', 'No title')}")
    
    # List all routes in the app
    routes = getattr(app, 'routes', [])
    print(f"Total routes in app: {len(routes)}")
    for route in routes:
        methods = getattr(route, 'methods', set())
        path = getattr(route, 'path', 'Unknown')
        print(f"  - {methods} {path}")
        
except Exception as e:
    print(f"❌ Error importing main app: {e}")
    import traceback
    traceback.print_exc()