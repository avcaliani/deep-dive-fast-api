import pytest
from app.models import User
from app.services import user as service
from bson import ObjectId

FAKE_RECORD = {
    "_id": "652a1f1e1f1e1f1e1f1e1f1e",
    "name": "Dwight Schrute",
    "email": "dwight@dundermifflin.com",
    "birthdate": "1970-01-20",
    "password": "hashed-secret",  # pragma: allowlist secret
    "points": 20,
}


async def _fake_find_one(collection, condition):
    return FAKE_RECORD


@pytest.mark.anyio
async def test_find_excludes_password_by_default(monkeypatch):
    monkeypatch.setattr(service.mongo, "find_one", _fake_find_one)

    user = await service.find(email="dwight@dundermifflin.com")

    assert "password" not in user


@pytest.mark.anyio
async def test_find_includes_password_when_requested(monkeypatch):
    monkeypatch.setattr(service.mongo, "find_one", _fake_find_one)

    user = await service.find(email="dwight@dundermifflin.com", include_password=True)

    assert user["password"] == "hashed-secret"  # pragma: allowlist secret


@pytest.mark.anyio
async def test_add_points_earning_increases_balance(monkeypatch):
    calls = {}

    async def _fake_find_one_and_update(collection, condition, update):
        calls["condition"] = condition
        calls["update"] = update
        return {**FAKE_RECORD, "points": 25}

    monkeypatch.setattr(service.mongo, "find_one_and_update", _fake_find_one_and_update)

    user = await service.add_points("dwight@dundermifflin.com", 5)

    assert user["points"] == 25
    assert calls["condition"] == {"email": "dwight@dundermifflin.com"}
    assert calls["update"] == {"$inc": {"points": 5}}


@pytest.mark.anyio
async def test_add_points_spending_decreases_balance(monkeypatch):
    async def _fake_find_one_and_update(collection, condition, update):
        assert condition == {"email": "dwight@dundermifflin.com", "points": {"$gte": 15}}
        return {**FAKE_RECORD, "points": 5}

    monkeypatch.setattr(service.mongo, "find_one_and_update", _fake_find_one_and_update)

    user = await service.add_points("dwight@dundermifflin.com", -15)

    assert user["points"] == 5


@pytest.mark.anyio
async def test_add_points_insufficient_funds_returns_none(monkeypatch):
    async def _fake_find_one_and_update(collection, condition, update):
        return None

    monkeypatch.setattr(service.mongo, "find_one_and_update", _fake_find_one_and_update)

    user = await service.add_points("dwight@dundermifflin.com", -1000)

    assert user is None


@pytest.mark.anyio
async def test_create_keeps_generated_object_id(monkeypatch):
    async def _fake_create(collection, user):
        assert ObjectId.is_valid(user.id)
        return {**FAKE_RECORD, "_id": user.id}

    monkeypatch.setattr(service.mongo, "create", _fake_create)

    new_user = User(
        name="Pam Beesly",
        email="pam@dundermifflin.com",
        birthdate="1979-03-25",
        password="Test1234!",  # pragma: allowlist secret
    )
    original_id = new_user.id

    await service.create(new_user)

    assert original_id == new_user.id
    assert ObjectId.is_valid(new_user.id)
