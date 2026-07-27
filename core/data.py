"""
core/data.py — Static reference data: countries, languages, life stages,
financial goals, localized content, and scam warnings.
No external dependencies beyond stdlib.
"""

from __future__ import annotations

COUNTRIES: list[dict] = [
    {"code": "US", "name": "United States", "currency": "USD", "region": "north_america"},
    {"code": "GB", "name": "United Kingdom", "currency": "GBP", "region": "europe"},
    {"code": "CA", "name": "Canada", "currency": "CAD", "region": "north_america"},
    {"code": "AU", "name": "Australia", "currency": "AUD", "region": "oceania"},
    {"code": "IN", "name": "India", "currency": "INR", "region": "south_asia"},
    {"code": "NG", "name": "Nigeria", "currency": "NGN", "region": "africa"},
    {"code": "ZA", "name": "South Africa", "currency": "ZAR", "region": "africa"},
    {"code": "BR", "name": "Brazil", "currency": "BRL", "region": "latin_america"},
    {"code": "MX", "name": "Mexico", "currency": "MXN", "region": "latin_america"},
    {"code": "DE", "name": "Germany", "currency": "EUR", "region": "europe"},
    {"code": "FR", "name": "France", "currency": "EUR", "region": "europe"},
    {"code": "JP", "name": "Japan", "currency": "JPY", "region": "east_asia"},
    {"code": "PH", "name": "Philippines", "currency": "PHP", "region": "southeast_asia"},
    {"code": "KE", "name": "Kenya", "currency": "KES", "region": "africa"},
    {"code": "EG", "name": "Egypt", "currency": "EGP", "region": "middle_east"},
    {"code": "OTHER", "name": "Other / Prefer not to say", "currency": "USD", "region": "global"},
]

LANGUAGES: list[dict] = [
    {"code": "en", "name": "English"},
    {"code": "es", "name": "Español (Spanish)"},
    {"code": "fr", "name": "Français (French)"},
    {"code": "pt", "name": "Português (Portuguese)"},
    {"code": "hi", "name": "हिंदी (Hindi)"},
    {"code": "ar", "name": "العربية (Arabic)"},
    {"code": "sw", "name": "Kiswahili (Swahili)"},
    {"code": "yo", "name": "Yorùbá"},
    {"code": "de", "name": "Deutsch (German)"},
    {"code": "ja", "name": "日本語 (Japanese)"},
    {"code": "tl", "name": "Filipino (Tagalog)"},
    {"code": "zh", "name": "中文 (Chinese)"},
]

LIFE_STAGES: list[dict] = [
    {
        "id": "student",
        "label": "Student",
        "description": "Currently enrolled in school or university",
        "icon": ":material/school:",
        "priorities": ["budgeting", "student_debt", "emergency_fund", "first_job"],
    },
    {
        "id": "early_career",
        "label": "Early career",
        "description": "First years of professional life (20s–early 30s)",
        "icon": ":material/work:",
        "priorities": ["emergency_fund", "retirement_start", "debt_payoff", "investing"],
    },
    {
        "id": "parent",
        "label": "Parent / Caregiver",
        "description": "Raising children or caring for dependants",
        "icon": ":material/family_restroom:",
        "priorities": ["insurance", "education_savings", "budgeting", "emergency_fund"],
    },
    {
        "id": "immigrant",
        "label": "Immigrant / Expat",
        "description": "Living in a country different from your home country",
        "icon": ":material/flight_land:",
        "priorities": ["banking_access", "remittances", "credit_building", "tax_filing"],
    },
    {
        "id": "entrepreneur",
        "label": "Entrepreneur / Self-employed",
        "description": "Running or starting your own business",
        "icon": ":material/storefront:",
        "priorities": ["business_cashflow", "tax_planning", "insurance", "separation_of_finances"],
    },
    {
        "id": "caregiver",
        "label": "Full-time caregiver",
        "description": "Primarily caring for family members without paid employment",
        "icon": ":material/volunteer_activism:",
        "priorities": ["benefits", "re_entry_planning", "emergency_fund", "insurance"],
    },
    {
        "id": "pre_retirement",
        "label": "Pre-retirement",
        "description": "10–15 years away from retirement",
        "icon": ":material/hourglass_top:",
        "priorities": ["retirement_maximizing", "debt_payoff", "healthcare", "estate_planning"],
    },
    {
        "id": "retiree",
        "label": "Retired",
        "description": "No longer working full-time",
        "icon": ":material/beach_access:",
        "priorities": ["withdrawal_strategy", "healthcare", "estate_planning", "scam_protection"],
    },
]

