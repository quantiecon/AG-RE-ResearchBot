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
Be thorough and professional — no fluff.

LANGUAGE: Respond entirely in Simplified Chinese (简体中文). Numbers, percentages, currency \
symbols, dates, and proper nouns (Irvine, Orange County, Berkshire Hathaway, Federal Reserve, \
FOMC, Redfin, Realtor.com, Fannie Mae, Freddie Mac, etc.) may remain in their original form \
where conventional. When returning JSON, keep all keys in English; only string VALUES are \
translated to Chinese.

PRIMARY DATA SOURCES — concentrate on these where possible (not exclusive):
- OC Realtors / Pacific West Association of Realtors market data
- California Association of Realtors (CAR) — pending sales index, monthly market reports
- Redfin Data Center (Irvine and Orange County trackers)
- Realtor.com market trends and inventory data
You may supplement with Zillow, MLS feeds, Bankrate, FRED, NAR, and reputable financial \
news outlets when the four primary sources do not provide a needed datapoint."""

SYSTEM_ANALYST = """You are a CPA-trained real estate market strategist. You combine deep \
financial analysis with real estate expertise. You understand how Fed policy transmits \
to the mortgage market, how rate movements affect buyer affordability on jumbo loans \
(the dominant product in Irvine), how depreciation and cost segregation affect investor \
returns, and how macro conditions translate to micro movements in high-value California \
markets. Provide precise, data-driven analysis with a clear directional view.

LANGUAGE: Respond entirely in Simplified Chinese (简体中文). Numbers, percentages, currency \
symbols, dates, and proper nouns may remain in their original form. When returning JSON, \
keep all keys and enum values (sentiment labels, letter grades) in their specified form; \
only natural-language string values are translated to Chinese."""

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
produce a structured sentiment analysis. Return ONLY valid JSON — no text before or after. \
All natural-language string values MUST be in Simplified Chinese (简体中文); JSON keys \
and the sentiment_label enum stay as specified.

Research:
{research}

Required JSON format:
{{
  "sentiment_score": <integer 1-5>,
  "sentiment_label": "<强烈持有|持有|中性|买入|强烈买入>",
  "bullish_factors": [
    "<具体指标的简短中文描述,例如:\\"橙县库存同比下降 18% 至 2.1 个月供应 — 明显卖方市场\\">",
    "<具体指标的简短中文描述>",
    "<具体指标的简短中文描述>"
  ],
  "bearish_factors": [
    "<具体指标的简短中文描述,例如:\\"30 年大额贷款利率 7.25%,$1.5M 房产 (80% LTV) 月供本息约 $10,280,较两年均值高 23%\\">",
    "<具体指标的简短中文描述>",
    "<具体指标的简短中文描述>"
  ],
  "market_summary": "<3-4 句中文,CPA 视角的市场综述,需包含具体数字与走势方向>",
  "directional_prediction": "<1-2 句中文:对未来 5-7 天尔湾/橙县市场走向的预测及具体依据>",
  "key_metric_snapshot": {{
    "mortgage_30yr_conforming": "<利率,例如 6.87%>",
    "mortgage_30yr_jumbo": "<利率>",
    "treasury_10yr": "<收益率>",
    "irvine_median_price": "<价格>",
    "oc_months_supply": "<月数>",
    "irvine_dom": "<天数>"
  }}
}}

Sentiment scale:
  1 = 强烈持有 — 明显不利,逆风显著,建议持币观望
  2 = 持有 — 倾向等待,当前风险高于回报
  3 = 中性 — 因素均衡,时机取决于买家自身情况
  4 = 买入 — 条件有利,市场动能支持入市
  5 = 强烈买入 — 多项最优条件叠加,入市机会明确

Provide 3–5 bullets each for bullish and bearish. Every bullet must cite a specific number. \
Bullets are written in Chinese; numbers and proper nouns may remain in their original form.
"""

# ─────────────────────────────────────────────────────────────────────────────
# WEEKLY REPORT
# ─────────────────────────────────────────────────────────────────────────────

WEEKLY_OUTCOME_RESEARCH_PROMPT = """\
Today is {date}. Research what ACTUALLY happened in the Irvine, California \
and Orange County real estate market this week ({week_start} to {week_end}).

Answer specifically (output in Simplified Chinese):
1. 房价 / 挂牌价是上涨、下跌还是持平?
2. 房贷利率上升、下降还是持稳?变动多少基点?
3. 买卖双方活跃度 (待过户、报价、开放日人流) 较上周更高还是更低?
4. 是否有政策、经济或本地新闻对市场产生实质性影响?
5. 数据机构或市场分析师本周对市场状况有何评价?
6. 综合判断:本周整体偏多 (有利于买卖双方现在入市) 还是偏空 (理性应等待)?

Be specific — use numbers. Cite sources where possible.

PRIMARY DATA SOURCES — concentrate on these (not exclusive):
- OC Realtors / Pacific West Association of Realtors
- California Association of Realtors (CAR)
- Redfin Data Center
- Realtor.com market trends
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

Return ONLY valid JSON. Letter grade stays as the English enum; all natural-language \
string values (rationale, best_call, missed_call, trend_insight) MUST be in Simplified \
Chinese (简体中文):
{{
  "grade": "<A+|A|A-|B+|B|B-|C+|C|C-|D+|D|D-|F>",
  "score": <integer 0-100>,
  "rationale": "<2-3 句中文,客观说明评分依据>",
  "best_call": "<本周最准确的一次预测或洞察 (中文)>",
  "missed_call": "<最大的失误或盲点 (中文)>",
  "trend_insight": "<本周累积数据对下周市场走向的提示 (中文)>"
}}
"""

WEEKLY_NARRATIVE_PROMPT = """\
Write a professional weekly market report in Simplified Chinese (简体中文) for a \
CPA-licensed BHHS real estate agent in Irvine, CA covering {week_start} to {week_end}.

Context:
- Daily predictions: {predictions}
- Actual outcome: {actual_outcome}
- Prediction grade: {grade} ({score}/100)
- Grade rationale: {grade_rationale}
- Best call: {best_call}
- Missed call: {missed_call}
- Forward trend: {trend_insight}

Write 3–4 focused paragraphs in Chinese:
  1. 本周尔湾/橙县市场实际发生了什么 (具体数据)
  2. 对预测准确性的诚实复盘
  3. 关键主题与正在形成的趋势
  4. 对下周的前瞻判断

Tone: professional, direct, data-driven. Audience is a CPA — no hand-holding. \
This message is sent via Telegram so avoid markdown headers; use plain paragraph breaks. \
Numbers, percentages, and proper nouns may remain in their original form.
"""
