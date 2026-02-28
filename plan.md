# RP Hypo to STRONG Exporter - Project Plan

## Overview

Open-source monorepo to extract workout data from the RP Hypo app and convert it to STRONG app import format. Uses a `uv` workspace with two packages: a CLI frontend (`click`) and a Dagster pipeline (all scraping, transformation, and export logic).

---

## Architecture

```
rp-to-strong/
├── pyproject.toml              # uv workspace root
├── .mise.toml                  # dev toolchain (Python version, env vars)
├── .python-version
├── packages/
│   ├── cli/                    # Click CLI - thin frontend
│   │   ├── pyproject.toml
│   │   └── src/
│   │       └── rp_to_strong_cli/
│   │           ├── __init__.py
│   │           └── main.py     # click commands
│   └── pipeline/               # Dagster - all business logic
│       ├── pyproject.toml
│       └── src/
│           └── rp_to_strong_pipeline/
│               ├── __init__.py
│               ├── definitions.py      # Dagster Definitions entry
│               ├── assets/
│               │   ├── extract.py      # RP Hypo API scraping
│               │   ├── transform.py    # Polars transformations
│               │   └── export.py       # STRONG CSV generation
│               └── resources/
│                   ├── rp_client.py    # RP Hypo API client
│                   └── exercise_map.py # RP -> STRONG name mapping
└── README.md
```

### Communication: CLI <-> Dagster

The CLI does **not** contain business logic. It communicates with Dagster via:

1. **Dagster GraphQL API** (`dagster-graphql`) - trigger jobs, check run status, fetch asset materializations
2. **Dagster CLI subprocess calls** - as a fallback, wrap `dagster job execute` commands
3. The CLI can also read materialized outputs (CSV files) from a shared IO manager path

---

## Execution Blocks

> **Important**: The AI agent must complete each block, present the result, and **wait for explicit user confirmation** before proceeding to the next block.

---

### Block 1: Scaffold the Monorepo

**Goal**: Initialize the `uv` workspace with both packages, `mise` config, and basic project metadata.

**Steps**:
1. Create the root `pyproject.toml` with `uv` workspace members pointing to `packages/*`
2. Create `packages/cli/pyproject.toml` with `click` dependency and console script entry point
3. Create `packages/pipeline/pyproject.toml` with `dagster`, `dagster-webserver`, `polars`, `httpx` dependencies
4. Add CLI's dependency on the pipeline package (intra-workspace dep)
5. Create `.mise.toml` with Python version and any env var placeholders
6. Create `.python-version`
7. Run `uv sync` to verify the workspace resolves
8. Initialize git repo with `.gitignore`

**Checkpoint**: Both packages install cleanly, `uv run python -c "import click; import dagster"` works.

---

### Block 2: CLI Skeleton (Click)

**Goal**: Minimal CLI with placeholder commands that will later call Dagster.

**Steps**:
1. Create `rp_to_strong_cli/main.py` with a Click group and subcommands:
   - `rp-to-strong extract` - will trigger the extraction job
   - `rp-to-strong transform` - will trigger the transformation job
   - `rp-to-strong export` - will trigger the full pipeline (extract + transform + export)
   - `rp-to-strong status` - will query Dagster for run status
2. Wire the console script entry point (`rp-to-strong = "rp_to_strong_cli.main:cli"`)
3. Verify: `uv run rp-to-strong --help` prints the command tree

**Checkpoint**: CLI installs and responds to `--help` on all subcommands.

---

### Block 3: Dagster Project Foundation

**Goal**: Working Dagster project with empty asset stubs and the Definitions object.

**Steps**:
1. Create `definitions.py` with the `Definitions` object
2. Create asset stubs in `assets/`:
   - `extract.py`: `@asset def raw_rp_data()` - returns empty dict placeholder
   - `transform.py`: `@asset def transformed_workouts(raw_rp_data)` - returns empty Polars DataFrame
   - `export.py`: `@asset def strong_csv(transformed_workouts)` - writes placeholder CSV
