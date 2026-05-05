"""
Central configuration — all tunable settings live here.
Modify this file to adjust schedule, metrics tracked, sentiment thresholds, etc.
"""

# ── Scheduling ────────────────────────────────────────────────────────────────
TIMEZONE = "America/Los_Angeles"
DAILY_HOUR = 7
DAILY_MINUTE = 30
WEEKLY_REPORT_DAY = "sun"
WEEKLY_REPORT_HOUR = 16
WEEKLY_REPORT_MINUTE = 0

# ── Agent Profile ─────────────────────────────────────────────────────────────
AGENT_PROFILE = {
    "brokerage": "Berkshire Hathaway HomeServices",
    "market_focus": "Irvine, California / Orange County",
    "audience": "CPA-licensed real estate professional",
}

# ── Perplexity Model ──────────────────────────────────────────────────────────
# Options: "sonar" (faster/cheaper), "sonar-pro" (deeper web search), "sonar-reasoning"
PERPLEXITY_MODEL = "sonar-pro"
PERPLEXITY_MAX_TOKENS_RESEARCH = 2500
PERPLEXITY_MAX_TOKENS_SENTIMENT = 1200
PERPLEXITY_MAX_TOKENS_WEEKLY = 2000

# ── Memory ────────────────────────────────────────────────────────────────────
CONTEXT_DAYS = 7  # Days of prior research passed as context to each new query

# ── Sentiment Scale ───────────────────────────────────────────────────────────
SENTIMENT_LABELS = {
    1: "强烈持有",
    2: "持有",
    3: "中性",
    4: "买入",
    5: "强烈买入",
}

SENTIMENT_EMOJI = {1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢", 5: "💚"}

SENTIMENT_BAR = {
    1: "▓░░░░",
    2: "▓▓░░░",
    3: "▓▓▓░░",
    4: "▓▓▓▓░",
    5: "▓▓▓▓▓",
}

# ── Key Metrics Tracked Daily ─────────────────────────────────────────────────
# These inform the research prompt — add/remove to adjust research focus.
TRACKED_METRICS = [
    "30-year fixed conforming mortgage rate",
    "30-year fixed jumbo mortgage rate (critical for Irvine)",
    "15-year fixed mortgage rate",
    "Federal funds rate and most recent Fed statement / upcoming FOMC dates",
    "10-year Treasury yield and spread to 30yr mortgage",
    "Irvine median home price (most recent available) with YoY %",
    "Orange County active listing count and months of supply",
    "Irvine days on market vs 6 months prior",
    "List-to-sale price ratio in Irvine",
    "% of Irvine listings with price reductions",
    "Orange County unemployment rate",
    "Consumer Confidence Index",
    "NAHB Housing Market Index",
    "CAR (California Association of Realtors) pending sales index",
    "Irvine/OC cap rate estimates for SFR rentals",
    "Average Irvine SFR rent and price-to-rent ratio",
]

# ── Weekly Grading ────────────────────────────────────────────────────────────
# Score thresholds (lower bound inclusive) mapped to letter grade
GRADE_THRESHOLDS = [
    (95, "A+"), (90, "A"), (85, "A-"),
    (80, "B+"), (75, "B"), (70, "B-"),
    (65, "C+"), (60, "C"), (55, "C-"),
    (50, "D+"), (45, "D"), (40, "D-"),
    (0,  "F"),
]
