"""
Nick v3 daily scanner — runs every US trading day at 9:30 AM EDT.

v3 changes vs v2:
  - Regime: VIX <25 EARLY, 25-30 EXTENDED (no entries), >=30 DANGER (no entries + alerts)
  - Trade logic: profit ladder L1/L2/L3 + ratchet stop (see kill_conditions.py)
  - Entry: universe scan (Tier1 daily, Tier2 weekly/Monday) replaces weekly-rec BUY execution
  - Capital: contribution gate — available_capital grows $110/month from inception
  - Max positions: 3
  - SELL/TRIM orders from weekly-rec.md are still executed

Flow:
  1. Load state + market context (regime)
  2. Fetch holdings news (--nick-news) for kill check
  3. Kill check + execute exits (stop / profit ladder / news alerts)
  4. Fetch universe news (--universe-news) for entry discovery
  5. Universe scan — find candidates, run 4-layer funnel, auto-buy
  6. Execute SELL/TRIM from latest weekly-rec.md (if any)
  7. Write daily audit log + update NAV + save state
"""

from __future__ import annotations

import argparse
import functools
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import pandas as pd
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO           = Path(__file__).resolve().parents[3]
NICK_DIR       = REPO / "vault/20_investment/nick"
WEEKLY_DIR     = NICK_DIR / "weekly"
TRADE_LOG      = NICK_DIR / "trade-log.md"
NAV_LOG        = NICK_DIR / "performance/nav_log.md"
STATE_FILE     = NICK_DIR / "nick_state.json"
DAILY_DIR      = NICK_DIR / "daily"
CONVERGENCE_MD   = REPO / "vault/Knowledge/thesis-convergence.md"
NICK_SIGNALS     = REPO / "vault/Knowledge/nick-signals.md"
NEWS_SCRIPT      = REPO / "scripts/news-snapshot.py"
MISOPHONIA_PATH  = REPO / "vault/Knowledge/misophonia-triggers.md"
PYTHON           = Path(sys.executable)

MAX_POSITIONS = 3

# ---------------------------------------------------------------------------
# Sibling module loader
# ---------------------------------------------------------------------------

def _import_sibling(name: str):
    path = Path(__file__).parent / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


kc_mod   = _import_sibling("kill_conditions")
el_mod   = _import_sibling("entry_logic")
univ_mod = _import_sibling("universe")

# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def load_state() -> dict:
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def append_trade_log(row: dict) -> None:
    with open(TRADE_LOG, "a", encoding="utf-8") as f:
        f.write(
            "| {date} | {ticker} | {action} | {shares} | ${price:.2f} | "
            "- | {conviction} | {vix} | - | - | {reason} |\n".format(**row)
        )


def append_nav_log(nav: float, note: str = "") -> None:
    row = f"| {date.today()} | ${nav:,.2f} | - | - | {note} |\n"
    with open(NAV_LOG, "a", encoding="utf-8") as f:
        f.write(row)

# ---------------------------------------------------------------------------
# Contribution gate
# ---------------------------------------------------------------------------

def get_available_capital(state: dict) -> float:
    """Max capital deployable — preloaded contributions count as already-elapsed months."""
    contrib = state.get("contributions", {})
    if not contrib:
        return float("inf")
    base      = contrib.get("base_capital_usd", 1000.0)
    monthly   = contrib.get("monthly_usd", 110.0)
    total     = contrib.get("preloaded_total_usd", base)
    inception = contrib.get("inception_date")
    if not inception:
        return base
    days_elapsed   = max(0, (date.today() - date.fromisoformat(inception)).days)
    months_elapsed = days_elapsed // 30
    # Preloaded contributions are treated as already-elapsed months
    preloaded_months = int((total - base) / monthly) if monthly > 0 else 0
    effective_months = months_elapsed + preloaded_months
    return min(base + effective_months * monthly, total)


def get_deployed_capital(state: dict) -> float:
    """Sum of entry_price * shares for all open positions (cost basis)."""
    total = 0.0
    for pos in state.get("positions", {}).values():
        total += pos.get("entry_price", 0) * pos.get("shares", 0)
    return total

# ---------------------------------------------------------------------------
# Market context
# ---------------------------------------------------------------------------

