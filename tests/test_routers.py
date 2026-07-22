from app.models import Mood
from app.routers import mood, vending

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


def test_mood_checkin_awards_schrute_bucks(api_client, monkeypatch, auth_as):
    async def _fake_add_points(email, delta):
        assert email == FAKE_USER["email"]
        assert delta == mood.CHECKIN_POINTS
        return {**FAKE_USER, "points": FAKE_USER["points"] + delta}

    monkeypatch.setattr(mood.service, "add_points", _fake_add_points)
    auth_as(FAKE_USER)

    response = api_client.get(f"/mood/{Mood.happy.value}")

    assert response.status_code == 200
    body = response.json()
    assert body["schrute_bucks_earned"] == mood.CHECKIN_POINTS
    assert body["balance"] == FAKE_USER["points"] + mood.CHECKIN_POINTS


def test_vending_redeem_success(api_client, monkeypatch, auth_as):
    item = vending.ITEMS[0]

    async def _fake_add_points(email, delta):
        assert delta == -item.cost
        return {**FAKE_USER, "points": FAKE_USER["points"] + delta}

    monkeypatch.setattr(vending.service, "add_points", _fake_add_points)
    auth_as(FAKE_USER)

    response = api_client.post("/vending/0")

    assert response.status_code == 200
    assert response.json()["balance"] == FAKE_USER["points"] - item.cost


def test_vending_redeem_insufficient_funds(api_client, monkeypatch, auth_as):
    async def _fake_add_points(email, delta):
        return None

    monkeypatch.setattr(vending.service, "add_points", _fake_add_points)
    auth_as(FAKE_USER)

    response = api_client.post("/vending/0")

    assert response.status_code == 402


def test_vending_item_not_found(api_client, auth_as):
    auth_as(FAKE_USER)

    response = api_client.get(f"/vending/{len(vending.ITEMS) + 1}")

    assert response.status_code == 404
