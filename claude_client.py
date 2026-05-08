"""
Anthropic Claude reasoning interface.
Mirrors research._ask shape so the swap is mechanical.

Used for tasks that require analysis, not retrieval:
  - Daily sentiment analysis (research.run_daily_research)
  - Weekly prediction grading (research.grade_predictions)
  - Weekly narrative report (weekly_report.run_weekly_report)
"""
import json
import logging
import os

from anthropic import Anthropic

from config import CLAUDE_MODEL

logger = logging.getLogger(__name__)


def _client() -> Anthropic:
    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def reason(system: str, user: str, max_tokens: int) -> str:
    """Single Claude completion call. Returns raw text."""
    logger.info(f"Calling Claude ({CLAUDE_MODEL}) — max_tokens={max_tokens}")
    resp = _client().messages.create(
        model=CLAUDE_MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
    return "".join(parts)


def _parse_json(text: str) -> dict:
    """Strip markdown fences if present, then parse JSON.
    Identical logic to research._parse_json — duplicated to keep this module
    independent and avoid importing a private symbol across modules."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        end = -1 if lines[-1].strip() == "```" else len(lines)
        text = "\n".join(lines[1:end])
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(text[start:end])
    raise ValueError(f"No JSON found in Claude response: {text[:300]}")


def reason_json(system: str, user: str, max_tokens: int) -> dict:
    """Calls Claude, parses JSON from response, returns dict."""
    return _parse_json(reason(system, user, max_tokens))
