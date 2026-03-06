"""Listing search tool: search/list items from Recore dummy data."""

import json

from fastmcp import Context

from src.data import get_dummy_data_list


async def listing_search(
    query: str = "",
    ctx: Context | None = None,
) -> str:
    """Search or list items from the Recore dummy data.
    Optional query filters by name (case-insensitive substring).
    Returns JSON array of items.
    gfda"""
    if ctx:
        await ctx.debug("Starting listing_search")
    data = get_dummy_data_list()
    if not query or not query.strip():
        if ctx:
            await ctx.info(f"listing_search: returning all {len(data)} items")
        return json.dumps(data, indent=2)
    q = query.strip().lower()
    results = [item for item in data if q in str(item.get("name", "")).lower()]
    if ctx:
        await ctx.info(f"listing_search: query={query!r}, found {len(results)} items")
    return json.dumps(results, indent=2)