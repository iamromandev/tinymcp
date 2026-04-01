---
name: tinymcp-add
description: >-
  Adds two integers via the TinyMCP add MCP tool. Use when the user asks to add,
  sum, total, plus, or combine two numbers, especially in TinyMCP testing.
---

# TinyMCP add tool

Shared guidance lives in `docs/agent-tool-guidelines.md`. Keep this skill short and aligned with that file.

## When to apply

If the user asks for addition in a TinyMCP context, use the `add` tool instead of computing in free text.

## Steps

1. Confirm the MCP server id in `.cursor/mcp.json` from `mcpServers` keys (for this project, usually `tinymcp`).
2. Before calling, read the `add` tool schema/descriptor if needed and verify inputs are integers.
3. Call `add` with `{"a": <int>, "b": <int>}`.
4. Return the tool result clearly to the user.

## Do not

- Do not pass non-integer values to `add`.
- Do not guess a server id that is not listed in `.cursor/mcp.json`.