def get_regime() -> dict:
    data: dict = {}
    # VIX: fetch 1y for percentile_252d (used in VIX-Rank continuous scaling)
    try:
        vix_hist  = yf.Ticker("^VIX").history(period="1y")["Close"]
        vix_price = float(vix_hist.iloc[-1])
        vix_ma50  = float(vix_hist.rolling(50).mean().iloc[-1])
        vix_pct   = float((vix_hist <= vix_price).sum() / len(vix_hist))
        data["VIX"] = {
            "value":          round(vix_price, 2),
            "above_50ma":     bool(vix_price > vix_ma50),
            "percentile_252d": round(vix_pct, 3),
        }
    except Exception:
        data["VIX"] = {"value": None, "above_50ma": None, "percentile_252d": 0.5}

    for name, sym in {"TNX": "^TNX", "SOXX": "SOXX", "QQQM": "QQQM"}.items():
        try:
            hist  = yf.Ticker(sym).history(period="60d")["Close"]
            price = hist.iloc[-1]
            ma50  = hist.rolling(50).mean().iloc[-1]
            data[name] = {"value": round(float(price), 2), "above_50ma": bool(price > ma50)}
        except Exception:
            data[name] = {"value": None, "above_50ma": None}

    vix = data.get("VIX", {}).get("value") or 20
    # v3 thresholds: <25 EARLY, 25-30 EXTENDED (scaled), >=30 DANGER (hard block)
    data["tier"] = "EARLY" if vix < 25 else ("EXTENDED" if vix < 30 else "DANGER")
    return data


def get_price(ticker: str) -> float | None:
    """Latest price via Alpaca latest-trade; falls back to yfinance."""
    api_key    = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if api_key and secret_key:
        try:
            from alpaca.data import StockHistoricalDataClient
            from alpaca.data.requests import StockLatestTradeRequest
            client = StockHistoricalDataClient(api_key, secret_key)
            resp   = client.get_stock_latest_trade(StockLatestTradeRequest(symbol_or_symbols=[ticker]))
            if ticker in resp:
                return float(resp[ticker].price)
        except Exception:
            pass
    try:
        return float(yf.Ticker(ticker).fast_info["lastPrice"])
    except Exception:
        return None


def get_atr14(ticker: str) -> float | None:
    """ATR14 in price units via Alpaca 45-day bars; falls back to yfinance."""
    from datetime import datetime as _dt
    api_key    = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if api_key and secret_key:
        try:
            from alpaca.data import StockHistoricalDataClient
            from alpaca.data.requests import StockBarsRequest
            from alpaca.data.timeframe import TimeFrame
            client = StockHistoricalDataClient(api_key, secret_key)
            start  = _dt.combine(date.today() - timedelta(days=45), _dt.min.time())
            bars   = client.get_stock_bars(
                StockBarsRequest(symbol_or_symbols=[ticker], timeframe=TimeFrame.Day, start=start)
            ).data.get(ticker, [])
            if len(bars) < 15:
                return None
            highs  = [b.high  if hasattr(b, "high")  else b["high"]  for b in bars]
            lows   = [b.low   if hasattr(b, "low")   else b["low"]   for b in bars]
            closes = [b.close if hasattr(b, "close") else b["close"] for b in bars]
            tr_vals = [
                max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
                for i in range(1, len(bars))
            ]
            if len(tr_vals) < 14:
                return None
            return float(sum(tr_vals[-14:]) / 14)
        except Exception:
            pass
    # fallback to yfinance
    try:
        hist = yf.Ticker(ticker).history(period="30d")
        if len(hist) < 15:
            return None
        tr = pd.concat([
            hist["High"] - hist["Low"],
            (hist["High"] - hist["Close"].shift(1)).abs(),
            (hist["Low"]  - hist["Close"].shift(1)).abs(),
        ], axis=1).max(axis=1)
        return float(tr.rolling(14).mean().iloc[-1])
    except Exception:
        return None


@functools.lru_cache(maxsize=256)
def _earnings_within_days(ticker: str, days: int = 2) -> bool:
    """Return True if ticker has confirmed earnings date within next `days` calendar days."""
    try:
        cal = yf.Ticker(ticker).calendar
        if not cal:
            return False
        today  = date.today()
        cutoff = today + timedelta(days=days)
        for d in cal.get("Earnings Date", []):
            try:
                d_date = d.date() if hasattr(d, "date") else d
                if today <= d_date <= cutoff:
                    return True
            except Exception:
                pass
        return False
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Misophonia trigger registry loader
# ---------------------------------------------------------------------------