PRESET_GOALS: list[dict] = [
    {"id": "emergency_fund", "label": "Build an emergency fund", "icon": ":material/savings:"},
    {"id": "debt_payoff", "label": "Pay off debt", "icon": ":material/credit_card_off:"},
    {"id": "buy_home", "label": "Buy a home", "icon": ":material/home:"},
    {"id": "investing", "label": "Start investing", "icon": ":material/trending_up:"},
    {"id": "retirement", "label": "Save for retirement", "icon": ":material/elderly:"},
    {"id": "start_business", "label": "Start a business", "icon": ":material/storefront:"},
    {"id": "education", "label": "Save for education", "icon": ":material/school:"},
    {"id": "travel", "label": "Travel / experiences", "icon": ":material/travel_explore:"},
    {"id": "insurance", "label": "Get proper insurance", "icon": ":material/shield:"},
]

AGE_RANGES: list[str] = [
    "Under 18",
    "18–24",
    "25–34",
    "35–44",
    "45–54",
    "55–64",
    "65+",
    "Prefer not to say",
]

# ---------------------------------------------------------------------------
# Accessibility & communication preferences
# ---------------------------------------------------------------------------

ACCESSIBILITY_NEEDS: list[dict] = [
    {
        "id": "deaf_hoh",
        "label": "Deaf or hard of hearing",
        "icon": ":material/hearing_disabled:",
        "description": "Text and captions stay primary; spoken output is never the only way information is given.",
    },
    {
        "id": "low_vision",
        "label": "Low vision or blind",
        "icon": ":material/visibility:",
        "description": "Larger text, higher contrast, and structure that doesn't depend on colour or icons alone.",
    },
    {
        "id": "cognitive",
        "label": "Cognitive accessibility (e.g., ADHD, dyslexia, memory or focus differences)",
        "icon": ":material/psychology_alt:",
        "description": "Shorter sentences, one idea at a time, and less visual clutter.",
    },
    {
        "id": "none",
        "label": "None of these apply",
        "icon": ":material/check_circle:",
        "description": "",
    },
    {
        "id": "prefer_not_say",
        "label": "Prefer not to say",
        "icon": ":material/lock:",
        "description": "",
    },
]

COMMUNICATION_MODES: list[dict] = [
    {
        "id": "text",
        "label": "Text only",
        "icon": ":material/chat:",
        "description": "Type and read — no audio.",
    },
    {
        "id": "voice",
        "label": "Voice only",
        "icon": ":material/record_voice_over:",
        "description": "Speak your questions and hear responses read aloud, with a live visual transcript.",
    },
    {
        "id": "both",
        "label": "Text and voice",
        "icon": ":material/forum:",
        "description": "Use whichever feels right, message to message.",
    },
]

# ---------------------------------------------------------------------------
# Localized financial guidance snippets
# ---------------------------------------------------------------------------

