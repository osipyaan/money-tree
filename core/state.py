"""
core/state.py — Centralised session-state initialisation and helpers.
All mutable per-user state lives here; no module-level mutable globals.
"""

from __future__ import annotations

import datetime
import uuid
import streamlit as st


# ---------------------------------------------------------------------------
# Default profile (used before onboarding completes)
# ---------------------------------------------------------------------------

_DEFAULTS: dict = {
    # Onboarding
    "onboarding_complete": False,
    "profile_name": "",
    "profile_country": "IN",
    "profile_language": "en",
    "profile_age_range": "25–34",
    "profile_life_stage": "early_career",
    "profile_goals": ["emergency_fund", "investing"],
    "profile_custom_goals": [],
    # Accessibility / UI mode
    "accessibility_mode": False,
    "high_contrast": False,
    "large_text": False,
    "reduced_motion": True,
    # Accessibility needs & communication preferences (structured, not free text)
    "accessibility_needs": [],       # list of ids from core.data.ACCESSIBILITY_NEEDS
    "communication_mode": "text",    # "text" | "voice" | "both" — from core.data.COMMUNICATION_MODES
    "captions_enabled": True,        # live visual transcript whenever the assistant speaks
    "simplified_language": False,    # cognitive accessibility: shapes AI response style
    # Theme: "purple" | "pink" | "lofi" | "bw"
    "active_theme": "purple",
    # Privacy
    "privacy_mode": False,           # no conversation history stored
    "history_consent": False,        # explicit consent to use history for personalisation
    "sync_enabled": False,
    # Conversations
    "conversations": [],             # list of {id, ts, role, content, deleted}
    # Budgeting
    "budget_income": 0.0,
    "budget_items": [],              # list of {category, amount, type: need/want/saving}
    "budget_goals": [],              # list of {id, label, target, saved, currency}
    # Knowledge level (adapts over sessions)
    "knowledge_level": "beginner",   # beginner / intermediate / advanced
    "session_query_count": 0,
    # Voice/speech
    "voice_enabled": False,
    "speech_lang": "en-US",
    # Downloaded content (offline cache tracking)
    "downloaded_modules": [],
    # Pending sync queue (for offline-first support)
    "sync_queue": [],
}


def init() -> None:
    """Initialise all session state keys with defaults if not already set."""
    for key, value in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_profile() -> None:
    """Clear profile and return to onboarding."""
    for key in [
        "onboarding_complete", "profile_name", "profile_country", "profile_language",
        "profile_age_range", "profile_life_stage", "profile_goals",
        "profile_custom_goals",
    ]:
        st.session_state[key] = _DEFAULTS[key]
    st.session_state["onboarding_complete"] = False


def add_message(role: str, content: str) -> str:
    """Add a message to conversation history. Returns the message id."""
    if st.session_state.get("privacy_mode"):
        return ""  # no-op in privacy mode
    msg_id = str(uuid.uuid4())
    st.session_state["conversations"].append({
        "id": msg_id,
        "ts": datetime.datetime.utcnow().isoformat(),
        "role": role,
        "content": content,
        "deleted": False,
    })
    return msg_id


def delete_message(msg_id: str) -> None:
    """Permanently delete a single message by id."""
    st.session_state["conversations"] = [
        m for m in st.session_state["conversations"] if m["id"] != msg_id
    ]


def clear_all_history() -> None:
    """Permanently delete all conversation history."""
    st.session_state["conversations"] = []


def visible_messages() -> list[dict]:
    return [m for m in st.session_state["conversations"] if not m.get("deleted")]


def bump_knowledge(response_length: int) -> None:
    """Nudge the knowledge level upward after sophisticated queries."""
    st.session_state["session_query_count"] += 1
    count = st.session_state["session_query_count"]
    if count >= 10 and st.session_state["knowledge_level"] == "beginner":
        st.session_state["knowledge_level"] = "intermediate"
    elif count >= 25 and st.session_state["knowledge_level"] == "intermediate":
        st.session_state["knowledge_level"] = "advanced"


def get_knowledge_suffix() -> str:
    level = st.session_state.get("knowledge_level", "beginner")
    if level == "beginner":
        return " Explain in plain language, avoid jargon, and use a simple analogy where helpful."
    if level == "intermediate":
        return " You can use standard financial terminology but briefly define any technical concepts."
    return " The user has demonstrated solid financial literacy; feel free to use precise financial language."
