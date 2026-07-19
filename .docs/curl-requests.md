# Curl Requests

Public endpoints only — the two routes with no auth requirement. Copy, paste, and run.

Base URL: `http://127.0.0.1:8000`

## GET / — home page

```bash
curl -s http://127.0.0.1:8000/
```

## POST /auth — login

Returns a JWT bearer token. Needs a real user in MongoDB with a matching bcrypt
password hash — see [Seeding a test user](#seeding-a-test-user) below.

```bash
curl -s -X POST http://127.0.0.1:8000/auth \
  --data-urlencode "username=test.user@fast-app.dev" \
  --data-urlencode "password=Test1234!"
```

> ⚠️ Known bug: login always returns 401. `app/services/user.py`'s `find()`
> strips the password field before returning it, but `app/routers/base.py`'s
> `get_token()` relies on that same `find()` to check it — so the hash is
> always `None` and `check_password()` always fails, regardless of credentials.

## Seeding a test user

`POST /auth` needs a user to already exist in MongoDB. There's no public
endpoint to create one (`POST /users/` itself requires a token), so insert
one directly:

```bash
docker-compose exec -T mongo mongosh "mongodb://fast-app-api:123456@127.0.0.1:27017/fastAppDB" --eval '
db.users.updateOne(
  { email: "test.user@fast-app.dev" },
  {
    $setOnInsert: {
      _id: "652a1f1e1f1e1f1e1f1e1f1e",
      name: "Test User",
      email: "test.user@fast-app.dev",
      birthdate: "1990-05-15",
      mood: "😁",
      enabled: true,
      password: "$2b$12$2KMA3sYfbT3BpBVjdFcwhuyBEBTYdg38OrnvHslHrOjFAlqBrcJbO",
      updatedAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
    },
  },
  { upsert: true }
);
'
```

Password for the seeded user is `Test1234!`.