REGIONAL_CONTENT: dict[str, dict] = {
    "north_america": {
        "tax_note": "Tax-advantaged accounts like 401(k), IRA (US) or RRSP, TFSA (Canada) can significantly accelerate savings.",
        "retirement_programs": "Social Security (US) / CPP & OAS (Canada)",
        "credit_note": "Credit scores (FICO/VantageScore in the US; Equifax/TransUnion in Canada) heavily influence loan terms.",
        "scam_alert": "IRS/CRA impersonation calls are very common. Tax agencies never demand immediate payment by gift card.",
    },
    "europe": {
        "tax_note": "Many European countries offer pension auto-enrollment and ISA-style wrappers. Contribution limits vary by country.",
        "retirement_programs": "State pension systems vary widely; check your national insurance record.",
        "credit_note": "Credit scoring systems differ across EU countries. Building a local credit history takes time for immigrants.",
        "scam_alert": "HMRC (UK) / tax-authority impersonation emails and SMS are prevalent. Verify via official government portals.",
    },
    "south_asia": {
        "tax_note": "PPF, EPF, NPS, and ELSS funds in India offer tax benefits under Section 80C. Consult a CA for optimisation.",
        "retirement_programs": "Employees' Provident Fund (EPF), National Pension Scheme (NPS)",
        "credit_note": "CIBIL score (India) is the primary credit reference. Timely EMI payments are the fastest way to build it.",
        "scam_alert": "KYC update fraud via fake bank calls/SMS is widespread. Never share OTPs or Aadhaar numbers over phone.",
    },
    "africa": {
        "tax_note": "Mobile money platforms (M-Pesa, Flutterwave, etc.) can be tax-efficient for small business cashflows. Check local regulations.",
        "retirement_programs": "NSSF (Kenya/Uganda), SSNIT (Ghana), NSITF (Nigeria) — contribution rates and benefits vary.",
        "credit_note": "Formal credit histories are limited in many markets. Mobile money repayment records increasingly influence lending.",
        "scam_alert": "Advance-fee (419) fraud, fake investment schemes, and cryptocurrency scams are very common. No legitimate investment guarantees returns.",
    },
    "latin_america": {
        "tax_note": "AFORE (Mexico), FGTS (Brazil), and similar mandatory pension systems require understanding your employer contributions.",
        "retirement_programs": "AFORE (MX), INSS/FGTS (BR), and country-specific social security systems.",
        "credit_note": "Bureaux de crédito (Buró de Crédito in MX, Serasa in BR) track your credit history; review your report annually.",
        "scam_alert": "Pyramid schemes disguised as savings clubs ('tandas', 'rifas', investment clubs) carry high loss risk.",
    },
    "east_asia": {
        "tax_note": "Japan's NISA (Nippon Individual Savings Account) offers tax-free investment growth. iDeCo is Japan's defined-contribution pension.",
        "retirement_programs": "National Pension (Kokumin Nenkin) and Employees' Pension Insurance (Kosei Nenkin) in Japan.",
        "credit_note": "Credit infrastructure in Japan differs from Western countries; maintaining bank accounts and utilities helps build history.",
        "scam_alert": "Ore-ore fraud (impersonation of family members in distress) targets elderly women in Japan.",
    },
    "southeast_asia": {
        "tax_note": "SSS/PhilHealth/Pag-IBIG (Philippines) are mandatory contributions; maximising voluntary contributions can boost retirement.",
        "retirement_programs": "SSS (Philippines), EPF (Malaysia), CPF (Singapore) — highly varied by country.",
        "credit_note": "Credit scoring is maturing in the region; on-time loan and credit card payments are the core drivers.",
        "scam_alert": "Online lending app scams and text-based phishing for OTPs are very prevalent across Southeast Asia.",
    },
    "middle_east": {
        "tax_note": "Many GCC countries have no personal income tax, but gratuity entitlements and local pension schemes vary. Verify local labour law.",
        "retirement_programs": "End-of-service gratuity is the primary benefit for many expat workers; invest it proactively.",
        "credit_note": "Al Etihad Credit Bureau (UAE) and SIMAH (Saudi Arabia) report credit history; review annually.",
        "scam_alert": "Fake job offers requiring upfront fees and investment scheme scams are very common for women workers abroad.",
    },
    "oceania": {
        "tax_note": "Superannuation (Australia) contributions are mandatory. Consider voluntary top-ups and the First Home Super Saver scheme.",
        "retirement_programs": "Superannuation (AU), KiwiSaver (NZ)",
        "credit_note": "Equifax and Experian operate in Australia. Comprehensive credit reporting now includes positive repayment data.",
        "scam_alert": "ATO (Australian Tax Office) impersonation scams via phone and email spike every tax season.",
    },
    "global": {
        "tax_note": "Tax rules are highly country-specific. Universal principle: understand whether any savings or investment accounts offer tax benefits in your jurisdiction.",
        "retirement_programs": "Check your country's national pension authority website for your specific entitlements.",
        "credit_note": "Building credit globally: pay bills on time, keep debt-to-income low, and review your credit report at least annually.",
        "scam_alert": "Red flags everywhere: guaranteed high returns, pressure to act immediately, requests for unusual payment methods (gift cards, crypto, wire transfers to unknown accounts).",
    },
}