def load_misophonia_triggers() -> list[tuple[str, str]]:
    """Parse Company-Level triggers → [(category, keyword_lowercase)].
    Only quoted phrases or first token before '|' are extracted.
    """
    if not MISOPHONIA_PATH.exists():
        return []
    triggers: list[tuple[str, str]] = []
    in_company = False
    for line in MISOPHONIA_PATH.read_text(encoding="utf-8").splitlines():
        if "## Company-Level" in line:
            in_company = True
        elif line.startswith("## ") and "Company-Level" not in line:
            in_company = False
        elif in_company and line.strip().startswith("["):
            cat = re.match(r'\[(\w+)\]', line)
            phrase = re.search(r'"([^"]+)"', line)
            if cat and phrase:
                triggers.append((cat.group(1), phrase.group(1).lower()))
            elif cat:
                text = re.search(r'\]\s+([^|]+)', line)
                if text:
                    triggers.append((cat.group(1), text.group(1).strip().lower()))
    return triggers


# ---------------------------------------------------------------------------
# Tourette overnight reflex scan
# ---------------------------------------------------------------------------

def run_tourette_scan(state: dict, market_data: dict) -> list[str]:
    """Flag any holding that moved >5% overnight — fires BEFORE kill analysis."""
    flags: list[str] = []
    for ticker in state.get("positions", {}):
        d       = market_data.get(ticker, {})
        current = d.get("current_price")
        prev    = d.get("prev_close")
        if current and prev and prev > 0:
            move = (current - prev) / prev
            if abs(move) > 0.05:
                direction = "UP" if move > 0 else "DN"
                flags.append(f"[REFLEX] {ticker} {direction} {move:+.1%} overnight -- verify kill conditions")
    return flags


# ---------------------------------------------------------------------------
# Thesis convergence (for Layer 1 of 4-gate funnel)
# ---------------------------------------------------------------------------

def get_strong_convergence_theses() -> set[str]:
    """Parse thesis-convergence.md and return thesis IDs with STRONG signal."""
    if not CONVERGENCE_MD.exists():
        return set()
    text = CONVERGENCE_MD.read_text(encoding="utf-8")
    strong: set[str] = set()
    in_strong = False
    for line in text.splitlines():
        if line.startswith("###") and "STRONG" in line:
            in_strong = True
        elif line.startswith("###"):
            in_strong = False
        elif in_strong and "**Theses:**" in line:
            for m in re.findall(r"T(\d+)", line):
                strong.add(f"T{m}")
    return strong

# ---------------------------------------------------------------------------
# News helpers
# ---------------------------------------------------------------------------

def _run_news_script(flag: str) -> dict:
    try:
        result = subprocess.run(
            [str(PYTHON), str(NEWS_SCRIPT), flag],
            capture_output=True, text=True, timeout=90,
            cwd=str(REPO),
        )
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                print(f"  {line}")
        if result.returncode != 0 or not result.stdout.strip():
            print(f"  [WARN] {flag} fetch failed — proceeding without news")
            return {}
        return json.loads(result.stdout)
    except Exception as e:
        print(f"  [WARN] {flag} exception: {e}")
        return {}


def fetch_holdings_news() -> dict:
    print("  Fetching holdings news (--nick-news)...")
    return _run_news_script("--nick-news")


def fetch_universe_news() -> dict:
    print("  Fetching universe news (--universe-news)...")
    return _run_news_script("--universe-news")

# ---------------------------------------------------------------------------
# L3 peak tracker
# ---------------------------------------------------------------------------

def update_l3_peaks(state: dict, market_data: dict) -> dict:
    """Update peak_price for free-ride positions (profit_level>=3, stop=None).
    Called before kill check so drawdown is measured against today's high-water mark.
    """
    for ticker, pos in state.get("positions", {}).items():
        if pos.get("profit_level", 0) < 3 or pos.get("dynamic_stop_pct") is not None:
            continue
        current = market_data.get(ticker, {}).get("current_price")
        if not current:
            continue
        old_peak = pos.get("peak_price", pos.get("entry_price", current))
        if current > old_peak:
            pos["peak_price"] = round(current, 2)
    return state


