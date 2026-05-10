"""
decision.py — LLM synthesis layer for BTC bot signals

Wraps quant signals (VP-MACD + MA trend + 1h momentum) and HMM regime
into a structured Anthropic prompt, returns a JSON decision with
justification and confidence. Gracefully falls back if no API key.

Source: QuantAgent architecture (Y-Research-SBU/QuantAgent, arXiv:2509.09995v3)
"""

import json
import os
from pathlib import Path


_SYSTEM = """\
You are a systematic BTC/USDT trading assistant. Your role is to synthesize \
quantitative signals into a single trading decision.

Respond ONLY with valid JSON in this exact format — no markdown, no extra text:
{
  "action": "long" | "exit" | "hold",
  "justification": "1-2 sentences referencing specific signal values",
  "confidence": "high" | "medium" | "low"
}

Rules:
- action must match OR be more conservative than the quant action provided
- confidence=high: all signals aligned; medium: majority aligned; low: mixed/conflicting
- justification must cite actual numbers from the prompt, not generic statements
- if signals conflict (e.g., buy crossover but bear regime), always output hold or exit\
"""


def _load_api_key() -> str | None:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    env_file = Path(__file__).parent.parent.parent / ".secrets" / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ANTHROPIC_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


def get_decision(signal: dict, regime: dict) -> dict:
    """
    Synthesize VP-MACD signal + HMM regime into LLM-justified decision.

    Returns dict with all original signal keys plus:
      llm_action      : str  (may be more conservative than signal action)
      llm_justification: str
      llm_confidence  : str  (high/medium/low)
      llm_used        : bool
    """
    api_key = _load_api_key()

    base = {
        **signal,
        "llm_action":       signal["action"],
        "llm_justification": signal["reason"],
        "llm_confidence":   None,
        "llm_used":         False,
    }

    if not api_key:
        return base

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        user_msg = f"""\
Quant signals for BTC/USDT — latest 1h bar. What is the optimal action?

=== Momentum Signal (1h bars, VP-MACD) ===
VP-MACD value : {signal['vp_macd_val']}
Signal line   : {signal['signal_val']}
Quant action  : {signal['action'].upper()}
Quant reason  : {signal['reason']}
1h momentum   : {signal['mom_1h']:+.4%}
Daily trend   : {'BULL' if signal['is_bull'] else 'BEAR'} (MA20=${signal['ma20']:,.0f} MA100=${signal['ma100']:,.0f})

=== Regime (3-state HMM, 1d bars) ===
State         : {regime['state'].upper()}
Prob Bull     : {regime['prob_bull']:.1%}
Prob Neutral  : {regime['prob_neutral']:.1%}
Prob Bear     : {regime['prob_bear']:.1%}
Allow long    : {regime['allow_long']}
"""

        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system=[{"type": "text", "text": _SYSTEM,
                     "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user_msg}],
        )

        parsed = json.loads(resp.content[0].text)
        base["llm_action"]        = parsed.get("action", signal["action"])
        base["llm_justification"] = parsed.get("justification", signal["reason"])
        base["llm_confidence"]    = parsed.get("confidence")
        base["llm_used"]          = True

    except Exception:
        pass  # fallback to quant action silently

    return base
