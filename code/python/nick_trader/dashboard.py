"""
Nick Portfolio Dashboard — Streamlit
Deploy: Streamlit Community Cloud (free) → connect sodruksa-max/ltd-os
Main file: code/python/nick_trader/dashboard.py
"""

import os
import re
from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from alpaca.trading.client import TradingClient

# ── Config ───────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Nick Dashboard",
    page_icon="📈",
    layout="wide",
)

REPO = Path(__file__).resolve().parents[3]
NICK_DIR = REPO / "vault/20_investment/nick"
KB_DIR = REPO / "vault/Knowledge"


# ── Secrets ───────────────────────────────────────────────────────────────────

def get_secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key, "")


# ── Data loaders ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def load_alpaca():
    client = TradingClient(get_secret("ALPACA_API_KEY"), get_secret("ALPACA_SECRET_KEY"), paper=True)
    account = client.get_account()
    positions = client.get_all_positions()
    nav = float(account.portfolio_value)
    cash = float(account.cash)

    rows = []
    for p in positions:
        ticker = p.symbol
        qty = float(p.qty)
        avg = float(p.avg_entry_price)
        price = float(p.current_price)
        pnl_pct = (price - avg) / avg * 100
        mkt_val = qty * price
        rows.append({
            "Ticker": ticker,
            "Shares": int(qty),
            "Avg Cost": avg,
            "Price": price,
            "P&L %": round(pnl_pct, 2),
            "Value": round(mkt_val, 2),
            "Weight %": round(mkt_val / nav * 100, 1),
        })

    return pd.DataFrame(rows), nav, cash


@st.cache_data(ttl=300)
def load_benchmark():
    result = {}
    for sym in ["QQQM", "SOXX", "SPY"]:
        try:
            hist = yf.Ticker(sym).history(period="5d")["Close"]
            result[sym] = round((hist.iloc[-1] - hist.iloc[0]) / hist.iloc[0] * 100, 2)
        except Exception:
            result[sym] = 0.0
    blended = round((result["QQQM"] + result["SOXX"]) / 2, 2)
    result["Blended"] = blended
    return result


@st.cache_data(ttl=60)
def load_nav_history():
    nav_log = NICK_DIR / "performance/nav_log.md"
    if not nav_log.exists():
        return pd.DataFrame()
    rows = []
    for line in nav_log.read_text(encoding="utf-8").splitlines():
        if "|" in line and "$" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                try:
                    d = parts[0]
                    nav = float(parts[1].replace("$", "").replace(",", ""))
                    rows.append({"Date": d, "NAV": nav})
                except Exception:
                    pass
    return pd.DataFrame(rows)


@st.cache_data(ttl=60)
def load_trade_log():
    log = NICK_DIR / "trade-log.md"
    if not log.exists():
        return pd.DataFrame()
    rows = []
    for line in log.read_text(encoding="utf-8").splitlines():
        if "|" in line and line.count("|") >= 10:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 10 and parts[0] not in ("Date", "---", ""):
                try:
                    rows.append({
                        "Date": parts[0], "Ticker": parts[1], "Action": parts[2],
                        "Shares": parts[3], "Price": parts[4], "NAV%": parts[5],
                        "Conviction": parts[6], "VIX": parts[7], "10Y": parts[8],
                        "SOXX": parts[9], "Reason": parts[10] if len(parts) > 10 else "",
                    })
                except Exception:
                    pass
    return pd.DataFrame(rows)


@st.cache_data(ttl=60)
def load_thesis_tracker():
    path = KB_DIR / "THESIS_TRACKER.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


@st.cache_data(ttl=60)
def load_latest_weekly():
    weekly_dir = NICK_DIR / "weekly"
    files = sorted(weekly_dir.glob("*_weekly-rec.md"), reverse=True)
    if not files:
        return ""
    return files[0].read_text(encoding="utf-8")


@st.cache_data(ttl=60)
def load_latest_ipo():
    inbox = REPO / "vault/00_inbox"
    files = sorted(inbox.glob("ipo-radar-*.md"), reverse=True)
    if not files:
        return ""
    return files[0].read_text(encoding="utf-8")


