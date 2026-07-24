"""
core/ai.py — Modular AI/speech abstraction layer.

Architecture:
  - Transcription, LLM inference, and TTS are each a swappable "provider"
  - Providers are resolved by availability at import time
  - All public functions gracefully degrade to demo/offline mode
  - No sensitive data is sent anywhere without explicit user action
"""

from __future__ import annotations

import json
import os
import textwrap
from typing import Iterator

# ---------------------------------------------------------------------------
# Provider availability detection
# ---------------------------------------------------------------------------

def _has(module: str) -> bool:
    import importlib.util
    return importlib.util.find_spec(module) is not None


HAS_OPENAI = _has("openai")
HAS_GTTS = _has("gtts")
HAS_SR = _has("speech_recognition")

# ---------------------------------------------------------------------------
# AI response generation (LLM layer)
# ---------------------------------------------------------------------------

def build_system_prompt(
    country: str,
    language: str,
    life_stage: str,
    goals: list[str],
    knowledge_level: str,
    regional_content: dict,
) -> str:
    goals_str = ", ".join(goals) if goals else "general financial wellness"
    return textwrap.dedent(f"""
        You are Money Tree, an AI-powered financial literacy assistant designed specifically
        for women worldwide. Your mission: help users build genuine financial confidence,
        not overwhelm them.

        USER CONTEXT
        ─────────────
        Country / region : {country}
        Preferred language: {language}
        Life stage        : {life_stage}
        Primary goals     : {goals_str}
        Knowledge level   : {knowledge_level}

        REGIONAL GUIDANCE (for this user's country/region)
        ───────────────────────────────────────────────────
        Tax note      : {regional_content.get('tax_note', '')}
        Retirement    : {regional_content.get('retirement_programs', '')}
        Credit note   : {regional_content.get('credit_note', '')}
        Scam alert    : {regional_content.get('scam_alert', '')}

        RESPONSE GUIDELINES
        ────────────────────
        1. Always respond in {language}. If you cannot, default to English and note it.
        2. Explain concepts in plain, warm language appropriate to the knowledge level.
        3. Clearly distinguish between UNIVERSAL financial principles and country-specific
           guidance. Flag country-specific information with "⚠️ {country}-specific:".
        4. Proactively mention relevant scam risks when the topic warrants it.
        5. If advice depends on local regulations or requires professional judgement,
           explicitly say: "For your specific situation, please consult a licensed
           financial professional in {country}."
        6. Cite your assumptions (e.g., "Assuming you have no existing investments…").
        7. Never guarantee investment returns or make speculative promises.
        8. Be encouraging but honest — financial progress takes time.
        9. Keep responses concise and scannable; use bullet points and headers.
        10. Privacy: never repeat or reference the user's personal identifying details
            in the response text.
        11. CRITICAL — always end your response with a single, specific follow-up question
            relevant to the user's life stage ({life_stage}) and country ({country}).
            The question should feel personal and helpful, like:
            "Are you interested in learning more about [specific topic] for {life_stage}s in {country}?"
            or "Would it help to walk through [specific next step] together?"
            Keep it to one short sentence at the end, set apart on its own line.
    """).strip()


def generate_response(
    user_message: str,
    conversation_history: list[dict],
    system_prompt: str,
    stream: bool = False,
) -> str | Iterator[str]:
    """
    Generate an AI response.

    Provider priority:
    1. OpenAI (if openai package installed and OPENAI_API_KEY set)
    2. Demo / offline mode (keyword-based from data.py)

    Returns a plain string (or a generator when stream=True and OpenAI is active).
    """
    if HAS_OPENAI and os.environ.get("OPENAI_API_KEY"):
        return _openai_response(user_message, conversation_history, system_prompt, stream)
    return _demo_response(user_message)


def _openai_response(
    user_message: str,
    history: list[dict],
    system_prompt: str,
    stream: bool,
) -> str | Iterator[str]:
    import openai  # type: ignore
    client = openai.OpenAI()
    messages = [{"role": "system", "content": system_prompt}]
    # Include recent history (last 10 turns to stay within context limits)
    for m in history[-10:]:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_message})
    if stream:
        def _gen():
            with client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
                max_tokens=800,
            ) as resp:
                for chunk in resp:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta
        return _gen()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=800,
    )
    return resp.choices[0].message.content


