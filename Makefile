.DEFAULT_GOAL := info

# Project
PROJECT_NAME = "dunder-mifflin-api"

info:
	@echo "-----------< project >-----------"
	@echo " name              $(PROJECT_NAME)"
	@echo ""

install:
	uv sync

update-deps:
	uv lock --upgrade
	uvx pre-commit autoupdate

test:
	uv run pytest -sx

create-user:
	PYTHONPATH=. uv run python scripts/create_user.py

run:
	# APP_ENV is an environment variable used by Dynaconf
	# to indicate which profile should be used.
	APP_ENV=dev uv run uvicorn main:app --log-config "resources/log-config.yml" --reload

.PHONY: info install update-deps test create-user run
