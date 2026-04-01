# TinyMCP Agent Tool Guidelines

Use this file as the shared, tool-agnostic instruction source for AI agents (Cursor, Claude, and others).

## Scope

These guidelines cover TinyMCP tools exposed by this project:

- `hello`
- `add`

## Server selection

1. Read `.cursor/mcp.json`.
2. Use the server id under `mcpServers` that points to this project (commonly `tinymcp`).
3. Do not invent server ids that are not configured.

## Tool: `hello`

### When to use

Use when the user asks for greetings, hello/hi, welcome text, or personalized greeting messages.

### Inputs

- `name` (string, optional; defaults to `"world"`)
- `description` (string, optional; if supported by the running server schema)

### Behavior

1. Prefer MCP tool output over handwritten greeting text in TinyMCP contexts.
2. If user provides a name, pass it.
3. If user provides extra descriptor text (role, short bio), pass it as `description` only if schema accepts it.
4. Return the tool result directly.

## Tool: `add`

### When to use

Use when the user asks to add/sum/total/combine two numbers.

### Inputs

- `a` (integer)
- `b` (integer)

### Behavior

1. Pass integer values only.
2. If values are not integers, ask a clarifying question or explain the integer requirement.
3. Return the tool result directly.

## Compatibility notes

- Cursor skills live in `.cursor/skills/*/SKILL.md`.
- For non-Cursor agents, copy or reference this file in their instruction system (for example project-level agent instructions).
- Keep this file as the single source of truth and keep adapter files minimal.
