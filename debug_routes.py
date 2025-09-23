import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    # Try to import the user routes
    from app.routes.user_routes import router
    print("✅ User routes imported successfully")
    print(f"Router prefix: {getattr(router, 'prefix', 'No prefix')}")
    print(f"Number of routes: {len(getattr(router, 'routes', []))}")
    
    # List all routes
    for route in getattr(router, 'routes', []):
        methods = getattr(route, 'methods', 'Unknown')
        path = getattr(route, 'path', 'Unknown')
        print(f"  - {methods} {path}")
        
except Exception as e:
    print(f"❌ Error importing user routes: {e}")
    import traceback
    traceback.print_exc()

try:
    # Try to import the main app
    from app.main import app
    print("\n✅ Main app imported successfully")
    print(f"App title: {getattr(app, 'title', 'No title')}")
    
    # List all routes in the app
    routes = getattr(app, 'routes', [])
    print(f"Total routes in app: {len(routes)}")
    for route in routes:
        methods = getattr(route, 'methods', 'Unknown')
        path = getattr(route, 'path', 'Unknown')
        print(f"  - {methods} {path}")
        
except Exception as e:
    print(f"❌ Error importing main app: {e}")
    import traceback
    traceback.print_exc()