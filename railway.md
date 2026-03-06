# Railway Deployment Plan

Deploy the rp-to-hevy pipeline on [Railway](https://railway.com) as a set of cron-scheduled services backed by managed Redis.

## Why Railway

- **CLI is already containerized** — production-ready multi-stage Dockerfile in `packages/cli/`
- **Per-second billing with scale-to-zero** — pipeline is bursty, pays only when running
- **Managed Redis** — one-click plugin for LLM judge caching
- **Native Docker builds** — eliminates Tailscale + remote BuildKit setup in CI
- **Built-in secrets management** — replaces `.env` file management

## Architecture

```
Railway Project: rp-to-hevy
├── rp-export (cron service)           # Weekly RP data export
├── hevy-export (cron service)         # Weekly Hevy data export
├── embedding-pipeline (cron service)  # Embed → similarity search → LLM judge
├── port-workouts (cron service)       # Convert & upload workouts to Hevy
├── Redis (plugin)                     # LLM judge result cache
└── Volume (persistent)                # ChromaDB + exported JSON data
```

## Services

### rp-export

Exports RP exercises, mesocycles, templates, and history.

| Setting    | Value                                                  |
| ---------- | ------------------------------------------------------ |
| Dockerfile | `packages/cli/Dockerfile`                              |
| Command    | `rp-to-hevy-cli rp export --type all -o /data/rp/`    |
| Schedule   | `0 6 * * 1` (weekly, Monday 6 AM UTC)                  |
| Volume     | `/data`                                                |

### hevy-export

Exports Hevy exercise templates and existing workouts.

| Setting    | Value                                                  |
| ---------- | ------------------------------------------------------ |
| Dockerfile | `packages/cli/Dockerfile`                              |
| Command    | `rp-to-hevy-cli hevy export --type all -o /data/hevy/` |
| Schedule   | `0 6 * * 1` (weekly, Monday 6 AM UTC)                  |
| Volume     | `/data`                                                |

### embedding-pipeline

Encodes exercises into ChromaDB, runs similarity search, and invokes LLM judge.

| Setting    | Value                                                  |
| ---------- | ------------------------------------------------------ |
| Dockerfile | `packages/cli/Dockerfile`                              |
| Command    | see below                                              |
| Schedule   | `30 6 * * 1` (weekly, Monday 6:30 AM UTC, after exports) |
| Volume     | `/data`                                                |

```sh
rp-to-hevy-cli embedding embd \
  --rp-exercises /data/rp/exercises.json \
  --hevy-exercises /data/hevy/exercises.json \
  --chroma-mode persistent \
  --chroma-path /data/chromadb \
&& rp-to-hevy-cli embedding run-rp-similarity-search \
  --chroma-mode persistent \
  --chroma-path /data/chromadb \
  -o /data/embeddings/output \
&& rp-to-hevy-cli embedding llm-judge \
  --input-dir /data/embeddings/output \
  -o /data/embeddings/llm-matches.yaml
```

### port-workouts

Converts RP workouts to Hevy format and uploads via API.

| Setting    | Value                                                  |
| ---------- | ------------------------------------------------------ |
| Dockerfile | `packages/cli/Dockerfile`                              |
| Command    | `rp-to-hevy-cli port-rp-workout-to-hevy --matches /data/embeddings/llm-matches.yaml` |
| Schedule   | `0 7 * * 1` (weekly, Monday 7 AM UTC, after embedding) |
| Volume     | `/data`                                                |

### Redis

Railway managed Redis plugin. Used by `embedding llm-judge` for caching LLM results.

| Setting | Value        |
| ------- | ------------ |
| Plugin  | Redis        |
| Plan    | Hobby / Pro  |

Exposed as `REDIS_URL` to all services via shared variable.

## Environment Variables

Configure these as shared variables in the Railway project:

| Variable             | Description                          |
| -------------------- | ------------------------------------ |
| `RP_BEARER_TOKEN`    | RP API auth token                    |
| `RP_APP_BASE_URL`    | RP API base URL (has default)        |
| `HEVY_API_KEY`       | Hevy developer API key               |
| `HEVY_API_BASE_URL`  | Hevy API base URL (has default)      |
| `OPENROUTER_API_KEY` | OpenRouter API key for embeddings    |
| `TITLE_API_BASE_URL` | LLM base URL for workout titles      |
| `TITLE_API_KEY`      | LLM API key for workout titles       |
| `TITLE_API_MODEL`    | LLM model name (e.g. `gemini-2.5-flash`) |
| `REDIS_URL`          | Auto-injected by Railway Redis plugin |

## What This Replaces

| Before                              | After                       |
| ----------------------------------- | --------------------------- |
| Tailscale + remote BuildKit in CI   | Railway native Docker builds |
| `.env` file management              | Railway shared variables    |

## Setup

```bash
# Install Railway CLI
brew install railway

# Login
railway login

# Link to project
railway link

# Deploy
railway up --dockerfile packages/cli/Dockerfile
```

## Cost Estimate

| Resource       | Estimate         |
| -------------- | ---------------- |
| Hobby plan     | $5/mo base       |
| Cron services  | ~$0.50/mo (scale-to-zero, runs ~4x/month, minutes each) |
| Redis (idle)   | ~$1–2/mo         |
| Volume (1 GB)  | ~$0.25/mo        |
| **Total**      | **~$7–8/mo**     |

## Limitations

- **No event-driven S3 triggers** — uses cron scheduling instead (simpler for this use case)
- **No DAG visualization** — pipeline is linear, no graph to visualize
- **Sequential cron dependency** — services are staggered by time, not wired as dependencies (30-min gaps provide buffer)
