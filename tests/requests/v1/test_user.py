from fastapi.testclient import TestClient
from spbd.main import app
from spbd.infra.db import get_session
from fastapi import status


def test_get(session_callable_fixture, users_fixture):
    app.dependency_overrides[get_session] = session_callable_fixture
    client = TestClient(app)
    response = client.get("/v1/users/1")
    data = response.json()

    assert data["id"] == 1


def test_get_not_found(session_callable_fixture):
    app.dependency_overrides[get_session] = session_callable_fixture
    client = TestClient(app)
    response = client.get("/v1/users/1")
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in data["detail"]