def _demo_response(user_message: str) -> str:
    from core.data import classify_query, DEMO_RESPONSES
    key = classify_query(user_message)
    return DEMO_RESPONSES.get(key, DEMO_RESPONSES["default"])


# ---------------------------------------------------------------------------
# Speech-to-text (transcription)
# ---------------------------------------------------------------------------

def transcribe_audio(audio_bytes: bytes, language: str = "en") -> str | None:
    """
    Transcribe audio bytes to text.

    Provider priority:
    1. SpeechRecognition + Google STT (if speechrecognition installed)
    2. Returns None → caller should fall back to text input

    NOTE: For production, swap in a local Whisper model or a privacy-respecting
    API by replacing this function's body. The interface (bytes → str | None)
    stays stable.
    """
    if not HAS_SR:
        return None
    try:
        import speech_recognition as sr  # type: ignore
        import io
        recognizer = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language=language)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Text-to-speech (synthesis)
# ---------------------------------------------------------------------------

def synthesize_speech(text: str, language: str = "en") -> bytes | None:
    """
    Convert text to audio bytes (MP3).

    Provider priority:
    1. gTTS (if gtts installed)
    2. Returns None → caller renders text only

    NOTE: For production, swap in a local TTS engine or a privacy-respecting
    API by replacing this function's body.
    """
    if not HAS_GTTS:
        return None
    try:
        from gtts import gTTS  # type: ignore
        import io
        lang_code = language.split("-")[0][:2]
        tts = gTTS(text=text[:500], lang=lang_code, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Capability report (shown in settings)
# ---------------------------------------------------------------------------

def capability_report() -> dict:
    openai_key = bool(os.environ.get("OPENAI_API_KEY"))
    return {
        "llm": "OpenAI GPT-4o mini" if (HAS_OPENAI and openai_key) else "Demo / offline mode",
        "stt": "Google Speech Recognition (via SpeechRecognition)" if HAS_SR else "Not available (install speechrecognition)",
        "tts": "Google Text-to-Speech (gTTS)" if HAS_GTTS else "Not available (install gtts)",
        "privacy": "On-device demo mode — no data sent to external services" if not (HAS_OPENAI and openai_key) else "OpenAI API (data sent per OpenAI privacy policy)",
    }


# ---------------------------------------------------------------------------
# Live financial news (country-specific, no API key required)
# ---------------------------------------------------------------------------

# Maps country code → search query term for Google News RSS
_NEWS_QUERIES: dict[str, str] = {
    "IN": "India women personal finance",
    "US": "United States women personal finance",
    "GB": "UK women personal finance",
    "CA": "Canada women personal finance",
    "AU": "Australia women personal finance",
    "NG": "Nigeria women personal finance",
    "ZA": "South Africa women personal finance",
    "BR": "Brazil women finanças pessoais",
    "MX": "Mexico mujeres finanzas personales",
    "DE": "Deutschland Frauen Finanzen",
    "FR": "France femmes finances personnelles",
    "JP": "Japan women personal finance",
    "PH": "Philippines women personal finance",
    "KE": "Kenya women personal finance",
    "EG": "Egypt women personal finance",
}


def fetch_financial_news(country_code: str, max_items: int = 5) -> list[dict]:
    """
    Fetch recent financial news headlines for the given country.
    Uses Google News RSS — no API key required.
    Returns a list of {title, link, published} dicts, or [] on failure.
    """
    import urllib.request
    import urllib.parse
    import xml.etree.ElementTree as ET

    query = _NEWS_QUERIES.get(country_code, f"{country_code} women personal finance")
    encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=en&gl=US&ceid=US:en"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
        items = []
        for item in root.findall(".//item")[:max_items]:
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            pub = item.findtext("pubDate", "").strip()
            if title and link:
                items.append({"title": title, "link": link, "published": pub})
        return items
    except Exception:
        return []
