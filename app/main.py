from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Since we're in the container and files are directly in /app, we import directly
from routes import user_routes
from database import Base, engine
from config import Config

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

app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Backend with Postgres, JWT & Alembic!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}