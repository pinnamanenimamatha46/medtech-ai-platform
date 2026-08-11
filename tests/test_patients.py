"""Tests for patient API endpoints."""

from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_medtech.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db() -> Generator[Session, None, None]:
    """Provide a test database session."""
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_function() -> None:
    """Reset the test database before each test."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


def test_create_patient() -> None:
    """A patient should be created successfully."""
    response = client.post(
        "/api/v1/patients",
        json={
            "first_name": "Anita",
            "last_name": "Kotha",
            "date_of_birth": "1970-10-15",
            "email": "anita@example.com",
            "phone": "310-555-0101",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "first_name": "Anita",
        "last_name": "Kotha",
        "date_of_birth": "1970-10-15",
        "email": "anita@example.com",
        "phone": "310-555-0101",
        "id": 1,
    }


def test_list_patients() -> None:
    """Created patients should appear in the patient list."""
    client.post(
        "/api/v1/patients",
        json={
            "first_name": "Anita",
            "last_name": "Kotha",
            "date_of_birth": "1970-10-15",
            "email": "anita@example.com",
            "phone": "310-555-0101",
        },
    )

    response = client.get("/api/v1/patients")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == "Anita"
    assert response.json()[0]["id"] == 1
