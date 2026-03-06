"""MCP client that connects to the Tiny MCP server via stdio and calls tools."""

import asyncio
import os
import sys

from fastmcp import Client
from fastmcp.client.logging import LogMessage
from fastmcp.client.transports import StdioTransport
from loguru import logger

from src.lib import project_root, tool_result_text

# Map MCP log levels to loguru level names.
LOGGING_LEVEL_MAP = {
    "DEBUG": "DEBUG",
    "INFO": "INFO",
    "NOTICE": "INFO",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
    "CRITICAL": "CRITICAL",
    "ALERT": "CRITICAL",
    "EMERGENCY": "CRITICAL",
}


def _read_input(prompt: str) -> str:
    """Read one line from stdin (used in executor to avoid blocking)."""
    print(prompt, end="", flush=True)
    return input().strip()


async def elicitation_handler(
    message: str,
    response_type: type | None,
    params: object,
    context: object,
) -> dict:
    """Respond to server elicitation by reading from stdin (e.g. name and age)."""
    logger.info("Elicitation request: {}", message)
    sys.stderr.write(f"{message}\n")
    sys.stderr.flush()
    loop = asyncio.get_event_loop()
    name = await loop.run_in_executor(None, lambda: _read_input("Name: "))
    age_str = await loop.run_in_executor(None, lambda: _read_input("Age: "))
    try:
        age = int(age_str)
    except ValueError:
        age = 0
    return {"name": name or "Unknown", "age": age}


async def log_handler(message: LogMessage) -> None:
    """Forward MCP server logs to loguru."""
    data = message.data
    if isinstance(data, dict):
        msg = data.get("msg", data)
        extra = data.get("extra")
    else:
        msg = data
        extra = None
    level = LOGGING_LEVEL_MAP.get(
        (message.level or "info").upper(),
        "INFO",
    )
    if extra:
        logger.bind(**extra).log(level, str(msg))
    else:
        logger.log(level, str(msg))


def create_client() -> Client:
    """Build a client that spawns the server as a subprocess (stdio)."""
    root = project_root()
    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "src.server"],
        cwd=str(root),
        env=os.environ.copy(),  # inherit so subprocess finds src package
    )
    return Client(
        transport,
        name="tinymcp-client",
        log_handler=log_handler,
        elicitation_handler=elicitation_handler,
    )


# Default arguments for each known tool when calling from the client.
# collect_user_info prompts for name and age via stdin.
DEFAULT_TOOL_ARGS: dict[str, dict] = {
    "hello": {"name": "Tiny MCP"},
    "ai_summarize": {
        "text": "First sentence here. Second sentence there. Third one. Fourth. Fifth.",
        "max_sentences": 2,
    },
    "listing_search": {"query": "Item"},
    "collect_user_info": {},
}


async def run_client() -> None:
    """Connect to the server, list tools, and call each tool that has default args."""
    client = create_client()
    async with client:
        info = await client.initialize()
        server_name = info.serverInfo.name if info.serverInfo else "unknown"
        logger.info("Connected to {}", server_name)

        tools = await client.list_tools()
        logger.info("Tools ({}): {}", len(tools), [t.name for t in tools])

        for tool in tools:
            args = DEFAULT_TOOL_ARGS.get(tool.name)
            if args is None:
                logger.debug("Skipping tool (no default args): {}", tool.name)
                continue
            result = await client.call_tool(tool.name, args)
            if result.is_error:
                logger.error("{} error: {}", tool.name, result.content)
            else:
                out = tool_result_text(result)
                logger.info("{} result: {}", tool.name, out)


def main() -> None:
    """Entrypoint for running the client."""
    try:
        asyncio.run(run_client())
    except Exception as e:
        logger.exception("Client failed: {}", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
