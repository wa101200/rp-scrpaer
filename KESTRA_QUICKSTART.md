# Kestra Integration Quick Reference

> **TL;DR**: Kestra is recommended over Dagster for orchestrating scheduled workout data extraction in this project. This document provides a quick reference for getting started.

## Why Kestra?

✅ **No code refactoring** - Use existing CLI directly  
✅ **Simple YAML workflows** - Declarative, easy to understand  
✅ **Native Docker support** - Container-based task isolation  
✅ **Faster implementation** - 7-11 days vs 12-18 days with Dagster  
✅ **Easy maintenance** - Update YAML files, not Python code  

## Quick Start (5 minutes)

### 1. Start Kestra

```bash
# From project root
mise kestra:up

# Or without mise:
docker-compose -f docker-compose.kestra.yml up -d
```

Wait 30-60 seconds for services to start.

### 2. Access UI

Open http://localhost:8080 in your browser.

### 3. Upload Example Workflow

**Via UI:**
1. Click "Flows" → "Create"
2. Copy content from `kestra-flows/rp-hevy-extraction.yml`
3. Paste and click "Save"

**Via CLI:**
```bash
curl -X POST http://localhost:8080/api/v1/flows \
  -H "Content-Type: application/yaml" \
  --data-binary @kestra-flows/rp-hevy-extraction.yml
```

### 4. Configure Secrets

In Kestra UI, go to "Secrets" and add:
- `RP_AUTH_TOKEN` - Your RP authentication token
- `HEVY_API_KEY` - Your Hevy API key
- `SLACK_WEBHOOK_URL` - (Optional) For notifications

### 5. Test Run

1. Go to "Flows" → `workouts.pipeline` → `rp-hevy-extraction`
2. Click "Execute"
3. Monitor progress in real-time
4. View logs and outputs

## Common Commands

```bash
# Start Kestra
mise kestra:up

# Stop Kestra
mise kestra:down

# View logs
mise kestra:logs

# Restart Kestra
mise kestra:restart

# Reset everything (removes all data)
mise kestra:reset

# Open UI in browser
mise kestra:open
```

## Workflow Overview

The example workflow (`kestra-flows/rp-hevy-extraction.yml`) orchestrates:

1. **Extract RP Workouts** → API call to RP Hypertrophy
2. **Extract Hevy Workouts** → API call to Hevy
3. **Match Exercises** → Semantic embeddings for cross-platform matching
4. **Transform Data** → Polars transformations
5. **Generate Stats** → Summary metrics
6. **Notify** → Slack notification

**Scheduling:** Daily at 2 AM UTC (configurable in YAML)

## File Structure

```
project-root/
├── KESTRA_RESEARCH.md              # Full research & comparison
├── KESTRA_QUICKSTART.md            # This file
├── docker-compose.kestra.yml       # Docker setup
├── .mise.toml                      # Added kestra:* tasks
└── kestra-flows/
    ├── README.md                   # Detailed setup guide
    └── rp-hevy-extraction.yml     # Example workflow
```

## Key Concepts

### Tasks
Individual steps in a workflow (extract, transform, export, etc.)

```yaml
tasks:
  - id: my_task
    type: io.kestra.plugin.scripts.python.Script
    script: |
      print("Hello from Kestra!")
```

### Outputs & Inputs
Tasks produce output files that can be consumed by subsequent tasks:

```yaml
# Task 1: Produce output
outputFiles:
  - data.json

# Task 2: Consume output
inputFiles:
  data.json: "{{ outputs.task1.outputFiles['data.json'] }}"
```

### Triggers
Schedule or event-based execution:

```yaml
triggers:
  - id: daily
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 2 * * *"
```

### Secrets
Store credentials securely:

```yaml
env:
  API_KEY: "{{ secret('MY_API_KEY') }}"
```

## Customization Examples

### Change Schedule

Edit the `triggers` section:

```yaml
triggers:
  - id: hourly
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 * * * *"  # Every hour
```

### Add Cloud Storage Export

Uncomment cloud storage tasks in the workflow:

```yaml
# For AWS S3
- id: upload_to_s3
  type: io.kestra.plugin.aws.s3.Upload
  from: "{{ outputs.transform.outputFiles['export.csv'] }}"
  to: "s3://my-bucket/exports/data.csv"
```

### Change Notifications

Replace Slack with email:

```yaml
- id: notify
  type: io.kestra.plugin.notifications.mail.MailSend
  from: "kestra@example.com"
  to: "user@example.com"
  subject: "Export Complete"
  htmlTextContent: "<h1>Success!</h1>"
```

### Use Custom Docker Image

Build your own image:

```yaml
tasks:
  - id: my_task
    type: io.kestra.plugin.scripts.python.Script
    containerImage: my-custom-image:latest
```

## Comparison with Dagster

| Feature | Kestra | Dagster |
|---------|--------|---------|
| **Workflow Definition** | YAML | Python |
| **Code Refactoring** | Not required | Required |
| **Setup Time** | 5 minutes | Hours |
| **Learning Curve** | Low | Steep |
| **Docker Integration** | Native | Requires config |
| **Implementation** | 7-11 days | 12-18 days |

## Troubleshooting

### Kestra won't start
```bash
# Check Docker
docker --version

# Check ports
lsof -i :8080
lsof -i :5432

# View logs
mise kestra:logs
```

### Workflow not appearing
```bash
# Validate YAML
yamllint kestra-flows/rp-hevy-extraction.yml

# Re-upload
curl -X POST http://localhost:8080/api/v1/flows \
  -H "Content-Type: application/yaml" \
  --data-binary @kestra-flows/rp-hevy-extraction.yml
```

### Task failures
1. Click failed task in UI to view logs
2. Check Docker image is available: `docker pull <image>`
3. Verify secrets are configured
4. Check input files exist from previous tasks

### Reset database
```bash
mise kestra:reset  # Removes all data
mise kestra:up     # Start fresh
```

## Resources

| Resource | Link |
|----------|------|
| **Full Research** | [KESTRA_RESEARCH.md](KESTRA_RESEARCH.md) |
| **Setup Guide** | [kestra-flows/README.md](kestra-flows/README.md) |
| **Example Workflow** | [kestra-flows/rp-hevy-extraction.yml](kestra-flows/rp-hevy-extraction.yml) |
| **Kestra Docs** | https://kestra.io/docs |
| **Python Integration** | https://kestra.io/docs/how-to-guides/python |
| **Plugin Index** | https://kestra.io/plugins |
| **Community Slack** | https://kestra.io/slack |

## Next Steps

1. ✅ Start Kestra: `mise kestra:up`
2. ✅ Upload workflow: Copy `kestra-flows/rp-hevy-extraction.yml` to UI
3. ✅ Configure secrets: Add API tokens in Kestra UI
4. ✅ Test run: Execute workflow manually
5. ✅ Review logs: Check execution details
6. ✅ Customize: Modify YAML for your needs
7. ✅ Schedule: Set up cron triggers

## Support

- **Project questions**: Review [KESTRA_RESEARCH.md](KESTRA_RESEARCH.md)
- **Kestra questions**: https://kestra.io/docs or Slack
- **Issues**: https://github.com/kestra-io/kestra/issues

---

**Summary**: Kestra provides a simpler, faster path to orchestrated workflow execution for this project compared to Dagster. Start with the quick start above, then dive into the full research document for deeper understanding.
