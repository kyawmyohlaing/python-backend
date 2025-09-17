from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError   
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from configuration
# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.config (local development)
    from app.config import Config
    config = Config()
    DATABASE_URL = config.DATABASE_URL
except ImportError:
    try:
        # Try importing from config directly (Docker container)
        from config import Config
        config = Config()
        DATABASE_URL = config.DATABASE_URL
    except ImportError:
        # Fallback to environment variable
        import os
        DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/mydb')

# When running in Docker, we need to use the service name 'db' instead of 'localhost'
# Check if we're running in Docker by checking for the .dockerenv file
import os
if os.path.exists('/.dockerenv'):
    # We're in Docker, replace localhost with db service name
    DATABASE_URL = DATABASE_URL.replace('localhost', 'db')

logger.info(f"Connecting to database: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error in database session: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()