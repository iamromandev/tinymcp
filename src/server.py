"""FastMCP server with a hello tool, loguru logging, and pydantic-settings."""

from fastmcp import FastMCP
from loguru import logger

from src.tools import register_tools


def create_mcp() -> FastMCP:
    """Build the FastMCP app with settings and tools."""
    mcp = FastMCP("Tiny MCP")
    register_tools(mcp)
    logger.info("MCP server created: Tiny MCP")
    return mcp


mcp = create_mcp()


def main() -> None:
    """Entrypoint for running the server (stdio by default)."""
    mcp.run()


if __name__ == "__main__":
    main()
