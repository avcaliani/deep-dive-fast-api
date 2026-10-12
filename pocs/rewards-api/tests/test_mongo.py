from types import SimpleNamespace

import pytest
from app.infra.mongo import MongoFacade
from app.models import User


class FakeCollection:
    def __init__(self, stored: dict | None = None):
        self.stored = stored
        self.filters: list[dict] = []

    async def insert_one(self, document: dict) -> SimpleNamespace:
        return SimpleNamespace(inserted_id=document["_id"])

    async def find_one(self, condition: dict) -> dict | None:
        self.filters.append(condition)
        return self.stored


def _new_user() -> User:
    return User(
        name="Pam Beesly",
        email="pam@dundermifflin.com",
        birthdate="1979-03-25",
        password="Test1234!",  # pragma: allowlist secret
    )


def _facade_with(collection: FakeCollection) -> MongoFacade:
    facade = MongoFacade()
    facade.db = {"users": collection}
    return facade


@pytest.mark.anyio
async def test_create_looks_up_inserted_record_by_underscore_id():
    user = _new_user()
    collection = FakeCollection(stored={"_id": user.id})

    record = await _facade_with(collection).create("users", user)

    assert collection.filters == [{"_id": user.id}]
    assert record["_id"] == user.id


@pytest.mark.anyio
async def test_create_raises_when_inserted_record_is_missing():
    collection = FakeCollection(stored=None)

    with pytest.raises(LookupError):
        await _facade_with(collection).create("users", _new_user())