@st.cache_data(ttl=60)
def parse_holdings_review(weekly_text: str) -> dict:
    """Extract per-ticker thesis/kill/status/rec/reason from Holdings Review section."""
    result = {}
    section = re.search(r"## Holdings Review(.*?)(?=\n## |\Z)", weekly_text, re.DOTALL)
    if not section:
        return result
    blocks = re.split(r"\n### ", section.group(1))
    for block in blocks:
        if not block.strip():
            continue
        header = block.splitlines()[0]
        ticker_match = re.match(r"([A-Z]+)\s*[—–-]\s*(.*)", header)
        if not ticker_match:
            continue
        ticker = ticker_match.group(1)
        verdict = ticker_match.group(2).strip()
        fields = {}
        for line in block.splitlines()[1:]:
            for key in ("Thesis", "Kill condition", "Status this week", "Rec", "Reason"):
                if f"**{key}:**" in line:
                    fields[key] = re.sub(r"\*\*.*?\*\*:\s*", "", line).strip("- ").strip()
        result[ticker] = {"verdict": verdict, **fields}
    return result


@st.cache_data(ttl=60)
def get_entry_reasons(trade_log_df: pd.DataFrame) -> dict:
    """First BUY reason per ticker from trade log."""
    if trade_log_df.empty:
        return {}
    buys = trade_log_df[trade_log_df["Action"] == "BUY"]
    return {
        row["Ticker"]: f"{row['Reason']}  (entry {row['Date']} @ {row['Price']})"
        for _, row in buys.drop_duplicates("Ticker", keep="first").iterrows()
    }


# ── Status helpers ────────────────────────────────────────────────────────────

def status_badge(pnl):
    if pnl >= 50:
        return "🎯 Target zone"
    elif pnl <= -20:
        return "⚠️ Near stop"
    elif pnl < 0:
        return "🔴 Loss"
    else:
        return "✅ Intact"


# ── Main ─────────────────────────────────────────────────────────────────────

st.title("📈 Nick Portfolio Dashboard")
st.caption(f"Paper trading · Blinded thesis portfolio · Updated {date.today()}")

# Load data
try:
    df_holdings, nav, cash = load_alpaca()
    alpaca_ok = True
except Exception as e:
    st.error(f"Alpaca connection error: {e}")
    alpaca_ok = False
    df_holdings = pd.DataFrame()
    nav, cash = 10000.0, 1000.0

benchmark = load_benchmark()

# ── Row 1: Metrics ────────────────────────────────────────────────────────────

col1, col2, col3, col4, col5 = st.columns(5)

inception_nav = 10000.0
total_pnl = round((nav - inception_nav) / inception_nav * 100, 2)
blended_week = benchmark["Blended"]

# Week P&L: weight-averaged 5-day price change across holdings (not avg-cost-based P&L)
if not df_holdings.empty:
    weekly_changes = []
    for _, row in df_holdings.iterrows():
        try:
            hist = yf.Ticker(row["Ticker"]).history(period="5d")["Close"]
            chg = (hist.iloc[-1] - hist.iloc[0]) / hist.iloc[0] * 100
            weekly_changes.append(chg * (row["Weight %"] / 100))
        except Exception:
            pass
    week_pnl = round(sum(weekly_changes), 2) if weekly_changes else 0.0
else:
    week_pnl = 0.0
alpha = round(week_pnl - blended_week, 2)
cash_pct = round(cash / nav * 100, 1)

col1.metric("NAV", f"${nav:,.0f}", f"{total_pnl:+.2f}% since inception")
col2.metric("This week", f"{week_pnl:+.2f}%", f"alpha {alpha:+.2f}%")
col3.metric("Blended benchmark", f"{blended_week:+.2f}%", "50% QQQM + 50% SOXX")
col4.metric("Cash", f"${cash:,.0f}", f"{cash_pct}% NAV")
col5.metric("Positions", len(df_holdings))

st.divider()

# ── Row 2: Holdings + Chart ───────────────────────────────────────────────────

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Holdings")
    if not df_holdings.empty:
        df_display = df_holdings.copy()
        df_display["Status"] = df_display["P&L %"].apply(status_badge)
        df_display["P&L %"] = df_display["P&L %"].apply(lambda x: f"{x:+.2f}%")
        df_display["Price"] = df_display["Price"].apply(lambda x: f"${x:.2f}")
        df_display["Avg Cost"] = df_display["Avg Cost"].apply(lambda x: f"${x:.2f}")
        df_display["Value"] = df_display["Value"].apply(lambda x: f"${x:,.0f}")
        df_display["Weight %"] = df_display["Weight %"].apply(lambda x: f"{x}%")
        st.dataframe(
            df_display[["Ticker", "Shares", "Avg Cost", "Price", "P&L %", "Value", "Weight %", "Status"]],
            use_container_width=True, hide_index=True
        )
    else:
        st.info("No open positions")

with col_right:
    st.subheader("Allocation")
    if not df_holdings.empty:
        cash_row = pd.DataFrame([{"Ticker": "CASH", "Value": cash}])
        pie_data = pd.concat([df_holdings[["Ticker", "Value"]], cash_row], ignore_index=True)
        fig = px.pie(
            pie_data, names="Ticker", values="Value",
            color_discrete_sequence=px.colors.sequential.Teal,
            hole=0.4,
        )
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# ── Why Nick holds these ──────────────────────────────────────────────────────

if not df_holdings.empty:
    st.subheader("Why Nick holds these")
    weekly_text = load_latest_weekly()
    holdings_review = parse_holdings_review(weekly_text)
    trade_log_df = load_trade_log()
    entry_reasons = get_entry_reasons(trade_log_df)

    cols = st.columns(2)
    for i, ticker in enumerate(df_holdings["Ticker"].tolist()):
        review = holdings_review.get(ticker, {})
        entry = entry_reasons.get(ticker, "")
        verdict = review.get("verdict", "—")
        verdict_color = (
            "🟢" if "Intact" in verdict else
            "🟡" if "Evolving" in verdict else
            "🔴" if "Invalidated" in verdict else "⚪"
        )
        with cols[i % 2]:
            with st.expander(f"{verdict_color} **{ticker}** — {verdict}", expanded=False):
                if review.get("Thesis"):
                    st.markdown(f"**Thesis:** {review['Thesis']}")
                if review.get("Kill condition"):
                    st.markdown(f"**Kill condition:** {review['Kill condition']}")
                if review.get("Status this week"):
                    st.markdown(f"**Status:** {review['Status this week']}")
                if review.get("Rec"):
                    st.markdown(f"**Nick's rec:** {review['Rec']}")
                if review.get("Reason"):
                    st.markdown(f"**Reason:** {review['Reason']}")
                if entry:
                    st.caption(f"Entry: {entry}")
                if not review and not entry:
                    st.info("No review data yet — runs every Friday")

    st.divider()

# ── Row 3: NAV History ────────────────────────────────────────────────────────

nav_hist = load_nav_history()
if not nav_hist.empty:
    st.subheader("NAV History")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=nav_hist["Date"], y=nav_hist["NAV"],
        mode="lines+markers", name="Nick NAV",
        line=dict(color="#00d4aa", width=2),
    ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#2a2d3a"), xaxis=dict(gridcolor="#2a2d3a"),
        margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Row 4: Tabs ───────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs(["📋 Recent Trades", "🎯 Kill Conditions", "🔍 KB Gaps", "🚀 IPO Radar"])

with tab1:
    trade_log = load_trade_log()
    if not trade_log.empty:
        st.dataframe(trade_log.tail(20).iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("No trades yet — execute.py will log here after first order")

with tab2:
    thesis = load_thesis_tracker()
    if thesis:
        st.markdown(thesis)
    else:
        st.info("vault/Knowledge/THESIS_TRACKER.md not found")

with tab3:
    weekly = load_latest_weekly()
    if weekly:
        # Extract KB Gaps section
        m = re.search(r"## KB Gaps.*?(?=##|$)", weekly, re.DOTALL)
        if m:
            st.markdown(m.group(0))
        else:
            st.info("No KB Gaps section in latest weekly rec")
    else:
        st.info("No weekly rec yet — runs automatically every Friday")

with tab4:
    ipo = load_latest_ipo()
    if ipo:
        st.markdown(ipo)
    else:
        st.info("No IPO radar yet — runs automatically every Monday")
