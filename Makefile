-include .env
export

.PHONY: install dev worker docker-build docker-run-api docker-run-worker test lint format upgrade

install:
	uv sync

dev:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

worker:
	uv run python -m app.worker

docker-build:
	docker build -t drexor-python:latest .

docker-run-api:
	docker run --rm --env-file .env -p 8000:8000 drexor-python:latest

docker-run-worker:
	docker run --rm --env-file .env drexor-python:latest python -m app.worker

test:
	uv run pytest -v

lint:
	uvx ruff check .
	uvx ruff format --check .

format:
	uvx ruff check . --fix && uvx ruff format .

upgrade:
	uv lock --upgrade
	uv sync
