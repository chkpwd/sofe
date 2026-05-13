FROM python:3.13-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /src

FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

FROM base AS final

RUN adduser -u 1000 python

USER python

ENV DEBUG=false

COPY --from=builder /src/.venv ./.venv
COPY app/ ./app/
COPY main.py .

ENTRYPOINT ["/src/.venv/bin/python3", "./main.py"]
