"""
dashboard: Streamlit trading bot UI - Screener, Bot, and Positions tabs.

Usage: streamlit run scripts/dashboard.py --server.headless true
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import streamlit as st

# -- Paths -------------------------------------------------------------------
ROOT = Path(__file__).parent.parent
PYTHON = str(ROOT / "code" / "python" / ".venv" / "Scripts" / "python")
SCREENER = str(ROOT / "scripts" / "screener.py")
AUTOBUY = str(ROOT / "scripts" / "auto-buy.py")


# -- Env loader --------------------------------------------------------------
def load_env():
    """Read .secrets/.env and push keys into os.environ (same pattern as screener.py)."""
    env_file = ROOT / ".secrets" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


load_env()

# -- Page config -------------------------------------------------------------
st.set_page_config(page_title="LTD Trading Bot", layout="wide")
st.title("LTD Trading Bot")

# -- Session state defaults --------------------------------------------------
if "previewed" not in st.session_state:
    st.session_state["previewed"] = False
if "preview_cmd" not in st.session_state:
    st.session_state["preview_cmd"] = []


# -- Helpers -----------------------------------------------------------------
def run_subprocess(cmd, timeout=120):
    """Run a command, return (stdout, stderr, returncode). Captures output safely."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(ROOT),
            timeout=timeout,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "ERROR: command timed out after 120s", 1
    except Exception as e:
        return "", f"ERROR: {e}", 1


def render_colored_table(rows, columns, junk_key="junk_level"):
    """Render rows as an HTML table with green/yellow/red row backgrounds."""
    bg_map = {
        "PASS": "#1b3b1b",
        "WARN": "#3b3b00",
        "FAIL": "#3b0000",
    }
    text_color = "#e8e8e8"

    header_html = "".join(
        "<th style='padding:6px 12px;border-bottom:1px solid #444'>"
        + c + "</th>"
        for c in columns
    )
    rows_html = ""
    for row in rows:
        junk = row.get(junk_key, "PASS")
        bg = bg_map.get(junk, "#1b1b1b")
        cells = "".join(
            "<td style='padding:5px 12px'>" + str(row.get(c, "")) + "</td>"
            for c in columns
        )
        rows_html += (
            "<tr style='background-color:" + bg + ";color:" + text_color + "'>"
            + cells + "</tr>"
        )

    html = (
        "<table style='border-collapse:collapse;width:100%;font-size:14px'>"
        "<thead><tr style='background-color:#222;color:#ccc'>" + header_html + "</tr></thead>"
        "<tbody>" + rows_html + "</tbody>"
        "</table>"
    )
    st.markdown(html, unsafe_allow_html=True)


# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs(["Screener", "Bot", "Positions"])


# ---------------------------------------------------------------------------
# TAB 1 - Screener
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Momentum / Reversal Screener")

    col_left, col_right = st.columns([1, 2])
    with col_left:
        screen_mode = st.radio("Mode", ["Momentum", "Reversal"], horizontal=True)
        top_n = st.slider("Top N", min_value=5, max_value=25, value=10, step=1)
        run_btn = st.button("Run Screen", type="primary")

    if run_btn:
        cmd = [PYTHON, SCREENER, "--json", "--top", str(top_n)]
        if screen_mode == "Reversal":
            cmd.append("--reversal")

        with st.spinner("Running screener... (may take 15-30s)"):
            stdout, stderr, rc = run_subprocess(cmd, timeout=120)

        if rc != 0:
            st.error("Screener failed (exit " + str(rc) + ")")
            if stderr:
                st.code(stderr, language="text")
        else:
            try:
                results = json.loads(stdout)
            except Exception as e:
                st.error("Could not parse screener output: " + str(e))
                st.code(stdout[:500], language="text")
                results = []

            if not results:
                st.warning("Screener returned no results.")
            else:
                st.success("Found " + str(len(results)) + " stocks in " + screen_mode + " mode")

                if screen_mode == "Momentum":
                    display_rows = []
                    for r in results:
                        ma50_flag = "Y" if r.get("above_ma50") else "n"
                        junk = r.get("junk_level", "PASS")
                        summary = r.get("junk_summary", "OK")
                        filter_str = "[" + junk + "] " + summary if junk != "PASS" else "[OK]"
                        ret20 = r["return_20d_pct"]
                        rs = r["rs_vs_spy_pct"]
                        display_rows.append({
                            "Ticker":   r["ticker"],
                            "Price":    "$" + format(r["price"], ",.2f"),
                            "20d Ret%": ("+" if ret20 >= 0 else "") + str(round(ret20, 1)) + "%",
                            "RS/SPY%":  ("+" if rs >= 0 else "") + str(round(rs, 1)) + "%",
                            "VolRatio": str(round(r["vol_ratio"], 2)) + "x",
                            "MA50":     ma50_flag,
                            "Score":    str(round(r["score"], 4)),
                            "Filter":   filter_str,
                            "junk_level": junk,
                        })
                    render_colored_table(
                        display_rows,
                        ["Ticker", "Price", "20d Ret%", "RS/SPY%", "VolRatio", "MA50", "Score", "Filter"],
                    )
                else:
                    display_rows = []
                    for r in results:
                        cross = "X" if r.get("crossed_ma50") else "-"
                        junk = r.get("junk_level", "PASS")
                        summary = r.get("junk_summary", "OK")
                        filter_str = "[" + junk + "] " + summary if junk != "PASS" else "[OK]"
                        over = " OVER" if r.get("overextended") else ""
                        ret5 = r["return_5d_pct"]
                        ret20 = r["return_20d_pct"]
                        display_rows.append({
                            "Ticker":   r["ticker"],
                            "Price":    "$" + format(r["price"], ",.2f"),
                            "5d Ret%":  ("+" if ret5 >= 0 else "") + str(round(ret5, 1)) + "%",
                            "20d Ret%": ("+" if ret20 >= 0 else "") + str(round(ret20, 1)) + "%",
                            "MA50X":    cross,
                            "VolRatio": str(round(r["vol_ratio"], 2)) + "x",
                            "R-Score":  str(round(r["reversal_score"], 4)),
                            "Filter":   filter_str + over,
                            "junk_level": junk,
                        })
                    render_colored_table(
                        display_rows,
                        ["Ticker", "Price", "5d Ret%", "20d Ret%", "MA50X", "VolRatio", "R-Score", "Filter"],
                    )

                st.caption(
                    "Green row = PASS  |  Yellow = WARN  |  Red = FAIL  "
                    "|  Score = RS_vs_SPY * clamp(VolRatio, 0.5, 3.0)"
                )

        if stderr:
            with st.expander("Screener log (stderr)"):
                st.code(stderr, language="text")


