#!/usr/bin/env python3
"""
Auto-update nick-signals.md with RSI14 / MA20 position / RS-vs-SPY for all universe tickers.
Run daily before daily_scan.py so candidate scoring uses fresh signal data.

Signal tiers:
  RSI:  OVERSOLD <30 | LOW 30-45 | NEUTRAL 45-60 | HIGH 60-70 | OVERBOUGHT >70
  MA20: BELOW | MID 0-5% above | NEAR 5-10% above | EXTENDED >10% above
  RS:   WEAK <-5% vs SPY(60d) | NEUTRAL ±5% | STRONG >+5% vs SPY(60d)
"""

from __future__ import annotations

import importlib.util
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

REPO = Path(__file__).resolve().parent.parent
NICK_SIGNALS_PATH = REPO / "vault/Knowledge/nick-signals.md"
UNIVERSE_PATH     = REPO / "code/python/nick_trader/universe.py"


def _load_env() -> None:
    env_file = REPO / ".secrets" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


def _load_universe():
    spec = importlib.util.spec_from_file_location("universe", UNIVERSE_PATH)
    mod  = importlib.util.module_from_spec(spec)
    sys.modules["universe"] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Signal computation
# ---------------------------------------------------------------------------

def _rsi14(close: pd.Series) -> float | None:
    if len(close) < 15:
        return None
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss.replace(0, float("nan"))
    val   = 100.0 - 100.0 / (1.0 + rs.iloc[-1])
    return float(val) if not pd.isna(val) else None


def _rsi_tier(rsi: float | None) -> str:
    if rsi is None:  return "?"
    if rsi < 30:     return "OVERSOLD"
    if rsi < 45:     return "LOW"
    if rsi < 60:     return "NEUTRAL"
    if rsi < 70:     return "HIGH"
    return "OVERBOUGHT"


def _ma20_tier(price: float, ma20: float) -> str:
    if ma20 <= 0:      return "?"
    pct = (price - ma20) / ma20
    if pct < 0:        return "BELOW"
    if pct < 0.05:     return "MID"
    if pct < 0.10:     return "NEAR"
    return "EXTENDED"


def _rs_tier(ticker_ret60: float, spy_ret60: float) -> str:
    diff = ticker_ret60 - spy_ret60
    if diff > 0.05:   return "STRONG"
    if diff < -0.05:  return "WEAK"
    return "NEUTRAL"


def _signal_summary(rsi_t: str, ma20_t: str, rs_t: str) -> str:
    if rsi_t == "OVERBOUGHT" and ma20_t == "EXTENDED":
        return "STRETCHED — wait for pullback"
    if rsi_t == "OVERSOLD":
        return "OVERSOLD — thesis entry watch"
    if rsi_t == "NEUTRAL" and rs_t == "STRONG":
        return "SETUP — RSI neutral + RS strong"
    if rs_t == "STRONG" and ma20_t in ("NEAR", "MID"):
        return "RS STRONG + near MA"
    if ma20_t == "BELOW":
        return "BELOW MA20"
    return ""


# ---------------------------------------------------------------------------
# Alpaca data fetch (primary) — avoids yfinance rate limiting on 60+ tickers
# ---------------------------------------------------------------------------

