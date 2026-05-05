"""
All Perplexity prompts in one place.
Edit these to shift research depth, tone, focus areas, or output structure
without touching any other file.
"""

SYSTEM_RESEARCHER = """You are an elite real estate market analyst specializing exclusively \
in Irvine, California and Orange County. Your audience is a CPA-licensed real estate \
professional at Berkshire Hathaway HomeServices who fully understands cap rates, NOI, \
1031 exchanges, cost segregation, depreciation schedules, conforming vs jumbo loan structures, \
basis points, and macro policy transmission to mortgage markets. Provide precise, \
current data with specific numbers, percentages, and dates. Cite sources where possible. \
Be thorough and professional — no fluff."""

SYSTEM_ANALYST = """You are a CPA-trained real estate market strategist. You combine deep \
financial analysis with real estate expertise. You understand how Fed policy transmits \
to the mortgage market, how rate movements affect buyer affordability on jumbo loans \
(the dominant product in Irvine), how depreciation and cost segregation affect investor \
returns, and how macro conditions translate to micro movements in high-value California \
markets. Provide precise, data-driven analysis with a clear directional view."""

# ─────────────────────────────────────────────────────────────────────────────
# DAILY RESEARCH
# ─────────────────────────────────────────────────────────────────────────────

DAILY_RESEARCH_PROMPT = """\
Today is {date}. Conduct a thorough real estate market research brief for a \
CPA-licensed BHHS agent operating in Irvine, California and Orange County.

Cover ALL of the following sections with specific, current numbers:

**1. INTEREST RATE ENVIRONMENT**
- Current 30-year fixed conforming rate and 30-year fixed jumbo rate
- 15-year fixed rate
- 10-year Treasury yield and current spread to 30yr conforming
- Federal funds rate; most recent Fed statement summary; next FOMC date
- Affordability illustration: monthly P&I on a $1.5M Irvine home at current jumbo rate \
vs 12 months ago (assume 20% down)

**2. INVENTORY & SUPPLY**
- Active listings in Irvine (current count and YoY %)
- Orange County months of supply (note: <3 = strong seller's market, 6+ = buyer's market)
- New listings this week vs same week last year
- Absorption rate in OC
- Notable new construction in Irvine (Great Park Neighborhoods, Eastwood, etc.)

**3. PRICING & DEMAND**
- Irvine median home price (most recent data, YoY %)
- Orange County median home price (most recent, YoY %)
- Irvine days on market vs 6 months prior
- List-to-sale price ratio in Irvine
- % of Irvine listings with active price reductions

**4. MACRO & POLICY FACTORS**
- Any new or pending federal legislation affecting real estate (tax policy, GSE news, \
conforming loan limits, FHA/VA changes)
- California-specific: Prop 13 developments, SB 9/zoning policy, rent control updates
- Significant employer news in Irvine/OC (expansions, layoffs, relocations)
- Any geopolitical or financial market events with direct housing market implications

**5. INVESTOR METRICS**
- Estimated cap rates for Irvine SFR rentals
- Average Irvine SFR monthly rent; price-to-rent ratio
- Cash flow viability illustration: is a $1.5M Irvine SFR cash-flow positive at \
current rates with 25% down? Approximate numbers.

**6. RECENT ANALYST COMMENTARY**
- Any notable market reports, analyst takes, or significant transactions in the past 7 days

PRIOR WEEK CONTEXT — use to identify trends and directional changes:
{context}
"""

SENTIMENT_ANALYSIS_PROMPT = """\
Based on the following Irvine/Orange County real estate market research for {date}, \
produce a structured sentiment analysis. Return ONLY valid JSON — no text before or after.

Research:
{research}

Required JSON format:
{{
  "sentiment_score": <integer 1-5>,
  "sentiment_label": "<Strong Hold|Hold|Neutral|Buy|Strong Buy>",
  "bullish_factors": [
    "<bullet with exact metric, e.g. \\"OC inventory fell 18% YoY to 2.1 months supply — firmly seller territory\\">",
    "<bullet with exact metric>",
    "<bullet with exact metric>"
  ],
  "bearish_factors": [
    "<bullet with exact metric, e.g. \\"Jumbo 30yr at 7.25% puts P&I on $1.5M (80% LTV) at $10,280/mo — 23% above 2-yr avg\\">",
    "<bullet with exact metric>",
    "<bullet with exact metric>"
  ],
  "market_summary": "<3-4 sentences, CPA-level market overview with specific numbers and trend direction>",
  "directional_prediction": "<1-2 sentences: predicted direction for Irvine/OC market over next 5-7 days with specific reasoning>",
  "key_metric_snapshot": {{
    "mortgage_30yr_conforming": "<rate, e.g. 6.87%>",
    "mortgage_30yr_jumbo": "<rate>",
    "treasury_10yr": "<yield>",
    "irvine_median_price": "<price>",
    "oc_months_supply": "<months>",
    "irvine_dom": "<days>"
  }}
}}

Sentiment scale:
  1 = Strong Hold — materially suboptimal; significant headwinds; hold cash
  2 = Hold — lean toward waiting; more risk than reward currently
  3 = Neutral — balanced factors; timing depends on individual buyer circumstances
  4 = Buy — favorable conditions; market dynamics support entry
  5 = Strong Buy — aligned optimal conditions; clear entry opportunity

Provide 3–5 bullets each for bullish and bearish. Every bullet must cite a specific number.
"""

# ─────────────────────────────────────────────────────────────────────────────
# WEEKLY REPORT
# ─────────────────────────────────────────────────────────────────────────────

WEEKLY_OUTCOME_RESEARCH_PROMPT = """\
Today is Friday, {date}. Research what ACTUALLY happened in the Irvine, California \
and Orange County real estate market this week ({week_start} to {week_end}).

Answer specifically:
1. Did home prices / list prices move up, down, or hold flat?
2. Did mortgage rates rise, fall, or hold? By how many basis points?
3. Was buyer/seller activity (pending sales, offers, open house traffic) higher or lower \
than the prior week?
4. Did any policy, economic, or local news materially affect the market?
5. What did data services or market analysts say about this week's conditions?
6. Net verdict: was this a bullish week (favorable to buyers or sellers entering now) \
or bearish (rational to wait)?

Be specific — use numbers. Cite sources where possible.
"""

WEEKLY_GRADING_PROMPT = """\
Grade the accuracy of a real estate market prediction bot for the week of \
{week_start} to {week_end} in Irvine, California / Orange County.

DAILY PREDICTIONS MADE BY THE BOT:
{predictions}

WHAT ACTUALLY HAPPENED THIS WEEK:
{actual_outcome}

Grade on accuracy across three dimensions:
- Directional accuracy: did bullish/bearish sentiment match actual market direction?
- Metric accuracy: were key metrics (rates, inventory, prices) correctly anticipated?
- Prediction quality: were the specific cited factors accurate and relevant?

Return ONLY valid JSON:
{{
  "grade": "<A+|A|A-|B+|B|B-|C+|C|C-|D+|D|D-|F>",
  "score": <integer 0-100>,
  "rationale": "<2-3 sentences explaining the grade objectively>",
  "best_call": "<the single most accurate prediction or insight made this week>",
  "missed_call": "<the biggest miss or blind spot>",
  "trend_insight": "<what the cumulative week's data tells us about the market direction going into next week>"
}}
"""

WEEKLY_NARRATIVE_PROMPT = """\
Write a professional weekly market report for a CPA-licensed BHHS real estate agent \
in Irvine, CA covering {week_start} to {week_end}.

Context:
- Daily predictions: {predictions}
- Actual outcome: {actual_outcome}
- Prediction grade: {grade} ({score}/100)
- Grade rationale: {grade_rationale}
- Best call: {best_call}
- Missed call: {missed_call}
- Forward trend: {trend_insight}

Write 3–4 focused paragraphs:
  1. What happened in the Irvine/OC market this week (specific data)
  2. Honest review of prediction accuracy
  3. Key themes and developing trends
  4. Forward-looking perspective for next week

Tone: professional, direct, data-driven. Audience is a CPA — no hand-holding. \
This message is sent via Telegram so avoid markdown headers; use plain paragraph breaks.
"""
