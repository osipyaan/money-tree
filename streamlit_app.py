"""
streamlit_app.py — Money Tree entry point.

Multi-page navigation with st.navigation / st.Page.
Handles onboarding gate, theme injection, accessibility CSS, and global state init.
"""

from __future__ import annotations

import sys, pathlib

APP_ROOT = pathlib.Path(__file__).parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

# Load OPENAI_API_KEY (and any other secrets) from a local .env file, if present.
# .env is gitignored — never commit real keys.
try:
    from dotenv import load_dotenv
    load_dotenv(APP_ROOT / ".env")
except ImportError:
    pass

import streamlit as st
from core import state

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Money Tree — Financial Guide for Women",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": (
            "**Money Tree** — AI-powered financial literacy assistant for women worldwide.\n\n"
            "Provides financial *education* only. Not a substitute for professional advice.\n\n"
            "Made with IBM Bob."
        ),
    },
)

# ── Global state init ─────────────────────────────────────────────────────────
state.init()

# ── Theme definitions ─────────────────────────────────────────────────────────
THEMES: dict[str, dict] = {
    "purple": {
        "label": "💜 Original Purple",
        "short_label": "💜 Purple",
        "primary": "#7c3aed",
        "bg": "#ffffff",
        "surface": "#f5f3ff",
        "text": "#1e1b2e",
        "muted": "#57606a",
        "border": "#e5e7eb",
        "sidebar_bg": "#f5f3ff",
        "font_family": "'Quicksand', -apple-system, 'Segoe UI', system-ui, sans-serif",
        "extra_css": """
            h1, h2, h3, h4,
            [data-testid="stHeadingWithActionElements"] *:not([data-testid="stIconMaterial"]):not([role="img"]) {
                font-family: 'Baloo 2', 'Quicksand', cursive, sans-serif !important;
                font-weight: 700 !important;
            }
        """,
    },
    "pink": {
        "label": "🌸 Soft Pink",
        "short_label": "🌸 Pink",
        "primary": "#d946a8",
        "bg": "#fff5fb",
        "surface": "#fce7f3",
        "text": "#4a1536",
        "muted": "#8a4070",
        "border": "#fbcfe8",
        "sidebar_bg": "#fce7f3",
        "font_family": "'Georgia', 'Palatino Linotype', serif",
        "extra_css": """
            h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                font-family: 'Georgia', serif !important;
                font-style: italic;
                letter-spacing: 0.02em;
            }
            [data-testid="stSidebarContent"] h1,
            [data-testid="stSidebarContent"] strong {
                font-family: 'Georgia', serif !important;
                font-style: italic;
            }
        """,
    },
    "lofi": {
        "label": "🎧 Lo-fi Blue",
        "short_label": "🎧 Lo-fi",
        "primary": "#3b6fd4",
        "bg": "#0f1923",
        "surface": "#1a2638",
        "text": "#c8d8e8",
        "muted": "#7a9bb5",
        "border": "#2a3f55",
        "sidebar_bg": "#131e2b",
        "font_family": "'Courier New', 'Consolas', monospace",
        "extra_css": """
            h1, h2, h3 { letter-spacing: 0.04em; font-weight: 500 !important; }
            [data-testid="stVerticalBlockBorderWrapper"] { border-color: #2a4a6a !important; }
            .stChatMessage { background: #1a2638 !important; border: 1px solid #2a3f55; border-radius: 8px; }
            input, textarea { background: #1a2638 !important; }
        """,
    },
    "bw": {
        "label": "🖤 Black & White",
        "short_label": "🖤 B&W",
        "primary": "#111111",
        "bg": "#ffffff",
        "surface": "#f4f4f4",
        "text": "#111111",
        "muted": "#555555",
        "border": "#cccccc",
        "sidebar_bg": "#f4f4f4",
        "font_family": "'Helvetica Neue', 'Arial', sans-serif",
        "extra_css": """
            h1, h2, h3 { font-weight: 900 !important; letter-spacing: -0.02em; }
            .stButton button { border: 2px solid #111 !important; border-radius: 0 !important; }
            [data-testid="stVerticalBlockBorderWrapper"] {
                border: 1.5px solid #111 !important;
                border-radius: 0 !important;
            }
        """,
    },
}


