"""Tests for the MedTech AI Platform health endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Root endpoint should report that the platform is running."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "MedTech AI Platform",
        "status": "running",
    }


def test_health_endpoint() -> None:
    """Health endpoint should report healthy status."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }
