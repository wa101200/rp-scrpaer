# syntax=docker/dockerfile:1.13-labs

FROM jdxcode/mise:2026.2.23 AS mise

FROM debian:trixie-slim@sha256:1d3c811171a08a5adaa4a163fbafd96b61b87aa871bbc7aa15431ac275d3d430 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential=12.12 \
    ca-certificates=20250419 \
    curl=8.14.1-2+deb13u2 \
    git=1:2.47.3-0+deb13u1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=mise /usr/local/bin/mise /usr/local/bin/mise
ENV MISE_YES=1 \
    MISE_DATA_DIR=/opt/mise

WORKDIR /app
COPY .mise.toml mise.lock ./
COPY packages/api-consumer/.mise.toml packages/api-consumer/.mise.toml

WORKDIR /app/packages/api-consumer
RUN --mount=type=secret,id=GITHUB_TOKEN \
    GITHUB_TOKEN=$(cat /run/secrets/GITHUB_TOKEN 2>/dev/null || true) \
    mise install node bun npm:@redocly/cli

COPY packages/api-consumer/openapi.yaml /app/packages/api-consumer/openapi.yaml
RUN mise //packages/api-consumer:compile-openai

FROM caddy:2-alpine

COPY --from=builder /app/packages/api-consumer/openapi/ /usr/share/caddy/

EXPOSE 8080
CMD ["caddy", "file-server", "--listen", ":8080", "--root", "/usr/share/caddy"]
