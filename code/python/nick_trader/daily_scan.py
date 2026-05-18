"""
Nick v2 daily scanner — runs every US trading day at 9:30 AM EDT.

Flow:
  1. Load state + market context (regime)
  2. Fetch news digest per holding (news-snapshot.py --nick-news)
  3. Kill condition check + execute exits (EXIT actions)
  4. Entry check from latest weekly-rec.md ORDERS (guarded against re-execution)
  5. Write daily audit log to vault/20_investment/nick/daily/YYYY-MM-DD.json
  6. Update NAV log + save state

Replaces exit_check.py + execute.py.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO      = Path(__file__).resolve().parents[3]
NICK_DIR  = REPO / "vault/20_investment/nick"
WEEKLY_DIR = NICK_DIR / "weekly"
TRADE_LOG  = NICK_DIR / "trade-log.md"
NAV_LOG    = NICK_DIR / "performance/nav_log.md"
STATE_FILE = NICK_DIR / "nick_state.json"
DAILY_DIR  = NICK_DIR / "daily"

NICK_SIGNALS_PATH = REPO / "vault/Knowledge/nick-signals.md"
NEWS_SCRIPT       = REPO / "scripts/news-snapshot.py"
PYTHON            = Path(sys.executable)

# ---------------------------------------------------------------------------
# Import sibling modules (no package __init__)
# ---------------------------------------------------------------------------
def _import_sibling(name: str):
    path = Path(__file__).parent / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # must register before exec so @dataclass can find module context
    spec.loader.exec_module(mod)
    return mod

kc_mod = _import_sibling("kill_conditions")
el_mod = _import_sibling("entry_logic")

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
# Market context
# ---------------------------------------------------------------------------

def get_regime() -> dict:
    data: dict = {}
    for name, sym in {"VIX": "^VIX", "TNX": "^TNX", "SOXX": "SOXX", "QQQM": "QQQM"}.items():
        try:
            hist  = yf.Ticker(sym).history(period="60d")["Close"]
            price = hist.iloc[-1]
            ma50  = hist.rolling(50).mean().iloc[-1]
            data[name] = {"value": round(float(price), 2), "above_50ma": bool(price > ma50)}
        except Exception:
            data[name] = {"value": None, "above_50ma": None}

    vix = data.get("VIX", {}).get("value") or 25
    data["tier"] = "EARLY" if vix < 20 else ("EXTENDED" if vix < 28 else "DANGER")
    return data


def get_price(ticker: str) -> float | None:
    try:
        return float(yf.Ticker(ticker).fast_info["lastPrice"])
    except Exception:
        return None


# ---------------------------------------------------------------------------
# News digest
# ---------------------------------------------------------------------------

def fetch_news_digest() -> dict:
    try:
        result = subprocess.run(
            [str(PYTHON), str(NEWS_SCRIPT), "--nick-news"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO),
        )
        # stderr has per-ticker warnings — print them
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                print(f"  {line}")
        if result.returncode != 0 or not result.stdout.strip():
            print("  [WARN] news digest fetch failed — proceeding without news gate")
            return {}
        return json.loads(result.stdout)
    except Exception as e:
        print(f"  [WARN] news digest exception: {e} -- proceeding without news gate")
        return {}


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
) -> dict:
    """Evaluate kill conditions; execute EXIT orders; log ALERT flags. Returns updated state."""
    triggered = kc_mod.check_all_kills(state, market_data, news_digest)
    audit["kill_check"] = {}

    for ticker, conditions in triggered.items():
        for cond in conditions:
            action = cond["action"]
            label  = cond["label"]
            pct    = cond.get("price_pct", 0)
            audit["kill_check"].setdefault(ticker, []).append(cond)

            if action == "EXIT":
                pos_state = state["positions"].get(ticker, {})
                partial   = cond.get("partial")

                try:
                    alpaca_positions = {p.symbol: p for p in client.get_all_positions()}
                    pos = alpaca_positions.get(ticker)
                    if not pos:
                        print(f"  [EXIT] {ticker}: no Alpaca position found — skipping order")
                        continue

                    qty    = int(float(pos.qty))
                    price  = float(pos.current_price)
                    sell_q = max(1, int(qty * partial)) if partial else qty

                    # Guard: don't sell if partial already taken for kc2
                    if cond.get("id") == "kc2" and pos_state.get("partial_taken"):
                        print(f"  [SKIP] {ticker} kc2: partial already taken")
                        continue

                    client.submit_order(MarketOrderRequest(
                        symbol=ticker, qty=sell_q, side=OrderSide.SELL, time_in_force=TimeInForce.DAY
                    ))
                    print(f"  [EXIT ORDER] {ticker}: {sell_q} shares @ ${price:.2f} -- {label} ({pct:+.1%})")

                    append_trade_log(dict(
                        date=date.today(), ticker=ticker,
                        action="EXIT" if not partial else "PARTIAL-EXIT",
                        shares=sell_q, price=price, conviction="kill",
                        vix=vix, reason=label,
                    ))

                    if partial and cond.get("id") == "kc2":
                        state["positions"].setdefault(ticker, {})["partial_taken"] = True
                    elif not partial:
                        state["positions"].pop(ticker, None)

                except Exception as e:
                    print(f"  [ERROR] {ticker} exit failed: {e}")

            else:  # ALERT
                print(f"  [ALERT] {ticker}: {label} ({pct:+.1%}) -- flag for /nick-weekly review")

    if not triggered:
        print("  Kill check: all clear")

    return state


# ---------------------------------------------------------------------------
# Entry check (from latest weekly-rec.md ORDERS)
# ---------------------------------------------------------------------------

def get_latest_weekly_orders() -> tuple[str | None, list[dict]]:
    files = sorted(WEEKLY_DIR.glob("*_weekly-rec.md"), reverse=True)
    if not files:
        return None, []
    rec = files[0]
    m   = re.search(r"## ORDERS.*?```json\s*\n(\[.*?\])\s*\n```", rec.read_text(encoding="utf-8"), re.DOTALL)
    if not m:
        return rec.name, []
    return rec.name, json.loads(m.group(1))


def run_entry_check(
    state: dict,
    client: TradingClient,
    regime: dict,
    news_digest: dict,
    nav: float,
    cash: float,
    audit: dict,
) -> dict:
    """Try to execute BUY orders from latest weekly rec if not already done."""
    rec_name, orders = get_latest_weekly_orders()
    audit["entry_check"] = {"rec": rec_name, "orders_tried": [], "orders_executed": []}

    if not rec_name:
        print("  No weekly rec found — skipping entry check")
        return state

    if state.get("last_executed_rec") == rec_name:
        print(f"  Entry: {rec_name} already executed -- skipping")
        return state

    tier = regime.get("tier", "EARLY")
    vix  = regime.get("VIX", {}).get("value", "?")

    nick_signals  = el_mod.parse_nick_signals()
    alpaca_positions = {p.symbol: p for p in client.get_all_positions()}
    pending_orders   = {
        o.symbol for o in client.get_orders(
            filter=GetOrdersRequest(status=QueryOrderStatus.OPEN)
        )
    }

    buy_executed = False

    for order in orders:
        action     = order.get("action", "").upper()
        ticker     = order.get("ticker", "").upper()
        conviction = order.get("conviction", "med").lower()
        reason     = order.get("reason", "")

        if action != "BUY":
            continue

        audit["entry_check"]["orders_tried"].append(ticker)
        price = get_price(ticker)
        if not price:
            print(f"  SKIP {ticker}: cannot get price")
            continue

        result = el_mod.evaluate_entry(
            ticker=ticker,
            conviction=conviction,
            nav=nav,
            cash=cash,
            price=price,
            regime=regime,
            news_digest=news_digest,
            nick_signals=nick_signals,
            existing_positions=set(alpaca_positions.keys()),
            pending_orders=pending_orders,
        )

        if not result.should_buy:
            print(f"  SKIP {ticker}: {result.skip_reason}")
            continue

        try:
            client.submit_order(MarketOrderRequest(
                symbol=ticker, qty=result.shares, side=OrderSide.BUY, time_in_force=TimeInForce.DAY
            ))
            print(f"  [BUY ORDER] {ticker}: {result.shares} shares @ ~${price:.2f} ({result.size_pct*100:.0f}% NAV)")
            append_trade_log(dict(
                date=date.today(), ticker=ticker, action="BUY",
                shares=result.shares, price=price, conviction=conviction,
                vix=vix, reason=reason,
            ))
            state["positions"][ticker] = {
                "partial_taken": False,
                "entry_date": str(date.today()),
                "entry_price": round(price, 2),
                "shares": result.shares,
                "weight": result.size_pct,
            }
            audit["entry_check"]["orders_executed"].append(ticker)
            cash -= result.shares * price
            buy_executed = True

        except Exception as e:
            print(f"  [ERROR] {ticker} buy failed: {e}")

    if buy_executed:
        state["last_executed_rec"] = rec_name

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
    load_env()
    state = load_state()

    audit: dict = {
        "date": str(date.today()),
        "version": "nick-v2",
    }

    print(f"\n=== Nick Daily Scan {date.today()} ===")

    # 1. Market context
    print("\n[1] Market context...")
    regime = get_regime()
    tier   = regime.get("tier")
    vix    = regime.get("VIX", {}).get("value", "?")
    tnx    = regime.get("TNX", {}).get("value", "?")
    print(f"  Tier={tier} | VIX={vix} | 10Y={tnx}")
    audit["regime"] = regime

    # 2. News digest
    print("\n[2] Fetching news digest...")
    news_digest = fetch_news_digest()
    audit["news_tickers_clean"] = {t: d.get("clean") for t, d in news_digest.items()}

    # 3. Build market_data from Alpaca positions
    print("\n[3] Kill condition check...")
    client = TradingClient(os.environ["ALPACA_API_KEY"], os.environ["ALPACA_SECRET_KEY"], paper=True)
    account = client.get_account()
    nav     = round(float(account.portfolio_value), 2)
    cash    = float(account.cash)

    alpaca_positions = {p.symbol: p for p in client.get_all_positions()}
    market_data: dict[str, dict] = {}
    for ticker in state.get("positions", {}):
        pos = alpaca_positions.get(ticker)
        if pos:
            market_data[ticker] = {"current_price": float(pos.current_price)}
        else:
            price = get_price(ticker)
            if price:
                market_data[ticker] = {"current_price": price}

    state = run_kill_exits(state, client, market_data, news_digest, vix, audit)

    # 4. Entry check
    print("\n[4] Entry check (latest weekly rec)...")
    state = run_entry_check(state, client, regime, news_digest, nav, cash, audit)

    # 5. Save state + NAV log
    save_state(state)
    nav_after = round(float(client.get_account().portfolio_value), 2)
    append_nav_log(nav_after, f"daily-scan | tier={tier} | VIX={vix}")
    audit["nav_after"] = nav_after

    # 6. Write audit log
    print("\n[5] Writing audit log...")
    write_daily_audit(audit)

    print(f"\nDone. NAV=${nav_after:,.2f} | Tier={tier}\n")


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
