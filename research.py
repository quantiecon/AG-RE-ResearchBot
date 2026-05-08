"""
Perplexity API integration.
All calls go through _ask(); swap PERPLEXITY_MODEL in config.py to change depth.
"""
import logging
import os

from openai import OpenAI

import claude_client
from config import (
    CLAUDE_MAX_TOKENS_GRADING,
    CLAUDE_MAX_TOKENS_SENTIMENT,
    CLAUDE_MODEL_GRADING,
    CLAUDE_MODEL_SENTIMENT,
    PERPLEXITY_MAX_TOKENS_RESEARCH,
    PERPLEXITY_MODEL,
)
from prompts import (
    DAILY_RESEARCH_PROMPT,
    SENTIMENT_ANALYSIS_PROMPT,
    SYSTEM_ANALYST,
    SYSTEM_RESEARCHER,
    WEEKLY_GRADING_PROMPT,
    WEEKLY_OUTCOME_RESEARCH_PROMPT,
)

logger = logging.getLogger(__name__)

_SENTIMENT_REQUIRED = {
    "sentiment_score", "sentiment_label", "bullish_factors", "bearish_factors",
    "market_summary", "directional_prediction", "key_metric_snapshot",
}
_KEY_METRIC_REQUIRED = {
    "mortgage_30yr_conforming", "mortgage_30yr_jumbo", "treasury_10yr",
    "irvine_median_price", "oc_months_supply", "irvine_dom",
}
_GRADING_REQUIRED = {
    "grade", "score", "rationale", "best_call", "missed_call", "trend_insight",
}


def _check_keys(d: dict, required: set, name: str) -> None:
    missing = required - d.keys()
    if missing:
        logger.warning(f"{name} schema drift — missing keys: {sorted(missing)}")


def _client() -> OpenAI:
    return OpenAI(
        api_key=os.environ["PERPLEXITY_API_KEY"],
        base_url="https://api.perplexity.ai",
    )


def _ask(system: str, user: str, max_tokens: int) -> str:
    resp = _client().chat.completions.create(
        model=PERPLEXITY_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content


def run_daily_research(date_str: str, context_text: str) -> dict:
    """Full daily pipeline: raw research → structured sentiment. Returns merged dict."""
    logger.info("Fetching raw market research from Perplexity")
    raw = _ask(
        SYSTEM_RESEARCHER,
        DAILY_RESEARCH_PROMPT.format(date=date_str, context=context_text),
        PERPLEXITY_MAX_TOKENS_RESEARCH,
    )
    logger.info("Generating structured sentiment analysis")
    result = claude_client.reason_json(
        SYSTEM_ANALYST,
        SENTIMENT_ANALYSIS_PROMPT.format(research=raw, date=date_str),
        CLAUDE_MAX_TOKENS_SENTIMENT,
        model=CLAUDE_MODEL_SENTIMENT,
    )
    _check_keys(result, _SENTIMENT_REQUIRED, "sentiment")
    _check_keys(result.get("key_metric_snapshot") or {}, _KEY_METRIC_REQUIRED, "key_metric_snapshot")
    result["raw_research"] = raw
    return result


def research_weekly_outcome(date_str: str, week_start: str, week_end: str) -> str:
    logger.info("Researching actual weekly market outcome")
    return _ask(
        SYSTEM_RESEARCHER,
        WEEKLY_OUTCOME_RESEARCH_PROMPT.format(
            date=date_str, week_start=week_start, week_end=week_end
        ),
        1500,
    )


def grade_predictions(predictions_text: str, actual_outcome: str, week_start: str, week_end: str) -> dict:
    logger.info("Grading weekly predictions")
    result = claude_client.reason_json(
        SYSTEM_ANALYST,
        WEEKLY_GRADING_PROMPT.format(
            week_start=week_start,
            week_end=week_end,
            predictions=predictions_text,
            actual_outcome=actual_outcome,
        ),
        CLAUDE_MAX_TOKENS_GRADING,
        model=CLAUDE_MODEL_GRADING,
    )
    _check_keys(result, _GRADING_REQUIRED, "grading")
    return result
