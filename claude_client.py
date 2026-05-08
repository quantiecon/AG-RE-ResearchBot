"""
Anthropic Claude reasoning interface.
Mirrors research._ask shape so the swap is mechanical.

Used for tasks that require analysis, not retrieval:
  - Daily sentiment analysis (research.run_daily_research)
  - Weekly prediction grading (research.grade_predictions)
  - Weekly narrative report (weekly_report.run_weekly_report)
"""
import logging
import os

from anthropic import Anthropic

from config import CLAUDE_MODEL
from json_utils import parse_json

logger = logging.getLogger(__name__)


def _client() -> Anthropic:
    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def reason(system: str, user: str, max_tokens: int, model: str | None = None) -> str:
    """Single Claude completion call. Returns raw text.
    `model` overrides the default CLAUDE_MODEL for this call."""
    chosen = model or CLAUDE_MODEL
    logger.info(f"Calling Claude ({chosen}) — max_tokens={max_tokens}")
    resp = _client().messages.create(
        model=chosen,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
    return "".join(parts)


def reason_json(system: str, user: str, max_tokens: int, model: str | None = None) -> dict:
    """Calls Claude, parses JSON from response, returns dict."""
    return parse_json(reason(system, user, max_tokens, model=model))


_TRANSLATE_SYSTEM = (
    "You are a professional translator specializing in real estate and finance. "
    "Translate the user's message into Simplified Chinese (简体中文). "
    "Preserve all formatting exactly: line breaks, separator lines (━━━), "
    "bullet markers (•), emoji, and the overall structure. Translate the "
    "section headers and labels (e.g. \"MARKET OVERVIEW\", \"SENTIMENT\") into "
    "natural Chinese. Keep numerical values, percentages, and tickers as-is. "
    "Return only the translation — no preamble, no explanation."
)


def translate_to_simplified_chinese(text: str, max_tokens: int) -> str:
    """Translate a Telegram message into Simplified Chinese, preserving layout."""
    return reason(_TRANSLATE_SYSTEM, text, max_tokens)
