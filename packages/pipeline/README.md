# rp-to-strong-pipeline

Orchestration pipeline for automated workout data extraction, transformation, and export. This package handles the same data flow as the [CLI](../cli/README.md) but runs on a schedule with DAG-based execution, failure handling, retries, and user notifications.

> **⚠️ Important Update**: While this package is scaffolded for Dagster, **Kestra is now recommended** as a simpler alternative for this project. See the [Kestra Research Document](../../KESTRA_RESEARCH.md) for a detailed comparison and implementation guide.

**Status: Orchestration layer planned but not yet implemented.**

## Orchestration Options

### Option 1: Kestra (Recommended) ✅

**Why Kestra?**
- ✅ No code refactoring needed - use existing CLI directly
- ✅ Simple YAML-based workflow definitions
- ✅ Native Docker container orchestration
- ✅ Faster to implement and maintain
- ✅ Better suited for scheduled extraction tasks

**Get started:**
```bash
# Start Kestra
mise kestra:up

# Access UI at http://localhost:8080
# See ../../kestra-flows/ for example workflows
# Read ../../KESTRA_RESEARCH.md for full details
```

### Option 2: Dagster (Original Plan)

Dagster remains a valid choice if your team:
- Prefers Python-first orchestration
- Needs sophisticated asset-level data lineage
- Is building a large-scale data platform
- Wants to deeply integrate with Python data ecosystem

**Implementation would require:**
- Refactoring CLI code into Dagster assets
- Setting up Docker executor or Kubernetes
- Understanding Dagster's IOManager and Resource concepts
- More development time (~5-7 additional days)

## Comparison: Kestra vs Dagster for This Project

| Feature | Kestra | Dagster |
|---------|--------|---------|
| **Setup Complexity** | ✅ Single Docker Compose file | ⚠️ Requires executor setup |
| **Code Refactoring** | ✅ None - use CLI as-is | ⚠️ Required - restructure into assets |
| **Workflow Definition** | ✅ Declarative YAML | ⚠️ Python code |
| **Learning Curve** | ✅ Low | ⚠️ Steep |
| **Implementation Time** | ✅ 7-11 days | ⚠️ 12-18 days |
| **Docker Integration** | ✅ Native | ⚠️ Needs executor config |
| **Maintenance** | ✅ Simple YAML updates | ⚠️ Python code changes |
| **Best For** | ✅ This project's needs | ⚠️ Large data platforms |

**Bottom Line**: For scheduled workout extraction with existing CLI tools, Kestra is the pragmatic choice.

## Planned Architecture

```
                ┌──────────────┐
                │   Scheduler  │  (cron / sensor)
                └──────┬───────┘
                       │
          ┌────────────▼────────────┐
          │  Extract RP + Hevy Data │  (assets)
          └────────────┬────────────┘
                       │
          ┌────────────▼────────────┐
          │   Transform with Polars │  (assets)
          └────────────┬────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
  ┌────▼────┐   ┌──────▼──────┐  ┌────▼────┐
  │  Export  │   │  Embedding  │  │  Notify │
  │      │   │  Matching   │  │  User   │
  │  CSV     │   │  (optional) │  │         │
  └─────────┘   └─────────────┘  └─────────┘
```

### Responsibilities

- **Scheduled extraction** --- Pull workout data from RP and Hevy APIs on a cron schedule (or triggered by a sensor)
- **DAG execution** --- Dagster manages the dependency graph so steps run in the right order with proper retries on failure
- **Failure handling** --- Built-in retry policies and alerting when API calls or transformations fail
- **User communication** --- Notify users on successful exports or when manual intervention is needed (e.g., expired tokens)

### Differences from the CLI

| | CLI | Pipeline |
|---|---|---|
| Trigger | Manual (user runs a command) | Scheduled (cron) or event-driven (sensor) |
| Failure handling | Exits with error code | Retries with backoff, sends alerts |
| User input | Token file, CLI flags | Dagster UI / config, stored credentials |
| Orchestration | Single async function | Dagster DAG with observable assets |
| Monitoring | Terminal output | Dagster webserver dashboard |

## Package Structure

```
src/rp_to_strong_pipeline/
  __init__.py
  assets/           # Dagster software-defined assets (placeholder)
    __init__.py
  resources/        # Dagster resources — API clients, config (placeholder)
    __init__.py
```

## Dependencies

| Package | Purpose |
|---|---|
| `dagster` >=1.9 | Orchestration framework |
| `dagster-webserver` >=1.9 | Web UI for monitoring and triggering runs |
| `polars` >=1.0 | Data transformation |
| `httpx` >=0.27 | Async HTTP client |

Requires **Python >= 3.12**.

## Docker

```bash
mise //packages/pipeline:build
```

Multi-stage build (debian:trixie-slim runtime). Runs `dagster-webserver` on port 3000 as non-root `app` user.

---

## Next Steps

### If Choosing Kestra (Recommended)

1. **Review the research**: Read [../../KESTRA_RESEARCH.md](../../KESTRA_RESEARCH.md)
2. **Start Kestra**: Run `mise kestra:up` from project root
3. **Explore examples**: Check [../../kestra-flows/](../../kestra-flows/) for workflow examples
4. **Deploy workflows**: Upload YAML flows via UI or API
5. **Configure secrets**: Add API tokens in Kestra UI
6. **Test execution**: Run a manual flow execution
7. **Set up scheduling**: Configure cron triggers for automation

**Resources:**
- Setup guide: [../../kestra-flows/README.md](../../kestra-flows/README.md)
- Docker Compose: [../../docker-compose.kestra.yml](../../docker-compose.kestra.yml)
- Example workflow: [../../kestra-flows/rp-hevy-extraction.yml](../../kestra-flows/rp-hevy-extraction.yml)

### If Choosing Dagster

1. **Plan the migration**: Decide which CLI functions become assets
2. **Set up Dagster**: Install dependencies and configure workspace
3. **Refactor code**: Convert CLI logic into Dagster assets/ops
4. **Define IOManagers**: Configure data passing between assets
5. **Add resources**: Create configurable resources for APIs
6. **Test locally**: Use Dagster UI for development
7. **Deploy**: Set up Docker executor or Kubernetes

**Estimated effort:** 12-18 days vs. 7-11 days for Kestra

---

## Questions?

- For Kestra questions: See [../../KESTRA_RESEARCH.md](../../KESTRA_RESEARCH.md) or [Kestra docs](https://kestra.io/docs)
- For Dagster questions: See [Dagster docs](https://docs.dagster.io/) or the [original plan](../../plan.md)
