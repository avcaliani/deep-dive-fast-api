from app.config import settings

ALLOWED_ORIGIN = settings.CORS_ORIGINS[0]
DISALLOWED_ORIGIN = "https://evil.example.com"


def _preflight(api_client, origin: str, method: str = "POST", headers: str = "Authorization"):
    return api_client.options(
        "/vending/0",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": headers,
        },
    )


def test_preflight_from_allowed_origin_is_accepted(api_client):
    response = _preflight(api_client, ALLOWED_ORIGIN)

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN


def test_preflight_from_disallowed_origin_is_rejected(api_client):
    response = _preflight(api_client, DISALLOWED_ORIGIN)

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_preflight_with_unlisted_method_is_rejected(api_client):
    response = _preflight(api_client, ALLOWED_ORIGIN, method="DELETE")

    assert response.status_code == 400


def test_preflight_with_unlisted_header_is_rejected(api_client):
    response = _preflight(api_client, ALLOWED_ORIGIN, headers="X-Custom")

    assert response.status_code == 400


def test_credentials_are_not_allowed(api_client):
    response = _preflight(api_client, ALLOWED_ORIGIN)

    assert "access-control-allow-credentials" not in response.headers


def test_simple_request_from_disallowed_origin_gets_no_cors_headers(api_client):
    response = api_client.get("/", headers={"Origin": DISALLOWED_ORIGIN})

    assert "access-control-allow-origin" not in response.headers
