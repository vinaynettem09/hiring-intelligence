"""Health endpoint tests (Story 0.6)."""

from fastapi.testclient import TestClient

from app.main import create_app
from app.version import VERSION


def test_health_returns_structured_status() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["version"] == VERSION
    assert body["status"] in {"healthy", "degraded"}
    # Application is always healthy if the process is serving; DB may be absent in unit runs.
    assert body["checks"]["application"] == "healthy"
    assert "database" in body["checks"]
