#!/usr/bin/env python3
"""
Script to run the backend server with the seat assignment fix.
This script ensures that the fixed table_routes.py is used.
"""

import os
import sys
import subprocess

def main():
    print("Starting backend server with seat assignment fix...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the app directory
    app_dir = os.path.join(current_dir, "app")
    if os.path.exists(app_dir):
        os.chdir(app_dir)
        print(f"Changed to directory: {app_dir}")
    else:
        print(f"App directory not found: {app_dir}")
        return
    
    # Try to run the FastAPI server
    try:
        # Check if uvicorn is installed
        import uvicorn
        print("Starting FastAPI server with uvicorn...")
        
        # Run the server
        # Assuming the main app is in main.py and the app instance is named "app"
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
        
    except ImportError:
        print("uvicorn not found. Trying with standard Python...")
        try:
            # Try to run main.py directly
            subprocess.run([sys.executable, "main.py"])
        except Exception as e:
            print(f"Failed to start server: {e}")
            print("Please make sure you have the required dependencies installed.")
            print("You can install them with: pip install fastapi uvicorn sqlalchemy")
    except Exception as e:
        print(f"Failed to start server: {e}")

if __name__ == "__main__":
    main()