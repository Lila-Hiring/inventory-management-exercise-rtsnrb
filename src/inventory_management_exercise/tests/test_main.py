"""Tests for the main FastAPI application."""

from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from inventory_management_exercise.main import app

client = TestClient(app)


def test_read_hello_endpoint() -> None:
    """Test the root endpoint."""
    response = client.get("/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to inventory_management_exercise!"}


def test_health_check() -> None:
    """Test the health check endpoint."""
    response = client.get("/healthz")
    assert response.status_code == 200

    data = response.json()
    assert data["version"] is not None

    # Check that the current_time is within the last minute
    current_time = datetime.fromisoformat(data["current_time"].replace("Z", "+00:00"))
    time_diff = datetime.now(UTC) - current_time
    assert time_diff < timedelta(minutes=1)
