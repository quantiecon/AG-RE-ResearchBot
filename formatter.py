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
    most_significant_change: str = "",
) -> str:
    emoji = SENTIMENT_EMOJI.get(sentiment_score, "🟡")
    bar = SENTIMENT_BAR.get(sentiment_score, "▓▓▓░░")

    bull_text = "\n".join(f"  • {f}" for f in bullish_factors)
    bear_text = "\n".join(f"  • {f}" for f in bearish_factors)

    metric_labels = {
        "mortgage_30yr_conforming": "30年合规房贷",
        "mortgage_30yr_jumbo":      "30年大额房贷",
        "treasury_10yr":            "10年期国债",
        "irvine_median_price":      "尔湾房价中位数",
        "oc_months_supply":         "橙县供应月数",
        "irvine_dom":               "尔湾在售天数",
    }
    metrics_lines = [
        f"  {label}: {key_metrics[key]}"
        for key, label in metric_labels.items()
        if key_metrics.get(key)
    ]
    metrics_text = "\n".join(metrics_lines) if metrics_lines else "  （指标暂无）"

    return (
        f"📊 BHHS 尔湾房市简报 — {date_str}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏠 市场概览\n"
        f"{market_summary}\n\n"
        f"📉 关键指标\n"
        f"{metrics_text}\n\n"
        f"📈 入市理由\n"
        f"{bull_text}\n\n"
        f"⚠️ 谨慎原因\n"
        f"{bear_text}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{emoji} 综合判断:{sentiment_label}\n"
        f"[{bar}] {sentiment_score}/5\n\n"
        f"{directional_prediction}\n\n"
        f"🔥 本周最重大变动\n"
        f"{most_significant_change or '(本周暂无突出单一变动)'}\n\n"
        f"—\n"
        f"Berkshire Hathaway HomeServices | 加州尔湾\n"
        f"橙县房产市场情报"
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
    day_labels = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    pred_lines = []
    for i, pred in enumerate(predictions[:7]):
        label = day_labels[i] if i < len(day_labels) else f"第{i + 1}天"
        e = SENTIMENT_EMOJI.get(pred.get("sentiment_score", 3), "🟡")
        pred_lines.append(f"  {label}: {e} {pred.get('sentiment_label', 'N/A')}")
    prediction_summary = "\n".join(pred_lines) if pred_lines else "  暂无预测记录 — 首周运行。"

    return (
        f"📋 每周市场报告\n"
        f"覆盖周期 {week_start} → {week_end}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📆 每日预测\n"
        f"{prediction_summary}\n\n"
        f"📝 本周分析\n"
        f"{report_text}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 预测评分:{grade} ({score}/100)\n\n"
        f"✅ 最佳判断:{best_call}\n"
        f"❌ 遗漏:    {missed_call}\n\n"
        f"🔭 后市展望\n"
        f"{trend_insight}\n\n"
        f"—\n"
        f"Berkshire Hathaway HomeServices | 加州尔湾\n"
        f"橙县房产市场情报"
    )
