"""
app_pages/settings.py — Privacy controls, accessibility, profile management,
and capability/integration status.
"""

from __future__ import annotations

import streamlit as st
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from core import state, ai
from core.data import (
    COUNTRIES, LANGUAGES, LIFE_STAGES, PRESET_GOALS, AGE_RANGES, get_country_name,
    ACCESSIBILITY_NEEDS, COMMUNICATION_MODES, default_speech_lang,
)
from core.i18n import t

_EXCLUSIVE_NEEDS = {"none", "prefer_not_say"}


def _resolve_exclusive_needs(selected: list[str]) -> list[str]:
    exclusive_selected = [n for n in selected if n in _EXCLUSIVE_NEEDS]
    if exclusive_selected and len(selected) > 1:
        return [exclusive_selected[-1]]
    return selected


def render() -> None:
    state.init()

    st.title(t(":material/settings: Settings"))

    tab_privacy, tab_access, tab_profile, tab_integrations = st.tabs([
        t(":material/lock: Privacy & data"),
        t(":material/accessibility: Accessibility"),
        t(":material/person: Profile"),
        t(":material/extension: Integrations"),
    ])

    # ── Privacy & Data ───────────────────────────────────────────────────────
    with tab_privacy:
        _render_privacy()

    # ── Accessibility ────────────────────────────────────────────────────────
    with tab_access:
        _render_accessibility()

    # ── Profile ──────────────────────────────────────────────────────────────
    with tab_profile:
        _render_profile()

    # ── Integrations ─────────────────────────────────────────────────────────
    with tab_integrations:
        _render_integrations()


# ---------------------------------------------------------------------------

def _render_privacy() -> None:
    st.subheader(t("Conversation history"))

    privacy_mode = st.toggle(
        t(":material/visibility_off: Privacy-first mode"),
        value=st.session_state.get("privacy_mode", False),
        help=t("No conversation history is stored. The assistant works fully offline."),
    )
    st.session_state.privacy_mode = privacy_mode

    history_consent = st.toggle(
        t(":material/psychology: Use conversation history for personalisation"),
        value=st.session_state.get("history_consent", False),
        disabled=privacy_mode,
        help=t("Lets Money Tree give better answers by referencing your previous questions."),
    )
    if not privacy_mode:
        st.session_state.history_consent = history_consent

    st.divider()
    st.subheader(t("Delete conversation data"))

    msgs = state.visible_messages()
    st.caption(t("{n} message{suffix} in history.").format(n=len(msgs), suffix="s" if len(msgs) != 1 else ""))

    if msgs:
        with st.expander(t(":material/manage_search: View and delete individual messages")):
            for msg in msgs:
                col_content, col_del = st.columns([10, 1])
                with col_content:
                    role_label = t("You") if msg["role"] == "user" else t("Money Tree")
                    preview = msg["content"][:120] + ("…" if len(msg["content"]) > 120 else "")
                    st.markdown(f"**{role_label}:** {preview}")
                with col_del:
                    if st.button(
                        ":material/delete:",
                        key=f"settings_del_{msg['id']}",
                        help=t("Permanently delete this message"),
                    ):
                        state.delete_message(msg["id"])
                        st.rerun()

    col_wipe, _ = st.columns([2, 3])
    with col_wipe:
        if st.button(
            t(":material/delete_forever: Delete ALL conversation history"),
            type="primary",
        ):
            state.clear_all_history()
            st.success(
                t("All conversation history permanently deleted from this session. "
                  "If cloud sync is enabled, deletion will be queued for remote removal."),
                icon=":material/check_circle:",
            )
            st.rerun()

    st.divider()
    st.subheader(t("Data principles"))
    st.markdown(t("""
| Principle | Status |
|---|---|
| Sensitive data processed on-device | ✅ Active |
| No personally identifiable data linked to AI conversations | ✅ Active |
| Minimum data collection | ✅ Active |
| One-tap message deletion | ✅ Active |
| Explicit consent required for personalisation | ✅ Active |
| Offline-capable assistant | ✅ Active |
| Encrypted local storage | ⚙️ Enabled when persistent storage is configured |
| Cloud sync | ⚙️ Disabled (opt-in only) |
"""))


