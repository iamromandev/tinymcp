"""User elicitation tool: collect user info via interactive prompts."""

from dataclasses import dataclass

from fastmcp import Context


@dataclass
class UserInfo:
    """User information collected via elicitation."""

    name: str
    age: int


async def collect_user_info(ctx: Context) -> str:
    """Collect user information through interactive prompts (name and age)."""
    await ctx.info("Requesting user information via elicitation")
    result = await ctx.elicit(
        message="Please provide your information (name and age)",
        response_type=UserInfo,
    )
    if result.action == "accept":
        user = result.data
        await ctx.info(f"User provided: name={user.name}, age={user.age}")
        return f"Hello {user.name}, you are {user.age} years old."
    if result.action == "decline":
        await ctx.info("User declined to provide information")
        return "Information not provided."
    # cancel
    await ctx.info("User cancelled the operation")
    return "Operation cancelled."
