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
    
    # Determine if we're running in Docker
    @staticmethod
    def is_running_in_docker():
        """Check if the application is running in a Docker container"""
        return os.path.exists('/.dockerenv') or 'HOSTNAME' in os.environ
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # If no DATABASE_URL is set, determine the appropriate default
    if not DATABASE_URL:
        # Check environment
        env = os.getenv('ENVIRONMENT', 'development')
        
        if is_running_in_docker():
            # In Docker, use PostgreSQL with 'db' service
            DATABASE_URL = "postgresql://postgres:password@db:5432/mydb"
        else:
            # Local development, use SQLite
            if env == 'testing':
                DATABASE_URL = "sqlite:///./test.db"
            elif env == 'production':
                DATABASE_URL = "postgresql://user:password@localhost/prod_db"
            else:
                DATABASE_URL = "sqlite:///./app/dev.db"
    
    # Special handling for Docker - ensure we're using the 'db' service
    if is_running_in_docker() and DATABASE_URL:
        # Replace localhost/127.0.0.1 with 'db' service name for Docker
        DATABASE_URL = DATABASE_URL.replace('127.0.0.1', 'db').replace('localhost', 'db')
    
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    
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

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG: bool = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING: bool = True

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