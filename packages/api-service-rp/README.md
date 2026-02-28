# rp-to-strong-api-service-rp

Async Python client library for the [RP Strength Training API](https://training.rpstrength.com). Provides type-safe access to user profiles, subscriptions, mesocycles, exercises, templates, and exercise history — with a single `export_all()` call to retrieve everything in parallel.

Also ships an OpenAPI 3.0.3 specification and a Dockerized [Redocly](https://redocly.com/) documentation viewer.

## Usage

```python
import asyncio
from rp_to_strong_api_consumer.service import RPClient

async def main():
    async with RPClient(token="<bearer-token>") as client:
        profile = await client.get_user_profile()
        mesocycles = await client.get_all_mesocycles()

        # Or grab everything at once
        data = await client.export_all()

asyncio.run(main())
```

## API Coverage

| Method | Endpoint | Returns |
| --- | --- | --- |
| `get_user_profile()` | `GET /user/profile` | `UserProfile` |
| `get_user_subscriptions()` | `GET /user/subscriptions` | `UserSubscriptions` |
| `get_bootstrap()` | `GET /training/bootstrap` | `BootstrapResponse` |
| `get_exercises()` | `GET /training/exercises` | `list[Exercise]` |
| `get_mesocycles()` | `GET /training/mesocycles` | `list[MesocycleSummary]` |
| `get_mesocycle(key)` | `GET /training/mesocycles/{key}` | `MesocycleDetail` |
| `get_all_mesocycles()` | parallel fetch of all mesocycles | `list[MesocycleDetail]` |
| `get_templates()` | `GET /training/templates` | `list[TemplateSummary]` |
| `get_exercise_history(id)` | `GET /training/exercises/{id}/history` | `list[ExerciseHistoryEntry]` |
| `get_user_exercise_history()` | `GET /training/user-exercise-history` | `dict[str, str]` |
| `get_second_meso_meta()` | `GET /training/second-meso-meta` | `SecondMesoMeta` |
| `export_all()` | all of the above | `dict` |

## Package Structure

```
src/rp_to_strong_api_consumer/
  models.py    # Pydantic models with automatic camelCase <-> snake_case conversion
  service.py   # RPClient — async HTTP client built on aiohttp
openapi.yaml   # OpenAPI 3.0.3 specification (60+ endpoints)
external-api.md # Endpoint and data-model reference notes
```

## Dependencies

| Package | Purpose |
| --- | --- |
| `aiohttp` >=3.13 | Async HTTP client |
| `aiofiles` >=25.1 | Async file I/O |
| `pydantic` >=2.12 | Data validation and serialization |

Requires **Python >= 3.12**.

## OpenAPI Documentation

Compile and serve the spec locally:

```bash
mise run compile-openai   # builds openapi/index.html via Redocly
mise run serve-openapi    # serves on http://localhost:8000
```

Or run the Dockerized viewer:

```bash
mise run build            # multi-stage Docker build (Caddy)
mise run run-docker       # serves on http://localhost:8080
```

## Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `RP_APP_BASE_URL` | `https://training.rpstrength.com/api` | API base URL |
| `RP_APP_VERSION` | `1.1.13` | `accept-version` header value |