# ---------------------------------------------------------------------------
# Kill check + exits
# ---------------------------------------------------------------------------

def run_kill_exits(
    state: dict,
    client: TradingClient,
    market_data: dict,
    news_digest: dict,
    vix: float,
    audit: dict,
    dry_run: bool = False,
) -> dict:
    """Evaluate kill conditions; execute exits; apply state mutations."""
    triggered_map = kc_mod.check_all_kills(state, market_data, news_digest)
    audit["kill_check"] = {}

    if not triggered_map:
        print("  Kill check: all clear")
        return state

    for ticker, conditions in triggered_map.items():
        audit["kill_check"][ticker] = conditions

        for cond in conditions:
            action = cond["action"]
            label  = cond["label"]
            pct    = cond.get("price_pct", 0)

            if action == "ALERT":
                print(f"  [ALERT] {ticker}: {label} ({pct:+.1%})")
                continue

            # --- EXIT ---
            try:
                alpaca_pos = {p.symbol: p for p in client.get_all_positions()}.get(ticker)
                if not alpaca_pos:
                    print(f"  [EXIT] {ticker}: no Alpaca position — skipping")
                    continue

                total_qty = int(float(alpaca_pos.qty))
                price     = float(alpaca_pos.current_price)
                partial   = cond.get("partial")
                sell_qty  = max(1, int(total_qty * partial)) if partial else total_qty
                action_label = f"PARTIAL-EXIT ({int(partial * 100)}%)" if partial else "EXIT"

                if dry_run:
                    print(f"  [DRY-RUN {action_label}] {ticker}: would sell {sell_qty} shares @ ${price:.2f} -- {label} ({pct:+.1%})")
                    continue

                client.submit_order(MarketOrderRequest(
                    symbol=ticker, qty=sell_qty, side=OrderSide.SELL, time_in_force=TimeInForce.DAY
                ))
                print(f"  [{action_label}] {ticker}: {sell_qty} shares @ ${price:.2f} -- {label} ({pct:+.1%})")

                append_trade_log(dict(
                    date=date.today(), ticker=ticker, action=action_label,
                    shares=sell_qty, price=price, conviction="auto",
                    vix=vix, reason=label,
                ))

                # Apply state mutations
                pos = state["positions"].get(ticker, {})

                if not partial:
                    state["positions"].pop(ticker, None)
                else:
                    pos["shares"] = max(0, pos.get("shares", 0) - sell_qty)
                    if "new_profit_level" in cond:
                        pos["profit_level"] = cond["new_profit_level"]
                    if cond.get("free_ride"):
                        pos["dynamic_stop_pct"] = None
                    elif "new_stop_pct" in cond:
                        pos["dynamic_stop_pct"] = cond["new_stop_pct"]
                    state["positions"][ticker] = pos

            except Exception as e:
                print(f"  [ERROR] {ticker} exit failed: {e}")

    # DANGER regime: alert all remaining positions
    if state.get("_regime_tier") == "DANGER":
        for ticker in state.get("positions", {}):
            if ticker not in triggered_map:
                print(f"  [DANGER ALERT] {ticker}: VIX>=30, review for manual exit")

    return state

# ---------------------------------------------------------------------------
# Universe scan (4-layer entry funnel)
# ---------------------------------------------------------------------------

