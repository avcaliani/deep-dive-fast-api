<div align="center">

# Rewards API

![License](https://img.shields.io/github/license/avcaliani/deep-dive-fast-api?logo=opensourceinitiative&logoColor=white&color=lightseagreen)
![Python](https://img.shields.io/badge/python-3.10.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Latest Tag](https://img.shields.io/github/v/tag/avcaliani/deep-dive-fast-api?logo=github&logoColor=white&color=blueviolet)

My goal with this repository is an in-depth exploration of FastAPI internals, the async execution model, and production-ready backend design.

**Schrute Bucks Rewards**, an employee rewards app inspired on "The Office" 📎

</div>

```mermaid
%%{ init: { 'look': 'handDrawn', 'theme': 'neutral' } }%%
flowchart LR
    A[👤 Employee] -->|"POST /auth"| B[🔑 JWT Token]
    B -->|"GET /mood/😁"| C[💰 Earn Schrute Bucks]
    C -->|"GET /vending/"| D[🗂️ Browse Catalog]
    D -->|"POST /vending/0"| E{Enough Schrute Bucks?}
    E -->|Yes| F[🏆 200 - Reward Redeemed]
    E -->|No| G[🚫 402 - Not Enough Schrute Bucks]
```

> [!NOTE]
> Start the API and check `http://127.0.0.1:8000`  
> The homepage has an interactive playground to run every endpoint live,
> plus copy-paste curl commands for each one.

## Getting Started

```bash
# One-time setup
make install
echo "
[default]
TOKEN_SECRET_KEY = '$(openssl rand -hex 32)'
" > resources/.secrets.toml

# Start MongoDB, create the demo user, and run the API
docker-compose up -d
make create-user
make run
```

<details>
<summary>More commands: tests, formatting, Docker 👇</summary>

```bash
# Run tests
make test

# Format & lint (same checks as CI)
uvx pre-commit run --all-files

# Update locked dependencies
make update-deps
```

Or run the API itself in a container (still requires `resources/.secrets.toml` and MongoDB running as above).

```bash
docker build -t dunder-mifflin-api .
docker run -p 8000:8000 --env APP_ENV=dev dunder-mifflin-api
```

</details>

## References

- [FastAPI: docs](https://fastapi.tiangolo.com/) — the framework this whole repo explores
- [pydantic: docs](https://docs.pydantic.dev/) — v2 data validation, used throughout `app/models.py`
- [uv: docs](https://docs.astral.sh/uv/) — dependency management
- [pre-commit: docs](https://pre-commit.com/) — hooks run in CI, see `.pre-commit-config.yaml`
- [MongoDB: Quick Start FastAPI](https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/) — the ObjectId pattern in `app/models.py` follows this guide