3. Register all assets in `Definitions`
4. Verify: `uv run dagster dev` launches the webserver and shows the asset graph

**Checkpoint**: Dagster UI shows the 3-asset dependency graph: `raw_rp_data -> transformed_workouts -> strong_csv`.

---

### Block 4: RP Hypo Extraction Logic

**Goal**: Implement the actual API scraping inside Dagster assets/resources.

**Steps**:
1. Create `resources/rp_client.py` - a Dagster `ConfigurableResource` that:
   - Accepts auth token / credentials as config
   - Uses `httpx` to call RP Hypo API endpoints
   - Handles pagination if needed
2. Implement `assets/extract.py`:
   - Use AI browser automation (Playwright + LLM) to discover API paths and intercept auth tokens
   - OR accept a manually-provided JWT/token via config
   - Fetch full workout history as raw JSON
   - Store as a Dagster asset (JSON file via IO manager)
3. Add the RP client resource to `Definitions`

**Checkpoint**: Running the extract asset produces a JSON dump of real RP workout data.

---

### Block 5: Transformation Layer (Polars)

**Goal**: Parse raw RP JSON into the STRONG schema using Polars.

**Steps**:
1. Create `resources/exercise_map.py`:
   - Dictionary mapping RP exercise names -> STRONG exact names
   - Flag unmapped exercises so the user can resolve them
2. Implement `assets/transform.py`:
   - Parse RP JSON into a Polars DataFrame
   - Normalize fields: dates, exercise names, sets, reps, load, RIR -> RPE
   - Apply the exercise mapping table
   - Sort chronologically (oldest first - **critical** for STRONG import)
3. Output a clean Polars DataFrame matching STRONG schema

**Checkpoint**: Transformation produces a Polars DataFrame with correct column names and sorted dates.

---

### Block 6: STRONG CSV Export

**Goal**: Generate the final CSV that STRONG accepts.

**Steps**:
1. Implement `assets/export.py`:
   - Enforce exact STRONG headers: `Date`, `Workout Name`, `Exercise Name`, `Set Order`, `Weight`, `Weight Unit`, `Reps`, `RPE`, `Distance`, `Distance Unit`, `Seconds`, `Notes`, `Workout Notes`, `Workout Duration`
   - Format dates as `YYYY-MM-DD HH:MM:SS`
   - Validate no nulls in required fields
   - Write CSV to output path
2. Add Dagster asset check or `@asset_check` to validate the output schema

**Checkpoint**: CSV file imports successfully into the STRONG app.

---

### Block 7: Wire CLI to Dagster

**Goal**: CLI commands trigger real Dagster jobs and report results.

**Steps**:
1. Implement Dagster GraphQL client helper in the CLI package
2. `rp-to-strong extract` -> triggers extract asset materialization
3. `rp-to-strong transform` -> triggers transform asset materialization
4. `rp-to-strong export` -> triggers full pipeline materialization
5. `rp-to-strong status` -> queries latest run status and prints results
6. Add `--output` flag to `export` to copy the final CSV to a user-specified path
7. Add progress indicators (click `echo` / spinners) while waiting for Dagster runs

**Checkpoint**: Full end-to-end flow works from CLI: `rp-to-strong export --output ./my-workouts.csv`

---

## Tech Stack Summary

| Component       | Technology                         |
| --------------- | ---------------------------------- |
| Monorepo        | `uv` workspaces                    |
| Dev environment | `mise` (Python version, env vars)  |
| CLI             | `click`                            |
| Orchestrator    | Dagster (Software-Defined Assets)  |
| Data transform  | Polars (**no Pandas**)             |
| HTTP client     | `httpx`                            |
| Browser auto    | Playwright (optional, for Phase 4) |

## Constraints

- **Polars only** - no Pandas anywhere in the codebase
- **CLI is a thin frontend** - zero business logic, only Dagster communication
- **Step-by-step execution** - agent pauses after each block for user review
- **Chronological sort** - STRONG import fails or truncates on reverse-ordered data
- **Exercise name mapping** - must match STRONG's exact names to avoid custom exercise pollution
