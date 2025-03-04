from collections.abc import Callable, Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.database import Base, get_db
from app.main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a new session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    # Override the get_db dependency to use the test database
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            pass  # Don't close the db here, it will be closed by the db fixture

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Remove the override after the test
    app.dependency_overrides.clear()


def refresh_objects(db: Session, *objects: Any) -> None:
    """Refresh multiple objects to avoid detached instance errors."""
    for obj in objects:
        if obj is not None:
            db.refresh(obj)


@pytest.fixture
def refresh() -> Callable[[Session, Any], None]:
    """Fixture to provide the refresh_objects function."""
    return refresh_objects
