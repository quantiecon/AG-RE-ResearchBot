"""
Perplexity API integration.
All calls go through _ask(); swap PERPLEXITY_MODEL in config.py to change depth.
"""
import json
import logging
import os

from openai import OpenAI

from config import (
    PERPLEXITY_MAX_TOKENS_RESEARCH,
    PERPLEXITY_MAX_TOKENS_SENTIMENT,
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


def _parse_json(text: str) -> dict:
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


def run_daily_research(date_str: str, context_text: str) -> dict:
    """Full daily pipeline: raw research → structured sentiment. Returns merged dict.
    Falls back to a neutral payload (with the raw research as market_summary) if
    the sentiment model returns unparseable JSON, so Telegram always gets *something*.
    """
    logger.info("Fetching raw market research from Perplexity")
    raw = _ask(
        SYSTEM_RESEARCHER,
        DAILY_RESEARCH_PROMPT.format(date=date_str, context=context_text),
        PERPLEXITY_MAX_TOKENS_RESEARCH,
    )
    logger.info("Generating structured sentiment analysis")
    sentiment_raw = _ask(
        SYSTEM_ANALYST,
        SENTIMENT_ANALYSIS_PROMPT.format(research=raw, date=date_str),
        PERPLEXITY_MAX_TOKENS_SENTIMENT,
    )
    try:
        result = _parse_json(sentiment_raw)
    except (ValueError, json.JSONDecodeError) as e:
        logger.warning(f"Sentiment JSON parse failed: {e}. Falling back to raw research payload.")
        result = {
            "sentiment_score": 3,
            "sentiment_label": "中性",
            "bullish_factors": [],
            "bearish_factors": [],
            "market_summary": (
                "(结构化情绪解析失败,以下为原始研究摘要)\n\n" + raw[:1500]
            ),
            "directional_prediction": "",
            "key_metric_snapshot": {},
            "most_significant_change": "",
        }
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
    raw = _ask(
        SYSTEM_ANALYST,
        WEEKLY_GRADING_PROMPT.format(
            week_start=week_start,
            week_end=week_end,
            predictions=predictions_text,
            actual_outcome=actual_outcome,
        ),
        800,
    )
    try:
        return _parse_json(raw)
    except (ValueError, json.JSONDecodeError) as e:
        logger.warning(f"Grading JSON parse failed: {e}. Returning fallback dict.")
        return {
            "grade": "N/A",
            "score": 0,
            "rationale": "Grading model did not return valid JSON; raw output preserved in trend_insight.",
            "best_call": "—",
            "missed_call": "—",
            "trend_insight": raw[:600],
        }