def _score_candidate(
    ticker: str,
    nick_signals: dict,
    universe_news: dict,
    strong_theses: set[str],
    is_tier1: bool,
    miso_triggers: list[tuple[str, str]] | None = None,
) -> int | None:
    """Score a candidate 0-100. Returns None if hard-blocked."""
    score = 50

    # Layer 1 — Signal quality (nick-signals.md)
    sig  = nick_signals.get(ticker, {})
    rsi  = sig.get("rsi", "?")
    ma20 = sig.get("ma20", "?")
    rs   = sig.get("rs", "?")

    if rsi == "OVERBOUGHT" and ma20 == "EXTENDED":
        return None  # stretched — don't chase

    if rsi == "NEUTRAL":
        score += 10
    if ma20 in ("NEAR", "MID"):
        score += 10
    if rs == "STRONG":
        score += 15
    elif rs == "WEAK":
        score -= 10

    # Layer 2 — News clean for entry (universe-news)
    news = universe_news.get(ticker, {})
    if not news.get("clean_for_entry", True):
        return None  # negative news gates entry
    if news.get("has_catalyst", False):
        # [HYPERLEXIA] spin language detected → catalyst is management PR, not real news
        # [PARANOID]   single-source → PR echo, not independent corroboration
        spin         = news.get("spin_detected", False)
        single_src   = news.get("source_count", 2) <= 1
        score += 5 if (spin or single_src) else 15

    # [TOURETTE] unusual headline volume when clean → something is happening
    if news.get("high_activity", False) and news.get("clean_for_entry", True):
        score += 3

    # Layer 2.5 — Earnings-eve gate (binary event risk within 2 calendar days)
    if _earnings_within_days(ticker):
        return None  # undisclosed binary risk — skip until after earnings

    # Misophonia hard gate — check headlines against trigger registry
    if miso_triggers:
        headlines = news.get("headlines", [])
        joined    = " ".join(h.lower() for h in headlines)
        for cat, kw in miso_triggers:
            if kw in joined:
                return None  # trigger pattern found — hard block, cannot suppress

    # Layer 3 — Thesis convergence
    thesis = univ_mod.TICKER_THESIS.get(ticker, "")
    if thesis in strong_theses:
        score += 10

    # Layer 4 — Tier priority
    if is_tier1:
        score += 5

    return score


