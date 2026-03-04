# CLI Package — rp-to-hevy-cli

## What This Is

Python CLI that exports data from **RP Hypertrophy** and **Hevy** fitness apps, then matches exercises between the two using embeddings + LLM judging. Part of the `rp-scraper` monorepo.

## Tech Stack

- **Python** ≥3.12, **Click** CLI framework, **Pydantic** v2 for data models
- **uv** package manager (workspace mode from monorepo root)
- **mise** for task orchestration and tool versions
- **ruff** for linting/formatting (rules: E, F, I, UP, B, SIM; line-length 88)
- **Docker** 3-stage build (debian:trixie-slim)
- **hk** for git hooks

## Commands

| Command | Module | Purpose |
|---------|--------|---------|
| `rp export` | `rp.py` | Export RP data (profile, exercises, mesocycles, etc.) |
| `hevy export` | `hevy.py` | Export Hevy exercise templates (paginated) |
| `embedding embd` | `embedding/embd.py` | Encode exercises into ChromaDB |
| `embedding run-rp-similarity-search` | `embedding/similarity_search.py` | Query embeddings, compute metrics |
| `embedding llm-judge` | `embedding/judge.py` | LLM selects best match per exercise |
| `port-rp-workout-to-hevy` | `port.py` | Convert RP workouts to Hevy format (WIP) |

## Key Commands to Run

```bash
# Install deps (from monorepo root)
uv sync --all-packages

# Run CLI
uv run python -m rp_to_hevy_cli <command>

# Via mise (from monorepo root or packages/cli)
mise //packages/cli:cli <args>

# Lint + format
mise format   # hk fix -a
mise lint     # hk check -a

# Tests
mise //...:test
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `HEVY_API_KEY` | Hevy API key (UUID) — required for `hevy export` |
| `OPENROUTER_API_KEY` | LLM API key — required for `llm-judge` |
| `RP_APP_BASE_URL` | RP API base (default: `https://training.rpstrength.com/api`) |
| `HEVY_API_BASE_URL` | Hevy API base (default: `https://api.hevyapp.com`) |

RP auth uses a bearer token file (default: `token.txt`).

## Coding Conventions

- **All files** start with `from __future__ import annotations`
- **Async pattern**: Click commands are sync, wrap async work with `asyncio.run()`
- **API clients**: `async with ApiClient(config) as client:` context managers
- **Private functions**: prefixed with `_` (e.g., `_fetch_all()`, `_export()`)
- **Error handling**: `raise click.ClickException(...)` for user-facing errors
- **Cloud I/O**: `cloudpathlib.AnyPath` for unified local/S3/GCS paths
- **JSON output**: Pydantic `model_dump(mode="json", by_alias=True)` → custom `_serialize()`
- **YAML output**: `ruamel.yaml` (preferred over pyyaml)
- **Reusable Click options**: decorator pattern (e.g., `_chromadb_options`, `_embedder_options`)
- **Concurrency**: `asyncio.gather()` for parallel API calls; `asyncio.Semaphore` for rate limiting
- **No logging module** — use `click.echo()` and `click.style()` for output

## Architecture Notes

- **Embedder** is pluggable: `ApiEmbedder` (OpenAI-compatible) or `LocalEmbedder` (sentence-transformers)
- **ChromaDB** supports 3 modes: `memory`, `persistent`, `http` — configured via CLI options
- **LLM judge** uses `pydantic-ai` Agent with structured output (`JudgeResult` model)
- **API SDKs** are auto-generated from OpenAPI specs (in `api-service` package)
- Data flows: APIs → JSON export → embedding → ChromaDB → similarity search → LLM judge → match YAML

## When Editing

- Keep functions small and single-purpose — follow existing module boundaries
- New commands go in their own file, registered in `__main__.py`
- Shared Click option decorators go in `embedding/utils.py` or `utils.py`
- Don't add tests unless asked — the project currently has no CLI tests
- Run `mise lint` before committing to catch ruff issues
