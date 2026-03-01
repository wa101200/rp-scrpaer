# Kestra Research: Alternative to Dagster for rp-to-hevy Project

## Executive Summary

This document evaluates **Kestra** as an alternative to **Dagster** for orchestrating the rp-to-hevy workout data extraction pipeline. Based on comprehensive research, **Kestra is recommended** as it offers significant advantages for this project's specific use case while maintaining simplicity and ease of adoption.

### Key Recommendation: ✅ Migrate to Kestra

**Why Kestra is a better fit:**
1. **Simpler adoption** - YAML-based workflows vs. Python code refactoring
2. **Better for scheduled extraction** - Event-driven architecture with robust scheduling
3. **Easier Docker integration** - Native container orchestration without complex setup
4. **Lower complexity** - No need to restructure existing CLI code into assets
5. **Better for small-scale projects** - Lighter weight, faster to deploy and maintain
6. **Universal orchestration** - Can handle both data and infrastructure tasks

---

## 1. What is Kestra?

Kestra is a modern, open-source **universal orchestration platform** that uses declarative YAML syntax to define and manage workflows. Unlike Dagster (which is Python-centric and data-asset focused), Kestra can orchestrate:

- Data pipelines (ETL/ELT)
- Business workflows
- Infrastructure automation
- API integrations
- Mixed-language tasks

### Core Features

| Feature | Description |
|---------|-------------|
| **Declarative YAML** | Define workflows in simple YAML files - no code refactoring needed |
| **Event-driven** | Trigger on schedules, webhooks, file changes, or custom events |
| **Container-native** | Each task runs in isolated Docker containers |
| **600+ Plugins** | Pre-built integrations for databases, APIs, cloud services, Python, SQL, etc. |
| **Visual UI** | Web interface for designing, monitoring, and managing flows |
| **Language agnostic** | Run Python, SQL, Shell, Node.js, any script language |
| **Lightweight** | Can run as single Docker container or scale to Kubernetes |

---

## 2. Kestra vs Dagster Comparison

### High-Level Comparison

| Aspect | Dagster | Kestra |
|--------|---------|--------|
| **Primary Language** | Python only | Any (YAML config, plugins for logic) |
| **Workflow Definition** | Python code (`@asset`, `@op`) | Declarative YAML |
| **Learning Curve** | Steep (requires understanding assets, resources, IOManagers) | Shallow (YAML syntax, task plugins) |
| **Code Refactoring** | **Required** - must restructure into Dagster paradigm | **Not required** - call existing scripts/CLI commands |
| **Setup Complexity** | Moderate to High | Low (single Docker Compose file) |
| **Best For** | Large data engineering teams, asset-centric data platforms | Small-to-medium teams, diverse workflows, rapid prototyping |
| **Data Lineage** | First-class citizen (asset-level tracking) | Supported but more generic |
| **Docker Integration** | Requires custom executor setup | Native, built-in |
| **Scheduling** | Via sensors, schedules | Native cron, event-driven triggers |
| **CLI Integration** | Requires wrapping in Dagster assets/ops | Direct task execution (no refactoring) |

### Detailed Feature Comparison

#### Workflow Definition

**Dagster:**
```python
from dagster import asset, IOManager

@asset
def extract_rp_data():
    # Must refactor existing CLI code into asset
    # Must define IOManagers for data passing
    return raw_data

@asset
def transform_workouts(extract_rp_data):
    # Asset dependencies via function parameters
    return transformed_data
```

**Kestra:**
```yaml
id: rp-extraction
namespace: rp.workouts
tasks:
  - id: extract_rp
    type: io.kestra.plugin.scripts.python.Script
    script: |
      # Can reuse existing code directly
      from rp_to_strong_cli import cli
      cli.export_rp()
  
  - id: transform
    type: io.kestra.plugin.scripts.python.Script
    script: |
      # Process the extracted data
      import polars as pl
      df = pl.read_json('{{ outputs.extract_rp.outputFiles["data.json"] }}')
```

#### Docker Integration

**Dagster:**
- Requires configuring `DockerExecutor` or `K8sRunLauncher`
- Complex setup for custom images
- Need to understand Dagster deployment architecture

**Kestra:**
- Native Docker support per task
- Simple `containerImage` field in YAML
- No deployment complexity

```yaml
tasks:
  - id: my_task
    type: io.kestra.plugin.scripts.python.Script
    containerImage: python:3.12-slim
    beforeCommands:
      - pip install httpx polars
    script: |
      # Your code here
```

#### Scheduling and Triggers

**Dagster:**
```python
from dagster import ScheduleDefinition

daily_schedule = ScheduleDefinition(
    job=my_job,
    cron_schedule="0 0 * * *"
)
```

**Kestra:**
```yaml
triggers:
  - id: daily_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 0 * * *"
```

