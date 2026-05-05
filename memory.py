"""
SQLite-backed storage for daily research and weekly reports.
All cumulative memory lives in data/research.db.
"""
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "research.db"


def init_db() -> None:
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS daily_research (
                id                      INTEGER PRIMARY KEY AUTOINCREMENT,
                date                    TEXT    NOT NULL UNIQUE,
                raw_research            TEXT,
                sentiment_score         INTEGER,
                sentiment_label         TEXT,
                bullish_factors         TEXT,
                bearish_factors         TEXT,
                market_summary          TEXT,
                directional_prediction  TEXT,
                key_metrics             TEXT,
                telegram_message        TEXT,
                created_at              TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS weekly_reports (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                week_ending      TEXT NOT NULL,
                week_start       TEXT NOT NULL,
                report_text      TEXT,
                grade            TEXT,
                score            INTEGER,
                grade_rationale  TEXT,
                best_call        TEXT,
                missed_call      TEXT,
                trend_insight    TEXT,
                actual_outcome   TEXT,
                predictions_json TEXT,
                created_at       TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()


def save_daily(
    date_str: str,
    raw_research: str,
    sentiment_score: int,
    sentiment_label: str,
    bullish_factors: list,
    bearish_factors: list,
    market_summary: str,
    directional_prediction: str,
    key_metrics: dict,
    telegram_message: str,
) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO daily_research
            (date, raw_research, sentiment_score, sentiment_label,
             bullish_factors, bearish_factors, market_summary,
             directional_prediction, key_metrics, telegram_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date_str, raw_research, sentiment_score, sentiment_label,
                json.dumps(bullish_factors), json.dumps(bearish_factors),
                market_summary, directional_prediction,
                json.dumps(key_metrics), telegram_message,
            ),
        )
        conn.commit()


def get_recent_context(days: int = 7) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT date, sentiment_score, sentiment_label, market_summary,
                   directional_prediction, key_metrics
            FROM daily_research
            ORDER BY date DESC
            LIMIT ?
            """,
            (days,),
        ).fetchall()
    return [
        {
            "date": r[0],
            "sentiment_score": r[1],
            "sentiment_label": r[2],
            "market_summary": r[3],
            "directional_prediction": r[4],
            "key_metrics": json.loads(r[5]) if r[5] else {},
        }
        for r in rows
    ]


def get_week_predictions(start_date: str, end_date: str) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT date, sentiment_score, sentiment_label,
                   market_summary, directional_prediction
            FROM daily_research
            WHERE date BETWEEN ? AND ?
            ORDER BY date
            """,
            (start_date, end_date),
        ).fetchall()
    return [
        {
            "date": r[0],
            "sentiment_score": r[1],
            "sentiment_label": r[2],
            "market_summary": r[3],
            "directional_prediction": r[4],
        }
        for r in rows
    ]


def save_weekly_report(
    week_ending: str,
    week_start: str,
    report_text: str,
    grade: str,
    score: int,
    grade_rationale: str,
    best_call: str,
    missed_call: str,
    trend_insight: str,
    actual_outcome: str,
    predictions: list,
) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO weekly_reports
            (week_ending, week_start, report_text, grade, score, grade_rationale,
             best_call, missed_call, trend_insight, actual_outcome, predictions_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                week_ending, week_start, report_text, grade, score, grade_rationale,
                best_call, missed_call, trend_insight, actual_outcome,
                json.dumps(predictions),
            ),
        )
        conn.commit()
