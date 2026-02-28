# syntax=docker/dockerfile:1

# --- Mise binary ---
FROM jdxcode/mise:latest AS mise

# --- Builder ---
FROM debian:trixie-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Grab mise from its official image (not installed via apt/curl)
COPY --from=mise /usr/local/bin/mise /usr/local/bin/mise
ENV MISE_YES=1 \
    MISE_DATA_DIR=/opt/mise

# Install Python version declared in root .mise.toml
WORKDIR /app
COPY .mise.toml ./
RUN mise install python \
    && cp -a "$(mise where python)" /opt/python

ENV PATH="/opt/python/bin:$PATH"

# Grab uv from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy workspace layout for dependency resolution
COPY pyproject.toml uv.lock ./
COPY packages/pipeline/pyproject.toml packages/pipeline/
COPY packages/cli/pyproject.toml packages/cli/

# Copy sources
COPY packages/pipeline/src packages/pipeline/src
COPY packages/cli/src packages/cli/src

# Install CLI and all its dependencies (including pipeline from workspace)
RUN uv sync --frozen --package rp-to-strong-cli --no-editable \
    && uv pip install --no-deps packages/cli/

# --- Runtime ---
FROM debian:trixie-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -r -s /usr/sbin/nologin -d /app app

COPY --from=builder /opt/python /opt/python
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:/opt/python/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
USER app

ENTRYPOINT ["python", "-c", "from rp_to_strong_cli.main import cli; cli()"]
