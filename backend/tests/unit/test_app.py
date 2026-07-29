"""Smoke tests for the app scaffold."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_app_factory_returns_configured_app() -> None:
    app = create_app()
    assert app.title == "Hiring Intelligence (MVP)"
    assert app.version == "0.1.0"


def test_root_placeholder_responds() -> None:
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "hiring-intelligence", "status": "scaffold"}
