from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# Since we're in the container and files are directly in /app, we import directly
from config import Config

# Get database URL from configuration
config = Config()
DATABASE_URL = config.DATABASE_URL

# When running in Docker, we need to use the service name 'db' instead of 'localhost'
# Check if we're running in Docker by checking for the .dockerenv file
import os
if os.path.exists('/.dockerenv'):
    # We're in Docker, replace localhost with db service name
    DATABASE_URL = DATABASE_URL.replace('localhost', 'db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()