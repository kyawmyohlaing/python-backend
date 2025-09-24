import os
from dotenv import load_dotenv

load_dotenv()

# Get SECRET_KEY with validation
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


class Config:
    """Configuration class for the application"""
    
    # Database settings (example values)
    # Primary PostgreSQL database
    # When running in Docker, we need to use the service name 'db' instead of 'localhost'
    # Check if we're running in Docker by checking for the .dockerenv file or specific environment variables
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mydb")
    # Check if we're in Docker by checking for the .dockerenv file or specific environment variables
    is_in_docker_container = os.path.exists('/.dockerenv') or 'HOSTNAME' in os.environ
    if is_in_docker_container:
        # We're in Docker, replace localhost/127.0.0.1 with db service name
        DATABASE_URL = DATABASE_URL.replace('127.0.0.1', 'db').replace('localhost', 'db')
    
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    
    # SQLite reference (kept for reference)
    SQLITE_DATABASE_URL: str = "sqlite:///./mydb.db"
    
    # Security settings
    SECRET_KEY: str = SECRET_KEY  # Use the validated module-level SECRET_KEY
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Learning path settings
    DEFAULT_LEARNING_PATH: str = os.getenv("DEFAULT_LEARNING_PATH", "beginner")
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("DEV_DATABASE_URL", "postgresql://postgres:password@localhost:5432/mydb")
    # Check if we're in Docker by checking for the .dockerenv file or specific environment variables
    is_in_docker_container = os.path.exists('/.dockerenv') or 'HOSTNAME' in os.environ
    if is_in_docker_container:
        # We're in Docker, replace localhost/127.0.0.1 with db service name
        DATABASE_URL = DATABASE_URL.replace('127.0.0.1', 'db').replace('localhost', 'db')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG: bool = False
    DATABASE_URL: str = os.getenv("PROD_DATABASE_URL", "postgresql://postgres:password@localhost:5432/mydb_prod")
    # Check if we're in Docker by checking for the .dockerenv file or specific environment variables
    is_in_docker_container = os.path.exists('/.dockerenv') or 'HOSTNAME' in os.environ
    if is_in_docker_container:
        # We're in Docker, replace localhost/127.0.0.1 with db service name
        DATABASE_URL = DATABASE_URL.replace('127.0.0.1', 'db').replace('localhost', 'db')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING: bool = True
    DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:password@localhost:5432/mydb_test")
    # Check if we're in Docker by checking for the .dockerenv file or specific environment variables
    is_in_docker_container = os.path.exists('/.dockerenv') or 'HOSTNAME' in os.environ
    if is_in_docker_container:
        # We're in Docker, replace localhost/127.0.0.1 with db service name
        DATABASE_URL = DATABASE_URL.replace('127.0.0.1', 'db').replace('localhost', 'db')

# Configuration dictionary
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}

def get_config() -> Config:
    """Get the appropriate configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development")
    return config_dict.get(env, DevelopmentConfig)()