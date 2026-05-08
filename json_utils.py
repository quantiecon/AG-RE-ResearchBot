"""
Shared JSON utilities.
Single source of truth for the fence-stripping JSON parser used by both
the Perplexity (research.py) and Claude (claude_client.py) reasoning paths.
"""
import json


def parse_json(text: str) -> dict:
    """Strip markdown fences if present, then parse JSON."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        end = -1 if lines[-1].strip() == "```" else len(lines)
        text = "\n".join(lines[1:end])
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(text[start:end])
    raise ValueError(f"No JSON found in response: {text[:300]}")
