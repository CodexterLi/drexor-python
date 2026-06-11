FROM ghcr.io/astral-sh/uv:latest AS uv-source

FROM public.ecr.aws/docker/library/python:3.14-slim AS runtime
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:${PATH}" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY --from=uv-source /uv /uvx /usr/local/bin/

# Install dependencies first for better layer caching.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY app/ app/
COPY packages/ packages/
RUN uv sync --frozen --no-dev \
    && groupadd --system app \
    && useradd --system --gid app --home-dir /app app \
    && mkdir -p logs \
    && chown -R app:app /app

EXPOSE 8000
USER app

# Default role: API. Run the worker with:
# docker run --env-file .env drexor-python:latest python -m app.worker
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
