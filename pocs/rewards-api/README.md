<div align="center">

# Rewards API

![License](https://img.shields.io/github/license/avcaliani/lab-fast-api?logo=opensourceinitiative&logoColor=white&color=lightseagreen)
![Python](https://img.shields.io/badge/python-3.10.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Latest Tag](https://img.shields.io/github/v/tag/avcaliani/lab-fast-api?logo=github&logoColor=white&color=blueviolet)

![Cellular](https://media.giphy.com/media/SW3PNayoSGXao/giphy.gif)

My goal with this repository is an in-depth exploration of FastAPI internals, the async execution model, and production-ready backend design.

**Schrute Bucks Rewards**, an employee rewards app inspired on "The Office" 📎

</div>

Part of [FastAPI Lab](../../README.md).

```mermaid
%%{ init: { 'look': 'handDrawn', 'theme': 'neutral' } }%%
sequenceDiagram
    actor E as Employee
    participant A@{ "type": "boundary" } as Rewards API
    participant M@{ "type": "database" } as MongoDB

    E->>A: POST /auth
    A->>M: Find user and check password
    A-->>E: JWT token

    E->>A: POST /mood/😁 (Bearer token)
    A->>M: Add check-in points
    A-->>E: 200 - Schrute Bucks earned

    E->>A: GET /vending/
    A-->>E: Catalog

    E->>A: POST /vending/0 (Bearer token)
    A->>M: Spend points (only if balance covers the cost)
    alt Enough Schrute Bucks
        A-->>E: 200 - Reward redeemed
    else Not enough Schrute Bucks
        A-->>E: 402 - Not enough Schrute Bucks
    end
```

> [!NOTE]
> Start the API and check `http://127.0.0.1:8000`  
> The homepage has an interactive playground to run every endpoint live,
> plus copy-paste curl commands for each one.

<details>
<summary>Playground preview 👇</summary>

![Playground](.docs/screenshot.png)

</details>

## Getting Started

### 💻 Run local

API on your machine, MongoDB in Docker.

```bash
# All commands run from the poc folder
cd pocs/rewards-api

# Install dependencies
make install

# Create the secrets file
echo "
[default]
TOKEN_SECRET_KEY = '$(openssl rand -hex 32)'
" > resources/.secrets.toml

# Start MongoDB, create the demo user, and run the API
docker-compose up -d mongo
make create-user
make run
```

### 🐳 Run in Docker

API and MongoDB both in Docker, using the `docker` profile from `resources/settings.toml`.

```bash
# All commands run from the poc folder
cd pocs/rewards-api

# Set the token secret (Dynaconf reads DYNACONF_* env vars, no secrets file needed)
export DYNACONF_TOKEN_SECRET_KEY="$(openssl rand -hex 32)"

# Build and start MongoDB and the API
docker-compose up -d --build

# Create the demo user (runs on your machine, MongoDB port is published)
make install
make create-user
```

> [!NOTE]
> Both modes use port 8000, so stop one before starting the other.

<details>
<summary>More commands: tests, formatting 👇</summary>

```bash
# Run tests
make test

# Format & lint (same checks as CI)
uvx pre-commit run --all-files

# Update locked dependencies
make update-deps
```

</details>

<details>
<summary>Project structure 👇</summary>

```text
.
├── app/
│   ├── main.py          # FastAPI app entrypoint
│   ├── routers/         # endpoints (auth, mood, vending, users)
│   ├── services/        # business logic
│   ├── infra/           # MongoDB client
│   ├── security.py      # JWT and password hashing
│   ├── dependencies.py  # Bearer token -> current user
│   ├── models.py        # Pydantic models
│   └── config.py        # Dynaconf settings loader
├── static/              # homepage with the interactive playground
├── resources/           # settings, Mongo init script, log config
├── scripts/             # one-off scripts (create demo user)
├── tests/               # unit tests
├── docker-compose.yml   # MongoDB and API containers
└── Dockerfile
```

</details>

## References

- [FastAPI: docs](https://fastapi.tiangolo.com/) — the framework this whole repo explores
- [pydantic: docs](https://docs.pydantic.dev/) — v2 data validation, used throughout `app/models.py`
- [uv: docs](https://docs.astral.sh/uv/) — dependency management
- [pre-commit: docs](https://pre-commit.com/) — hooks run in CI, see [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml)
- [MongoDB: Quick Start FastAPI](https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/) — the ObjectId pattern in `app/models.py` follows this guide
