import time

from app.models import User


def _make_user() -> User:
    return User(name="Homer", email="homer@duff.com", birthdate="1990-01-01", password="secret")


def test_user_default_timestamps_are_generated_per_instance():
    first = _make_user()
    time.sleep(0.001)
    second = _make_user()

    assert first.updated_at != second.updated_at
    assert first.created_at != second.created_at
