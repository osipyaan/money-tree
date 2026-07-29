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
from core.i18n import t


def _level_badge(level: str) -> str:
    colours = {"Beginner": "#10b981", "Intermediate": "#f59e0b", "Advanced": "#ef4444"}
    return f"<span style='background:{colours.get(level,'#7c3aed')};color:white;border-radius:4px;padding:2px 8px;font-size:0.72rem'>{t(level)}</span>"


def render() -> None:
    state.init()

    st.title(t(":material/library_books: Financial Education"))
    st.caption(
        t("Plain-language guides tailored to your life stage and goals. "
          "All content distinguishes universal principles from country-specific guidance.")
    )

    country = st.session_state.get("profile_country", "IN")
    regional = get_regional_content(country)

    # Regional context banner
    with st.container(border=True):
        st.markdown(t("### :material/place: Guidance for {country}").format(country=get_country_name(country)))
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(t("**:material/account_balance: Tax & retirement:**\n\n{note}").format(note=regional.get("tax_note", "")))
            st.markdown(t("**:material/credit_score: Credit:**\n\n{note}").format(note=regional.get("credit_note", "")))
        with col2:
            st.markdown(t("**:material/elderly: Retirement programmes:**\n\n{note}").format(note=regional.get("retirement_programs", "")))
            st.error(t("**:material/security: Scam watch:**\n\n{note}").format(note=regional.get("scam_alert", "")), icon=None)

    st.info(
        t(":material/newspaper: **Latest financial news** is on the **News** page in the sidebar "
          "under Tools — headlines tailored to your country."),
        icon=None,
    )

    st.divider()

    # ── Filter controls ──────────────────────────────────────────────────────
    with st.container(horizontal=True):
        search = st.text_input(
            t("Search modules"),
            placeholder="Search by topic or keyword…",
            label_visibility="collapsed",
        )
        category_options_en = ["All"] + sorted(set(m["category"] for m in EDUCATION_MODULES))
        category_options_display = [t(c) for c in category_options_en]
        selected_category_display = st.selectbox(
            t("Category"),
            category_options_display,
            label_visibility="collapsed",
        )
        selected_category = category_options_en[category_options_display.index(selected_category_display)]

        level_options_en = ["All levels", "Beginner", "Intermediate", "Advanced"]
        level_options_display = [t(lv) for lv in level_options_en]
        selected_level_display = st.selectbox(
            t("Level"),
            level_options_display,
            label_visibility="collapsed",
        )
        selected_level = level_options_en[level_options_display.index(selected_level_display)]

    # Filter modules
    filtered = EDUCATION_MODULES
    if search.strip():
        q = search.lower()
        filtered = [
            m for m in filtered
            if q in m["title"].lower() or q in m["content"].lower()
            or any(q in tag for tag in m["tags"])
        ]
    if selected_category != "All":
        filtered = [m for m in filtered if m["category"] == selected_category]
    if selected_level != "All levels":
        filtered = [m for m in filtered if m["level"] == selected_level]

    st.caption(t("{n} module{suffix} found").format(n=len(filtered), suffix="s" if len(filtered) != 1 else ""))

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
        st.info(t("No modules match your search. Try different keywords."), icon=":material/search:")
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
                    f":material/category: {t(module['category'])}  ·  "
                    f":material/schedule: {t('{duration} min read').format(duration=module['duration_min'])}  ·  "
                    f"{t('Tags: {tags}').format(tags=', '.join(module['tags'][:3]))}"
                )
                btn_col, dl_col = st.columns([3, 1])
                with btn_col:
                    if st.button(
                        t(":material/open_in_new: Read"),
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
                            help=t("Save for offline access"),
                        ):
                            st.session_state.downloaded_modules = downloaded + [module["id"]]
                            st.toast(t("'{title}' saved for offline access.").format(title=module["title"]), icon=":material/download:")
                    else:
                        st.caption(t("📥 Offline"))


def _render_module_detail(module_id: str) -> None:
    module = next((m for m in EDUCATION_MODULES if m["id"] == module_id), None)
    if not module:
        st.error(t("Module not found."))
        st.session_state.open_module = None
        st.rerun()
        return

    if st.button(t(":material/arrow_back: Back to library")):
        st.session_state.open_module = None
        st.rerun()

    st.divider()
    st.markdown(
        f"## {module['title']} "
        f"{_level_badge(module['level'])}",
        unsafe_allow_html=True,
    )
    st.caption(
        f":material/category: {t(module['category'])}  ·  "
        f":material/schedule: {t('{duration} min read').format(duration=module['duration_min'])}"
    )
    tags_str = " · ".join(f"`{tag}`" for tag in module["tags"])
    st.caption(t("Tags: {tags}").format(tags=tags_str))

    st.divider()
    st.markdown(module["content"])

    st.divider()
    country = st.session_state.get("profile_country", "US")
    regional = get_regional_content(country)

    with st.expander(t(":material/place: How this applies in {country}").format(country=get_country_name(country))):
        st.markdown(t("**Tax & savings:** {note}").format(note=regional.get("tax_note", "")))
        st.markdown(t("**Credit:** {note}").format(note=regional.get("credit_note", "")))
        st.markdown(t("**Retirement:** {note}").format(note=regional.get("retirement_programs", "")))
        st.warning(t("**Scam watch:** {note}").format(note=regional.get("scam_alert", "")), icon=":material/security:")

    st.divider()
    # Ask the assistant about this topic
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(
            t(":material/auto_awesome: Ask Money Tree about this topic"),
            type="primary",
        ):
            state.add_message(
                "user",
                t("I just read about '{title}'. Can you help me understand "
                  "how it applies to my specific situation?").format(title=module["title"]),
            )
            st.switch_page("app_pages/assistant.py")
    with col_b:
        downloaded = st.session_state.get("downloaded_modules", [])
        if module["id"] not in downloaded:
            if st.button(t(":material/download: Save for offline")):
                st.session_state.downloaded_modules = downloaded + [module["id"]]
                st.toast(t("Saved for offline access."), icon=":material/download:")
        else:
            st.success(t(":material/check: Saved for offline access"))


# ── Module-level call required by st.Page ────────────────────────────────────
render()
