import uvicorn
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the app
from app.main import app

if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8088, log_level="info")