---

## 3. How Kestra Fits This Project

### Current Project Architecture

```
rp-to-hevy/
├── packages/
│   ├── api-service/      # RP + Hevy SDKs (working)
│   ├── embeddings/       # Semantic matching (working)
│   ├── cli/              # Click CLI (working)
│   └── pipeline/         # Dagster (placeholder, NOT implemented)
```

**Key Insight:** The Dagster pipeline is currently **scaffolded but empty**. The CLI already has all the working business logic. This makes Kestra a perfect fit because:

1. ✅ **No migration cost** - Pipeline isn't implemented yet
2. ✅ **Reuse existing code** - Can call CLI commands directly
3. ✅ **Simpler architecture** - Don't need to learn and implement Dagster's asset paradigm
4. ✅ **Faster time to production** - YAML flows vs. Python asset development

### Proposed Kestra Architecture

```
┌─────────────────────────────────────────┐
│          Kestra Orchestrator            │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │    Schedule/Trigger (cron/event)  │ │
│  └──────────────┬────────────────────┘ │
│                 │                       │
│  ┌──────────────▼────────────────────┐ │
│  │  Extract RP Data (Python Script)  │ │
│  │  - Calls existing CLI commands    │ │
│  │  - Or imports api-service directly│ │
│  └──────────────┬────────────────────┘ │
│                 │                       │
│  ┌──────────────▼────────────────────┐ │
│  │  Extract Hevy Data (Python Script)│ │
│  └──────────────┬────────────────────┘ │
│                 │                       │
│  ┌──────────────▼────────────────────┐ │
│  │  Match Exercises (Python Script)  │ │
│  │  - Calls embeddings package       │ │
│  └──────────────┬────────────────────┘ │
│                 │                       │
│  ┌──────────────▼────────────────────┐ │
│  │  Transform & Export (Python)      │ │
│  │  - Uses Polars transformations    │ │
│  └──────────────┬────────────────────┘ │
│                 │                       │
│  ┌──────────────▼────────────────────┐ │
│  │  Notify User (Slack/Email)        │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Example Kestra Flow for RP-to-Hevy

```yaml
id: rp-to-hevy-extraction
namespace: workouts.pipeline
description: |
  Automated extraction of RP Hypertrophy workout data, 
  exercise matching with semantic embeddings, and export to portable formats

inputs:
  - id: rp_auth_token
    type: SECRET
    description: RP Hypertrophy API authentication token
  
  - id: hevy_api_key
    type: SECRET
    description: Hevy API key

tasks:
  # Task 1: Extract RP workout data
  - id: extract_rp_workouts
    type: io.kestra.plugin.scripts.python.Script
    containerImage: ghcr.io/wa101200/rp-scrpaer/cli:latest
    env:
      RP_AUTH_TOKEN: "{{ inputs.rp_auth_token }}"
    script: |
      from rp_to_strong_cli.rp import export_workouts
      import json
      
      workouts = export_workouts()
      
      # Save to Kestra output
      with open('rp_workouts.json', 'w') as f:
          json.dump(workouts, f)
    outputFiles:
      - rp_workouts.json

  # Task 2: Extract Hevy workout data
  - id: extract_hevy_workouts
    type: io.kestra.plugin.scripts.python.Script
    containerImage: ghcr.io/wa101200/rp-scrpaer/cli:latest
    env:
      HEVY_API_KEY: "{{ inputs.hevy_api_key }}"
    script: |
      from rp_to_strong_cli.hevy import export_workouts
      import json
      
      workouts = export_workouts()
      
      with open('hevy_workouts.json', 'w') as f:
          json.dump(workouts, f)
    outputFiles:
      - hevy_workouts.json

  # Task 3: Generate exercise embeddings and find matches
  - id: match_exercises
    type: io.kestra.plugin.scripts.python.Script
    containerImage: ghcr.io/wa101200/rp-scrpaer/cli:latest
    inputFiles:
      rp_workouts.json: "{{ outputs.extract_rp_workouts.outputFiles['rp_workouts.json'] }}"
      hevy_workouts.json: "{{ outputs.extract_hevy_workouts.outputFiles['hevy_workouts.json'] }}"
    script: |
      from embeddings import generate_matches
      import json
      
      with open('rp_workouts.json') as f:
          rp_data = json.load(f)
      
      with open('hevy_workouts.json') as f:
          hevy_data = json.load(f)
      
      matches = generate_matches(rp_data, hevy_data)
      
      with open('exercise_matches.json', 'w') as f:
          json.dump(matches, f)
    outputFiles:
      - exercise_matches.json

  # Task 4: Transform and export to CSV
  - id: transform_and_export
    type: io.kestra.plugin.scripts.python.Script
    containerImage: ghcr.io/wa101200/rp-scrpaer/cli:latest
    inputFiles:
      rp_workouts.json: "{{ outputs.extract_rp_workouts.outputFiles['rp_workouts.json'] }}"
      exercise_matches.json: "{{ outputs.match_exercises.outputFiles['exercise_matches.json'] }}"
    script: |
      import polars as pl
      import json
      
      with open('rp_workouts.json') as f:
          workouts = json.load(f)
      
      with open('exercise_matches.json') as f:
          matches = json.load(f)
      
      # Transform using Polars
      df = pl.DataFrame(workouts)
      # ... transformation logic ...
      
      # Export to CSV
      df.write_csv('workout_export.csv')
    outputFiles:
      - workout_export.csv

  # Task 5: Upload to cloud storage (optional)
  - id: upload_to_storage
    type: io.kestra.plugin.gcp.gcs.Upload
    from: "{{ outputs.transform_and_export.outputFiles['workout_export.csv'] }}"
    to: gs://my-bucket/exports/workout_{{ execution.startDate }}.csv

  # Task 6: Notify user
  - id: notify_completion
    type: io.kestra.plugin.notifications.slack.SlackIncomingWebhook
    url: "{{ secret('SLACK_WEBHOOK_URL') }}"
    payload: |
      {
        "text": "✅ Workout data extraction completed successfully!",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Workout Export Complete*\nExecution ID: {{ execution.id }}\nDate: {{ execution.startDate }}"
            }
          }
        ]
      }

