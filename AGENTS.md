## About the Repo

**Stack**: Python, FastAPI, uv
**Goal**: This repo is the learning lab, prioritize clarity and teaching over cleverness. Be terse.

## Repo Layout

- `app/routers/` - API route handlers
- `app/services/` - business logic
- `app/infra/` - MongoDB facade and database access
- `app/security.py` - password hashing and JWT helpers
- `app/dependencies.py` - auth dependency injection (Bearer token -> current user)
- `app/config.py` - Dynaconf settings loader
- `app/models.py` - Pydantic models
- `static/` - static files served by the API, incl. the interactive playground on `/`
- `scripts/` - one-off maintenance scripts (e.g. `create_user.py`)
- `app/main.py` - FastAPI app entrypoint (`app.main:app`)
- `tests/` - unit tests
- `resources/settings.toml` / `resources/.secrets.toml` - Dynaconf settings
- `resources/init-mongo.js` - Mongo init script (creates the API's DB user)
- `resources/log-config.yml` - Uvicorn logging config
- `docker-compose.yml` - local MongoDB service and the containerized API (`docker` profile)
- `Dockerfile` - container build for the API
- `pyproject.toml` / `uv.lock` - dependencies, managed with uv
- `.github/ISSUE_TEMPLATE.md` - default GitHub issue template

## How to run

Requires `resources/.secrets.toml` (see README) and MongoDB running via `docker-compose up -d mongo`.

- install deps: `make install`
- activate the virtualenv before running Python commands: `source .venv/bin/activate`
- create the demo user (required before `/auth` will work): `make create-user`
- run unit tests: `make test`
- run: `make run`
- update deps: `make update-deps`

The Makefile and Dockerfile start Uvicorn with `app.main:app`. Tests import the application from `app.main`. Run commands from the repository root so relative `static/` and `resources/` paths resolve correctly.

## Releasing

To cut a release, tag manually to match the `version` in `pyproject.toml` / `app/main.py`'s `FastAPI(version=...)`, then push the tag:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```
