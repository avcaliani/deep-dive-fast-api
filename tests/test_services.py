import pytest

from app.services import user as service

FAKE_RECORD = {
    "_id": "652a1f1e1f1e1f1e1f1e1f1e",
    "name": "Homer Simpson",
    "email": "homer@duff.com",
    "birthdate": "1990-01-01",
    "password": "hashed-secret",
}


async def _fake_find_one(collection, condition):
    return FAKE_RECORD


@pytest.mark.anyio
async def test_find_excludes_password_by_default(monkeypatch):
    monkeypatch.setattr(service.mongo, "find_one", _fake_find_one)

    user = await service.find(email="homer@duff.com")

    assert "password" not in user


@pytest.mark.anyio
async def test_find_includes_password_when_requested(monkeypatch):
    monkeypatch.setattr(service.mongo, "find_one", _fake_find_one)

    user = await service.find(email="homer@duff.com", include_password=True)

    assert user["password"] == "hashed-secret"
