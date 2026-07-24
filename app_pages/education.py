"""
app_pages/education.py — Localised financial education library.

Features:
- Searchable module catalog
- Module detail view with full content
- "Download for offline" tracking
- Life stage and goal filtering
- Regional context banner
"""

from __future__ import annotations

import streamlit as st
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from core import state
from core.data import (
    EDUCATION_MODULES, get_regional_content, get_country_name,
)


def _level_badge(level: str) -> str:
    colours = {"Beginner": "#10b981", "Intermediate": "#f59e0b", "Advanced": "#ef4444"}
    return f"<span style='background:{colours.get(level,'#7c3aed')};color:white;border-radius:4px;padding:2px 8px;font-size:0.72rem'>{level}</span>"


def render() -> None:
    state.init()

    st.title(":material/library_books: Financial Education")
    st.caption(
        "Plain-language guides tailored to your life stage and goals. "
        "All content distinguishes universal principles from country-specific guidance."
    )

    country = st.session_state.get("profile_country", "IN")
    regional = get_regional_content(country)

    # Regional context banner
    with st.container(border=True):
        st.markdown(f"### :material/place: Guidance for {get_country_name(country)}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**:material/account_balance: Tax & retirement:**\n\n{regional.get('tax_note','')}")
            st.markdown(f"**:material/credit_score: Credit:**\n\n{regional.get('credit_note','')}")
        with col2:
            st.markdown(f"**:material/elderly: Retirement programmes:**\n\n{regional.get('retirement_programs','')}")
            st.error(f"**:material/security: Scam watch:**\n\n{regional.get('scam_alert','')}", icon=None)

    st.info(
        ":material/newspaper: **Latest financial news** is on the **News** page in the sidebar "
        "under Tools — headlines tailored to your country.",
        icon=None,
    )

    st.divider()

    # ── Filter controls ──────────────────────────────────────────────────────
    with st.container(horizontal=True):
        search = st.text_input(
            "Search modules",
            placeholder="Search by topic or keyword…",
            label_visibility="collapsed",
        )
        category_options = ["All"] + sorted(set(m["category"] for m in EDUCATION_MODULES))
        selected_category = st.selectbox(
            "Category",
            category_options,
            label_visibility="collapsed",
        )
        level_options = ["All levels", "Beginner", "Intermediate", "Advanced"]
        selected_level = st.selectbox(
            "Level",
            level_options,
            label_visibility="collapsed",
        )

    # Filter modules
    filtered = EDUCATION_MODULES
    if search.strip():
        q = search.lower()
        filtered = [
            m for m in filtered
            if q in m["title"].lower() or q in m["content"].lower()
            or any(q in t for t in m["tags"])
        ]
    if selected_category != "All":
        filtered = [m for m in filtered if m["category"] == selected_category]
    if selected_level != "All levels":
        filtered = [m for m in filtered if m["level"] == selected_level]

    st.caption(f"{len(filtered)} module{'s' if len(filtered) != 1 else ''} found")

    # ── Module catalog ────────────────────────────────────────────────────────
    if "open_module" not in st.session_state:
        st.session_state.open_module = None

    if st.session_state.open_module:
        _render_module_detail(st.session_state.open_module)
    else:
        _render_module_grid(filtered)


def _render_module_grid(modules: list[dict]) -> None:
    downloaded = st.session_state.get("downloaded_modules", [])

    if not modules:
        st.info("No modules match your search. Try different keywords.", icon=":material/search:")
        return

    cols = st.columns(2)
    for i, module in enumerate(modules):
        with cols[i % 2]:
            with st.container(border=True):
                is_downloaded = module["id"] in downloaded
                offline_badge = " 📥" if is_downloaded else ""
                st.markdown(
                    f"**{module['title']}**{offline_badge} "
                    f"{_level_badge(module['level'])}",
                    unsafe_allow_html=True,
                )
                st.caption(
                    f":material/category: {module['category']}  ·  "
                    f":material/schedule: {module['duration_min']} min read  ·  "
                    f"Tags: {', '.join(module['tags'][:3])}"
                )
                btn_col, dl_col = st.columns([3, 1])
                with btn_col:
                    if st.button(
                        ":material/open_in_new: Read",
                        key=f"open_{module['id']}",
                        type="primary",
                    ):
                        st.session_state.open_module = module["id"]
                        st.rerun()
                with dl_col:
                    if not is_downloaded:
                        if st.button(
                            ":material/download:",
                            key=f"dl_{module['id']}",
                            help="Save for offline access",
                        ):
                            st.session_state.downloaded_modules = downloaded + [module["id"]]
                            st.toast(f"'{module['title']}' saved for offline access.", icon=":material/download:")
                    else:
                        st.caption("📥 Offline")


def _render_module_detail(module_id: str) -> None:
    module = next((m for m in EDUCATION_MODULES if m["id"] == module_id), None)
    if not module:
        st.error("Module not found.")
        st.session_state.open_module = None
        st.rerun()
        return

    if st.button(":material/arrow_back: Back to library"):
        st.session_state.open_module = None
        st.rerun()

    st.divider()
    st.markdown(
        f"## {module['title']} "
        f"{_level_badge(module['level'])}",
        unsafe_allow_html=True,
    )
    st.caption(
        f":material/category: {module['category']}  ·  "
        f":material/schedule: {module['duration_min']} min read"
    )
    tags_str = " · ".join(f"`{t}`" for t in module["tags"])
    st.caption(f"Tags: {tags_str}")

    st.divider()
    st.markdown(module["content"])

    st.divider()
    country = st.session_state.get("profile_country", "US")
    regional = get_regional_content(country)

    with st.expander(f":material/place: How this applies in {get_country_name(country)}"):
        st.markdown(f"**Tax & savings:** {regional.get('tax_note','')}")
        st.markdown(f"**Credit:** {regional.get('credit_note','')}")
        st.markdown(f"**Retirement:** {regional.get('retirement_programs','')}")
        st.warning(f"**Scam watch:** {regional.get('scam_alert','')}", icon=":material/security:")

    st.divider()
    # Ask the assistant about this topic
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(
            ":material/auto_awesome: Ask Money Tree about this topic",
            type="primary",
        ):
            state.add_message(
                "user",
                f"I just read about '{module['title']}'. Can you help me understand "
                f"how it applies to my specific situation?",
            )
            st.switch_page("app_pages/assistant.py")
    with col_b:
        downloaded = st.session_state.get("downloaded_modules", [])
        if module["id"] not in downloaded:
            if st.button(":material/download: Save for offline"):
                st.session_state.downloaded_modules = downloaded + [module["id"]]
                st.toast("Saved for offline access.", icon=":material/download:")
        else:
            st.success(":material/check: Saved for offline access")


# ── Module-level call required by st.Page ────────────────────────────────────
render()
