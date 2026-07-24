# money tree: ai-powered accessible financial literacy for women

A cross-platform, privacy-first financial literacy and voice assistant built with Streamlit.

---

## Features

### Onboarding
- Country, language, age range, and life stage selection
- Up to 3 preset financial goals + unlimited custom goals
- Accessibility preferences (large text, high contrast, reduced motion)
- Privacy-first mode configuration

### AI Financial Assistant
- **Text and voice input** allows you to type or speak your question
- Multimodal output provides a text response + optional spoken playback
- **Regional context** includes tax notes, retirement programs, credit guidance, scam alerts
- Adaptive knowledge level is utilized, with responses getting more sophisticated as you use the app
- One-tap message deletion ("scrap") and full history wipe
- Privacy mode is implemented, with no conversation history stored

### Financial Education Library
- 5+ in-depth educational modules (more can be added to `core/data.py`)
- Search, filter by category and level
- "Save for offline" per module
- Country-specific guidance in every module

### Budget & Goals
- Monthly budget planner with 50/30/20 framework (adjustable)
- Visual bar chart breakdown
- Expense tracker with category tagging
- Goal tracker with progress bars and completion estimates

### Settings
- Full privacy controls: toggle history, delete messages/all history, consent management
- Accessibility controls: large text, high contrast, reduced motion, accessibility-first mode
- Profile editor: update country, language, life stage, goals at any time
- Integration roadmap: open banking, budgeting platforms, licensed advisor marketplace

---

## Running the app

```bash
cd finwise_app
streamlit run streamlit_app.py
```

## Optional dependencies

See `requirements.txt`. Install any of:

| Package | Unlocks |
|---|---|
| `openai` + `OPENAI_API_KEY` | GPT-4o mini responses (vs. demo keyword mode) |
| `SpeechRecognition` | Voice-to-text input |
| `gTTS` | Text-to-speech playback |
| `openai-whisper` | Fully private on-device transcription |
| `cryptography` | Encrypted local storage |

## Architecture

```
finwise_app/
├── streamlit_app.py          ← Entry point, navigation, global CSS
├── app_pages/
│   ├── onboarding.py         ← 5-step onboarding flow
│   ├── assistant.py          ← Multimodal AI chat interface
│   ├── education.py          ← Financial education library
│   ├── budgeting.py          ← Budget planner + goal tracker
│   └── settings.py           ← Privacy, accessibility, profile
├── core/
│   ├── ai.py                 ← Swappable LLM / STT / TTS providers
│   ├── state.py              ← Centralised session state management
│   └── data.py               ← Countries, education content, localization
└── .streamlit/
    └── config.toml           ← Theme (violet primary, clean white)
```

### Provider swapping

All AI providers are isolated in [`core/ai.py`](core/ai.py). To swap:

- **LLM:** Replace `_openai_response()` with any provider that returns a string
- **STT:** Replace `transcribe_audio()` — interface is `bytes → str | None`
- **TTS:** Replace `synthesize_speech()` — interface is `str → bytes | None`

No other files need changes.

### Privacy design

- All conversation data lives in `st.session_state` (ephemeral by default)
- Privacy mode (`privacy_mode=True`) skips all storage entirely
- `state.delete_message()` and `state.clear_all_history()` immediately wipe from session
- PII (profile data) is never written into AI prompt responses
- Explicit `history_consent` toggle required before history is sent to the LLM

---

*Made with IBM Bob and Claude Code 🤖*