def _fetch_bars_alpaca(all_tickers: list[str]) -> dict[str, pd.DataFrame | None] | None:
    """Fetch 130 calendar days of daily bars via Alpaca in one batch request.
    Returns {ticker: DataFrame(Close)} or None if Alpaca keys not set / request fails."""
    api_key    = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        return None

    from alpaca.data import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame

    client = StockHistoricalDataClient(api_key, secret_key)
    start  = datetime.combine(date.today() - timedelta(days=130), datetime.min.time())
    try:
        bars_data = client.get_stock_bars(
            StockBarsRequest(symbol_or_symbols=all_tickers, timeframe=TimeFrame.Day, start=start)
        ).data
    except Exception as exc:
        print(f"  [warn] Alpaca fetch failed: {exc}")
        return None

    hist: dict[str, pd.DataFrame | None] = {}
    for t in all_tickers:
        bars = bars_data.get(t)
        if not bars:
            hist[t] = None
            continue
        records = []
        for b in bars:
            if isinstance(b, dict):
                records.append({"Close": b["close"], "timestamp": b["timestamp"]})
            else:
                records.append({"Close": b.close, "timestamp": b.timestamp})
        df = pd.DataFrame(records).set_index("timestamp")
        df.index = pd.to_datetime(df.index, utc=True)
        hist[t] = df
    return hist


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def compute_signals(tier1: list[str], tier2: list[str]) -> dict[str, dict]:
    all_tickers = list(dict.fromkeys(tier1 + tier2 + ["SPY"]))
    print(f"  Fetching 90d data for {len(all_tickers)} tickers via Alpaca...")

    hist = _fetch_bars_alpaca(all_tickers)
    if hist is None:
        print("  Alpaca unavailable — falling back to yfinance...")
        raw = yf.download(all_tickers, period="90d", progress=False, auto_adjust=True)
        hist = {}
        if isinstance(raw.columns, pd.MultiIndex):
            for t in all_tickers:
                try:
                    df = raw.xs(t, axis=1, level=1).dropna(how="all")
                    hist[t] = df if len(df) > 0 else None
                except KeyError:
                    hist[t] = None
        else:
            hist[all_tickers[0]] = raw

    # SPY 60-day return for RS baseline
    spy_df = hist.get("SPY")
    spy_ret60 = (
        float((spy_df["Close"].iloc[-1] / spy_df["Close"].iloc[-60]) - 1)
        if spy_df is not None and len(spy_df) >= 60
        else 0.0
    )

    signals: dict[str, dict] = {}
    for ticker in tier1 + tier2:
        df = hist.get(ticker)
        if df is None or len(df) < 20:
            signals[ticker] = {"rsi": "?", "ma20": "?", "rs": "?", "signal": "no data"}
            continue

        close   = df["Close"]
        price   = float(close.iloc[-1])
        ma20    = float(close.rolling(20).mean().iloc[-1])
        rsi_val = _rsi14(close)
        ret60   = float((close.iloc[-1] / close.iloc[-60]) - 1) if len(close) >= 60 else float((close.iloc[-1] / close.iloc[0]) - 1)

        rsi_t  = _rsi_tier(rsi_val)
        ma20_t = _ma20_tier(price, ma20)
        rs_t   = _rs_tier(ret60, spy_ret60)
        sig    = _signal_summary(rsi_t, ma20_t, rs_t)

        signals[ticker] = {"rsi": rsi_t, "ma20": ma20_t, "rs": rs_t, "signal": sig}

    return signals


# ---------------------------------------------------------------------------
# Write nick-signals.md
# ---------------------------------------------------------------------------

def write_signals(tier1: list[str], tier2: list[str], signals: dict[str, dict]) -> None:
    now      = datetime.now().strftime("%Y-%m-%d %H:%M")
    tier2_ex = [t for t in tier2 if t not in set(tier1)]  # exclude T1 duplicates

    lines: list[str] = [
        "# Nick Signals",
        f"*Auto-updated: {now} | RSI14 / MA20-position / RS-vs-SPY(60d)*",
        "",
        "---",
        "",
        "## Signal Key",
        "- **RSI**: OVERSOLD <30 | LOW 30-45 | NEUTRAL 45-60 | HIGH 60-70 | OVERBOUGHT >70",
        "- **MA20**: BELOW | MID 0-5% above | NEAR 5-10% above | EXTENDED >10% above",
        "- **RS**: WEAK <-5% vs SPY(60d) | NEUTRAL ±5% | STRONG >+5% vs SPY(60d)",
        "",
        "---",
        "",
        "## Universe Signals",
        "",
        "**Tier 1 — Core Thesis (36 tickers)**",
        "",
        "| Ticker | RSI | MA20 | RS | Signal |",
        "|---|---|---|---|---|",
    ]
    for t in tier1:
        s = signals.get(t, {"rsi": "?", "ma20": "?", "rs": "?", "signal": ""})
        lines.append(f"| {t} | {s['rsi']} | {s['ma20']} | {s['rs']} | {s['signal']} |")

    lines += [
        "",
        "**Tier 2 — Growth Expansion (26 tickers)**",
        "",
        "| Ticker | RSI | MA20 | RS | Signal |",
        "|---|---|---|---|---|",
    ]
    for t in tier2_ex:
        s = signals.get(t, {"rsi": "?", "ma20": "?", "rs": "?", "signal": ""})
        lines.append(f"| {t} | {s['rsi']} | {s['ma20']} | {s['rs']} | {s['signal']} |")

    NICK_SIGNALS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    _load_env()
    univ    = _load_universe()
    tier1   = univ.TIER1
    tier2   = univ.TIER2
    signals = compute_signals(tier1, tier2)

    write_signals(tier1, tier2, signals)

    # Summary
    setups    = [t for t, s in signals.items() if "SETUP"     in s.get("signal", "")]
    stretched = [t for t, s in signals.items() if "STRETCHED" in s.get("signal", "")]
    strong_rs = [t for t, s in signals.items() if s.get("rs") == "STRONG"]
    oversold  = [t for t, s in signals.items() if s.get("rsi") == "OVERSOLD"]

    total = len(tier1) + len([t for t in tier2 if t not in set(tier1)])
    print(f"  Wrote {NICK_SIGNALS_PATH.name} ({total} tickers)")
    print(f"  SETUP:     {setups     or 'none'}")
    print(f"  STRETCHED: {stretched  or 'none'}")
    print(f"  RS STRONG: {strong_rs  or 'none'}")
    print(f"  OVERSOLD:  {oversold   or 'none'}")


if __name__ == "__main__":
    main()
