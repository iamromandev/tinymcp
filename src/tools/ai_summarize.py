"""AI summarize tool."""

import re

from fastmcp import Context


async def ai_summarize(
    text: str,
    max_sentences: int = 3,
    ctx: Context | None = None,
) -> str:
    """Summarize the given text by returning up to the first max_sentences sentences."""
    if ctx:
        await ctx.debug("Starting ai_summarize")
    if not text or not text.strip():
        if ctx:
            await ctx.warning("Empty text provided")
        return ""
    # Split on sentence-ending punctuation followed by space or end
    normalized = re.sub(r"\s+", " ", text.strip())
    sentences = re.split(r"(?<=[.!?])\s+", normalized)
    sentences = [s.strip() for s in sentences if s.strip()]
    summary = " ".join(sentences[:max_sentences])
    if ctx:
        await ctx.info(
            f"ai_summarize tool called: input_len={len(text)}, "
            f"max_sentences={max_sentences}, output_len={len(summary)}"
        )
    return summary
