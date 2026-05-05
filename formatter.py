"""
Formats research data into Telegram-ready plain text messages.
Edit layout and copy here without touching logic files.
"""
from config import SENTIMENT_BAR, SENTIMENT_EMOJI


def format_daily_message(
    date_str: str,
    market_summary: str,
    bullish_factors: list,
    bearish_factors: list,
    sentiment_score: int,
    sentiment_label: str,
    directional_prediction: str,
    key_metrics: dict,
) -> str:
    emoji = SENTIMENT_EMOJI.get(sentiment_score, "🟡")
    bar = SENTIMENT_BAR.get(sentiment_score, "▓▓▓░░")

    bull_text = "\n".join(f"  • {f}" for f in bullish_factors)
    bear_text = "\n".join(f"  • {f}" for f in bearish_factors)

    metric_labels = {
        "mortgage_30yr_conforming": "30yr Conforming",
        "mortgage_30yr_jumbo":      "30yr Jumbo",
        "treasury_10yr":            "10yr Treasury",
        "irvine_median_price":      "Irvine Median",
        "oc_months_supply":         "OC Supply",
        "irvine_dom":               "Irvine DOM",
    }
    metrics_lines = [
        f"  {label}: {key_metrics[key]}"
        for key, label in metric_labels.items()
        if key_metrics.get(key)
    ]
    metrics_text = "\n".join(metrics_lines) if metrics_lines else "  (metrics unavailable)"

    return (
        f"📊 BHHS IRVINE MARKET BRIEF — {date_str}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏠 MARKET OVERVIEW\n"
        f"{market_summary}\n\n"
        f"📉 KEY METRICS\n"
        f"{metrics_text}\n\n"
        f"📈 REASONS TO ENTER THE MARKET\n"
        f"{bull_text}\n\n"
        f"⚠️ REASONS FOR CAUTION\n"
        f"{bear_text}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{emoji} SENTIMENT: {sentiment_label.upper()}\n"
        f"[{bar}] {sentiment_score}/5\n\n"
        f"{directional_prediction}\n\n"
        f"—\n"
        f"Berkshire Hathaway HomeServices | Irvine, CA\n"
        f"Orange County Real Estate Intelligence"
    )


def format_weekly_message(
    week_start: str,
    week_end: str,
    predictions: list,
    actual_outcome: str,
    report_text: str,
    grade: str,
    score: int,
    best_call: str,
    missed_call: str,
    trend_insight: str,
) -> str:
    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    pred_lines = []
    for i, pred in enumerate(predictions[:5]):
        label = day_labels[i] if i < len(day_labels) else f"Day {i + 1}"
        e = SENTIMENT_EMOJI.get(pred.get("sentiment_score", 3), "🟡")
        pred_lines.append(f"  {label}: {e} {pred.get('sentiment_label', 'N/A')}")
    prediction_summary = "\n".join(pred_lines) if pred_lines else "  No predictions recorded."

    return (
        f"📋 WEEKLY MARKET REPORT\n"
        f"Week of {week_start} → {week_end}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📆 DAILY PREDICTIONS\n"
        f"{prediction_summary}\n\n"
        f"📝 WEEKLY ANALYSIS\n"
        f"{report_text}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 PREDICTION GRADE: {grade} ({score}/100)\n\n"
        f"✅ Best Call: {best_call}\n"
        f"❌ Missed:    {missed_call}\n\n"
        f"🔭 OUTLOOK\n"
        f"{trend_insight}\n\n"
        f"—\n"
        f"Berkshire Hathaway HomeServices | Irvine, CA\n"
        f"Orange County Real Estate Intelligence"
    )
