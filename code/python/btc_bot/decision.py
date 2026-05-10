"""
decision.py — LLM synthesis layer for BTC bot signals

Wraps quant signals (VP-MACD + MA trend + 1h momentum) and HMM regime
into a structured Gemini prompt, returns a JSON decision with
justification and confidence. Gracefully falls back if no API key.

Source: QuantAgent architecture (Y-Research-SBU/QuantAgent, arXiv:2509.09995v3)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
from _llm import call_gemini  # noqa: E402

_SYSTEM = (
    "You are a systematic BTC/USDT trading assistant. Synthesize quant signals into a decision. "
    'Respond ONLY with valid JSON: {"action": "long"|"exit"|"hold", '
    '"justification": "1-2 sentences citing specific values", "confidence": "high"|"medium"|"low"}. '
    "action must match or be more conservative than the quant action. "
    "If signals conflict (buy crossover + bear regime), output hold or exit."
)


def get_decision(signal: dict, regime: dict) -> dict:
    """
    Synthesize VP-MACD signal + HMM regime into LLM-justified decision.

    Returns dict with all original signal keys plus:
      llm_action       : str  (may be more conservative than signal action)
      llm_justification: str
      llm_confidence   : str  (high/medium/low)
      llm_used         : bool
    """
    base = {
        **signal,
        "llm_action":        signal["action"],
        "llm_justification": signal["reason"],
        "llm_confidence":    None,
        "llm_used":          False,
    }

    user_msg = (
        f"BTC/USDT latest 1h bar signals:\n"
        f"VP-MACD={signal['vp_macd_val']} vs Signal={signal['signal_val']} | "
        f"action={signal['action'].upper()} | mom={signal['mom_1h']:+.4%} | "
        f"daily={'BULL' if signal['is_bull'] else 'BEAR'} "
        f"(MA20=${signal['ma20']:,.0f} MA100=${signal['ma100']:,.0f})\n"
        f"HMM regime={regime['state'].upper()} | "
        f"p_bull={regime['prob_bull']:.1%} p_bear={regime['prob_bear']:.1%} | "
        f"allow_long={regime['allow_long']}"
    )

    text = call_gemini(_SYSTEM, user_msg, max_tokens=200)
    if not text:
        return base

    try:
        # Strip markdown code fences if present
        clean = text.strip().strip("```json").strip("```").strip()
        parsed = json.loads(clean)
        base["llm_action"]        = parsed.get("action", signal["action"])
        base["llm_justification"] = parsed.get("justification", signal["reason"])
        base["llm_confidence"]    = parsed.get("confidence")
        base["llm_used"]          = True
    except Exception:
        pass  # fallback to quant action silently

    return base
