"""Error-model tests (Story 0.5)."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.shared.error_handlers import register_error_handlers
from app.shared.errors import ConflictError
from app.shared.middleware import CorrelationMiddleware


class _Body(BaseModel):
    name: str


def _make_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(CorrelationMiddleware)
    register_error_handlers(app)

    @app.get("/conflict")
    async def _conflict() -> None:
        raise ConflictError(
            "Campaign already active",
            code="CAMPAIGN_ALREADY_ACTIVE",
            metadata={"status": "active"},
        )

    @app.get("/boom")
    async def _boom() -> None:
        raise RuntimeError("secret internal detail")

    @app.post("/thing")
    async def _thing(body: _Body) -> dict[str, str]:
        return {"name": body.name}

    return app


def test_application_error_maps_to_shaped_json() -> None:
    client = TestClient(_make_app())
    response = client.get("/conflict")
    assert response.status_code == 409
    body = response.json()
    assert body["type"] == "conflict"
    assert body["code"] == "CAMPAIGN_ALREADY_ACTIVE"
    assert body["message"] == "Campaign already active"
    assert body["correlation_id"]
    assert body["metadata"] == {"status": "active"}


def test_unexpected_error_is_generic_and_does_not_leak() -> None:
    client = TestClient(_make_app(), raise_server_exceptions=False)
    response = client.get("/boom")
    assert response.status_code == 500
    body = response.json()
    assert body["type"] == "internal_error"
    assert body["code"] == "INTERNAL_ERROR"
    assert body["correlation_id"]
    assert "secret internal detail" not in response.text  # no leak


def test_request_validation_maps_to_validation_error() -> None:
    client = TestClient(_make_app())
    response = client.post("/thing", json={})  # missing required "name"
    assert response.status_code == 400
    body = response.json()
    assert body["type"] == "validation_error"
    assert body["code"] == "REQUEST_VALIDATION"
    assert body["correlation_id"]
    assert isinstance(body["details"], list) and body["details"]
