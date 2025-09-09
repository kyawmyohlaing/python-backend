import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Since we're in the container and files are directly in /app, we import directly
from database import Base

# This file contains pytest fixtures that can be shared across multiple test files

@pytest.fixture(scope="session")
def sqlite_test_db():
    """Create a SQLite in-memory database for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    yield engine
    # Cleanup happens automatically for in-memory SQLite

@pytest.fixture(scope="session")
def postgres_test_db():
    """Create a PostgreSQL database connection for testing if URL is provided"""
    postgres_url = os.getenv("TEST_POSTGRES_URL")
    if postgres_url:
        engine = create_engine(postgres_url)
        Base.metadata.create_all(bind=engine)
        yield engine
    else:
        yield None

@pytest.fixture(scope="function")
def sqlite_session(sqlite_test_db):
    """Create a database session for SQLite testing"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_test_db)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def postgres_session(postgres_test_db):
    """Create a database session for PostgreSQL testing"""
    if postgres_test_db:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgres_test_db)
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None