def run_universe_scan(
    state: dict,
    client: TradingClient,
    regime: dict,
    universe_news: dict,
    nick_signals: dict,
    strong_theses: set[str],
    nav: float,
    audit: dict,
    dry_run: bool = False,
    miso_triggers: list[tuple[str, str]] | None = None,
) -> dict:
    """Scan universe for entry candidates; auto-buy top scorers."""
    tier = regime.get("tier")
    vix  = regime.get("VIX", {}).get("value", "?")
    audit["universe_scan"] = {"tier": tier, "candidates_scored": [], "orders_executed": []}

    if tier == "DANGER":
        print(f"  Universe scan: SKIP (tier=DANGER, VIX={vix})")
        return state

    current_count = len(state.get("positions", {}))
    if current_count >= MAX_POSITIONS:
        print(f"  Universe scan: SKIP (at max {MAX_POSITIONS} positions)")
        return state

    slots_open = MAX_POSITIONS - current_count

    # VIX-Rank continuous size scaling (arXiv:2508.16598)
    # percentile=0.0 → scale=1.0 (full size); percentile=1.0 → scale=0.50 (half size, floor)
    vix_pct   = regime.get("VIX", {}).get("percentile_252d", 0.5)
    vix_scale = max(0.50, 1.0 - 0.5 * vix_pct)
    audit["universe_scan"]["vix_scale"] = round(vix_scale, 3)
    print(f"  VIX-Rank: percentile={vix_pct:.0%} → size_scale={vix_scale:.2f}")

    # Contribution gate: how much capital can we deploy?
    avail_cap   = get_available_capital(state)
    deployed    = get_deployed_capital(state)
    free_cap    = avail_cap - deployed
    if free_cap < 50:
        print(f"  Universe scan: SKIP (available_capital=${avail_cap:.0f}, deployed=${deployed:.0f}, free=${free_cap:.0f})")
        return state

    # Get existing holdings + pending orders
    alpaca_held    = {p.symbol for p in client.get_all_positions()}
    state_held     = set(state.get("positions", {}).keys())
    already_held   = alpaca_held | state_held
    pending_orders = {
        o.symbol for o in client.get_orders(
            filter=GetOrdersRequest(status=QueryOrderStatus.OPEN)
        )
    }

    # Build candidate list (Tier1 daily, Tier2 on Mondays)
    tier1_set = set(univ_mod.TIER1)
    candidates: list[tuple[str, bool]] = []  # (ticker, is_tier1)
    for t in univ_mod.TIER1:
        if t not in already_held and t not in pending_orders:
            candidates.append((t, True))
    if date.today().weekday() == 0:  # Monday — add Tier2
        for t in univ_mod.TIER2:
            if t not in already_held and t not in pending_orders and t not in tier1_set:
                candidates.append((t, False))

    print(f"  Universe scan: {len(candidates)} candidates (Tier1 + {'Tier2 Monday' if date.today().weekday() == 0 else 'Tier2 skip'})")

    # Score all candidates
    scored: list[tuple[int, str, bool]] = []
    for ticker, is_t1 in candidates:
        s = _score_candidate(ticker, nick_signals, universe_news, strong_theses, is_t1,
                             miso_triggers=miso_triggers)
        tier_label = "T1" if is_t1 else "T2"
        audit["universe_scan"]["candidates_scored"].append(
            {"ticker": ticker, "tier": tier_label, "score": s}
        )
        if s is not None:
            scored.append((s, ticker, is_t1))

    scored.sort(reverse=True)

    # Score leaderboard — top 10 candidates (including those not bought due to slot limits)
    top_n = min(10, len(scored))
    if top_n > 0:
        print(f"  Leaderboard ({top_n} of {len(scored)} scored | {len(candidates) - len(scored)} blocked by gates):")
        for rank, (s, t, t1) in enumerate(scored[:top_n], 1):
            cat_tag = " [catalyst]" if universe_news.get(t, {}).get("has_catalyst") else ""
            tier_tag = "T1" if t1 else "T2"
            print(f"    {rank:2}. {t:<6} [{tier_tag}] score={s:3}{cat_tag}")
    else:
        print("  Universe scan: 0 candidates passed all gates")

    audit["universe_scan"]["top10"] = [
        {"rank": i + 1, "ticker": t, "score": s, "tier": "T1" if t1 else "T2"}
        for i, (s, t, t1) in enumerate(scored[:10])
    ]

    # Execute buys for top candidates
    # Dyslexia: track bought theses — don't buy 2 candidates from same thesis in one day
    bought_theses: set[str] = set()
    executed = 0
    for score, ticker, is_t1 in scored:
        if executed >= slots_open:
            break

        thesis = univ_mod.TICKER_THESIS.get(ticker, "")
        if thesis and thesis in bought_theses:
            print(f"  [DYSLEXIA] SKIP {ticker}: thesis {thesis} already bought today (concentration guard)")
            continue

        price = get_price(ticker)
        if not price:
            print(f"  SKIP {ticker}: cannot fetch price")
            continue

        # Size: base 33% (T1) / 25% (T2) × VIX-Rank scale
        base_size    = 0.33 if is_t1 else 0.25
        size_pct     = round(base_size * vix_scale, 3)
        target_value = avail_cap * size_pct
        per_slot_cap = free_cap / max(1, slots_open - executed)
        order_value  = min(target_value, per_slot_cap * 0.95)

        if order_value < price:
            print(f"  SKIP {ticker}: order_value=${order_value:.0f} < price=${price:.2f}")
            continue

        shares = max(1, int(order_value / price))

        try:
            # ATR-based initial stop (arXiv:2511.08571):
            # stop = max(-15%, -(2 × ATR14 / entry_price)) — tighter for low-vol stocks
            atr14 = get_atr14(ticker)
            if atr14 and price > 0:
                initial_stop = round(max(kc_mod.DEFAULT_STOP_PCT, -(2.0 * atr14 / price)), 4)
            else:
                initial_stop = kc_mod.DEFAULT_STOP_PCT

            atr_note = f"ATR14={atr14:.2f}" if atr14 else "ATR14=n/a"

            if dry_run:
                print(f"  [DRY-RUN BUY] {ticker}: would buy {shares} shares @ ~${price:.2f} "
                      f"(score={score}, size={size_pct:.0%}, stop={initial_stop:+.1%}, {atr_note})")
                if thesis:
                    bought_theses.add(thesis)
                executed += 1
                continue

            client.submit_order(MarketOrderRequest(
                symbol=ticker, qty=shares, side=OrderSide.BUY, time_in_force=TimeInForce.DAY
            ))

            state["positions"][ticker] = {
                "entry_date":        str(date.today()),
                "entry_price":       round(price, 2),
                "shares":            shares,
                "weight":            round(size_pct, 3),
                "dynamic_stop_pct":  initial_stop,
                "profit_level":      0,
                "kill_conditions":   [],
            }
            audit["universe_scan"]["orders_executed"].append(ticker)

            print(f"  [BUY] {ticker}: {shares} shares @ ~${price:.2f} "
                  f"(score={score}, size={size_pct:.0%}, stop={initial_stop:+.1%}, {atr_note})")

            append_trade_log(dict(
                date=date.today(), ticker=ticker, action="BUY",
                shares=shares, price=price, conviction="high" if is_t1 else "med",
                vix=vix, reason=f"universe-scan score={score} stop={initial_stop:+.1%}",
            ))
            if thesis:
                bought_theses.add(thesis)
            executed += 1

        except Exception as e:
            print(f"  [ERROR] {ticker} buy failed: {e}")

    if executed == 0:
        print("  Universe scan: no buys executed")

    return state

