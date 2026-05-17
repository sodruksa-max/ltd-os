"""
_llm.py — shared LLM helper for scripts/

Cascade routing (arXiv:2603.04445, arXiv:2410.10347):
  Primary:  Google Gemini Flash Lite (free tier: 15 RPM, 1M tokens/day)
  Fallback: Anthropic Haiku (paid, activates only if Gemini returns None)

Use call_llm() for automatic cascade. Use call_gemini() / call_anthropic() directly if needed.
No extra packages needed — only `requests` (already installed).

Setup:
  GEMINI_API_KEY     — add to .secrets/.env (free: aistudio.google.com)
  ANTHROPIC_API_KEY  — optional, add to .secrets/.env for Haiku fallback
"""

import os
from pathlib import Path

_ENV_FILE = Path(__file__).parent.parent / ".secrets" / ".env"
_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash-lite:generateContent"
)
_ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
_ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"


def _load_key(name: str) -> str | None:
    key = os.environ.get(name)
    if key:
        return key
    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith(f"{name}="):
                return line.split("=", 1)[1].strip()
    return None


def load_gemini_key() -> str | None:
    return _load_key("GEMINI_API_KEY")


def load_anthropic_key() -> str | None:
    return _load_key("ANTHROPIC_API_KEY")


def call_gemini(system: str, user: str, max_tokens: int = 200) -> str | None:
    """Call Gemini Flash Lite. Returns text or None on error/no key."""
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


def call_anthropic(system: str, user: str, max_tokens: int = 200) -> str | None:
    """Call Anthropic Haiku. Returns text or None on error/no key."""
    api_key = load_anthropic_key()
    if not api_key:
        return None

    import requests
    try:
        resp = requests.post(
            _ANTHROPIC_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": _ANTHROPIC_MODEL,
                "max_tokens": max_tokens,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            },
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"].strip()
    except Exception:
        return None


def call_llm(system: str, user: str, max_tokens: int = 200) -> str | None:
    """
    Cascade: Gemini Flash Lite first → Anthropic Haiku fallback.
    Returns None only if both models unavailable/fail.
    """
    result = call_gemini(system, user, max_tokens)
    if result is not None:
        return result
    return call_anthropic(system, user, max_tokens)
