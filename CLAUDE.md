## About the Repo

**Stack**: Python, FastAPI, uv
**Goal**: This repo is the learning lab, prioritize clarity and teaching over cleverness. Be terse.

## Repo Layout

- `app/routers/` - API route handlers
- `app/services/` - business logic
- `app/utils/` - auth & MongoDB helpers
- `app/dependencies.py` - auth dependency injection (Bearer token -> current user)
- `app/config.py` - Dynaconf settings loader
- `app/models.py` - Pydantic models
- `static/` - static files served by the API, incl. the interactive playground on `/`
- `scripts/` - one-off maintenance scripts (e.g. `create_user.py`)
- `main.py` - FastAPI app entrypoint
- `tests/` - unit tests
- `resources/settings.toml` / `resources/.secrets.toml` - Dynaconf settings
- `resources/init-mongo.js` - Mongo init script (creates the API's DB user)
- `resources/log-config.yml` - Uvicorn logging config
- `docker-compose.yml` - local MongoDB service
- `Dockerfile` - container build for the API
- `pyproject.toml` / `uv.lock` - dependencies, managed with uv

## How to run

Requires `resources/.secrets.toml` (see README) and MongoDB running via `docker-compose up -d`.

- install deps: `make install`
- create the demo user (required before `/auth` will work): `make create-user`
- run unit tests: `make test`
- run: `make run`
- update deps: `make update-deps`

## Releasing

To cut a release, tag manually to match the `version` in `pyproject.toml` / `main.py`'s `FastAPI(version=...)`, then push the tag:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```
