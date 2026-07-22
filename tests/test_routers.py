from app.models import Mood
from app.routers import base, mood, vending

FAKE_USER = {
    "id": "652a1f1e1f1e1f1e1f1e1f1e",
    "name": "Dwight Schrute",
    "email": "dwight@dundermifflin.com",
    "birthdate": "1970-01-20",
    "enabled": True,
    "points": 20,
}


def test_response_ok(api_client):
    response = api_client.get("/")
    assert response.status_code == 200


def test_auth_with_unknown_user_returns_401_not_500(api_client, monkeypatch):
    async def _fake_find(id_=None, email=None, include_password=False):
        return None

    monkeypatch.setattr(base.service, "find", _fake_find)

    response = api_client.post("/auth", json={"username": "unknown@dundermifflin.com", "password": "x"})

    assert response.status_code == 401


def test_auth_success_returns_token(api_client, monkeypatch):
    async def _fake_find(id_=None, email=None, include_password=False):
        return {**FAKE_USER, "password": "hashed-secret"}  # pragma: allowlist secret

    monkeypatch.setattr(base.service, "find", _fake_find)
    monkeypatch.setattr(base.auth, "check_password", lambda plain, hashed: True)

    response = api_client.post("/auth", json={"username": FAKE_USER["email"], "password": "Test1234!"})

    assert response.status_code == 200
    assert "token" in response.json()


def test_mood_checkin_awards_schrute_bucks(api_client, monkeypatch, auth_as):
    async def _fake_earn_points(email, amount):
        assert email == FAKE_USER["email"]
        assert amount == mood.CHECKIN_POINTS
        return {**FAKE_USER, "points": FAKE_USER["points"] + amount}

    monkeypatch.setattr(mood.service, "earn_points", _fake_earn_points)
    auth_as(FAKE_USER)

    response = api_client.get(f"/mood/{Mood.happy.value}")

    assert response.status_code == 200
    body = response.json()
    assert body["schrute_bucks_earned"] == mood.CHECKIN_POINTS
    assert body["balance"] == FAKE_USER["points"] + mood.CHECKIN_POINTS


def test_vending_redeem_success(api_client, monkeypatch, auth_as):
    item = vending.ITEMS[0]

    async def _fake_spend_points(email, cost):
        assert cost == item.cost
        return {**FAKE_USER, "points": FAKE_USER["points"] - cost}

    monkeypatch.setattr(vending.service, "spend_points", _fake_spend_points)
    auth_as(FAKE_USER)

    response = api_client.post("/vending/0")

    assert response.status_code == 200
    assert response.json()["balance"] == FAKE_USER["points"] - item.cost


def test_vending_redeem_insufficient_funds(api_client, monkeypatch, auth_as):
    async def _fake_spend_points(email, cost):
        return None

    monkeypatch.setattr(vending.service, "spend_points", _fake_spend_points)
    auth_as(FAKE_USER)

    response = api_client.post("/vending/0")

    assert response.status_code == 402


def test_vending_item_not_found(api_client, auth_as):
    auth_as(FAKE_USER)

    response = api_client.get(f"/vending/{len(vending.ITEMS) + 1}")

    assert response.status_code == 404
