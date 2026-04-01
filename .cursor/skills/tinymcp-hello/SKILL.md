---
name: tinymcp-hello
description: >-
  Delivers personalized greetings via the TinyMCP hello MCP tool. Use when the
  user asks for a greeting, hello, hi, welcome message, or says hello using a
  name; when testing TinyMCP; or when a response should come from the server
  rather than improvising text.
---

# TinyMCP hello tool

Shared guidance lives in `docs/agent-tool-guidelines.md`. Keep this skill short and aligned with that file.

## When to apply

If the user wants a greeting **and** the TinyMCP server is relevant (this repo, MCP configured, or they name TinyMCP / the `hello` tool), satisfy the request with the **`hello`** tool instead of only replying in free text.

## Steps

1. Confirm the MCP server id: read `.cursor/mcp.json` → `mcpServers` keys (e.g. `tinymcp`). Use that identifier with the MCP tool caller in this environment.
2. Before calling: read the tool schema/descriptor for `hello` under the MCP file-system hints for this project if needed; required parameter is `name` (string; server default is `world`).
3. Call **`hello`** with `{"name": "<user's name or requested name>"}`. If no name is given, use `"world"` or omit per schema defaults.
4. Return the tool result to the user. Optionally mention the related resource `greeting://{name}` only if they ask for the resource-style wording.

## Do not

- Substitute a handwritten `Hello, X!` when the user clearly wants the MCP-backed greeting in a TinyMCP context.
- Guess the server id: always align with `.cursor/mcp.json` for this workspace.
