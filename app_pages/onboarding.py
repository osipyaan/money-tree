"""
app_pages/onboarding.py — Step-by-step onboarding flow.

Steps:
  1. Welcome + language/country selection
  2. Life stage selection
  3. Financial goals selection (preset + custom)
  4. Accessibility preferences
  5. Privacy preferences
  6. Completion → redirect to assistant
"""

from __future__ import annotations

import streamlit as st

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from core import state
from core.data import (
    COUNTRIES, LANGUAGES, LIFE_STAGES, PRESET_GOALS, AGE_RANGES,
)

_STAGE_EMOJI = {
    "student": "🎓",
    "early_career": "💼",
    "parent": "👨‍👩‍👧",
    "immigrant": "✈️",
    "entrepreneur": "🏪",
    "caregiver": "🤝",
    "pre_retirement": "📈",
    "retiree": "🌅",
}


def _apply_accessibility_css() -> None:
    if st.session_state.get("accessibility_mode"):
        st.html("""
        <style>
        html, body, [class*="css"] {
            font-size: 19px !important;
        }
        .stButton > button {
            font-size: 17px !important;
            padding: 0.6rem 1.2rem !important;
        }
        </style>
        """)


def render() -> None:
    state.init()
    _apply_accessibility_css()

    step = st.session_state.get("onboarding_step", 1)

    # ── Scroll to top on every step transition ───────────────────────────────
    st.html("""
    <script>
    (function() {
        var el = window.parent.document.querySelector('[data-testid="stAppViewBlockContainer"]');
        if (el) el.scrollTop = 0;
    })();
    </script>
    """)

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(
        "<div style='text-align:center; padding:1.5rem 1rem; border-radius:24px; margin-bottom:0.5rem; "
        "background:repeating-linear-gradient(135deg, #f5f3ff 0 18px, #ffffff 18px 36px); "
        "box-shadow:0 2px 14px rgba(0,0,0,0.06); position:relative;'>"
        "<span style='position:absolute; top:12px; left:18px; font-size:1.2rem'>⭐</span>"
        "<span style='position:absolute; top:16px; right:20px; font-size:1rem'>✨</span>"
        "<h1 style='margin-bottom:0'>🌳 Money Tree</h1>"
        "<p style='color:#7c3aed; font-size:1.05rem; margin-top:0.2rem; font-weight:600'>"
        "Your AI financial guide, built for women worldwide</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Progress bar
    progress_pct = (step - 1) / 5
    st.progress(progress_pct, text=f"Step {step} of 5")
    st.divider()

    # ── Step 1 — Name, Country & Language ───────────────────────────────────
    if step == 1:
        st.subheader(":material/language: Let's get to know you")
        st.caption(
            "Your name is only stored on this device and is never sent anywhere. "
            "Country and language help us tailor content to your region."
        )

        first_name = st.text_input(
            "Your first name *(optional)*",
            value=st.session_state.get("profile_name", ""),
            placeholder="e.g., Amara",
        )

        col1, col2 = st.columns(2)
        with col1:
            country_names = [c["name"] for c in COUNTRIES]
            current_country_name = next(
                (c["name"] for c in COUNTRIES if c["code"] == st.session_state.profile_country),
                COUNTRIES[0]["name"],
            )
            selected_country_name = st.selectbox(
                "Country / region",
                country_names,
                index=country_names.index(current_country_name),
            )
            selected_country_code = next(
                c["code"] for c in COUNTRIES if c["name"] == selected_country_name
            )

        with col2:
            lang_names = [l["name"] for l in LANGUAGES]
            current_lang_name = next(
                (l["name"] for l in LANGUAGES if l["code"] == st.session_state.profile_language),
                LANGUAGES[0]["name"],
            )
            selected_lang_name = st.selectbox(
                "Preferred language",
                lang_names,
                index=lang_names.index(current_lang_name),
            )
            selected_lang_code = next(
                l["code"] for l in LANGUAGES if l["name"] == selected_lang_name
            )

        age = st.selectbox(
            "Age range *(optional — helps us tailor guidance)*",
            AGE_RANGES,
            index=AGE_RANGES.index(st.session_state.profile_age_range)
            if st.session_state.profile_age_range in AGE_RANGES
            else 2,
        )

        if st.button("Continue", type="primary", icon=":material/arrow_forward:"):
            st.session_state.profile_name = first_name.strip()
            st.session_state.profile_country = selected_country_code
            st.session_state.profile_language = selected_lang_code
            st.session_state.profile_age_range = age
            st.session_state.onboarding_step = 2
            st.rerun()

    # ── Step 2 — Life Stage ──────────────────────────────────────────────────
    elif step == 2:
        st.subheader(":material/person: What best describes your current life stage?")
        st.caption("We'll prioritise guidance that's most relevant to where you are right now.")

        current_stage = st.session_state.profile_life_stage
        cols = st.columns(2)
        selected_stage = None

        for i, stage in enumerate(LIFE_STAGES):
            with cols[i % 2]:
                is_selected = current_stage == stage["id"]
                border_color = "#7c3aed" if is_selected else "#e5e7eb"
                bg_color = "#f5f3ff" if is_selected else "#ffffff"
                check = "✓ " if is_selected else ""
                stage_icon = _STAGE_EMOJI.get(stage["id"], "◆")
                st.markdown(
                    f"""<div style='border:2px solid {border_color}; border-radius:10px;
                        padding:0.75rem 1rem; margin-bottom:0.5rem; background:{bg_color};
                        cursor:pointer'>
                        <strong>{stage_icon} {check}{stage["label"]}</strong><br>
                        <small style='color:#57606a'>{stage["description"]}</small>
                    </div>""",
                    unsafe_allow_html=True,
                )
                if st.button(
                    f"{'✓ Selected' if is_selected else 'Select'}",
                    key=f"stage_{stage['id']}",
                    type="primary" if is_selected else "secondary",
                ):
                    st.session_state.profile_life_stage = stage["id"]
                    st.rerun()

        st.divider()
        bcol1, bcol2 = st.columns([1, 4])
        with bcol1:
            if st.button("Back", icon=":material/arrow_back:"):
                st.session_state.onboarding_step = 1
                st.rerun()
        with bcol2:
            if st.button("Continue", type="primary", icon=":material/arrow_forward:"):
                st.session_state.onboarding_step = 3
                st.rerun()

    # ── Step 3 — Financial Goals ─────────────────────────────────────────────
    elif step == 3:
        st.subheader(":material/savings: What are your top financial goals?")
        st.caption("Select up to 3 preset goals, then add any custom goals you have.")

        selected_goals = list(st.session_state.profile_goals)

        # Preset goals grid
        cols = st.columns(3)
        for i, goal in enumerate(PRESET_GOALS):
            with cols[i % 3]:
                is_sel = goal["id"] in selected_goals
                if st.toggle(
                    goal["label"],
                    value=is_sel,
                    key=f"goal_{goal['id']}",
                    disabled=(len(selected_goals) >= 3 and not is_sel),
                ):
                    if goal["id"] not in selected_goals:
                        selected_goals.append(goal["id"])
                else:
                    if goal["id"] in selected_goals:
                        selected_goals.remove(goal["id"])

        st.session_state.profile_goals = selected_goals[:3]

        st.divider()
        st.markdown("**Custom goals** — add anything not listed above:")
        custom_goals = list(st.session_state.profile_custom_goals)

        # Display existing custom goals
        for idx, cg in enumerate(custom_goals):
            col_a, col_b = st.columns([5, 1])
            with col_a:
                st.text(f"• {cg}")
            with col_b:
                if st.button("Remove", icon=":material/delete:", key=f"del_cg_{idx}"):
                    custom_goals.pop(idx)
                    st.session_state.profile_custom_goals = custom_goals
                    st.rerun()

        new_goal = st.text_input(
            "Add a custom goal",
            placeholder="e.g., Pay off my student loan by 2027",
            label_visibility="collapsed",
        )
        if st.button("Add goal", icon=":material/add:") and new_goal.strip():
            custom_goals.append(new_goal.strip())
            st.session_state.profile_custom_goals = custom_goals
            st.rerun()

        if not selected_goals and not custom_goals:
            st.warning("Please select at least one goal to continue.")

        st.divider()
        bcol1, bcol2 = st.columns([1, 4])
        with bcol1:
            if st.button("Back", icon=":material/arrow_back:"):
                st.session_state.onboarding_step = 2
                st.rerun()
        with bcol2:
            if st.button("Continue", type="primary", icon=":material/arrow_forward:",
                         disabled=(not selected_goals and not custom_goals)):
                st.session_state.onboarding_step = 4
                st.rerun()

    # ── Step 4 — Accessibility ───────────────────────────────────────────────
    elif step == 4:
        st.subheader(":material/accessibility: Customise your experience")
        st.caption(
            "Adjust these settings at any time in Settings. They only affect appearance — "
            "your data and preferences are always preserved."
        )

        with st.container(border=True):
            acc = st.toggle(
                ":material/text_increase: Accessibility-first mode",
                value=st.session_state.accessibility_mode,
                help="Enables large text, simplified layouts, and higher-contrast colours.",
            )
            hc = st.toggle(
                ":material/contrast: High contrast",
                value=st.session_state.high_contrast,
            )
            lt = st.toggle(
                ":material/format_size: Large text",
                value=st.session_state.large_text,
            )
            rm = st.toggle(
                ":material/motion_photos_off: Reduce motion",
                value=st.session_state.reduced_motion,
                help="Disables animations and transitions.",
            )

        st.divider()
        bcol1, bcol2 = st.columns([1, 4])
        with bcol1:
            if st.button("Back", icon=":material/arrow_back:"):
                st.session_state.onboarding_step = 3
                st.rerun()
        with bcol2:
            if st.button("Continue", type="primary", icon=":material/arrow_forward:"):
                # Apply immediately so theme CSS picks them up before next render
                st.session_state.accessibility_mode = acc
                st.session_state.high_contrast = hc
                st.session_state.large_text = lt
                st.session_state.reduced_motion = rm
                st.session_state.onboarding_step = 5
                st.rerun()

    # ── Step 5 — Privacy ────────────────────────────────────────────────────
    elif step == 5:
        st.subheader(":material/lock: Your privacy, your control")
        st.caption(
            "Money Tree is built with privacy first. Below are your defaults — you can change "
            "these at any time and export or delete all your data instantly."
        )

        with st.container(border=True):
            st.markdown("**Conversation history**")
            privacy_mode = st.toggle(
                ":material/visibility_off: Privacy-first mode — store no conversation history",
                value=st.session_state.privacy_mode,
                help="The assistant works fully without storing any chats. Recommended for shared devices.",
            )
            history_consent = st.toggle(
                ":material/psychology: Allow conversation history to personalise responses",
                value=st.session_state.history_consent,
                disabled=privacy_mode,
                help="When enabled, Money Tree learns from your past questions to give better answers over time.",
            )

            st.divider()
            st.markdown("**Data principles (always applied)**")
            st.markdown("""
- :material/lock: All stored data is encrypted locally
- :material/person_off: Personal identity is never linked to AI conversation data
- :material/delete_forever: One-tap deletion of any response or entire history at any time
- :material/cloud_off: No data sent to external servers without your explicit consent
- :material/minimize: Minimum data collection — only what's needed for your goals
""")

        with st.expander(":material/info: What data does Money Tree store?"):
            st.markdown("""
| Data | Where stored | Can be deleted |
|------|-------------|----------------|
| Profile (country, life stage, goals) | Local session | Yes, via Settings → Reset profile |
| Accessibility preferences | Local session | Yes, via Settings |
| Conversation history | Local session (if enabled) | Yes, one-tap per message or wipe all |
| Budget & goals data | Local session | Yes, via Budgeting tools |
| AI model responses | Never stored externally | N/A |

*Cloud sync, if you enable it in the future, will encrypt all data before transmission.*
""")

        st.divider()
        bcol1, bcol2 = st.columns([1, 4])
        with bcol1:
            if st.button("Back", icon=":material/arrow_back:"):
                st.session_state.onboarding_step = 4
                st.rerun()
        with bcol2:
            if st.button("Get started!", type="primary", icon=":material/check_circle:"):
                st.session_state.privacy_mode = privacy_mode
                st.session_state.history_consent = history_consent if not privacy_mode else False
                st.session_state.onboarding_complete = True
                st.session_state.onboarding_step = 1  # reset for next time
                state.add_message("assistant", "Hello! I'm Money Tree, ready to help you on your financial journey.")
                st.rerun()

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown(
        "<hr style='margin-top:3rem'>"
        "<p style='text-align:center; color:#57606a; font-size:0.75rem'>"
        "Money Tree provides financial education and general guidance only — not personalised "
        "financial advice. Always consult a qualified professional for decisions specific to "
        "your situation. Made with IBM Bob</p>",
        unsafe_allow_html=True,
    )
