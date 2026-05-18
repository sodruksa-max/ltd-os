"""
Entry logic evaluator for Nick v3.

Decision tree for each candidate ticker:
  Gate 1 — VIX tier        : DANGER (>=30) = no buys; EXTENDED (25-29) = allowed with
                              reduced size via VIX-Rank continuous scaling (caller applies)
  Gate 2 — Capacity        : cash available, not already held, signal not OVERBOUGHT+EXTENDED
  Gate 3 — Signal          : RSI not OVERBOUGHT or MA20 not EXTENDED
  Gate 4 — News clean      : no kill flags from news digest
  -> PASS -> compute shares from conviction size (before VIX-Rank scale applied by caller)

Returns EvaluationResult dataclass with should_buy, skip_reason, shares, size_pct.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

REPO = Path(__file__).resolve().parents[3]
NICK_SIGNALS_PATH = REPO / "vault/Knowledge/nick-signals.md"

# v3: smaller capital, max 3 positions, 25-33% per position
CONVICTION_SIZE  = {"high": 0.33, "med": 0.25, "low": 0.15}
MAX_POSITION_PCT = 0.40
MIN_CASH_PCT     = 0.10
MAX_POSITIONS    = 3


@dataclass
class EvaluationResult:
    ticker:      str
    should_buy:  bool
    skip_reason: str = ""
    shares:      int = 0
    size_pct:    float = 0.0
    gates_log:   list[str] = field(default_factory=list)


def parse_nick_signals(path: Path = NICK_SIGNALS_PATH) -> dict[str, dict]:
    """
    Parse nick-signals.md table into {ticker: {rsi, ma20, rs, signal}}.
    Returns empty dict if file missing or unparseable.
    """
    if not path.exists():
        return {}

    signals: dict[str, dict] = {}
    # Match markdown table rows with 5 columns (Ticker | RSI | MA20 | RS | Signal)
    row_re = re.compile(
        r"^\|\s*([A-Z]+)\s*\|\s*([\w?]+)\s*\|\s*([\w?]+)\s*\|\s*([\w?]+)\s*\|\s*([^|]*?)\s*\|",
        re.MULTILINE,
    )
    for m in row_re.finditer(path.read_text(encoding="utf-8")):
        ticker, rsi, ma20, rs, sig = m.groups()
        if ticker in ("Ticker",):  # header row
            continue
        signals[ticker] = {
            "rsi":    rsi.strip().upper(),
            "ma20":   ma20.strip().upper(),
            "rs":     rs.strip().upper(),
            "signal": sig.strip(),
        }
    return signals


def _signal_blocks_entry(sig: dict) -> tuple[bool, str]:
    """
    Returns (blocks, reason). True if signal tier is unfavorable for a new entry.
    Don't buy: already OVERBOUGHT AND EXTENDED (stretched — likely to revert).
    """
    rsi  = sig.get("rsi", "?")
    ma20 = sig.get("ma20", "?")
    rs   = sig.get("rs", "?")

    if rsi == "OVERBOUGHT" and ma20 == "EXTENDED":
        return True, f"signal stretched (RSI={rsi}, MA20={ma20}) -- wait for pullback"

    if rs == "WEAK" and rsi == "OVERSOLD":
        return False, ""  # OVERSOLD + WEAK RS can still be valid thesis entry

    return False, ""


def evaluate_entry(
    ticker:      str,
    conviction:  str,
    nav:         float,
    cash:        float,
    price:       float,
    regime:      dict,
    news_digest: dict,
    nick_signals: dict,
    existing_positions: set[str],
    pending_orders:     set[str],
) -> EvaluationResult:
    log: list[str] = []
    tier = regime.get("tier", "EARLY")
    vix  = regime.get("VIX", {}).get("value", "?")

    # Gate 1 — VIX tier (v3: >=30 DANGER = hard block; EXTENDED 25-29 = allowed, caller scales size)
    if tier == "DANGER":
        return EvaluationResult(ticker, False, f"tier=DANGER (VIX={vix}): no new entries at VIX>=30", gates_log=log)
    log.append(f"Gate1 OK: tier={tier}, VIX={vix}")

    # Gate 2 — Capacity
    if ticker in existing_positions:
        return EvaluationResult(ticker, False, "already in portfolio", gates_log=log)
    if ticker in pending_orders:
        return EvaluationResult(ticker, False, "pending order exists", gates_log=log)

    size_pct     = CONVICTION_SIZE.get(conviction, 0.03)
    target_value = min(nav * size_pct, nav * MAX_POSITION_PCT)
    available    = cash * (1 - MIN_CASH_PCT)
    if available < price:
        return EvaluationResult(ticker, False, f"insufficient cash (${cash:.0f} available, need ${price:.0f})", gates_log=log)
    shares = int(min(target_value, available) / price)
    if shares < 1:
        return EvaluationResult(ticker, False, "cannot buy even 1 share at target sizing", gates_log=log)
    log.append(f"Gate2 OK: available=${available:.0f}, target={size_pct*100:.0f}% NAV, shares={shares}")

    # Gate 3 — Signal quality
    sig = nick_signals.get(ticker, {})
    if sig:
        blocked, reason = _signal_blocks_entry(sig)
        if blocked:
            return EvaluationResult(ticker, False, f"signal blocks entry: {reason}", gates_log=log)
        log.append(f"Gate3 OK: RSI={sig.get('rsi','?')}, MA20={sig.get('ma20','?')}, RS={sig.get('rs','?')}")
    else:
        log.append("Gate3 SKIP: no signal data for ticker -- proceeding")

    # Gate 4 — News clean
    news = news_digest.get(ticker, {})
    if not news.get("clean", True):
        flags = "; ".join(news.get("flags", []))
        return EvaluationResult(ticker, False, f"news kill flags active: {flags}", gates_log=log)
    log.append("Gate4 OK: news clean (no kill flags)")

    return EvaluationResult(
        ticker=ticker,
        should_buy=True,
        shares=shares,
        size_pct=size_pct,
        gates_log=log,
    )


if __name__ == "__main__":
    signals = parse_nick_signals()
    print(f"Parsed {len(signals)} ticker signals from nick-signals.md")
    for ticker in ["NVDA", "PLTR", "IONQ", "RKLB"]:
        s = signals.get(ticker, {})
        # strip non-ASCII for Windows console compatibility
        safe = {k: (v.encode("ascii", "replace").decode("ascii") if isinstance(v, str) else v)
                for k, v in s.items()}
        print(f"  {ticker}: {safe}")
