import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import only the user router to isolate the issue
try:
    # Try importing from app.module (local development)
    from app.routes.user_routes import router as user_router
    from app.database import Base, engine
    from app.config import Config
except ImportError:
    # Try importing directly (Docker container)
    try:
        from routes.user_routes import router as user_router
        from database import Base, engine
        from config import Config
    except ImportError:
        # This should not happen, but let's have a clear error message
        raise ImportError("Could not import required modules. Please check your installation.")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simplified FastAPI Backend")

# Add CORS middleware
config = Config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only the user router
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Simplified FastAPI Backend"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Get port from environment variable or default to 8088
    port = int(os.getenv("PORT", 8091))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "simplified_main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )