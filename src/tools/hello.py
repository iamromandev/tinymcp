"""Hello tool."""

from fastmcp import Context


async def hello(name: str = "World", ctx: Context | None = None) -> str:
    """Say hello to the given name."""
    msg = f"Hello, {name}!"
    if ctx:
        await ctx.info(f"hello tool called name: {name}, result: {msg}")
    return msg