# ---------------------------------------------------------------------------
# TAB 2 - Bot
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Auto-Buy Bot")

    budget = st.radio(
        "Budget",
        ["Paper ($100k)", "Real (~$1,400 / 50k THB)"],
        horizontal=True,
    )
    if budget == "Paper ($100k)":
        size_pct = 0.05
        max_top = 4
    else:
        size_pct = 0.0035
        max_top = 2

    strategy = st.radio("Strategy", ["Momentum", "Reversal"], horizontal=True)
    order_type = st.radio(
        "Orders",
        ["Market", "Bracket (stop -15% / target +30%)"],
        horizontal=True,
    )
    top_picks = st.slider("Top N picks", min_value=1, max_value=max_top, value=min(2, max_top))

    st.markdown(
        "Position size: **" + str(round(size_pct * 100, 2)) + "%** of portfolio"
        " | Max picks: **" + str(max_top) + "**"
        " | Selected: **" + str(top_picks) + "**"
    )

    if budget == "Real (~$1,400 / 50k THB)":
        st.warning(
            "REAL budget mode: size=0.35% maps ~$350/position onto $100k paper account. "
            "Still uses paper=True (no real money)."
        )

    def build_autobuy_cmd(dry_run=True):
        """Build the auto-buy.py command list with the current UI settings."""
        cmd = [
            PYTHON, AUTOBUY,
            "--top", str(top_picks),
            "--size", str(size_pct),
        ]
        if strategy == "Reversal":
            cmd.append("--reversal")
        if "Bracket" in order_type:
            cmd.append("--bracket")
        if dry_run:
            cmd.append("--dry-run")
        return cmd

    col_preview, col_confirm = st.columns([1, 1])

    with col_preview:
        if st.button("Preview (Dry Run)", type="primary"):
            st.session_state["previewed"] = False
            cmd = build_autobuy_cmd(dry_run=True)
            st.session_state["preview_cmd"] = cmd

            with st.spinner("Running dry-run... (may take 30s)"):
                stdout, stderr, rc = run_subprocess(cmd, timeout=120)

            st.session_state["previewed"] = True
            st.session_state["preview_stdout"] = stdout
            st.session_state["preview_stderr"] = stderr
            st.session_state["preview_rc"] = rc

    if st.session_state.get("previewed"):
        rc = st.session_state.get("preview_rc", 1)
        stdout = st.session_state.get("preview_stdout", "")
        stderr = st.session_state.get("preview_stderr", "")

        if rc != 0:
            st.error("Dry-run failed (exit " + str(rc) + ")")
            if stderr:
                st.code(stderr, language="text")
        else:
            st.code(stdout, language="text")
            if stderr:
                with st.expander("Log"):
                    st.code(stderr, language="text")

        with col_confirm:
            st.markdown("###")
            if rc == 0:
                st.warning("Review the preview above before confirming.")
                if st.button("CONFIRM BUY", type="primary"):
                    cmd_live = build_autobuy_cmd(dry_run=False)
                    with st.spinner("Placing orders..."):
                        out2, err2, rc2 = run_subprocess(cmd_live, timeout=120)
                    if rc2 != 0:
                        st.error("Live run failed (exit " + str(rc2) + ")")
                        if err2:
                            st.code(err2, language="text")
                    else:
                        st.success("Orders submitted.")
                        st.code(out2, language="text")
                    st.session_state["previewed"] = False


# ---------------------------------------------------------------------------
# TAB 3 - Positions
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Live Positions (Paper Account)")

    if st.button("Refresh", type="primary"):
        try:
            from alpaca.trading.client import TradingClient

            api_key = os.environ.get("ALPACA_API_KEY")
            secret_key = os.environ.get("ALPACA_SECRET_KEY")

            if not api_key or not secret_key:
                st.error("ALPACA keys not found in .secrets/.env")
            else:
                client = TradingClient(api_key, secret_key, paper=True)

                acct = client.get_account()
                portfolio_value = float(acct.portfolio_value or 0)
                buying_power = float(acct.buying_power or 0)

                positions = client.get_all_positions()
                n_pos = len(positions)

                m1, m2, m3 = st.columns(3)
                m1.metric("Portfolio Value", "$" + format(portfolio_value, ",.2f"))
                m2.metric("Buying Power", "$" + format(buying_power, ",.2f"))
                m3.metric("Open Positions", str(n_pos))

                if n_pos == 0:
                    st.info("No open positions.")
                else:
                    rows = []
                    for p in positions:
                        unreal = float(p.unrealized_pl or 0)
                        unreal_pct = float(p.unrealized_plpc or 0) * 100
                        pl_sign = "+" if unreal >= 0 else ""
                        pct_sign = "+" if unreal_pct >= 0 else ""
                        rows.append({
                            "Ticker":    p.symbol,
                            "Qty":       str(int(float(p.qty))),
                            "Avg Entry": "$" + format(float(p.avg_entry_price), ",.2f"),
                            "Current":   "$" + format(float(p.current_price), ",.2f"),
                            "P&L $":     pl_sign + "$" + format(unreal, ",.2f"),
                            "P&L %":     pct_sign + str(round(unreal_pct, 1)) + "%",
                            "junk_level": "PASS" if unreal >= 0 else "FAIL",
                        })
                    render_colored_table(
                        rows,
                        ["Ticker", "Qty", "Avg Entry", "Current", "P&L $", "P&L %"],
                    )
                    st.caption("Green = profit  |  Red = loss")

        except Exception as e:
            st.error("Alpaca connection error: " + str(e))
