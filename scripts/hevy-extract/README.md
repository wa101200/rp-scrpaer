# hevy-extract

Extract the OpenAPI spec from [Hevy API docs](https://api.hevyapp.com/docs/) into a JSON file.

## How it works

The Hevy API docs page loads a `swagger-ui-init.js` script that contains the full OpenAPI spec embedded inline. Rather than parsing the JS as text, the extractor evaluates it in a sandbox with mocked Swagger UI globals (`window`, `SwaggerUIBundle`, etc.). When the script calls `SwaggerUIBundle(opts)`, the mock intercepts the call and captures `opts.spec` — the OpenAPI document. This approach is resilient to formatting changes in the script since it relies on runtime behavior, not string patterns.

## Prerequisites

- [Bun](https://bun.sh/) >= 1.0

## Install

```sh
bun install
```

## Usage

```sh
bun run start
```

This fetches the spec and writes it to `openapi.json`.

### Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--url` | `-u` | `https://api.hevyapp.com/docs/swagger-ui-init.js` | URL of the swagger-ui-init.js file |
| `--output` | `-o` | `openapi.json` | Output file path |

### Examples

```sh
# Default — extract to openapi.json
bun run start

# Custom output path
bun run extract.ts extract -o spec.json

# Custom source URL
bun run extract.ts extract -u https://example.com/swagger-ui-init.js

# Show help
bun run extract.ts extract --help
```

## Scripts

| Script | Description |
|--------|-------------|
| `bun run start` | Run the extractor |
| `bun run lint` | Type-check with `tsc --noEmit` |
| `bun run check` | Alias for `lint` |
| `bun run build` | Compile a standalone binary to `dist/hevy-extract` with bytecode + minify |

### Build

```sh
bun run build
./dist/hevy-extract extract
```

Produces a single self-contained executable using [Bun's bytecode compilation](https://bun.sh/docs/bundler/bytecode) for faster startup.
