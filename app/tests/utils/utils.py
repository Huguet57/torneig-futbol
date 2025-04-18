"""Utility functions for testing."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base

# Create a test database in memory
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)


def get_test_db():
    """Get a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close() 