# ---------------------------------------------------------------------------
# SELL/TRIM from weekly-rec.md (manual override / nick weekly decisions)
# ---------------------------------------------------------------------------

def run_weekly_sell_trim(
    state: dict,
    client: TradingClient,
    vix: float,
    audit: dict,
    dry_run: bool = False,
) -> dict:
    """Execute SELL/TRIM orders from latest weekly-rec.md."""
    files = sorted(WEEKLY_DIR.glob("*_weekly-rec.md"), reverse=True)
    if not files:
        return state

    rec_name = files[0].name
    if state.get("last_sell_trim_rec") == rec_name:
        print(f"  SELL/TRIM: {rec_name} already executed")
        return state

    m = re.search(
        r"## ORDERS.*?```json\s*\n(\[.*?\])\s*\n```",
        files[0].read_text(encoding="utf-8"), re.DOTALL
    )
    if not m:
        return state

    orders = json.loads(m.group(1))
    alpaca_positions = {p.symbol: p for p in client.get_all_positions()}
    executed_any = False

    audit["sell_trim"] = {"rec": rec_name, "executed": []}

    for order in orders:
        action = order.get("action", "").upper()
        ticker = order.get("ticker", "").upper()
        reason = order.get("reason", "")

        if action not in ("SELL", "TRIM"):
            continue

        pos = alpaca_positions.get(ticker)
        if not pos:
            print(f"  SKIP {action} {ticker}: no Alpaca position")
            continue

        qty      = int(float(pos.qty))
        price    = float(pos.current_price)
        sell_qty = max(1, qty // 2) if action == "TRIM" else qty

        try:
            if dry_run:
                print(f"  [DRY-RUN {action}] {ticker}: would sell {sell_qty}/{qty} shares @ ${price:.2f} -- {reason}")
                audit["sell_trim"]["executed"].append(ticker)
                executed_any = True
                continue

            client.submit_order(MarketOrderRequest(
                symbol=ticker, qty=sell_qty, side=OrderSide.SELL, time_in_force=TimeInForce.DAY
            ))
            print(f"  [{action}] {ticker}: {sell_qty}/{qty} shares @ ${price:.2f} -- {reason}")
            append_trade_log(dict(
                date=date.today(), ticker=ticker, action=action,
                shares=sell_qty, price=price, conviction="manual",
                vix=vix, reason=reason,
            ))
            if action == "SELL":
                state["positions"].pop(ticker, None)
            audit["sell_trim"]["executed"].append(ticker)
            executed_any = True
        except Exception as e:
            print(f"  [ERROR] {ticker} {action} failed: {e}")

    if executed_any:
        state["last_sell_trim_rec"] = rec_name

    return state

# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------

def write_daily_audit(audit: dict) -> None:
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    path = DAILY_DIR / f"{date.today()}.json"
    path.write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")
    print(f"  Audit log: {path.name}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Nick v3 daily scanner")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview orders without submitting; state not saved")
    args = parser.parse_args()
    dry_run = args.dry_run

    load_env()
    state = load_state()

    audit: dict = {
        "date":    str(date.today()),
        "version": "nick-v3",
        "dry_run": dry_run,
    }

    mode_tag = " [DRY-RUN]" if dry_run else ""
    print(f"\n=== Nick v3 Daily Scan {date.today()}{mode_tag} ===")

    # 1. Market context
    print("\n[1] Market context...")
    regime = get_regime()
    tier   = regime.get("tier")
    vix    = regime.get("VIX", {}).get("value", "?")
    tnx    = regime.get("TNX", {}).get("value", "?")
    avail  = get_available_capital(state)
    deployed = get_deployed_capital(state)
    print(f"  Tier={tier} | VIX={vix} | 10Y={tnx}")
    print(f"  Capital: available=${avail:.0f} | deployed=${deployed:.0f} | free=${avail - deployed:.0f}")
    audit["regime"] = regime
    audit["capital"] = {"available": avail, "deployed": deployed}

    # Store tier for DANGER alert in kill exits
    state["_regime_tier"] = tier

    # 2. Holdings news (kill check)
    print("\n[2] Holdings news...")
    holdings_news = fetch_holdings_news() if state.get("positions") else {}
    audit["holdings_news_tickers"] = {t: d.get("clean") for t, d in holdings_news.items()}

    # 3. Kill check + exits
    print("\n[3] Kill condition check...")
    client  = TradingClient(os.environ["ALPACA_API_KEY"], os.environ["ALPACA_SECRET_KEY"], paper=True)
    account = client.get_account()
    nav     = round(float(account.portfolio_value), 2)
    cash    = float(account.cash)

    alpaca_positions_map = {p.symbol: p for p in client.get_all_positions()}
    market_data: dict[str, dict] = {}
    for ticker in state.get("positions", {}):
        pos = alpaca_positions_map.get(ticker)
        if pos:
            market_data[ticker] = {"current_price": float(pos.current_price)}
        else:
            price = get_price(ticker)
            if price:
                market_data[ticker] = {"current_price": price}
        # Fetch prev_close for Tourette overnight reflex
        try:
            hist = yf.Ticker(ticker).history(period="2d")["Close"]
            if len(hist) >= 2:
                market_data.setdefault(ticker, {})["prev_close"] = round(float(hist.iloc[-2]), 4)
        except Exception:
            pass

    state = update_l3_peaks(state, market_data)

    # Tourette overnight reflex — fires before any analysis
    tourette_flags = run_tourette_scan(state, market_data)
    if tourette_flags:
        print("  Tourette reflex flags (pre-analysis — verify in kill check):")
        for f in tourette_flags:
            print(f"    {f}")
        audit["tourette_flags"] = tourette_flags
    else:
        print("  Tourette reflex: clean")

    # Misophonia check on holdings news
    miso_triggers = load_misophonia_triggers()
    for ticker, news_data in holdings_news.items():
        headlines = news_data.get("headlines", [])
        joined    = " ".join(h.lower() for h in headlines)
        for cat, kw in miso_triggers:
            if kw in joined:
                print(f"  [MISOPHONIA: TRIGGER] {ticker} [{cat}] \"{kw}\" — cannot suppress, review before kill check")

    state = run_kill_exits(state, client, market_data, holdings_news, vix, audit, dry_run=dry_run)

    # 4. Universe news (entry discovery)
    print("\n[4] Universe news...")
    universe_news = fetch_universe_news()
    audit["universe_news_count"] = len(universe_news)

    # 5. Universe scan (auto-buy)
    print("\n[5] Universe scan (entry)...")
    nick_signals   = el_mod.parse_nick_signals()
    strong_theses  = get_strong_convergence_theses()
    miso_triggers  = load_misophonia_triggers()
    print(f"  Strong convergence theses: {sorted(strong_theses) or 'none detected'}")
    state = run_universe_scan(state, client, regime, universe_news, nick_signals, strong_theses, nav, audit,
                              dry_run=dry_run, miso_triggers=miso_triggers)

    # 6. SELL/TRIM from weekly-rec
    print("\n[6] SELL/TRIM from weekly-rec...")
    state = run_weekly_sell_trim(state, client, vix, audit, dry_run=dry_run)

    # 7. Save state + NAV + audit
    state.pop("_regime_tier", None)  # transient — don't persist

    nav_after = round(float(client.get_account().portfolio_value), 2)
    audit["nav_after"] = nav_after
    positions_count = len(state.get("positions", {}))

    if dry_run:
        print(f"\n[7] DRY-RUN complete — state not saved, trade log not updated")
        write_daily_audit(audit)
        print(f"\nDRY-RUN summary: NAV=${nav_after:,.2f} | Tier={tier} | Positions={positions_count}/{MAX_POSITIONS}\n")
    else:
        state["nav"]["current"] = nav_after
        state["nav"]["as_of"]   = str(date.today())
        save_state(state)
        append_nav_log(nav_after, f"daily-scan | tier={tier} | VIX={vix} | v3")
        print("\n[7] Writing audit log...")
        write_daily_audit(audit)
        print(f"\nDone. NAV=${nav_after:,.2f} | Tier={tier} | Positions={positions_count}/{MAX_POSITIONS}\n")


def load_env() -> None:
    env_file = REPO / ".secrets" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


if __name__ == "__main__":
    main()
