from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# Since we're in the container and files are directly in /app, we import directly
from config import Config

# Get database URL from configuration
config = Config()
DATABASE_URL = config.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()