# ---------------------------------------------------------------------------
# Educational modules catalog
# ---------------------------------------------------------------------------

EDUCATION_MODULES: list[dict] = [
    {
        "id": "emergency_fund_101",
        "title": "Building your emergency fund",
        "category": "Foundations",
        "duration_min": 5,
        "level": "Beginner",
        "tags": ["savings", "emergency", "universal"],
        "content": """
**What is an emergency fund?**

An emergency fund is money set aside specifically for unexpected financial shocks — a job loss, medical bill, urgent car repair, or any expense you didn't plan for.

**Why it matters**

Without one, an emergency typically means credit card debt or borrowing from family, which creates a cycle of financial stress. An emergency fund is your financial shock absorber.

**How much should you save?**

The universal guideline:
- **Minimum:** 1 month of essential expenses
- **Target:** 3–6 months of essential expenses
- **Higher-risk situations** (self-employed, single income, unstable industry): aim for 6–12 months

Your essential expenses include: rent/mortgage, utilities, food, transport, minimum debt payments, and insurance premiums.

**Where to keep it**

- A separate savings account (makes it harder to spend accidentally)
- High-yield savings account if available in your country (earns some interest)
- Must be liquid — accessible within 1–2 business days

**How to build it step by step**

1. Calculate your monthly essential expenses
2. Set a small automatic transfer each pay period (even $20/week adds up)
3. Direct any windfalls (tax refunds, bonuses) straight to this fund
4. Celebrate milestones (1 month saved, 3 months saved)
5. Do not invest this money — stability beats returns for this fund

**⚠️ Country-specific note:** Interest earned on savings may be taxable depending on your country. Check local rules.
""",
    },
    {
        "id": "budgeting_basics",
        "title": "Budgeting without the guilt",
        "category": "Foundations",
        "duration_min": 7,
        "level": "Beginner",
        "tags": ["budget", "spending", "universal"],
        "content": """
**Why budgets fail — and how to make yours work**

Most budgets fail because they feel like punishment. A good budget is simply a spending plan that reflects your values and reality.

**The 50/30/20 framework** *(universal starting point)*

| Category | % of take-home | Examples |
|---|---|---|
| Needs | 50% | Rent, food, utilities, transport, minimum debt payments |
| Wants | 30% | Dining out, subscriptions, hobbies, clothing |
| Savings/Debt | 20% | Emergency fund, retirement, extra debt payments |

This is a guide, not a law. High cost-of-living cities or low incomes may require different splits.

**Zero-based budgeting** *(alternative approach)*

Assign every currency unit a job. Income − all assigned categories = 0. Forces intentionality.

**Pay yourself first**

Before spending on anything, automatically transfer your savings amount. Treat savings as a non-negotiable expense.

**Tracking options** *(choose the simplest that you'll actually use)*

- Spreadsheet or notebook
- Banking app categories
- Dedicated budgeting app
- Envelope method (cash for each category)

**⚠️ Note:** If 50% of your take-home doesn't cover your needs, the priority is increasing income or reducing fixed costs, not cutting wants.
""",
    },
    {
        "id": "debt_payoff_strategies",
        "title": "Paying off debt: two proven strategies",
        "category": "Debt",
        "duration_min": 6,
        "level": "Beginner",
        "tags": ["debt", "loans", "credit card", "universal"],
        "content": """
**The avalanche method** *(mathematically optimal)*

1. List all debts with their interest rates
2. Pay the minimum on everything
3. Put all extra money toward the **highest interest rate** debt first
4. When it's paid off, roll that payment to the next highest
5. Saves the most money over time

**The snowball method** *(psychologically powerful)*

1. List all debts from smallest balance to largest
2. Pay the minimum on everything
3. Put all extra money toward the **smallest balance** first
4. When paid off, roll that payment to the next smallest
5. Builds momentum through quick wins — research shows this keeps people going

**Which should you choose?**

If you have high-interest debt (credit cards, payday loans): avalanche saves more money.

If you're struggling to stay motivated: snowball wins because you actually stick with it.

**Debt consolidation**

Combining multiple debts into one lower-interest loan can reduce your monthly payment and total interest. Watch out for: extending the term too long, fees, and secured debt risks (putting your home at risk for unsecured debt).

**⚠️ Country-specific note:** Debt collection laws and consumer protections vary widely. In the US, FDCPA protects you from harassment. In the UK, the FCA regulates debt collection. Know your rights.
""",
    },
    {
        "id": "investing_101",
        "title": "Investing 101: starting from zero",
        "category": "Investing",
        "duration_min": 10,
        "level": "Beginner",
        "tags": ["investing", "stocks", "index funds", "universal"],
        "content": """
**Why invest?**

Money in a savings account loses purchasing power to inflation over time. Investing puts your money to work so it grows faster than inflation.

**Key concepts**

- **Compound growth:** Returns on returns. The longer you're invested, the more powerful it becomes. Starting 10 years earlier can double your end result.
- **Risk vs. return:** Higher potential returns come with higher short-term volatility. Time in the market reduces risk.
- **Diversification:** Spreading investments across many assets reduces the damage any single failure can cause.

**Where to start: index funds**

Index funds track a market index (like the S&P 500 or a global index) by owning all or most of its stocks.

Why they're recommended for most people:
- Instant diversification
- Very low fees (expense ratios under 0.20%)
- Historically outperform most actively managed funds over 10+ years
- No stock-picking required

**Tax-advantaged accounts first**

Before investing in a regular brokerage account, maximise any tax-advantaged options available in your country:
- US: 401(k) employer match → Roth IRA → 401(k) remainder
- UK: ISA (£20,000/year tax-free)
- Canada: TFSA, then RRSP
- Australia: Superannuation voluntary contributions
- India: PPF, ELSS, NPS

**What to avoid as a beginner**
- Individual stock picking (needs significant research and risk tolerance)
- Cryptocurrency as a primary savings vehicle (highly volatile)
- Any investment promising guaranteed high returns
- Leveraged or inverse ETFs

**⚠️ This is financial education, not personalised investment advice. Your appropriate investment strategy depends on your goals, timeline, risk tolerance, and local regulations. Consider consulting a licensed financial adviser.**
""",
    },
    {
        "id": "scam_awareness",
        "title": "Protecting yourself from financial scams",
        "category": "Safety",
        "duration_min": 8,
        "level": "Beginner",
        "tags": ["scams", "fraud", "safety", "universal"],
        "content": """
**Why women are disproportionately targeted**

Scammers deliberately target people they perceive as more trusting, isolated, or less experienced with finance. Awareness is your strongest defence.

**Universal red flags — pause if you see ANY of these:**

1. 🚩 **Guaranteed returns** — No legitimate investment guarantees returns. Period.
2. 🚩 **Urgency and pressure** — "Act now or lose this opportunity forever." Legitimate opportunities wait.
3. 🚩 **Unusual payment methods** — Gift cards, cryptocurrency, wire to personal accounts = always a scam.
4. 🚩 **Upfront fees to receive money** — If you need to pay to receive winnings, inheritance, or a job offer, it's a scam.
5. 🚩 **Impersonation** — Calls/emails claiming to be your bank, tax authority, police, or tech support.
6. 🚩 **Romance investment scams (pig butchering)** — New online relationship that eventually involves investment advice. Extremely common and devastatingly effective.
7. 🚩 **Pyramid / MLM schemes** — Income primarily from recruiting, not selling real products.
8. 🚩 **Social media "investment gurus"** — Showing off wealth to sell you courses, signals, or access.

**If you think you've been targeted**

1. Stop all contact and don't send any more money
2. Preserve all evidence (screenshots, emails, transaction records)
3. Contact your bank immediately if money has moved
4. Report to your national financial regulator and/or consumer protection authority
5. Don't be ashamed — these are sophisticated criminal operations

**Verify first, trust later**

Always independently verify anyone asking for financial information or payments by looking up official contact details yourself — never use a phone number or link they provided.
""",
    },
]

