import time

from app.models import User, VendingItem


def _make_user() -> User:
    return User(
        name="Dwight",
        email="dwight@dundermifflin.com",
        birthdate="1970-01-20",
        password="secret",  # pragma: allowlist secret
    )


def test_user_default_timestamps_are_generated_per_instance():
    first = _make_user()
    time.sleep(0.001)
    second = _make_user()

    assert first.updated_at != second.updated_at
    assert first.created_at != second.created_at


def test_vending_item_requires_emoji_name_and_cost():
    item = VendingItem(emoji="🏆", name="Dundie Award", cost=50)

    assert item.cost == 50
