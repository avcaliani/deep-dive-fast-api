import pytest
from app import dependencies
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def api_client():
    return TestClient(app)


@pytest.fixture
def auth_as():
    def _auth_as(user: dict):
        app.dependency_overrides[dependencies.get_user] = lambda: user

    yield _auth_as
    app.dependency_overrides.clear()
