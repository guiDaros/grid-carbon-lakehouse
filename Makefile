# Convenience wrappers only: every target is a thin alias for a documented
# `uv run ...` / `docker compose ...` command (see CLAUDE.md "Commands").
.DEFAULT_GOAL := help
.PHONY: help setup lint test test-integration up down

help: ## List targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-18s %s\n", $$1, $$2}'

setup: ## Install dependencies and the git pre-commit hook
	uv sync
	uv run pre-commit install

lint: ## Run all pre-commit hooks (ruff, ruff-format, mypy, gitleaks, ...) on every file
	uv run pre-commit run --all-files

test: ## Unit tests (integration excluded by default)
	uv run pytest

test-integration: ## Integration tests against Azurite (run `make up` first)
	uv run pytest -m integration

up: ## Start Azurite in the background
	docker compose up -d azurite

down: ## Stop local services
	docker compose down
