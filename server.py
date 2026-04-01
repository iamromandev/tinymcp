import os

from dotenv import load_dotenv

load_dotenv()

from fastmcp import FastMCP
from fastmcp.server.auth.providers.auth0 import Auth0Provider

_base_url = os.environ.get("BASE_URL", "http://localhost:8000")
_auth_provider = os.environ.get("AUTH_PROVIDER", "auth0").lower().strip()

if _auth_provider == "clerk":
    from fastmcp.utilities.auth import parse_scopes

    from clerk_provider import ClerkAuthProvider

    _audience = os.environ.get("CLERK_AUDIENCE", "").strip() or None
    _verify_id = os.environ.get("CLERK_VERIFY_ID_TOKEN", "").lower() in (
        "1",
        "true",
        "yes",
    )
    _clerk_scopes_env = os.environ.get("CLERK_SCOPES", "").strip()
    _clerk_required_scopes = (
        parse_scopes(_clerk_scopes_env) if _clerk_scopes_env else None
    )
    auth = ClerkAuthProvider(
        config_url=os.environ["CLERK_CONFIG_URL"],
        client_id=os.environ["CLERK_CLIENT_ID"],
        client_secret=os.environ["CLERK_CLIENT_SECRET"],
        audience=_audience,
        base_url=_base_url,
        verify_id_token=_verify_id,
        required_scopes=_clerk_required_scopes,
    )
else:
    domain = os.environ["AUTH0_DOMAIN"]
    auth = Auth0Provider(
        config_url=f"https://{domain}/.well-known/openid-configuration",
        client_id=os.environ["AUTH0_CLIENT_ID"],
        client_secret=os.environ["AUTH0_CLIENT_SECRET"],
        audience=os.environ["AUTH0_AUDIENCE"],
        base_url=_base_url,
    )

mcp = FastMCP("TinyMCP", auth=auth)


@mcp.tool
def hello(name: str = "world", description: str | None = None) -> str:
    """Say hello to someone. Optional description adds context after the greeting."""
    msg = f"Hello, {name}!"
    if description:
        return f"{msg} {description}"
    return msg


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Welcome to TinyMCP, {name}!"


@mcp.resource("data://cities")
def list_cities() -> list[str]:
    """List supported cities."""
    return ["London", "Paris", "Tokyo"]


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
