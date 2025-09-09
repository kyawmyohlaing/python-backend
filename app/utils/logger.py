import logging
import sys
from typing import Optional
# Since we're in the container and files are directly in /app, we import directly
from config import Config

def setup_logger(config: Optional[Config] = None) -> logging.Logger:
    """Set up and configure the application logger"""
    
    if config is None:
        config = Config()
    
    # Create logger
    logger = logging.getLogger("python_learning_api")
    logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
    
    # Prevent adding multiple handlers if logger is already configured
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

def get_logger() -> logging.Logger:
    """Get the configured logger instance"""
    return logging.getLogger("python_learning_api")