# Hello MCP

A minimal [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server built with [FastMCP](https://fastmcp.wiki/), [uv](https://docs.astral.sh/uv/), [loguru](https://github.com/Delgan/loguru), and [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

## Features

- **FastMCP** – MCP server with a `hello` tool
- **uv** – Fast Python package and project management
- **loguru** – Structured logging
- **pydantic-settings** – Config from env (prefix `MCP_`) and `.env`
- **Docker** – Multi-stage image with uv

## Setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/). From the project root:

```bash
uv sync
```

Optional: create a lockfile for reproducible installs and Docker:

```bash
uv lock
```

## Run locally

**stdio (default, for MCP clients like Claude Desktop):**

```bash
uv run python -m src.server
```

Or with the FastMCP CLI (use the file path, run from project root):

```bash
uv run fastmcp run src/server.py:mcp
```

**HTTP (for remote clients):**

```bash
uv run fastmcp run src/server.py:mcp --transport http --port 8000
```

**Run the client (spawns server via stdio, lists tools, calls `hello`):**

```bash
uv run python -m src.client
```

## Configuration

Settings are loaded from the environment and optional `.env`. Prefix: `MCP_`.

| Variable     | Default    | Description   |
|-------------|------------|---------------|
| `MCP_APP_NAME` | Hello MCP | Server name   |
| `MCP_LOG_LEVEL` | INFO    | Log level     |

Example `.env`:

```env
MCP_APP_NAME=My MCP
MCP_LOG_LEVEL=DEBUG
```

## Docker

Build:

```bash
docker build -t hello-mcp .
```

Run (stdio):

```bash
docker run -i --rm hello-mcp
```

Run with env and HTTP:

```bash
docker run --rm -p 8000:8000 -e MCP_LOG_LEVEL=DEBUG hello-mcp \
  fastmcp run src/server.py:mcp --transport http --port 8000
```

**Docker Compose (HTTP server on port 8000):**

```bash
docker compose up -d
# Server at http://localhost:8000
docker compose down
```

Optional env in `.env`: `MCP_APP_NAME`, `MCP_LOG_LEVEL`.

Note: The image runs `python -m src.server`; no console script is required.

For a reproducible image, commit `uv.lock` and ensure the Dockerfile uses `uv sync --locked` (the Dockerfile supports both with and without a lockfile).
