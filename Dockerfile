FROM python:3.12-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /src

FROM base AS builder

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main

FROM base AS final

RUN adduser -u 1000 python

USER python

ENV DEBUG=false

COPY --from=builder /src/.venv ./.venv
COPY app/ ./app/
COPY main.py .

ENTRYPOINT ["/src/.venv/bin/python3", "./main.py"]
