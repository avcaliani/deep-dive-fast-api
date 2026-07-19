## About the Repo

**Stack**: Python, FastAPI
**Goal**: This repo is the learning lab, prioritize clarity and teaching over cleverness. Be terse.

## Repo Layout

- `app/routers/` - API route handlers
- `app/services/` - business logic
- `app/utils/` - auth & MongoDB helpers
- `app/models.py` - Pydantic models
- `main.py` - FastAPI app entrypoint
- `config.py` - Dynaconf settings loader
- `tests/` - unit tests
- `resources/log-config.yml` - Uvicorn logging config
- `docker-compose.yml` - local MongoDB service
- `Dockerfile` - container build for the API

## How to run

Requires `.secrets.toml` (see README) and MongoDB running via `docker-compose up -d`.

- install deps: `make install`
- run unit tests: `make test`
- run: `make run`
- update deps: `make update-deps`
