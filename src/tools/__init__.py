"""MCP tools package. Register all tools on a FastMCP instance."""

from fastmcp import FastMCP

from src.tools.ai_summarize import ai_summarize
from src.tools.hello import hello
from src.tools.listing_search import listing_search
from src.tools.user_elicitation import collect_user_info


def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the given FastMCP app."""
    mcp.tool(hello)
    mcp.tool(ai_summarize)
    mcp.tool(listing_search)
    mcp.tool(collect_user_info)
