from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError   
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine if we're running in Docker
def is_running_in_docker():
    """Check if the application is running in a Docker container"""
    return os.path.exists('/.dockerenv') or 'HOSTNAME' in os.environ

# Get database URL from environment or configuration
DATABASE_URL = os.getenv('DATABASE_URL')

# If no DATABASE_URL is set, determine the appropriate default
if not DATABASE_URL:
    # Check environment
    env = os.getenv('ENVIRONMENT', 'development')
    
    if is_running_in_docker():
        # In Docker, use PostgreSQL with 'db' service
        DATABASE_URL = "postgresql://postgres:password@db:5432/mydb"
        logger.info("Running in Docker environment, using PostgreSQL")
    else:
        # Local development, use SQLite
        if env == 'testing':
            DATABASE_URL = "sqlite:///./test.db"
        elif env == 'production':
            DATABASE_URL = "postgresql://user:password@localhost/prod_db"
        else:
            DATABASE_URL = "sqlite:///./app/dev.db"
        logger.info(f"Running in local environment, using {DATABASE_URL}")

# Special handling for Docker - ensure we're using the 'db' service
if is_running_in_docker() and DATABASE_URL:
    # Replace localhost/127.0.0.1 with 'db' service name for Docker
    DATABASE_URL = DATABASE_URL.replace('127.0.0.1', 'db').replace('localhost', 'db')
    logger.info(f"Updated DATABASE_URL for Docker environment: {DATABASE_URL}")

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