# ---------------------------------------------------------------------------
# Conversational AI response templates (used when no LLM is connected)
# ---------------------------------------------------------------------------

DEMO_RESPONSES: dict[str, str] = {
    "greeting": (
        "Hello! I'm Money Tree, your AI-powered financial guide. I'm here to help you build "
        "financial confidence at every stage of life — whether you're just starting out, "
        "navigating a major transition, or planning for the long term.\n\n"
        "Are you interested in exploring the financial topics most relevant to your life stage right now?"
    ),
    "emergency_fund": (
        "An emergency fund is truly the foundation of financial security. "
        "The general guidance is to save 3–6 months of essential living expenses in a liquid, "
        "accessible account — separate from your day-to-day spending. "
        "If that feels overwhelming, start with one month of expenses first. "
        "Even a small cushion dramatically reduces financial stress.\n\n"
        "Would you like to calculate your exact target amount based on your monthly expenses?"
    ),
    "investing": (
        "Investing is one of the most powerful tools for long-term wealth-building — "
        "and it's never too early or too late to start. For most beginners, low-cost index funds "
        "are an excellent starting point: diversified, inexpensive, and historically strong over time. "
        "Before a taxable account, always check if your country offers tax-advantaged options "
        "like PPF, NPS, or ELSS (India), ISAs (UK), or TFSAs (Canada).\n\n"
        "Are you interested in learning more about the tax-advantaged investment accounts available in your country?"
    ),
    "budget": (
        "Budgeting works best when it's honest and flexible. A popular starting framework is "
        "50/30/20: roughly 50% of take-home income on needs, 30% on wants, and 20% toward "
        "savings or debt repayment. These are guides, not rules — the most "
        "important thing is knowing where your money goes and making intentional choices.\n\n"
        "Would you like to walk through building your first monthly budget together?"
    ),
    "debt": (
        "Dealing with debt can feel heavy, but a clear strategy makes it manageable. "
        "Two proven approaches: the **avalanche method** (highest interest rate first — saves the most money) "
        "and the **snowball method** (smallest balance first — builds motivating momentum). "
        "Both work; the best one is whichever you'll actually stick with.\n\n"
        "Would it help to walk through which method fits your specific debt situation?"
    ),
    "scam": (
        "⚠️ Financial scams targeting women are alarmingly common. "
        "Universal red flags: guaranteed returns, urgent pressure to act, payment by gift card or crypto, "
        "and unsolicited contact claiming to be a bank, government, or investment opportunity. "
        "If something feels off, trust that instinct — verify independently before acting.\n\n"
        "Are you interested in learning about the most common financial scams reported in your region right now?"
    ),
    "default": (
        "That's a thoughtful question. Financial decisions depend heavily on your personal "
        "situation, goals, and local regulations. I want to make sure I give you accurate, "
        "relevant guidance tailored to where you are in life.\n\n"
        "Could you tell me a little more about what's on your mind — is there a specific goal, "
        "concern, or financial decision you're working through?"
    ),
}


