"""
APScheduler setup.
Daily job at 07:30 PT; weekly report Sunday at 16:00 PT.
"""
import logging
from datetime import date, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import (
    CONTEXT_DAYS,
    DAILY_HOUR,
    DAILY_MINUTE,
    TIMEZONE,
    WEEKLY_REPORT_DAY,
    WEEKLY_REPORT_HOUR,
    WEEKLY_REPORT_MINUTE,
)

logger = logging.getLogger(__name__)


async def daily_job() -> None:
    try:
        import memory
        from formatter import format_daily_message
        from research import run_daily_research
        from telegram_client import send_message

        today_iso = date.today().strftime("%Y-%m-%d")
        today_str = date.today().strftime("%B %d, %Y")
        logger.info(f"Daily job started — {today_str}")

        recent = memory.get_recent_context(CONTEXT_DAYS)
        context_lines = [
            f"{r['date']}: {r['sentiment_label']} ({r['sentiment_score']}/5) — "
            f"{(r.get('market_summary') or '')[:200]}"
            for r in recent
        ]
        context_text = (
            "\n".join(context_lines) if context_lines
            else "No prior data — this is the first run."
        )

        result = run_daily_research(today_str, context_text)

        message = format_daily_message(
            date_str=today_str,
            market_summary=result.get("market_summary", ""),
            bullish_factors=result.get("bullish_factors", []),
            bearish_factors=result.get("bearish_factors", []),
            sentiment_score=result.get("sentiment_score", 3),
            sentiment_label=result.get("sentiment_label", "中性"),
            directional_prediction=result.get("directional_prediction", ""),
            key_metrics=result.get("key_metric_snapshot", {}),
            most_significant_change=result.get("most_significant_change", ""),
        )

        memory.save_daily(
            date_str=today_iso,
            raw_research=result.get("raw_research", ""),
            sentiment_score=result.get("sentiment_score", 3),
            sentiment_label=result.get("sentiment_label", "中性"),
            bullish_factors=result.get("bullish_factors", []),
            bearish_factors=result.get("bearish_factors", []),
            market_summary=result.get("market_summary", ""),
            directional_prediction=result.get("directional_prediction", ""),
            key_metrics=result.get("key_metric_snapshot", {}),
            telegram_message=message,
            most_significant_change=result.get("most_significant_change", ""),
        )

        await send_message(message)
        logger.info("Daily job complete")

    except Exception as e:
        logger.exception("Daily job failed")
        try:
            from telegram_client import send_message
            await send_message(
                f"⚠️ BHHS Bot: Daily research failed.\n{type(e).__name__}: {str(e)[:300]}"
            )
        except Exception:
            pass


async def weekly_job() -> None:
    try:
        from formatter import format_weekly_message
        from telegram_client import send_message
        from weekly_report import run_weekly_report

        logger.info("Weekly report job started")
        report_text, grading, predictions, actual_outcome = run_weekly_report()

        today = date.today()
        week_start = (today - timedelta(days=6)).strftime("%B %d, %Y")
        week_end = today.strftime("%B %d, %Y")

        message = format_weekly_message(
            week_start=week_start,
            week_end=week_end,
            predictions=predictions,
            actual_outcome=actual_outcome,
            report_text=report_text,
            grade=grading.get("grade", "N/A"),
            score=grading.get("score", 0),
            best_call=grading.get("best_call", ""),
            missed_call=grading.get("missed_call", ""),
            trend_insight=grading.get("trend_insight", ""),
        )

        await send_message(message)
        logger.info("Weekly report job complete")

    except Exception as e:
        logger.exception("Weekly report job failed")
        try:
            from telegram_client import send_message
            await send_message(
                f"⚠️ BHHS Bot: Weekly report failed.\n{type(e).__name__}: {str(e)[:300]}"
            )
        except Exception:
            pass


def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    scheduler.add_job(
        daily_job,
        CronTrigger(hour=DAILY_HOUR, minute=DAILY_MINUTE, timezone=TIMEZONE),
        id="daily_research",
        name="Daily Market Research",
        misfire_grace_time=300,
    )

    scheduler.add_job(
        weekly_job,
        CronTrigger(
            day_of_week=WEEKLY_REPORT_DAY,
            hour=WEEKLY_REPORT_HOUR,
            minute=WEEKLY_REPORT_MINUTE,
            timezone=TIMEZONE,
        ),
        id="weekly_report",
        name="Weekly Report",
        misfire_grace_time=300,
    )

    return scheduler
