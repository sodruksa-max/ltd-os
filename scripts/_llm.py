"""
_llm.py — shared LLM helper for scripts/

Uses Google Gemini Flash (free tier: 15 RPM, 1M tokens/day).
No extra packages needed — only `requests` (already installed).

Setup: add GEMINI_API_KEY to .secrets/.env
Get key: aistudio.google.com -> Get API Key (free, needs Google account)
"""

import os
from pathlib import Path

_ENV_FILE = Path(__file__).parent.parent / ".secrets" / ".env"
_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash-lite:generateContent"
)


def load_gemini_key() -> str | None:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


def call_gemini(system: str, user: str, max_tokens: int = 200) -> str | None:
    """
    Call Gemini Flash Lite. Returns text or None on error/no key.
    Falls back silently — callers should handle None.
    """
    api_key = load_gemini_key()
    if not api_key:
        return None

    import requests
    try:
        payload = {
            "system_instruction": {"parts": [{"text": system}]},
            "contents": [{"parts": [{"text": user}]}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.3},
        }
        resp = requests.post(
            _GEMINI_URL,
            params={"key": api_key},
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return None
