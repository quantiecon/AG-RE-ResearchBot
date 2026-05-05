"""
Friday weekly report: research actual outcome, grade predictions, generate narrative.
"""
import logging
from datetime import date, timedelta

import memory
import research
from config import PERPLEXITY_MAX_TOKENS_WEEKLY
from prompts import SYSTEM_ANALYST, WEEKLY_NARRATIVE_PROMPT

logger = logging.getLogger(__name__)


def _predictions_text(predictions: list) -> str:
    if not predictions:
        return "No predictions recorded this week."
    lines = []
    for p in predictions:
        snippet = (p.get("directional_prediction") or p.get("market_summary") or "")[:150]
        lines.append(
            f"  {p['date']} — {p['sentiment_label']} ({p['sentiment_score']}/5): {snippet}"
        )
    return "\n".join(lines)


def run_weekly_report() -> tuple:
    """
    Runs the full Sunday report pipeline.
    Returns (formatted_message, grading_dict, predictions, actual_outcome).
    """
    today = date.today()
    week_end_iso = today.strftime("%Y-%m-%d")
    week_start_iso = (today - timedelta(days=6)).strftime("%Y-%m-%d")
    week_end_readable = today.strftime("%B %d, %Y")
    week_start_readable = (today - timedelta(days=6)).strftime("%B %d, %Y")
    date_str = today.strftime("%B %d, %Y")

    logger.info(f"Weekly report: {week_start_iso} to {week_end_iso}")

    predictions = memory.get_week_predictions(week_start_iso, week_end_iso)

    actual_outcome = research.research_weekly_outcome(
        date_str, week_start_readable, week_end_readable
    )

    if not predictions:
        logger.info("No predictions on record — emitting first-week report without grading.")
        grading = {
            "grade": "N/A",
            "score": 0,
            "rationale": "No daily predictions were recorded this week, so accuracy cannot be graded.",
            "best_call": "—",
            "missed_call": "—",
            "trend_insight": (
                "Daily research will begin populating the prediction record. "
                "Next Sunday's report will include accuracy grading."
            ),
        }
        report_text = (
            f"This is the first weekly report for the BHHS Irvine bot covering "
            f"{week_start_readable} through {week_end_readable}. No daily sentiment "
            f"predictions were on record this week, so prediction-accuracy grading is "
            f"skipped this cycle.\n\n"
            f"Market summary for the week:\n{actual_outcome}\n\n"
            f"Starting next week, daily research at 07:30 PT will accumulate sentiment "
            f"calls and the Sunday report will grade them against actual market movement."
        )
    else:
        predictions_text = _predictions_text(predictions)
        grading = research.grade_predictions(
            predictions_text, actual_outcome, week_start_readable, week_end_readable
        )
        report_text = research._ask(
            SYSTEM_ANALYST,
            WEEKLY_NARRATIVE_PROMPT.format(
                week_start=week_start_readable,
                week_end=week_end_readable,
                predictions=predictions_text,
                actual_outcome=actual_outcome,
                grade=grading.get("grade", "N/A"),
                score=grading.get("score", 0),
                grade_rationale=grading.get("rationale", ""),
                best_call=grading.get("best_call", ""),
                missed_call=grading.get("missed_call", ""),
                trend_insight=grading.get("trend_insight", ""),
            ),
            PERPLEXITY_MAX_TOKENS_WEEKLY,
        )

    memory.save_weekly_report(
        week_ending=week_end_iso,
        week_start=week_start_iso,
        report_text=report_text,
        grade=grading.get("grade", "N/A"),
        score=grading.get("score", 0),
        grade_rationale=grading.get("rationale", ""),
        best_call=grading.get("best_call", ""),
        missed_call=grading.get("missed_call", ""),
        trend_insight=grading.get("trend_insight", ""),
        actual_outcome=actual_outcome,
        predictions=predictions,
    )

    return report_text, grading, predictions, actual_outcome
