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

# Stub sources so uv can resolve the workspace
RUN mkdir -p packages/pipeline/src/rp_to_strong_pipeline \
    && touch packages/pipeline/src/rp_to_strong_pipeline/__init__.py \
    && mkdir -p packages/cli/src/rp_to_strong_cli \
    && touch packages/cli/src/rp_to_strong_cli/__init__.py

# Install external dependencies only (cached layer)
RUN uv sync --frozen --package rp-to-strong-pipeline --no-install-project

# Copy real source and install the package
COPY packages/pipeline/src packages/pipeline/src
RUN uv sync --frozen --package rp-to-strong-pipeline --no-editable

# --- Runtime ---
FROM debian:trixie-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libffi8 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -r -s /usr/sbin/nologin -d /app app

COPY --from=builder /opt/python /opt/python
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:/opt/python/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
USER app

EXPOSE 3000
ENTRYPOINT ["dagster-webserver"]
CMD ["-h", "0.0.0.0", "-p", "3000"]
