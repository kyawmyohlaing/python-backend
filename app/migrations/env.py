from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
import sys
import os

# Debug: Print current working directory and Python path
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Add the parent directory to the path so we can import app modules
# When running from migrations directory, parent directory contains the app module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Parent directory: {parent_dir}")

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    print(f"Added {parent_dir} to Python path")

# Debug: Print updated Python path
print(f"Updated Python path: {sys.path}")

# Import the database and models
# Handle imports for both local development and Docker container environments
try:
    # Try importing from database (Docker container)
    from database import Base
    from models import user
except ImportError:
    try:
        # Try importing from app.module (local development)
        from app.database import Base
        from app.models import user
    except ImportError:
        # Try one more approach for local development
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from app.database import Base
        from app.models import user

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Import the Config class and get database URL properly
    # Handle imports for both local development and Docker container environments
    try:
        # Try importing from config directly (Docker container)
        from config import Config
    except ImportError:
        try:
            # Try importing from app.config (local development)
            from app.config import Config
        except ImportError:
            # Fallback to environment variable
            import os
            database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/mydb')
            url = database_url
            context.configure(
                url=url,
                target_metadata=target_metadata,
                literal_binds=True,
                dialect_opts={"paramstyle": "named"},
            )

            with context.begin_transaction():
                context.run_migrations()
            return
    
    app_config = Config()
    database_url = app_config.DATABASE_URL or "postgresql://postgres:password@localhost:5432/mydb"
    
    url = database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Import the Config class and get database URL properly
    # Handle imports for both local development and Docker container environments
    try:
        # Try importing from config directly (Docker container)
        from config import Config
    except ImportError:
        try:
            # Try importing from app.config (local development)
            from app.config import Config
        except ImportError:
            # Fallback to environment variable
            import os
            database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/mydb')
            config.set_main_option('sqlalchemy.url', database_url)
            
            # Get the configuration section, providing an empty dict as fallback
            configuration = config.get_section(config.config_ini_section) or {}
            configuration["sqlalchemy.url"] = database_url
            
            connectable = engine_from_config(
                configuration,
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )

            with connectable.connect() as connection:
                context.configure(
                    connection=connection, target_metadata=target_metadata
                )

                with context.begin_transaction():
                    context.run_migrations()
            return
    
    app_config = Config()
    database_url = app_config.DATABASE_URL or "postgresql://postgres:password@localhost:5432/mydb"
    config.set_main_option('sqlalchemy.url', database_url)
    
    # Get the configuration section, providing an empty dict as fallback
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = database_url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()