"""
Kill condition evaluator for Nick v2.

Reads structured kill_conditions from nick_state.json and evaluates them
against live market data and a news digest.

Supported metrics:
  price_pct_from_entry  — (current_price - entry_price) / entry_price
  news_keyword          — substring match against today's headlines (case-insensitive)

Supported operators:
  lte          — less than or equal (price conditions, stop loss)
  gte          — greater than or equal (price conditions, take-profit)
  contains_any — any keyword from threshold list appears in headlines

Each condition returns either action="EXIT" (auto_exit=true) or action="ALERT" (alert_only=true).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STATE_PATH = Path("vault/20_investment/nick/nick_state.json")


def load_state() -> dict:
    return json.loads(STATE_PATH.read_text())


def load_kill_conditions(state: dict) -> dict[str, list[dict]]:
    return {
        ticker: pos.get("kill_conditions", [])
        for ticker, pos in state.get("positions", {}).items()
    }


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


def evaluate_condition(
    condition: dict,
    ticker: str,
    positions: dict,
    market_data: dict,
    news_digest: dict,
) -> bool:
    metric = condition.get("metric")
    operator = condition.get("operator")
    threshold = condition.get("threshold")

    if metric == "price_pct_from_entry":
        pct = _price_pct(ticker, positions, market_data)
        if pct is None:
            return False
        if operator == "lte":
            return pct <= threshold
        if operator == "gte":
            return pct >= threshold
        return False

    if metric == "news_keyword":
        if operator != "contains_any":
            return False
        headlines = news_digest.get(ticker, {}).get("headlines", [])
        return _headline_match(threshold, headlines)

    return False


def check_all_kills(
    state: dict,
    market_data: dict,
    news_digest: dict,
) -> dict[str, list[dict]]:
    """
    Evaluate all kill conditions for all positions.

    Returns {ticker: [triggered_conditions]} where each triggered entry has:
      id       — condition id from state
      label    — human-readable label
      action   — "EXIT" (auto-execute order) or "ALERT" (flag for weekly review)
      partial  — fraction to sell (only present when partial exit applies)
    """
    positions = state.get("positions", {})
    kill_map = load_kill_conditions(state)
    results: dict[str, list[dict]] = {}

    for ticker, conditions in kill_map.items():
        triggered: list[dict[str, Any]] = []
        for cond in conditions:
            if evaluate_condition(cond, ticker, positions, market_data, news_digest):
                entry: dict[str, Any] = {
                    "id": cond.get("id"),
                    "label": cond.get("label"),
                    "action": "EXIT" if cond.get("auto_exit") else "ALERT",
                }
                if "partial" in cond:
                    entry["partial"] = cond["partial"]

                pct = _price_pct(ticker, positions, market_data)
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
            pct_str = f" ({c['price_pct']:+.1%})" if "price_pct" in c else ""
            partial_str = f" [sell {int(c['partial'] * 100)}%]" if "partial" in c else ""
            lines.append(f"  {action_tag} {ticker} -- {c['id']}: {c['label']}{pct_str}{partial_str}")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    state = load_state()

    # Minimal smoke-test: inject dummy prices and empty news
    dummy_market = {
        ticker: {"current_price": pos["entry_price"] * 0.99}
        for ticker, pos in state["positions"].items()
    }
    dummy_news: dict[str, dict] = {}

    results = check_all_kills(state, dummy_market, dummy_news)
    print(format_kill_report(results))
    print(f"\nPositions checked: {list(state['positions'].keys())}")
    print("Smoke-test complete -- all prices at -1% from entry, no news.")
