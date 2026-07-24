"""
app_pages/news.py — Country-specific financial news headlines.

Pulls live headlines from Google News RSS, cached for 30 minutes.
"""

from __future__ import annotations

import streamlit as st
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from core import state, ai
from core.data import get_country_name, get_regional_content, LIFE_STAGES, PRESET_GOALS


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_news(country_code: str) -> list[dict]:
    return ai.fetch_financial_news(country_code, max_items=8)


def _get_life_stage_label() -> str:
    ls_id = st.session_state.get("profile_life_stage", "early_career")
    for ls in LIFE_STAGES:
        if ls["id"] == ls_id:
            return ls["label"]
    return ls_id.replace("_", " ").title()


def _get_goal_labels() -> list[str]:
    labels = []
    for g in st.session_state.get("profile_goals", []):
        for pg in PRESET_GOALS:
            if pg["id"] == g:
                labels.append(pg["label"])
    labels += st.session_state.get("profile_custom_goals", [])
    return labels


def _build_system_prompt() -> str:
    country = st.session_state.get("profile_country", "US")
    language = st.session_state.get("profile_language", "en")
    regional = get_regional_content(country)
    return ai.build_system_prompt(
        country=get_country_name(country),
        language=language,
        life_stage=_get_life_stage_label(),
        goals=_get_goal_labels(),
        knowledge_level=st.session_state.get("knowledge_level", "beginner"),
        regional_content=regional,
    )


def _analyze_headline(title: str) -> str:
    question = (
        f'A financial news headline just came up: "{title}". '
        "In 2-3 short sentences, explain why this might matter for someone in my situation "
        "and give one concrete takeaway. Don't just restate the headline."
    )
    response = ai.generate_response(
        user_message=question,
        conversation_history=[],
        system_prompt=_build_system_prompt(),
        stream=False,
    )
    if hasattr(response, "__iter__") and not isinstance(response, str):
        response = "".join(response)
    return response


def render() -> None:
    state.init()

    country = st.session_state.get("profile_country", "IN")

    st.title(":material/newspaper: Financial News")
    st.caption(
        f"Latest headlines relevant to {get_country_name(country)}. "
        "Stories open in a new tab — always verify with official sources."
    )

    col_refresh, col_country = st.columns([1, 3])
    with col_refresh:
        if st.button(":material/refresh: Refresh", type="secondary"):
            _cached_news.clear()
            st.rerun()
    with col_country:
        st.caption(f":material/place: Showing news for **{get_country_name(country)}**")

    st.divider()

    with st.spinner("Loading latest headlines…"):
        news_items = _cached_news(country)

    if news_items:
        for idx, item in enumerate(news_items):
            with st.container(border=True):
                pub = item.get("published", "")
                pub_short = pub[:16] if pub else ""
                st.markdown(f"**[{item['title']}]({item['link']})**")
                if pub_short:
                    st.caption(pub_short)

                analysis_key = f"news_analysis_{item['link']}"
                cached_analysis = st.session_state.get(analysis_key)
                if cached_analysis:
                    st.info(f"**What this means for you:** {cached_analysis}", icon=":material/psychology:")
                elif st.button(
                    "What does this mean for me?",
                    icon=":material/psychology:",
                    key=f"analyze_btn_{idx}",
                ):
                    with st.spinner("Analysing for your situation…"):
                        st.session_state[analysis_key] = _analyze_headline(item["title"])
                    st.rerun()
    else:
        st.info(
            "Headlines unavailable right now — check your internet connection and try refreshing.",
            icon=":material/wifi_off:",
        )

    st.divider()
    st.caption(
        "*Source: Google News RSS. Headlines are for awareness only and do not "
        "constitute financial advice.*"
    )


render()
