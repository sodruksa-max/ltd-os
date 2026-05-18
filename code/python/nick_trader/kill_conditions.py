"""
Kill condition evaluator for Nick v3.

v3 changes vs v2:
  - Dynamic stop: starts -15% (was -25%), ratchets UP as profit levels hit
  - Profit ladder:
      L1: price +40% -> sell 30%, stop ratchets to +5%
      L2: price +80% -> sell 20%, stop ratchets to +35%
      L3: price +150% -> sell 20%, remaining 30% rides free (stop removed)
  - Position schema additions: dynamic_stop_pct (float|None), profit_level (int 0-3)
  - kill_conditions array in position: news_keyword alert-only conditions only
  - Price-based exits are generated dynamically from dynamic_stop_pct + profit_level

Return schema for each triggered condition:
  id             — "stop" | "L1" | "L2" | "L3" | condition id from state
  label          — human-readable
  action         — "EXIT" (execute order) | "ALERT" (flag for review)
  partial        — fraction of shares to sell (omitted for full exits)
  price_pct      — current pct from entry
  new_stop_pct   — new dynamic_stop_pct to apply after execution (omitted if stop)
  new_profit_level — profit_level to set after execution (omitted if stop/alert)
  free_ride      — True if this is L3 (stop should be removed after execution)
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

STATE_PATH = Path("vault/20_investment/nick/nick_state.json")

DEFAULT_STOP_PCT = -0.15

# (level_id, entry_threshold, sell_fraction, new_stop_pct, tag, label)
# new_stop_pct = None means "free ride" (no stop after this level)
PROFIT_LADDER: list[tuple] = [
    (1, 0.40, 0.30, 0.05,  "L1", "L1 +40% — sell 30%, ratchet stop to +5%"),
    (2, 0.80, 0.20, 0.35,  "L2", "L2 +80% — sell 20%, ratchet stop to +35%"),
    (3, 1.50, 0.20, None,  "L3", "L3 +150% — sell 20%, free ride remaining 30%"),
]


def load_state() -> dict:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def _price_pct(ticker: str, positions: dict, market_data: dict) -> float | None:
    pos = positions.get(ticker, {})
    entry = pos.get("entry_price")
    current = market_data.get(ticker, {}).get("current_price")
    if entry is None or current is None or entry == 0:
        return None
    return (current - entry) / entry


def _headline_match(keywords: list[str], headlines: list[str]) -> bool:
    joined = " ".join(h.lower() for h in headlines)
    return any(kw.lower() in joined for kw in keywords)


def check_all_kills(
    state: dict,
    market_data: dict,
    news_digest: dict,
) -> dict[str, list[dict]]:
    """
    Evaluate all kill conditions for all positions.

    Returns {ticker: [triggered_conditions]}.
    Caller (daily_scan.py) applies state mutations after executing orders.
    """
    positions = state.get("positions", {})
    results: dict[str, list[dict]] = {}

    for ticker, pos_state in positions.items():
        triggered: list[dict[str, Any]] = []

        pct = _price_pct(ticker, positions, market_data)
        dynamic_stop = pos_state.get("dynamic_stop_pct", DEFAULT_STOP_PCT)
        profit_level = pos_state.get("profit_level", 0)

        # --- Dynamic stop check ---
        if dynamic_stop is not None and pct is not None and pct <= dynamic_stop:
            triggered.append({
                "id":        "stop",
                "label":     f"Dynamic stop hit at {dynamic_stop:+.0%} ({pct:+.1%} from entry)",
                "action":    "EXIT",
                "price_pct": round(pct, 4),
            })

        # --- Profit ladder check (skip if stop already triggered) ---
        elif pct is not None:
            for level_id, threshold, sell_frac, new_stop, tag, label in PROFIT_LADDER:
                if level_id <= profit_level:
                    continue  # already taken this level
                if pct >= threshold:
                    cond: dict[str, Any] = {
                        "id":               tag,
                        "label":            label,
                        "action":           "EXIT",
                        "partial":          sell_frac,
                        "price_pct":        round(pct, 4),
                        "new_profit_level": level_id,
                        "free_ride":        (level_id == 3),
                    }
                    if new_stop is not None:
                        cond["new_stop_pct"] = new_stop
                    triggered.append(cond)
                    break  # only one profit level triggers per day

        # --- L3 free-ride time-stop: alert if held >365 days after free-ride activated ---
        if profit_level >= 3 and dynamic_stop is None:
            entry_date_str = pos_state.get("entry_date")
            if entry_date_str:
                days_held = (date.today() - date.fromisoformat(entry_date_str)).days
                if days_held > 365:
                    triggered.append({
                        "id":        "L3-timestop",
                        "label":     f"L3 free-ride time-stop: {days_held} days held — review for exit or add time limit",
                        "action":    "ALERT",
                        "price_pct": round(pct, 4) if pct is not None else None,
                    })

        # --- News keyword alert conditions ---
        headlines = news_digest.get(ticker, {}).get("headlines", [])
        for cond in pos_state.get("kill_conditions", []):
            if cond.get("metric") != "news_keyword":
                continue
            keywords = cond.get("threshold", [])
            if _headline_match(keywords, headlines):
                entry: dict[str, Any] = {
                    "id":     cond.get("id"),
                    "label":  cond.get("label"),
                    "action": "ALERT",
                }
                if pct is not None:
                    entry["price_pct"] = round(pct, 4)
                triggered.append(entry)

        if triggered:
            results[ticker] = triggered

    return results


def format_kill_report(results: dict[str, list[dict]]) -> str:
    if not results:
        return "Kill check: no conditions triggered [CLEAN]"

    lines = ["Kill conditions triggered:"]
    for ticker, conditions in results.items():
        for c in conditions:
            action_tag = "[EXIT]" if c["action"] == "EXIT" else "[ALERT]"
            pct_str    = f" ({c['price_pct']:+.1%})" if "price_pct" in c else ""
            partial    = c.get("partial")
            extra      = f" [sell {int(partial * 100)}%]" if partial else ""
            if c.get("free_ride"):
                extra += " [free ride after]"
            lines.append(f"  {action_tag} {ticker} -- {c['id']}: {c['label']}{pct_str}{extra}")

    return "\n".join(lines)


if __name__ == "__main__":
    state = load_state()

    # Smoke-test: dummy prices at -1% from entry + one L1 hit
    dummy_market: dict[str, dict] = {}
    for ticker, pos in state.get("positions", {}).items():
        ep = pos.get("entry_price", 100)
        dummy_market[ticker] = {"current_price": ep * 0.99}

    # If there's at least one position, test the L1 trigger on the first one
    tickers = list(state.get("positions", {}).keys())
    if tickers:
        ep = state["positions"][tickers[0]].get("entry_price", 100)
        dummy_market[tickers[0]] = {"current_price": ep * 1.45}

    dummy_news: dict[str, dict] = {}
    results = check_all_kills(state, dummy_market, dummy_news)
    print(format_kill_report(results))
    print(f"\nPositions checked: {tickers or '(none)'}")
    print("Smoke-test complete.")
