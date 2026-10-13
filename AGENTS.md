## Who and Why

Python-first data engineer learning FastAPI. This repo is a lab: prioritize clarity and teaching over cleverness. Be terse.

**Stack**: Python 3.10, FastAPI, uv

## Repo Layout

Read `README.md` first, it has the file tree. Each project has its own README, and pocs also have their own `AGENTS.md` with the project specifics (run location, secrets, releasing):

- `pocs/rewards-api/README.md` and `pocs/rewards-api/AGENTS.md`
- `snippets/README.md`

## Virtual env rule

**NEVER run Python commands outside the virtual env.**

Do:
- Use `uv run ...` from the folder that owns the `pyproject.toml` (`pocs/rewards-api` or a snippet folder).
- Use the `make` targets, which call `uv run`.
- Or use the project's container.

Don't:
- `pip install`
- A bare `python` or `pytest`

This applies to the snippets too.

## Conventions

- Each project is isolated: own `pyproject.toml`, own `uv.lock`, run from its folder. Snippets never import code from a poc.
- Lint and format (same as CI), from anywhere in the repo: `uvx pre-commit run --all-files`.
- Work on feature branches: the `no-commit-to-branch` hook blocks commits on `main`.

## Keep Docs Updated

When a command, path or behavior changes, update the affected README and `AGENTS.md` in the same PR.