def _inject_theme_css() -> None:
    theme_key = st.session_state.get("active_theme", "purple")
    t = THEMES.get(theme_key, THEMES["purple"])

    # Dark surface detection (lo-fi theme has dark bg)
    is_dark = theme_key == "lofi"

    # Streamlit renders material icons under several different markers
    # depending on context (button/heading icon= param, inline ":material/x:"
    # shortcodes in markdown/labels, or st.info/warning/success icon= param).
    # Exclude all of them from font-family overrides so their ligatures
    # keep resolving to glyphs instead of falling back to literal text.
    ICON = ':not([data-testid="stIconMaterial"]):not([data-testid="stAlertDynamicIcon"]):not([role="img"])'

    st.html(f"""
    <style>
    /* ── Whimsical type pairing ───────────────────────────────
       Baloo 2: bubbly, rounded display font for headings/buttons.
       Quicksand: friendly rounded sans for body text. ────────── */
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Quicksand:wght@400;500;600;700&display=swap');

    /* ── Base reset ───────────────────────────────────────── */
    footer {{ visibility: hidden; }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 18px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}

    /* ── App background & text ────────────────────────────── */
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"] {{
        background: {t['bg']} !important;
    }}
    section[data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {{
        background: {t['sidebar_bg']} !important;
        border-right: 1px solid {t['border']} !important;
    }}

    /* ── Typography ───────────────────────────────────────── */
    html, body,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stText"],
    [data-testid="stHeadingWithActionElements"] *,
    h1, h2, h3, h4, p, li,
    span {{
        color: {t['text']} !important;
    }}
    [data-testid="stMarkdownContainer"] *{ICON},
    [data-testid="stHeadingWithActionElements"] *{ICON},
    span{ICON},
    html, body, [data-testid="stText"], h1, h2, h3, h4, p, li {{
        font-family: {t['font_family']} !important;
    }}

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {{
        color: {t['muted']} !important;
    }}
    [data-testid="stCaptionContainer"]{ICON},
    [data-testid="stCaptionContainer"] *{ICON} {{
        font-family: {t['font_family']} !important;
    }}

    /* ── Material icons (must keep ligature font) ─────────── */
    [data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"] *,
    [data-testid="stAlertDynamicIcon"],
    [role="img"] {{
        font-family: "Material Symbols Rounded" !important;
        font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
    }}

    /* ── Sidebar text ─────────────────────────────────────── */
    [data-testid="stSidebarContent"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebarContent"] [data-testid="stMarkdownContainer"] *,
    [data-testid="stSidebarContent"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebarContent"] [data-testid="stCaptionContainer"] * {{
        color: {t['text']} !important;
    }}

    /* ── Widget labels ────────────────────────────────────── */
    [data-testid="stWidgetLabel"] *,
    label {{
        color: {t['text']} !important;
    }}
    [data-testid="stWidgetLabel"] *{ICON},
    label{ICON} {{
        font-family: {t['font_family']} !important;
    }}

    /* ── Layout: prevent text crowding ────────────────────── */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    .stChatMessage [data-testid="stMarkdownContainer"] p {{
        overflow-wrap: anywhere;
        word-break: break-word;
    }}
    .stButton button {{
        white-space: normal;
        line-height: 1.4;
    }}

    /* ── Metric ───────────────────────────────────────────── */
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricValue"] * {{
        color: {t['text']} !important;
    }}

    /* ── Inputs ───────────────────────────────────────────── */
    input, textarea, select {{
        background: {t['surface']} !important;
        color: {t['text']} !important;
        border-color: {t['border']} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stChatInput"] {{
        border-radius: 999px !important;
    }}

    /* ── Chat messages ────────────────────────────────────── */
    .stChatMessage [data-testid="stMarkdownContainer"],
    .stChatMessage [data-testid="stMarkdownContainer"] * {{
        color: {t['text']} !important;
    }}
    .stChatMessage [data-testid="stMarkdownContainer"]{ICON},
    .stChatMessage [data-testid="stMarkdownContainer"] *{ICON} {{
        font-family: {t['font_family']} !important;
    }}

    /* ── Cards / containers ───────────────────────────────── */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: {t['surface']} !important;
        border-color: {t['border']} !important;
    }}

    /* ── Buttons ──────────────────────────────────────────────
       Secondary/default buttons keep Streamlit's own light
       background unless we set one explicitly — pair it with
       the theme's surface + text colours so contrast always
       holds, even for the dark lo-fi theme or high-contrast
       mode below. ─────────────────────────────────────────── */
    .stButton button {{
        background: {t['surface']} !important;
        border-color: {t['border']} !important;
        color: {t['text']} !important;
        border-radius: 999px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 14px rgba(0,0,0,0.12);
    }}
    .stButton button:active {{
        transform: translateY(0);
    }}
    .stButton button[kind="primary"] {{
        background: {t['primary']} !important;
        border-color: {t['primary']} !important;
        color: #ffffff !important;
        border-radius: 999px !important;
        box-shadow: 0 3px 10px {t['primary']}66;
    }}

    /* ── Theme extra ──────────────────────────────────────── */
    {t['extra_css']}
    </style>
    """)

    # Accessibility / large text overlay (applied on top of theme)
    if st.session_state.get("accessibility_mode") or st.session_state.get("large_text"):
        st.html("""
        <style>
        html, body,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stText"], .stChatMessage p,
        label, .stSelectbox label, .stTextInput label {
            font-size: 19px !important;
            line-height: 1.8 !important;
        }
        .stButton button {
            font-size: 17px !important;
            padding: 0.6rem 1.4rem !important;
            min-height: 48px !important;
        }
        </style>
        """)

    if st.session_state.get("high_contrast"):
        st.html("""
        <style>
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewBlockContainer"],
        section[data-testid="stSidebar"],
        [data-testid="stSidebarContent"],
        .stChatMessage { background: #000000 !important; }

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] *,
        [data-testid="stText"],
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] *,
        .stChatMessage [data-testid="stMarkdownContainer"],
        .stChatMessage [data-testid="stMarkdownContainer"] *,
        h1, h2, h3, h4, h5, h6, p, li,
        span:not([data-testid="stIconMaterial"]), label,
        [data-testid="stHeadingWithActionElements"] *:not([data-testid="stIconMaterial"]),
        [data-testid="stWidgetLabel"] *:not([data-testid="stIconMaterial"]),
        [data-testid="stMetricLabel"] *,
        [data-testid="stMetricValue"] *,
        [data-testid="stSidebarContent"] [data-testid="stMarkdownContainer"] *:not([data-testid="stIconMaterial"]),
        [data-testid="stSidebarContent"] [data-testid="stCaptionContainer"] *:not([data-testid="stIconMaterial"]) {
            color: #ffffff !important;
        }
        [data-testid="stIconMaterial"],
        [data-testid="stIconMaterial"] *,
        [data-testid="stAlertDynamicIcon"],
        [data-testid="stAlertDynamicIcon"] * {
            font-family: "Material Symbols Rounded" !important;
            color: #ffffff !important;
        }
        /* Secondary/default buttons: give them a black background AND force
           the label text white. The theme block above sets its own
           ".stButton button { color: {theme text} }" at equal specificity,
           so background-only overrides here were being cancelled out by
           that leftover (often dark) text colour — explicitly repaint the
           label (and any nested p/span) so it can never inherit it. */
        .stButton button,
        .stButton button p,
        .stButton button span:not([data-testid="stIconMaterial"]) {
            color: #ffffff !important;
        }
        .stButton button {
            background: #000000 !important;
            border-color: #ffffff !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #111111 !important;
            border-color: #ffffff !important;
        }
        /* Alert boxes (st.info / st.warning / st.success / st.error) keep
           Streamlit's default light tint unless repainted here — their text
           was already being forced white by the rules above, which left
           white-on-white/near-white alerts. Give the container a dark
           background so the (already white) text stays legible. */
        [data-testid="stAlertContainer"] {
            background: #111111 !important;
            border: 1px solid #ffffff !important;
        }
        [data-testid="stAlertContentInfo"],
        [data-testid="stAlertContentInfo"] *:not([data-testid="stIconMaterial"]),
        [data-testid="stAlertContentWarning"],
        [data-testid="stAlertContentWarning"] *:not([data-testid="stIconMaterial"]),
        [data-testid="stAlertContentSuccess"],
        [data-testid="stAlertContentSuccess"] *:not([data-testid="stIconMaterial"]),
        [data-testid="stAlertContentError"],
        [data-testid="stAlertContentError"] *:not([data-testid="stIconMaterial"]) {
            color: #ffffff !important;
        }
        input, textarea, select {
            background: #111111 !important;
            color: #ffffff !important;
            border-color: #888888 !important;
        }
        a { color: #7dd3fc !important; }
        </style>
        """)

    if st.session_state.get("reduced_motion"):
        st.html("""
        <style>
        *, *::before, *::after {
            animation-duration: 0.001ms !important;
            transition-duration: 0.001ms !important;
        }
        </style>
        """)

