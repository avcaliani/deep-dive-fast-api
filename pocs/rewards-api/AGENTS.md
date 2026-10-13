Repo-wide rules (venv rule, lint, branches) are in the root `AGENTS.md`. Commands are in `README.md`.

## Run and secrets

- Run every command from `pocs/rewards-api`, `static/` and `resources/` paths are relative.
- Local `make run` needs the gitignored `resources/.secrets.toml`. Never read, print or commit it.
- In CI and Docker the secrets come from `DYNACONF_*` env vars instead.

## Releasing

To cut a release, tag manually to match the `version` in `pyproject.toml` and `FastAPI(version=...)` in `app/main.py`, then push the tag:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```