def _render_accessibility() -> None:
    st.subheader(t("Accessibility needs"))
    st.caption(
        t("This actively shapes the layout and how the AI assistant responds — not just a note "
          "we file away. Changes take effect immediately.")
    )

    current_needs = list(st.session_state.get("accessibility_needs", []))
    picked_needs: list[str] = []
    for need in ACCESSIBILITY_NEEDS:
        checked = st.checkbox(
            t(need["label"]),
            value=need["id"] in current_needs,
            key=f"settings_need_{need['id']}",
            help=t(need["description"]) if need.get("description") else None,
        )
        if checked:
            picked_needs.append(need["id"])
    picked_needs = _resolve_exclusive_needs(picked_needs)
    st.session_state.accessibility_needs = picked_needs
    is_deaf_hoh = "deaf_hoh" in picked_needs

    st.divider()
    st.subheader(t("Communication mode"))
    if is_deaf_hoh:
        st.info(
            t(":material/info: Since you're Deaf or hard of hearing, live captions stay on for any "
              "spoken output regardless of mode."),
            icon=None,
        )
    mode_labels = [t(m["label"]) for m in COMMUNICATION_MODES]
    mode_captions = [t(m["description"]) for m in COMMUNICATION_MODES]
    current_mode_id = st.session_state.get("communication_mode", "text")
    current_mode_label = next(
        (t(m["label"]) for m in COMMUNICATION_MODES if m["id"] == current_mode_id),
        mode_labels[0],
    )
    selected_mode_label = st.radio(
        t("Would you prefer voice-only, text-only, or both?"),
        mode_labels,
        index=mode_labels.index(current_mode_label),
        captions=mode_captions,
        key="settings_comm_mode",
    )
    selected_mode_id = next(m["id"] for m in COMMUNICATION_MODES if t(m["label"]) == selected_mode_label)
    st.session_state.communication_mode = selected_mode_id
    st.session_state.voice_enabled = selected_mode_id in ("voice", "both")

    if selected_mode_id in ("voice", "both"):
        st.session_state.captions_enabled = st.toggle(
            t(":material/closed_caption: Live visual transcript for spoken responses"),
            value=st.session_state.get("captions_enabled", True) or is_deaf_hoh,
            disabled=is_deaf_hoh,
            key="settings_captions",
        )

    st.divider()
    st.subheader(t("Display preferences"))
    st.caption(t("Changes take effect immediately — no save button needed."))

    with st.container(border=True):
        # Explicit value= is required here: a key-only toggle never visually
        # renders as checked on its first appearance even when the underlying
        # session_state value is already True (e.g. set by defaults or by
        # onboarding), which also makes the widget unreliable to click since
        # there's no visual feedback of its real state.
        acc = st.toggle(
            t(":material/text_increase: Accessibility-first mode"),
            value=st.session_state.get("accessibility_mode", False),
            key="accessibility_mode",
            help=t("Enables large text, simplified layouts, and high-contrast styling."),
        )
        hc = st.toggle(
            t(":material/contrast: High contrast"),
            value=st.session_state.get("high_contrast", False),
            key="high_contrast",
        )
        lt = st.toggle(
            t(":material/format_size: Large text (19px+)"),
            value=st.session_state.get("large_text", False),
            key="large_text",
        )
        rm = st.toggle(
            t(":material/motion_photos_off: Reduce motion"),
            value=st.session_state.get("reduced_motion", True),
            key="reduced_motion",
        )

    st.toggle(
        t(":material/short_text: Use shorter sentences & simpler structure in AI responses"),
        value=st.session_state.get("simplified_language", False),
        key="simplified_language",
        help=t("Breaks answers into small steps, avoids idioms and jargon, and keeps one idea per sentence."),
    )

    st.caption(t(":material/check_circle: Settings applied — you'll see the effect on your next interaction."))

    st.divider()
    st.subheader(t("Preview"))
    if acc or lt:
        st.markdown(
            "<p style='font-size:19px;line-height:1.8'>"
            f"{t('This is how text will appear in accessibility mode. All content is fully accessible at this size.')}</p>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(t("Standard text size. Enable large text or accessibility mode above to preview."))

    if hc:
        st.markdown(
            "<div style='background:#000;color:#fff;padding:1rem;border-radius:8px'>"
            f"{t('High contrast mode is active.')}</div>",
            unsafe_allow_html=True,
        )


def _render_profile() -> None:
    st.subheader(t("Your profile"))
    st.caption(t("Update your profile at any time. Changes are applied immediately."))

    new_name = st.text_input(
        t("First name"),
        value=st.session_state.get("profile_name", ""),
        placeholder="e.g., Amara",
    )

    country_names = [c["name"] for c in COUNTRIES]
    current_country_name = get_country_name(st.session_state.get("profile_country", "US"))
    if current_country_name not in country_names:
        current_country_name = country_names[0]

    col1, col2 = st.columns(2)
    with col1:
        new_country_name = st.selectbox(
            t("Country"),
            country_names,
            index=country_names.index(current_country_name),
        )
        new_country_code = next(c["code"] for c in COUNTRIES if c["name"] == new_country_name)
    with col2:
        lang_names = [l["name"] for l in LANGUAGES]
        current_lang_name = next(
            (l["name"] for l in LANGUAGES if l["code"] == st.session_state.get("profile_language", "en")),
            lang_names[0],
        )
        new_lang_name = st.selectbox(
            t("Language"),
            lang_names,
            index=lang_names.index(current_lang_name),
        )
        new_lang_code = next(l["code"] for l in LANGUAGES if l["name"] == new_lang_name)

    stage_labels = [t(ls["label"]) for ls in LIFE_STAGES]
    current_stage_label = next(
        (t(ls["label"]) for ls in LIFE_STAGES if ls["id"] == st.session_state.get("profile_life_stage", "early_career")),
        stage_labels[0],
    )
    new_stage_label = st.selectbox(
        t("Life stage"),
        stage_labels,
        index=stage_labels.index(current_stage_label),
    )
    new_stage_id = next(ls["id"] for ls in LIFE_STAGES if t(ls["label"]) == new_stage_label)

    age_display = [t(a) for a in AGE_RANGES]
    age_selected_display = st.selectbox(
        t("Age range"),
        age_display,
        index=AGE_RANGES.index(st.session_state.get("profile_age_range", "25–34"))
        if st.session_state.get("profile_age_range") in AGE_RANGES
        else 2,
    )
    age = AGE_RANGES[age_display.index(age_selected_display)]

    st.markdown(t("**Goals** (select up to 3)"))
    selected_goals = list(st.session_state.get("profile_goals", []))
    cols = st.columns(3)
    for i, goal in enumerate(PRESET_GOALS):
        with cols[i % 3]:
            is_sel = goal["id"] in selected_goals
            if st.toggle(
                t(goal["label"]),
                value=is_sel,
                key=f"profile_goal_{goal['id']}",
                disabled=(len(selected_goals) >= 3 and not is_sel),
            ):
                if goal["id"] not in selected_goals:
                    selected_goals.append(goal["id"])
            else:
                if goal["id"] in selected_goals:
                    selected_goals.remove(goal["id"])

    st.markdown(t("**Custom goals**"))
    custom_goals = list(st.session_state.get("profile_custom_goals", []))
    for idx, cg in enumerate(custom_goals):
        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.text(f"• {cg}")
        with col_b:
            if st.button(":material/delete:", key=f"profile_del_cg_{idx}"):
                custom_goals.pop(idx)
                st.session_state.profile_custom_goals = custom_goals
                st.rerun()
    new_goal = st.text_input(
        t("Add custom goal"),
        placeholder="e.g., Pay off car by 2026",
        label_visibility="collapsed",
    )
    if st.button(t(":material/add: Add")) and new_goal.strip():
        custom_goals.append(new_goal.strip())
        st.session_state.profile_custom_goals = custom_goals
        st.rerun()

    if st.button(t("Save profile changes"), type="primary"):
        st.session_state.profile_name = new_name.strip()
        st.session_state.profile_country = new_country_code
        st.session_state.profile_language = new_lang_code
        st.session_state.speech_lang = default_speech_lang(new_lang_code)
        st.session_state.profile_life_stage = new_stage_id
        st.session_state.profile_age_range = age
        st.session_state.profile_goals = selected_goals[:3]
        st.session_state.profile_custom_goals = custom_goals
        st.success(t("Profile updated."), icon=":material/check_circle:")

    st.divider()
    with st.expander(t(":material/warning: Danger zone")):
        st.warning(
            t("Resetting your profile will clear your country, life stage, and goals. "
              "Budget and conversation data will be preserved."),
            icon=":material/warning:",
        )
        if st.button(t(":material/restart_alt: Reset profile and redo onboarding"), type="secondary"):
            state.reset_profile()
            st.session_state.onboarding_step = 1
            st.rerun()


def _render_integrations() -> None:
    st.subheader(t("AI provider capabilities"))
    caps = ai.capability_report()
    for name, value in caps.items():
        icon = ":material/check_circle:" if "Not available" not in value else ":material/cancel:"
        st.markdown(f"{icon} **{name.upper()}:** {value}")

    st.divider()
    st.subheader(t("Planned integrations"))
    st.caption(
        t("The following integrations are on the roadmap. Each will require explicit consent "
          "before any data is shared, and all communication will use encrypted channels.")
    )

    integrations = [
        {
            "name": "Open banking (account aggregation)",
            "status": "Planned",
            "notes": "Connects read-only to your bank to auto-populate budgets. OAuth-based, no credentials stored.",
        },
        {
            "name": "Budgeting platforms (YNAB, Monarch, etc.)",
            "status": "Planned",
            "notes": "Sync budget categories. Data flows one-way on demand only.",
        },
        {
            "name": "Government financial resources",
            "status": "Planned",
            "notes": "Deep links to relevant official pages per country (tax authority, pension portal, etc.).",
        },
        {
            "name": "Licensed financial advisor marketplace",
            "status": "Planned",
            "notes": "Opt-in referral to vetted advisors. No conversation data shared without explicit consent.",
        },
        {
            "name": "Multilingual TTS (ElevenLabs / Azure)",
            "status": "Modular — swap in by replacing core/ai.py TTS provider",
            "notes": "Current default: gTTS (if installed). Swap to any provider by updating synthesize_speech().",
        },
        {
            "name": "Local Whisper STT",
            "status": "Modular — swap in by replacing core/ai.py STT provider",
            "notes": "Install openai-whisper; replace transcribe_audio() for fully private on-device transcription.",
        },
    ]

    for intg in integrations:
        status_colour = "#10b981" if "Active" in intg["status"] else "#f59e0b"
        status_display = t(intg["status"]) if intg["status"] == "Planned" else intg["status"]
        with st.container(border=True):
            st.markdown(
                f"**{intg['name']}** — "
                f"<span style='color:{status_colour}'>{status_display}</span>",
                unsafe_allow_html=True,
            )
            st.caption(intg["notes"])

    st.divider()
    st.subheader(t("Voice & speech settings"))
    speech_lang_options = [
        "en-US", "en-GB", "es-ES", "fr-FR", "hi-IN", "pt-BR", "ar-SA", "sw-KE", "de-DE", "ja-JP", "zh-CN",
    ]
    current_speech_lang = st.session_state.get("speech_lang", "en-US")
    speech_lang = st.selectbox(
        t("Speech recognition language code"),
        speech_lang_options,
        index=speech_lang_options.index(current_speech_lang) if current_speech_lang in speech_lang_options else 0,
        help=t("Defaults to match your profile language — change this if you speak to Money Tree in a "
               "different language than you read it in."),
    )
    st.session_state.speech_lang = speech_lang
    st.caption(t("This controls the STT language. Text responses and TTS use your profile language setting."))


# ── Module-level call required by st.Page ────────────────────────────────────
render()