_inject_theme_css()

# ── Onboarding gate ───────────────────────────────────────────────────────────
if not st.session_state.get("onboarding_complete"):
    from app_pages import onboarding
    onboarding.render()
    st.stop()

# ── Main navigation ───────────────────────────────────────────────────────────
pg_assistant = st.Page(
    "app_pages/assistant.py",
    title="AI Assistant",
    icon=":material/auto_awesome:",
    default=True,
)
pg_education = st.Page(
    "app_pages/education.py",
    title="Learn",
    icon=":material/library_books:",
)
pg_news = st.Page(
    "app_pages/news.py",
    title="News",
    icon=":material/newspaper:",
)
pg_budgeting = st.Page(
    "app_pages/budgeting.py",
    title="Budget & Goals",
    icon=":material/account_balance_wallet:",
)
pg_settings = st.Page(
    "app_pages/settings.py",
    title="Settings",
    icon=":material/settings:",
)

pg = st.navigation(
    {
        "Money Tree": [pg_assistant],
        "Tools": [pg_education, pg_news, pg_budgeting],
        "Account": [pg_settings],
    }
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
from core.data import get_country_name, get_regional_content, LIFE_STAGES
from core import ai as _ai

with st.sidebar:
    t = THEMES.get(st.session_state.get("active_theme", "purple"), THEMES["purple"])

    _ff = t["font_family"]
    _muted = t["muted"]
    st.markdown(
        f"<div style='padding:1.1rem 0.75rem; text-align:center; border-radius:20px; "
        f"margin-bottom:0.6rem; overflow:hidden; position:relative; "
        f"background:repeating-linear-gradient(135deg, {t['surface']} 0 16px, {t['bg']} 16px 32px); "
        f"box-shadow:0 2px 10px rgba(0,0,0,0.07); border:1px solid {t['border']};'>"
        f"<span style='font-size:2rem'>🌳</span> "
        f"<strong style=\"font-size:1.25rem; font-family:'Baloo 2','Quicksand',{_ff}; color:{t['text']}\">Money Tree</strong><br>"
        f"<span style='font-size:0.75rem; color:{_muted}'>✨ Financial guide for women ✨</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Personalised, page-aware greeting ────────────────────────────────────
    _name = st.session_state.get("profile_name", "").strip()
    _country = st.session_state.get("profile_country", "IN")
    _stage_id = st.session_state.get("profile_life_stage", "early_career")
    _stage_label = next((ls["label"] for ls in LIFE_STAGES if ls["id"] == _stage_id), _stage_id)

    _cur_page = pg.title if hasattr(pg, "title") else ""
    if _cur_page == "Learn":
        _greeting_suffix = "ready to learn more? 📚"
    elif _cur_page == "News":
        _greeting_suffix = "here's what's happening in finance 📰"
    elif _cur_page == "AI Assistant":
        _greeting_suffix = "ready to take your financial goals further? 💜"
    elif _cur_page == "Budget & Goals":
        _greeting_suffix = "let's check in on your goals 🎯"
    else:
        _greeting_suffix = "great to see you 👋"

    if _name:
        st.markdown(f"**Hi {_name},** {_greeting_suffix}")
    else:
        st.markdown(f"**Welcome back —** {_greeting_suffix}")

    st.caption(f":material/place: {get_country_name(_country)}  ·  {_stage_label}")

    if st.session_state.get("privacy_mode"):
        st.caption(":material/visibility_off: Privacy mode on")

    # ── Theme switcher (inline, immediate) ───────────────────────────────────
    st.divider()
    st.markdown("**🎨 Theme**")
    theme_cols = st.columns(2)
    for idx, (tkey, tval) in enumerate(THEMES.items()):
        with theme_cols[idx % 2]:
            is_active = st.session_state.get("active_theme") == tkey
            if st.button(
                tval["short_label"],
                key=f"theme_btn_{tkey}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
                help=tval["label"],
            ):
                st.session_state.active_theme = tkey
                st.rerun()

    # ── Regional scam alert ───────────────────────────────────────────────────
    st.divider()
    _regional = get_regional_content(_country)
    st.info(
        f"**:material/security: Scam watch — {get_country_name(_country)}:**\n\n"
        f"{_regional.get('scam_alert', '')}",
        icon=None,
    )

    # ── AI provider status ────────────────────────────────────────────────────
    st.divider()
    _caps = _ai.capability_report()
    st.caption(f"🤖 **LLM:** {_caps['llm']}")
    if st.session_state.get("voice_enabled"):
        st.caption(f"🎙️ **STT:** {_caps['stt']}")
        st.caption(f"🔊 **TTS:** {_caps['tts']}")

    st.divider()
    if st.button(":material/delete_forever: Clear chat history", type="secondary", key="global_clear_history"):
        from core.state import clear_all_history
        clear_all_history()
        st.rerun()

pg.run()

# ── Persistent footer ─────────────────────────────────────────────────────────
t = THEMES.get(st.session_state.get("active_theme", "purple"), THEMES["purple"])
st.html(f"""
<div style="text-align:center;color:{t['muted']};font-size:0.72rem;
            border-top:1px solid {t['border']};margin-top:3rem;padding-top:0.75rem;
            font-family:{t['font_family']}">
  Money Tree provides financial education only — not personalised financial advice.<br>
  Always consult a qualified professional for decisions specific to your situation and jurisdiction.<br><br>
  <em>Made with IBM Bob</em>
</div>
""")
