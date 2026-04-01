# TinyMCP

A simple MCP server using streamable HTTP transport, secured with **Auth0** or **Clerk** (OAuth/OIDC upstream via FastMCP).

## Setup

```bash
uv sync
cp .env.example .env
```

### Auth0 Configuration

1. Create an [Auth0](https://auth0.com) account and tenant
2. Create a **Regular Web Application** — copy the Client ID and Client Secret
3. Create an **API** — copy the Audience (identifier)
4. Enable **Dynamic Client Registration** on your tenant (Settings > Advanced > OAuth)
5. Fill in your `.env`:

```
AUTH0_DOMAIN=your-tenant.us.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_AUDIENCE=your-api-audience
BASE_URL=http://localhost:8000
```

See `.env.example` for the full list.

Set **`AUTH_PROVIDER=auth0`** (default) or **`AUTH_PROVIDER=clerk`**.

### Clerk (Clerk as IdP)

1. In [Clerk Dashboard → OAuth applications](https://dashboard.clerk.com/~/oauth-applications), create an app and copy **Discovery URL**, **Client ID**, and **Client Secret**.
2. Under **Scopes** for that OAuth app, enable only what you need. This server defaults to requesting **`profile`** and **`email`** (no `openid`), which matches many Clerk apps. If you enable **`openid`** in the Dashboard (for OIDC / `id_token`), set `CLERK_SCOPES=openid profile email` in `.env` so the requested scopes match. See [How Clerk implements OAuth](https://clerk.com/docs/guides/configure/auth-strategies/oauth/how-clerk-implements-oauth).
3. In `.env`: `AUTH_PROVIDER=clerk`, `CLERK_CONFIG_URL`, `CLERK_CLIENT_ID`, `CLERK_CLIENT_SECRET`, and `BASE_URL`. Optional: `CLERK_SCOPES` (space- or comma-separated) to override requested scopes exactly.
4. Add the FastMCP callback to the Clerk app’s redirect URIs (same host/port as `BASE_URL`), e.g. `http://localhost:8000/auth/callback`, plus Cursor’s `cursor://anysphere.cursor-mcp/oauth/callback` if required by your setup.
5. If Clerk’s **access token** is opaque, set `CLERK_VERIFY_ID_TOKEN=true` so validation uses the OIDC **id_token** (JWT). That requires the **`openid`** scope on the Clerk OAuth app. See [Clerk as OIDC IdP](https://clerk.com/docs/advanced-usage/clerk-idp).

**`invalid_scope` / “not allowed to request scope `openid`”:** Your OAuth app was not created with the `openid` scope. Either edit the app in the Dashboard and add **`openid`**, then set `CLERK_SCOPES=openid profile email`, or leave `openid` off the app and do not request it (defaults `profile email` only).

**Do you need a Machine-to-Machine (M2M) app?** No — Cursor and MCP Inspector use interactive login (authorization code + PKCE). Use one **Regular Web Application** for your Client ID/Secret. M2M is only optional if you want **client-credentials** tokens for scripts or `curl` tests, not for Cursor.

### OIDC discovery 404 (`/.well-known/openid-configuration`)

That URL must return JSON in a browser. If you see **404**:

1. In Auth0: **Settings → General → Domain** — copy the value exactly into `.env` as **`AUTH0_DOMAIN`** (no `https://`). Open `https://<AUTH0_DOMAIN>/.well-known/openid-configuration` in a browser; it must return JSON, not 404.
2. If you use a **custom domain**, put that hostname in **`AUTH0_DOMAIN`** instead.

## Connect from Cursor (OAuth)

Cursor uses **Streamable HTTP** + **OAuth** for remote MCP. Your TinyMCP server must be running (`uv run python server.py`).

### Important: do **not** put Auth0 credentials in `mcp.json`

FastMCP’s OAuth proxy first acts as its **own** authorization server for MCP clients. Cursor must **dynamically register** with your server and get an **MCP client ID** (stored by FastMCP). That ID is **not** your Auth0 application’s Client ID.

If you add Cursor’s **`auth`** block with `AUTH0_CLIENT_ID` / `AUTH0_CLIENT_SECRET`, Cursor sends Auth0’s app id to `/authorize`, and FastMCP responds with **“Client Not Registered”** — that id was never registered on the MCP server.

**Use a URL-only entry** (see `.cursor/mcp.json.example`):

```json
{
  "mcpServers": {
    "tinymcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Then Cursor discovers OAuth metadata, calls **`/register`** on FastMCP, and completes the browser flow through FastMCP → Auth0.

If you previously used static `auth`, remove it, restart Cursor, and clear stale MCP auth (e.g. **Command Palette → sign out / remove** MCP or cached OAuth for this server) so Cursor registers again.

### 1. Auth0 application (same app as the server)

Use the **Regular Web Application** whose Client ID/Secret are already in **`.env`** (server-side only).

1. **Applications → your app → Settings**
2. Under **Allowed Callback URLs**, include **both**:
   - `http://localhost:8000/auth/callback` — FastMCP OAuth callback (change host/port if `BASE_URL` differs)
   - `cursor://anysphere.cursor-mcp/oauth/callback` — Cursor’s fixed redirect

3. Save changes.

(Optional) Under **Advanced Settings → Grant Types**, ensure **Authorization Code** is enabled.

### 2. Cursor `mcp.json`

- **Project:** `.cursor/mcp.json`  
- **Global:** `~/.cursor/mcp.json`

```bash
cp .cursor/mcp.json.example .cursor/mcp.json
```

### 3. Authorize in Cursor

1. **Cursor Settings → Features → MCP** (or **Cmd+Shift+J** → MCP)
2. Ensure **tinymcp** is enabled
3. When prompted, complete login in the browser (via FastMCP → Auth0)

If connection fails, open **Output → MCP** for errors.

### Scopes

Adjust `scopes` in `mcp.json` if your Auth0 API defines custom scopes (must match what the API allows).

## Run

```bash
uv run python server.py
```

The server starts at `http://localhost:8000/mcp`.

## Tools

- **hello** — Say hello to someone
- **add** — Add two numbers together

## Generic AI instructions (cross-client)

Cursor skills are Cursor-specific. For a generic setup that also works with other agents, keep shared tool instructions in:

- `docs/agent-tool-guidelines.md`

Then:

- Cursor: keep lightweight adapters in `.cursor/skills/*/SKILL.md` that reference the shared doc.
- Other agents (for example Claude): copy/reference `docs/agent-tool-guidelines.md` in their own project instruction system.

## Other clients

```bash
# Claude Code
claude mcp add --transport http tinymcp http://localhost:8000/mcp

# MCP Inspector (OAuth flow depends on client support)
npx -y @modelcontextprotocol/inspector
```
