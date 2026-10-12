## Who and Why

Python-first data engineer learning FastAPI. This repo is a lab: prioritize clarity and teaching over cleverness. Be terse.

**Stack**: Python 3.10, FastAPI, MongoDB, uv

## Repo Layout

Read `README.md` first, it has the file tree. Each project has its own README:

- `pocs/rewards-api/README.md`
- `snippets/README.md`

## Virtual env rule

**NEVER run Python commands outside the virtual env.** Always use `uv run ...` (or the `make` targets, which call `uv run`) from the folder that owns the `pyproject.toml` (`pocs/rewards-api`, or a snippet folder), or the project's container. Never `pip install`, never a bare `python` or `pytest`. This applies to the snippets too.

## How to run

Rewards API, from `pocs/rewards-api`:

- install deps: `make install`
- start MongoDB: `docker compose up -d mongo`
- create the demo user (required before `/auth` works): `make create-user`
- run unit tests: `make test`
- run the API: `make run`
- update deps: `make update-deps`
- API and MongoDB both in Docker: `export DYNACONF_TOKEN_SECRET_KEY="$(openssl rand -hex 32)"` then `docker compose up -d --build`

Local `make run` needs the gitignored `resources/.secrets.toml` (see the poc README). Never read, print or commit it.

Snippets, from the snippet folder (example): `uv run uvicorn main:app --reload`

Lint and format (same as CI), from anywhere in the repo: `uvx pre-commit run --all-files`

## Conventions

- Entrypoint is `app/main.py` (`app.main:app`), run from `pocs/rewards-api` so relative `static/` and `resources/` paths resolve.
- `routers/` stay thin, business logic in `services/`, MongoDB access (Motor) in `infra/`.
- Pydantic v2 models in `models.py`, JWT and bcrypt in `security.py`, Bearer token to current user in `dependencies.py`.
- Settings use Dynaconf, profile chosen by `APP_ENV`, from `resources/settings.toml`. Secrets live only in the gitignored `resources/.secrets.toml` locally, and in `DYNACONF_*` env vars in CI and Docker.
- Tests use `TestClient` and `dependency_overrides` (the `auth_as` fixture), run with `pytest --cov`.
- Ruff rules E, F, I, UP with line length 110, plus the pre-commit hooks (including `no-commit-to-branch` on `main`: work on feature branches).
- The Docker image installs with `uv sync --frozen --no-dev`.
- Snippets are isolated: own `pyproject.toml`, never import code from a poc.

## Releasing

To cut a release, tag manually to match the `version` in `pocs/rewards-api/pyproject.toml` and `FastAPI(version=...)` in `pocs/rewards-api/app/main.py`, then push the tag:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

## Keep Docs Updated

When a command, path or behavior changes, update the affected README and this file in the same PR.
