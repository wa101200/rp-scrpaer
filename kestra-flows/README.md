# Kestra Setup Guide

This directory contains Kestra workflow orchestration files as an alternative to Dagster for the rp-to-hevy project.

## What's Included

```
kestra-flows/
├── rp-hevy-extraction.yml    # Main workflow for RP + Hevy data extraction
└── README.md                  # This file
```

## Quick Start

### 1. Start Kestra

From the project root:

```bash
# Start Kestra and PostgreSQL
docker-compose -f docker-compose.kestra.yml up -d

# Wait for services to be ready (30-60 seconds)
docker-compose -f docker-compose.kestra.yml logs -f kestra

# Access the UI at http://localhost:8080
```

### 2. Upload Your First Flow

**Option A: Via UI**
1. Open http://localhost:8080
2. Go to "Flows" → "Create"
3. Copy/paste the content from `rp-hevy-extraction.yml`
4. Click "Save"

**Option B: Via API**
```bash
curl -X POST http://localhost:8080/api/v1/flows \
  -H "Content-Type: application/yaml" \
  --data-binary @kestra-flows/rp-hevy-extraction.yml
```

**Option C: Via mise** (recommended)
```bash
# If added to .mise.toml tasks
mise kestra:deploy-flows
```

### 3. Configure Secrets

Add your API credentials in the Kestra UI:

1. Go to "Secrets" in the sidebar
2. Add the following secrets:
   - `RP_AUTH_TOKEN` - Your RP Hypertrophy authentication token
   - `HEVY_API_KEY` - Your Hevy API key
   - `SLACK_WEBHOOK_URL` - (Optional) Slack webhook for notifications

### 4. Test the Flow

**Manual Execution:**
1. Go to "Flows" → `workouts.pipeline` → `rp-hevy-extraction`
2. Click "Execute"
3. Provide input values (or use configured secrets)
4. Monitor execution in real-time

**View Logs:**
- Click on any task to see its logs
- Download output files from the "Outputs" tab

## Workflow Overview

The `rp-hevy-extraction.yml` flow orchestrates:

1. **Extract RP Workouts** - Pulls data from RP Hypertrophy API
2. **Extract Hevy Workouts** - Pulls data from Hevy API  
3. **Match Exercises** - Uses semantic embeddings to match exercises across platforms
4. **Transform Data** - Normalizes and transforms with Polars
5. **Generate Stats** - Creates summary statistics
6. **Notify** - Sends Slack notification on completion

## Scheduling

The flow is configured to run **daily at 2 AM UTC**. To modify:

```yaml
triggers:
  - id: daily_extraction
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 2 * * *"  # Change this cron expression
    timezone: UTC
```

Common cron patterns:
- Every hour: `0 * * * *`
- Every 6 hours: `0 */6 * * *`
- Every Monday at 9 AM: `0 9 * * 1`
- Twice daily: `0 2,14 * * *`

## Customization

### Add Cloud Storage Export

Uncomment the cloud storage task in the YAML:

**For Google Cloud Storage:**
```yaml
- id: upload_to_gcs
  type: io.kestra.plugin.gcp.gcs.Upload
  from: "{{ outputs.transform_workouts.outputFiles['workouts_export.csv'] }}"
  to: "gs://my-bucket/exports/workouts_{{ execution.startDate | date('yyyy-MM-dd') }}.csv"
  serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}"
```

**For AWS S3:**
```yaml
- id: upload_to_s3
  type: io.kestra.plugin.aws.s3.Upload
  from: "{{ outputs.transform_workouts.outputFiles['workouts_export.csv'] }}"
  to: "s3://my-bucket/exports/workouts_{{ execution.startDate | date('yyyy-MM-dd') }}.csv"
  accessKeyId: "{{ secret('AWS_ACCESS_KEY_ID') }}"
  secretKeyId: "{{ secret('AWS_SECRET_ACCESS_KEY') }}"
  region: us-east-1
```

### Customize Notifications

The flow includes Slack notifications. To use email instead:

```yaml
- id: notify_success
  type: io.kestra.plugin.notifications.mail.MailSend
  from: "kestra@example.com"
  to: "user@example.com"
  subject: "Workout Export Complete"
  htmlTextContent: |
    <h2>Workout data extraction completed successfully!</h2>
    <p><strong>Execution ID:</strong> {{ execution.id }}</p>
    <p><strong>Date:</strong> {{ execution.startDate }}</p>
```

### Use Custom Docker Images

The flow uses pre-built images from GitHub Container Registry:
```yaml
containerImage: ghcr.io/wa101200/rp-scrpaer/cli:latest
```

To use locally built images:
```yaml
containerImage: rp-to-strong-cli:latest
```

## Monitoring

### View Execution History
- UI: "Executions" sidebar
- Shows all runs with status, duration, outputs

### Check Task Logs
- Click any execution → Click any task
- Real-time streaming logs
- Download full logs as text file

### Metrics & Statistics
- View execution duration trends
- Task success/failure rates
- Resource usage (if monitoring enabled)

## Troubleshooting

### Flow not showing up
```bash
# Check Kestra logs
docker-compose -f docker-compose.kestra.yml logs kestra

# Verify flow is valid YAML
yamllint kestra-flows/rp-hevy-extraction.yml

# Re-upload flow
curl -X POST http://localhost:8080/api/v1/flows \
  -H "Content-Type: application/yaml" \
  --data-binary @kestra-flows/rp-hevy-extraction.yml
```

### Task failures
1. Check task logs in UI
2. Verify Docker image is available: `docker pull ghcr.io/wa101200/rp-scrpaer/cli:latest`
3. Check secrets are configured correctly
4. Verify input files from previous tasks exist

### Database connection issues
```bash
# Check PostgreSQL is running
docker-compose -f docker-compose.kestra.yml ps

# Check database logs
docker-compose -f docker-compose.kestra.yml logs postgres

# Restart services
docker-compose -f docker-compose.kestra.yml restart
```

### Reset everything
```bash
# Stop and remove all containers + data
docker-compose -f docker-compose.kestra.yml down -v

# Start fresh
docker-compose -f docker-compose.kestra.yml up -d
```

## Comparison with CLI

| Feature | CLI | Kestra |
|---------|-----|--------|
| **Execution** | Manual | Scheduled / Triggered |
| **Monitoring** | Terminal output | Web UI dashboard |
| **Retries** | Manual | Automatic with backoff |
| **Notifications** | None | Slack, Email, Webhooks |
| **Logs** | Stdout/stderr | Persistent, queryable |
| **Outputs** | Local files | Cloud storage integration |
| **Dependencies** | Sequential execution | DAG-based parallelization |

## Advanced Usage

### Parallel Extraction

Extract RP and Hevy data in parallel:

```yaml
tasks:
  - id: extract_both
    type: io.kestra.plugin.core.flow.Parallel
    tasks:
      - id: extract_rp_workouts
        # ... RP extraction ...
      
      - id: extract_hevy_workouts
        # ... Hevy extraction ...
```

### Conditional Execution

Only run certain tasks if conditions are met:

```yaml
- id: upload_to_cloud
  type: io.kestra.plugin.core.flow.If
  condition: "{{ execution.trigger.type == 'io.kestra.plugin.core.trigger.Schedule' }}"
  then:
    - id: upload
      type: io.kestra.plugin.gcp.gcs.Upload
      # ...
```

### Sub-flows

Break complex workflows into modular sub-flows:

```yaml
- id: call_embedding_subflow
  type: io.kestra.plugin.core.flow.Subflow
  namespace: workouts.common
  flowId: generate-embeddings
  inputs:
    data: "{{ outputs.extract_rp_workouts.outputFiles['rp_workouts.json'] }}"
```

## Resources

- **Kestra Documentation**: https://kestra.io/docs
- **Flow Examples**: https://github.com/kestra-io/examples
- **Python Plugin Docs**: https://kestra.io/docs/how-to-guides/python
- **Plugin Index**: https://kestra.io/plugins
- **Community Slack**: https://kestra.io/slack

## Migrating from Dagster

If you previously used Dagster, here's the mapping:

| Dagster | Kestra |
|---------|--------|
| `@asset` | `tasks:` in YAML |
| `@job` | `id: flow-name` |
| `@schedule` | `triggers:` |
| IOManager | `outputFiles:` + `inputFiles:` |
| Resource | `env:` or Docker `containerImage` |
| Sensor | `triggers:` with event type |

See `KESTRA_RESEARCH.md` for detailed comparison and migration guide.

## Support

For questions or issues:
1. Check the [Kestra docs](https://kestra.io/docs)
2. Search [GitHub issues](https://github.com/kestra-io/kestra/issues)
3. Ask in [Slack community](https://kestra.io/slack)
4. Review `KESTRA_RESEARCH.md` in project root
