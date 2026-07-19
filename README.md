<div align="center">

<img src=".docs/logo.png" width="64px"/>

# Fast App - API

![License](https://img.shields.io/github/license/avcaliani/fast-app?logo=apache&color=lightseagreen)
![#](https://img.shields.io/badge/python-3.10.x-yellow.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Latest Tag](https://img.shields.io/github/v/tag/avcaliani/deep-dive-fast-api?logo=github&logoColor=white&color=blueviolet)

My goal with this repository is an in-depth exploration of FastAPI internals, the async
execution model, and production-ready backend design.

</div>

## Endpoints

```text
GET  /                  API home page (HTML)
POST /auth              login -> JWT bearer token
GET  /emoji/            random lucky emojis (auth required)
GET  /emoji/{item}      emoji by index (auth required)
GET  /mood/{item}       mood message by Mood enum (auth required)
GET  /users/me          current authenticated user (auth required)
GET  /users/{id}        user by id (auth required)
POST /users/            create user (auth required)
```

## User Shape

```json
{
  "id": "591528c0-3029-4f8c-9aa8-fee16e271dbd",
  "name": "Anthony",
  "email": "anthony@github.com",
  "birthdate": "1990-01-01",
  "mood": "😁",
  "enabled": true,
  "updated_at": "2026-07-19T12:00:00.000000"
}
```

## MongoDB

- Database: `fastAppDB`, collection: `users`
- `_id` is a Mongo ObjectId-format string, not a real BSON ObjectId
- `resources/init-mongo.js` creates the API's DB user on the container's first start

## Folder Structure

```bash
.
├── app/
│   ├── routers/         # 🚏 API route handlers.
│   ├── services/        # ⚙️ Business logic.
│   ├── utils/           # 🔧 Auth & MongoDB helpers.
│   ├── config.py        # ⚙️ Dynaconf settings loader.
│   └── models.py        # 📦 Pydantic models.
├── resources/
│   ├── init-mongo.js    # 🌱 Mongo init script (creates the API's DB user).
│   ├── log-config.yml   # 📝 Uvicorn logging config.
│   └── settings.toml    # 📝 Dynaconf settings.
├── static/               # 🖼️ Static files served by the API.
├── tests/                # ✅ Unit tests.
├── main.py               # 🚀 FastAPI app entrypoint.
├── Dockerfile            # 🐋 Dockerfile for the API.
└── docker-compose.yml    # 🧩 MongoDB service for local dev.
```

## Getting Started

One-time setup: Python env, dependencies, and a Dynaconf secrets file.

<details>
<summary>Show setup commands 👇</summary>

```bash
# 👇 Virtual Environment
pyenv local 3.10.0
python -m venv .venv && source .venv/bin/activate

# 👇 Dependencies
make install

# 👇 Dynaconf secrets file
echo "
[default]
TOKEN_SECRET_KEY = '$(openssl rand -hex 32)'
SECRET = '🚀'  # Dev Secret

[prod]
SECRET = '🤫'
" > resources/.secrets.toml
```

</details>

Commands to run the API locally.

<details>
<summary>Show run commands 👇</summary>

```bash
# Start MongoDB
docker-compose up -d

# Start the API
make run

# Run tests
make test

# Sanity Check
curl -s http://127.0.0.1:8000/
```

</details>

- API Home: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

![home](.docs/home.png)

## Docker

Build and run the API itself in a container (still requires `resources/.secrets.toml` and MongoDB running as above).

<details>
<summary>Show docker commands 👇</summary>

```bash
docker build -t fast-app-api .
docker run -p 8000:8000 --env APP_ENV=dev fast-app-api
```

</details>

## References

- [FastAPI: docs](https://fastapi.tiangolo.com/) — the framework this whole repo explores
- [pydantic: docs](https://docs.pydantic.dev/) — v2 data validation, used throughout `app/models.py`
- [uv: docs](https://docs.astral.sh/uv/) — dependency management
- [pre-commit: docs](https://pre-commit.com/) — hooks run in CI, see `.pre-commit-config.yaml`
- [MongoDB: Quick Start FastAPI](https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/) — the ObjectId pattern in `app/models.py` follows this guide
- [Icon made by Strokeicon from IconFinder](https://www.iconfinder.com/icons/2191531/best_fast_flash_good_light_speed_icon)

> 💡 Try `.docs/curl-requests.sh` for a runnable walkthrough of every endpoint above.