def get_region(country_code: str) -> str:
    for c in COUNTRIES:
        if c["code"] == country_code:
            return c["region"]
    return "global"


def get_regional_content(country_code: str) -> dict:
    region = get_region(country_code)
    return REGIONAL_CONTENT.get(region, REGIONAL_CONTENT["global"])


def get_country_name(country_code: str) -> str:
    for c in COUNTRIES:
        if c["code"] == country_code:
            return c["name"]
    return "Unknown"


def get_currency(country_code: str) -> str:
    for c in COUNTRIES:
        if c["code"] == country_code:
            return c["currency"]
    return "USD"


def classify_query(text: str) -> str:
    """Naive keyword classifier used when no LLM is available."""
    lower = text.lower()
    if any(w in lower for w in ["hello", "hi", "hey", "start", "begin"]):
        return "greeting"
    if any(w in lower for w in ["emergency", "rainy day", "cushion", "safety net"]):
        return "emergency_fund"
    if any(w in lower for w in ["invest", "stock", "fund", "etf", "portfolio", "index", "equity"]):
        return "investing"
    if any(w in lower for w in ["budget", "spending", "track", "50/30", "money plan"]):
        return "budget"
    if any(w in lower for w in ["debt", "loan", "credit card", "owe", "repay", "payoff", "snowball", "avalanche"]):
        return "debt"
    if any(w in lower for w in ["scam", "fraud", "phishing", "suspicious", "fake", "too good"]):
        return "scam"
    return "default"
