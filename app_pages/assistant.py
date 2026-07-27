"""
app_pages/assistant.py — Multimodal AI financial assistant page.

Features:
- Voice input (microphone) with local-first transcription
- Text input
- Streaming text responses with spoken output
- Per-message delete ("scrap") button
- Regional context surfaced in sidebar
- Privacy mode awareness
"""

from __future__ import annotations

import datetime
import streamlit as st
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from core import state, ai
from core.data import (
    get_regional_content, get_country_name, get_currency,
    LIFE_STAGES, PRESET_GOALS, classify_query,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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
    life_stage = _get_life_stage_label()
    goals = _get_goal_labels()
    knowledge = st.session_state.get("knowledge_level", "beginner")
    regional = get_regional_content(country)
    return ai.build_system_prompt(
        country=get_country_name(country),
        language=language,
        life_stage=life_stage,
        goals=goals,
        knowledge_level=knowledge,
        regional_content=regional,
        accessibility_needs=st.session_state.get("accessibility_needs", []),
        simplified_language=st.session_state.get("simplified_language", False),
        communication_mode=st.session_state.get("communication_mode", "text"),
    )


def _render_message(msg: dict, idx: int) -> None:
    role = msg["role"]
    content = msg["content"]
    ts = msg.get("ts", "")
    msg_id = msg["id"]

    # Synthesize speech up front (if applicable) so the text block below can be
    # explicitly labelled as the live transcript of that audio, rather than a
    # second, unlabelled copy of the same words.
    audio_bytes = None
    if role == "assistant" and st.session_state.get("voice_enabled"):
        audio_bytes = ai.synthesize_speech(
            content[:600],
            language=st.session_state.get("profile_language", "en"),
        )
    show_captions = audio_bytes and st.session_state.get("captions_enabled", True)

    with st.chat_message(role, avatar=":material/auto_awesome:" if role == "assistant" else ":material/person:"):
        col_text, col_del = st.columns([12, 1])
        with col_text:
            if show_captions:
                st.caption(":material/closed_caption: Live transcript of spoken response")
            st.markdown(content)
            if ts:
                try:
                    dt = datetime.datetime.fromisoformat(ts)
                    st.caption(dt.strftime("%H:%M"))
                except Exception:
                    pass
        with col_del:
            if st.button(
                ":material/delete:",
                key=f"del_msg_{msg_id}",
                help="Permanently delete this message",
            ):
                state.delete_message(msg_id)
                st.rerun()

        # TTS playback if speech synthesis available and voice enabled
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3", autoplay=False)


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> None:
    state.init()

    st.title(":material/auto_awesome: Money Tree Assistant")

    # Privacy banner
    if st.session_state.get("privacy_mode"):
        st.info(
            ":material/visibility_off: **Privacy mode is active.** Conversation history is not stored. "
            "Responses appear here during this session only.",
            icon=None,
        )
    elif not st.session_state.get("history_consent"):
        st.warning(
            ":material/info: Conversation history personalisation is off. Enable it in **Settings → Privacy** "
            "to let Money Tree improve responses based on your history.",
            icon=None,
        )

    # Render existing messages
    messages = state.visible_messages()
    if not messages:
        # Empty state
        with st.container(border=True):
            country = st.session_state.get("profile_country", "US")
            life_stage = _get_life_stage_label()
            st.markdown(
                f"👋 **Welcome back!** I'm Money Tree, your financial guide. "
                f"Based on your profile as a **{life_stage}** in **{get_country_name(country)}**, "
                f"here are some things I can help you with:"
            )
            goals = _get_goal_labels()
            if goals:
                for g in goals:
                    st.markdown(f"• Ask me about: *{g}*")
            st.markdown("• Understand investing, budgeting, and debt strategies")
            st.markdown("• Identify financial scams and protect yourself")
            st.markdown("• Understand local tax and retirement options")
    else:
        for i, msg in enumerate(messages):
            _render_message(msg, i)

    # Suggestion chips (shown when history is empty or short)
    if len(messages) < 2:
        st.markdown("**Quick questions to try:**")
        suggestion_cols = st.columns(3)
        suggestions = [
            "How do I build an emergency fund?",
            "What are the biggest financial scams I should know about?",
            "Explain index funds in plain language",
            "How do I start a budget?",
            "What is a good debt payoff strategy?",
            "How much should I save for retirement?",
        ]
        for i, suggestion in enumerate(suggestions):
            with suggestion_cols[i % 3]:
                if st.button(suggestion, key=f"sugg_{i}"):
                    _process_input(suggestion)

    st.divider()

    # Input area
    _render_input_area()


def _render_input_area() -> None:
    """Renders voice + text input controls."""
    voice_available = ai.HAS_SR and ai.HAS_GTTS
    voice_enabled = st.session_state.get("voice_enabled", False)

    col_voice, col_input = st.columns([1, 6])
    with col_voice:
        if voice_available:
            new_voice = st.toggle(
                ":material/mic:",
                value=voice_enabled,
                help="Enable voice input and spoken responses",
            )
            st.session_state.voice_enabled = new_voice
        else:
            st.caption(":material/mic_off:")

    with col_input:
        # Voice upload fallback (browser mic not directly accessible in Streamlit)
        if voice_enabled and voice_available:
            audio_val = st.audio_input(
                "Speak your question",
                label_visibility="collapsed",
            )
            if audio_val is not None:
                audio_bytes = audio_val.getvalue()
                with st.spinner("Transcribing…"):
                    lang = st.session_state.get("speech_lang", "en-US")
                    transcript = ai.transcribe_audio(audio_bytes, language=lang)
                if transcript:
                    st.success(f"Heard: *{transcript}*")
                    _process_input(transcript)
                else:
                    st.warning(
                        "Could not transcribe audio. Please type your question below.",
                        icon=":material/warning:",
                    )

    # Always show text input
    user_input = st.chat_input(
        "Ask me anything about your finances…",
        key="chat_input",
    )
    if user_input:
        _process_input(user_input)


def _process_input(text: str) -> None:
    """Handle a user message: store, generate response, store response."""
    # Add user message
    state.add_message("user", text)

    # Build context
    system_prompt = _build_system_prompt()
    all_msgs = state.visible_messages()
    if st.session_state.get("history_consent", False):
        # Pass the last 10 turns excluding the message we just added (last item)
        history = [
            {"role": m["role"], "content": m["content"]}
            for m in all_msgs[:-1][-10:]
        ]
    else:
        history = []

    # Generate response
    with st.spinner("Thinking…"):
        response = ai.generate_response(
            user_message=text,
            conversation_history=history,
            system_prompt=system_prompt,
            stream=False,
        )
        # Handle iterator (streaming) case — consume it
        if hasattr(response, "__iter__") and not isinstance(response, str):
            response = "".join(response)

    # Add disclaimer when applicable
    knowledge = st.session_state.get("knowledge_level", "beginner")
    if any(w in text.lower() for w in ["invest", "tax", "retire", "pension", "legal", "advice"]):
        response += (
            "\n\n---\n*⚠️ This is financial education, not personalised advice. "
            "For decisions specific to your situation and jurisdiction, "
            "please consult a licensed financial professional.*"
        )

    state.add_message("assistant", response)
    state.bump_knowledge(len(response))
    st.rerun()


# ── Module-level call required by st.Page ────────────────────────────────────
render()