triggers:
  # Run daily at 2 AM
  - id: daily_extraction
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 2 * * *"

errors:
  # Handle failures
  - id: notify_failure
    type: io.kestra.plugin.notifications.slack.SlackIncomingWebhook
    url: "{{ secret('SLACK_WEBHOOK_URL') }}"
    payload: |
      {
        "text": "❌ Workout extraction failed!",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Extraction Failed*\nExecution ID: {{ execution.id }}\nError: {{ error.message }}"
            }
          }
        ]
      }
```

---

## 4. Benefits of Kestra for This Project

### 1. **Zero Code Refactoring**
- ✅ Existing CLI commands work as-is
- ✅ Can import and call packages directly
- ✅ No need to learn Dagster's asset/op paradigm

### 2. **Simpler Docker Integration**
- ✅ This project already has Docker builds for each package
- ✅ Kestra can use these images directly
- ✅ No need for complex executor configuration

### 3. **Better Scheduling & Triggers**
- ✅ Native cron scheduling
- ✅ Event-driven triggers (webhooks, file changes)
- ✅ Manual triggers from UI

### 4. **Easier to Maintain**
- ✅ YAML is easier to read and modify than Python orchestration code
- ✅ Non-Python developers can understand and modify workflows
- ✅ Clear separation between business logic (Python) and orchestration (YAML)

### 5. **Rich Plugin Ecosystem**
- ✅ 600+ pre-built plugins
- ✅ Native integrations: Slack, email, cloud storage, databases, APIs
- ✅ Can extend with custom plugins

### 6. **Observability**
- ✅ Built-in UI for monitoring
- ✅ Execution logs per task
- ✅ Metrics and alerting
- ✅ Task-level retry policies

### 7. **Lower Resource Requirements**
- ✅ Can run as single Docker container
- ✅ Lightweight compared to Dagster
- ✅ Easier deployment (Docker Compose vs. complex k8s setup)

---

## 5. Migration Path from Dagster (Placeholder) to Kestra

Since the Dagster pipeline is **not yet implemented**, this is actually a **greenfield implementation**, not a migration. The path is straightforward:

### Step 1: Remove Dagster Dependencies
```bash
# Update packages/pipeline/pyproject.toml
# Remove:
# - dagster>=1.9
# - dagster-webserver>=1.9

# Keep:
# - polars>=1.0
# - httpx>=0.27
```

### Step 2: Deploy Kestra

Create `docker-compose.yml` in project root:

```yaml
version: "3.8"

services:
  kestra:
    image: kestra/kestra:latest
    container_name: kestra
    ports:
      - "8080:8080"
    volumes:
      - kestra-data:/app/storage
      - ./kestra-flows:/app/flows
    environment:
      KESTRA_CONFIGURATION: |
        datasources:
          postgres:
            url: jdbc:postgresql://postgres:5432/kestra
            username: kestra
            password: kestra
        kestra:
          server:
            basic-auth:
              enabled: false
          repository:
            type: postgres
          queue:
            type: postgres
  
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: kestra
      POSTGRES_USER: kestra
      POSTGRES_PASSWORD: kestra
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  kestra-data:
  postgres-data:
