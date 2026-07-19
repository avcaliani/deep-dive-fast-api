#!/usr/bin/env bash
#
# Exercises every API endpoint with curl and prints the results.
#
# Prerequisites:
#   - MongoDB running:  docker-compose up -d
#   - API running:      make run
#
# Usage:
#   ./.docs/curl-requests.sh
#
set -o pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
TEST_EMAIL="test.user@fast-app.dev"
TEST_PASSWORD="Test1234!"  # pragma: allowlist secret
# Bcrypt hash of TEST_PASSWORD, precomputed with:
#   uv run python -c "from passlib.context import CryptContext; \
#     print(CryptContext(schemes=['bcrypt']).hash('Test1234!'))"
# shellcheck disable=SC2016
TEST_PASSWORD_HASH='$2b$12$2KMA3sYfbT3BpBVjdFcwhuyBEBTYdg38OrnvHslHrOjFAlqBrcJbO'

LAST_STATUS=""
LAST_BODY=""

print_header() {
  echo
  echo "=== $1 ==="
}

# Runs a curl call, prints the status + pretty-printed body,
# and leaves the raw response in $LAST_STATUS / $LAST_BODY.
call() {
  local method="$1" path="$2"
  shift 2

  local tmp_body
  tmp_body="$(mktemp)"

  echo "> $method $BASE_URL$path"
  LAST_STATUS="$(curl -sS -o "$tmp_body" -w '%{http_code}' -X "$method" "$BASE_URL$path" "$@")"
  LAST_BODY="$(cat "$tmp_body")"
  rm -f "$tmp_body"

  echo "< HTTP $LAST_STATUS"
  if echo "$LAST_BODY" | python3 -m json.tool 2>/dev/null; then
    :
  else
    echo "$LAST_BODY"
  fi
}

print_header "Seeding a test user in MongoDB"
echo "Bypasses the API (POST /users/ itself requires a token) so there's someone to log in as."
docker-compose exec -T mongo mongosh --quiet "mongodb://fast-app-api:123456@127.0.0.1:27017/fastAppDB" --eval "
db.users.updateOne(
  { email: '$TEST_EMAIL' },
  {
    \$setOnInsert: {
      _id: '652a1f1e1f1e1f1e1f1e1f1e',
      name: 'Test User',
      email: '$TEST_EMAIL',
      birthdate: '1990-05-15',
      mood: '😁',
      enabled: true,
      password: '$TEST_PASSWORD_HASH',
      updatedAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
    },
  },
  { upsert: true }
);
"

print_header "GET / (home page)"
call GET "/"

print_header "POST /auth (login)"
call POST "/auth" \
  --data-urlencode "username=$TEST_EMAIL" \
  --data-urlencode "password=$TEST_PASSWORD"
TOKEN="$(echo "$LAST_BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('token',''))" 2>/dev/null)"

AUTH_HEADER_ARGS=()
if [ -z "$TOKEN" ]; then
  echo
  echo "KNOWN BUG: login always 401s. app/services/user.py's find() strips the"
  echo "password field before returning, but app/routers/base.py's get_token()"
  echo "relies on that same find() to check it — hashed is always None, so"
  echo "check_password() always fails, regardless of credentials."
  echo "Continuing without a token — every call below will 401 for the same reason."
else
  AUTH_HEADER_ARGS=(-H "Authorization: Bearer $TOKEN")
fi

print_header "GET /emoji/"
call GET "/emoji/" "${AUTH_HEADER_ARGS[@]}"

print_header "GET /emoji/{item}"
call GET "/emoji/0" "${AUTH_HEADER_ARGS[@]}"

print_header "GET /mood/{item}"
call GET "/mood/😁" "${AUTH_HEADER_ARGS[@]}"

print_header "GET /users/me"
call GET "/users/me" "${AUTH_HEADER_ARGS[@]}"
USER_ID="$(echo "$LAST_BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)"

print_header "GET /users/{id}"
call GET "/users/${USER_ID:-000000000000000000000000}" "${AUTH_HEADER_ARGS[@]}"

print_header "POST /users/ (create another user)"
SECOND_USER_PASSWORD="AnotherPass1!"  # pragma: allowlist secret
call POST "/users/" \
  "${AUTH_HEADER_ARGS[@]}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Second User\",
    \"email\": \"second.user@fast-app.dev\",
    \"birthdate\": \"1995-08-20\",
    \"password\": \"$SECOND_USER_PASSWORD\"
  }"

echo
echo "Done."
