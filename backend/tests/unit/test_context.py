"""Correlation id + envelope tests."""

from fastapi.testclient import TestClient

from app.main import create_app
from app.shared.middleware import CORRELATION_HEADER


def test_correlation_id_generated_when_absent() -> None:
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get(CORRELATION_HEADER)


def test_correlation_id_is_echoed_when_provided() -> None:
    client = TestClient(create_app())
    provided = "test-correlation-123"
    response = client.get("/", headers={CORRELATION_HEADER: provided})
    assert response.headers.get(CORRELATION_HEADER) == provided


def test_envelope_is_available_to_handler() -> None:
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "hiring-intelligence", "status": "scaffold"}