```

### Step 3: Create Kestra Flows

Create `kestra-flows/` directory with YAML workflow definitions (see example above).

### Step 4: Update Documentation

Update `README.md` and `packages/pipeline/README.md` to reflect Kestra usage.

### Step 5: Update `.mise.toml`

Add Kestra-related tasks:

```toml
[tasks.kestra-up]
description = "Start Kestra orchestrator"
run = "docker-compose up -d"

[tasks.kestra-down]
description = "Stop Kestra orchestrator"
run = "docker-compose down"

[tasks.kestra-logs]
description = "View Kestra logs"
run = "docker-compose logs -f kestra"
```

---

## 6. Drawbacks and Considerations

### Potential Challenges

1. **Learning Curve for YAML Syntax**
   - Team needs to learn Kestra's YAML structure
   - Mitigation: Excellent documentation, simple syntax

2. **Less Python-Native**
   - Can't use Python tooling (type hints, linting) for workflow logic
   - Mitigation: Business logic stays in Python; only orchestration in YAML

3. **Newer Ecosystem**
   - Kestra is younger than Dagster (but growing rapidly)
   - Mitigation: Active development, strong community

4. **Limited Dynamic Workflows**
   - Harder to generate workflows programmatically
   - Mitigation: Can use subflows and dynamic inputs; sufficient for this project

### When Dagster Might Be Better

Dagster would be preferred if:
- ❌ Team is 100% Python developers who prefer code over config
- ❌ Need sophisticated asset-level data lineage tracking
- ❌ Building a large-scale data platform with hundreds of assets
- ❌ Heavy investment in Python data ecosystem (Pandas, dbt in Python)

**None of these apply to this project.**

---

## 7. Recommendations

### Primary Recommendation: ✅ Use Kestra

**Rationale:**
1. Pipeline package is currently empty (no sunk cost)
2. Existing CLI code can be reused without refactoring
3. Simpler to implement and maintain
4. Better suited for scheduled extraction use case
5. Easier for non-Python contributors to understand

### Implementation Plan

1. **Phase 1: Setup** (1-2 days)
   - Add `docker-compose.yml` for Kestra
   - Update `packages/pipeline` to remove Dagster deps
   - Create initial flow YAML files

2. **Phase 2: Core Workflows** (3-5 days)
   - Implement RP extraction flow
   - Implement Hevy extraction flow
   - Implement exercise matching flow
   - Implement export flow

3. **Phase 3: Enhancements** (2-3 days)
   - Add error handling and retries
   - Add notifications (Slack/email)
   - Add cloud storage integration (if needed)
   - Set up scheduling/triggers

4. **Phase 4: Documentation** (1 day)
   - Update README.md
   - Update packages/pipeline/README.md
   - Add flow documentation

**Total estimated effort: 7-11 days**

### Alternative: Stick with Dagster

If the team is committed to Dagster (e.g., for resume building, learning experience), they should:
1. Understand this will take longer to implement
2. Accept higher complexity for this use case
3. Plan to refactor existing CLI logic into Dagster assets
4. Set up proper Docker executor configuration

**Estimated additional effort with Dagster: +5-7 days**

---

## 8. Resources and Next Steps

### Kestra Resources

- **Official Documentation:** https://kestra.io/docs
- **Python Integration Guide:** https://kestra.io/docs/how-to-guides/python
- **Docker Deployment:** https://kestra.io/docs/installation/docker
- **Example Flows:** https://github.com/kestra-io/examples
- **Community Forum:** https://kestra.io/slack

### Getting Started

```bash
# Clone this repo and start Kestra
git clone <repo>
cd rp-to-hevy

# Start Kestra
docker-compose up -d

# Access UI at http://localhost:8080
# Create your first flow via UI or upload YAML

# View logs
docker-compose logs -f kestra
```

### Next Steps

1. **Decision Point:** Team decides Kestra vs. Dagster
2. **If Kestra:** Follow implementation plan above
3. **If Dagster:** Create separate implementation plan for asset-based architecture

---

## 9. Conclusion

**Kestra is strongly recommended** for the rp-to-hevy project due to:

1. ✅ **Zero migration cost** - Pipeline not yet implemented
2. ✅ **Reuse existing code** - CLI and packages work as-is
3. ✅ **Simpler architecture** - YAML > Python orchestration code for this use case
4. ✅ **Faster time to value** - Get scheduled extraction working in days, not weeks
5. ✅ **Better maintainability** - Easier for team to understand and modify
6. ✅ **Native Docker support** - Leverages existing containerization

The project's current state (working CLI, empty pipeline) makes this an ideal time to adopt Kestra instead of Dagster. The simplicity and directness of Kestra's approach aligns perfectly with the project's goal of scheduled workout data extraction.

---

**Author:** GitHub Copilot Coding Agent  
**Date:** March 1, 2026  
**Status:** Research Complete - Awaiting Team Decision
