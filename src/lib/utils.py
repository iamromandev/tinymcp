"""Shared helper functions."""

from pathlib import Path


def tool_result_text(result) -> str:
    """Extract text from a tool call result (content or data)."""
    if result.data is not None:
        return str(result.data)
    parts = [
        c.text
        for c in result.content
        if getattr(c, "text", None) is not None
    ]
    return "\n".join(parts) if parts else str(result.content)


def project_root() -> Path:
    """Project root (parent of src/)."""
    return Path(__file__).resolve().parent.parent.parent
