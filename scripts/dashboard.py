"""
dashboard: Streamlit trading bot UI - Screener, Bot, and Positions tabs.

Usage: streamlit run scripts/dashboard.py --server.headless true
"""

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import streamlit as st

# -- Paths -------------------------------------------------------------------
ROOT = Path(__file__).parent.parent
PYTHON = str(ROOT / "code" / "python" / ".venv" / "Scripts" / "python")
SCREENER = str(ROOT / "scripts" / "screener.py")
AUTOBUY  = str(ROOT / "scripts" / "auto-buy.py")
EOD      = str(ROOT / "scripts" / "eod-report.py")


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


# -- Vault helpers -----------------------------------------------------------
def _daily_note_path():
    return ROOT / "vault" / "daily" / f"{date.today()}.md"


def _append_to_daily_note(content: str):
    path = _daily_note_path()
    if not path.exists():
        path.write_text(f"# {date.today()}\n\n", encoding="utf-8")
    existing = path.read_text(encoding="utf-8")
    path.write_text(existing.rstrip() + "\n\n" + content + "\n", encoding="utf-8")


def vault_save_screener(results: list, mode: str):
    """Append screener table to today's daily note."""
    now = datetime.now().strftime("%H:%M")
    is_rev = "Reversal" in mode
    lines = [f"## Screener — {now} ({mode})\n"]
    if is_rev:
        lines.append("| # | Ticker | Price | 5d% | 20d% | MA50X | VolRatio | R-Score | Filter |")
        lines.append("|---|--------|-------|-----|------|-------|----------|---------|--------|")
        for i, r in enumerate(results, 1):
            cross = "X" if r.get("crossed_ma50") else "-"
            lines.append(
                f"| {i} | {r['ticker']} | ${r['price']:,.2f}"
                f" | {r['return_5d_pct']:+.1f}% | {r['return_20d_pct']:+.1f}%"
                f" | {cross} | {r['vol_ratio']:.2f}x | {r.get('reversal_score', 0):.4f}"
                f" | {r.get('junk_level', '?')} |"
            )
    else:
        lines.append("| # | Ticker | Price | 20d% | RS/SPY% | VolRatio | MA50 | Score | Filter |")
        lines.append("|---|--------|-------|------|---------|----------|------|-------|--------|")
        for i, r in enumerate(results, 1):
            ma = "Y" if r.get("above_ma50") else "n"
            lines.append(
                f"| {i} | {r['ticker']} | ${r['price']:,.2f}"
                f" | {r['return_20d_pct']:+.1f}% | {r['rs_vs_spy_pct']:+.1f}%"
                f" | {r['vol_ratio']:.2f}x | {ma} | {r['score']:.4f}"
                f" | {r.get('junk_level', '?')} |"
            )
    _append_to_daily_note("\n".join(lines))


def vault_save_trade(ticker: str, shares: int, price: float,
                     stop: float | None, target: float | None, strategy: str):
    """Create a paper trade file in real-trades/."""
    today = date.today().strftime("%Y-%m-%d")
    order_type = "bracket" if stop else "market"
    fname = f"{today}-{ticker}-paper.md"
    path = ROOT / "vault" / "20_investment" / "_journal" / "real-trades" / fname
    cost = shares * price
    stop_str = f"${stop:,.2f}" if stop else "~"
    target_str = f"${target:,.2f}" if target else "~"
    content = f"""---
ticker: {ticker}
direction: long
status: open
type: paper
date_open: {today}
date_close: ~
entry_usd: {price}
shares: {shares}
fees_usd: 0
stop_usd: {stop if stop else "~"}
target_usd: {target if target else "~"}
exit_usd: ~
exit_fees_usd: ~
result: ~
setup_source: "bot-screener {strategy}"
---

# Paper Trade — {ticker} (LONG) — {today}
*Paper account — Alpaca | strategy: {strategy} | order: {order_type}*

## ราคา

| | ราคา USD | หมายเหตุ |
|---|---|---|
| **Entry** | ${price:,.2f} | bot ซื้ออัตโนมัติ |
| **Stop loss** | {stop_str} | -15% |
| **Target** | {target_str} | +30% |
| **Exit** | — | *กรอกตอนปิด* |

## Position

| | Value |
|---|---|
| **Shares** | {shares} หุ้น |
| **Cost basis** | ${cost:,.2f} |

## Notes

### เหตุผลที่เข้า
Bot คัดโดย {strategy} screener — คะแนนสูงสุดใน watchlist วันที่ {today}

### เหตุผลที่ออก
[hit target / stop hit / manual exit]

### Lesson (1 ประโยค)
[กรอกหลังปิด trade]
"""
    path.write_text(content, encoding="utf-8")
    return fname


def vault_save_positions(positions, portfolio_value: float, buying_power: float):
    """Append portfolio snapshot to today's daily note."""
    now = datetime.now().strftime("%H:%M")
    lines = [
        f"## Portfolio Snapshot — {now}\n",
        f"Portfolio: ${portfolio_value:,.2f} | Buying Power: ${buying_power:,.2f}\n",
    ]
    if positions:
        lines.append("| Ticker | Qty | Entry | Current | P&L $ | P&L % |")
        lines.append("|--------|-----|-------|---------|-------|-------|")
        for p in positions:
            unreal = float(p.unrealized_pl or 0)
            unreal_pct = float(p.unrealized_plpc or 0) * 100
            lines.append(
                f"| {p.symbol} | {int(float(p.qty))}"
                f" | ${float(p.avg_entry_price):,.2f}"
                f" | ${float(p.current_price):,.2f}"
                f" | {unreal:+,.2f}"
                f" | {unreal_pct:+.1f}% |"
            )
    else:
        lines.append("ไม่มี position เปิดอยู่")
    _append_to_daily_note("\n".join(lines))


# Regex to parse BUY lines from auto-buy.py output
_BUY_RE = re.compile(
    r"BUY\s+(\w+)\s+--\s+(\d+)\s+sh\s+@\s+~\$([0-9,.]+)"
    r"(?:.*?stop=\$([0-9.]+)\s*/\s*target=\$([0-9.]+))?"
)


def parse_buys(output: str):
    """Return list of (ticker, shares, price, stop, target) from auto-buy output."""
    trades = []
    for m in _BUY_RE.finditer(output):
        ticker = m.group(1)
        shares = int(m.group(2))
        price  = float(m.group(3).replace(",", ""))
        stop   = float(m.group(4)) if m.group(4) else None
        target = float(m.group(5)) if m.group(5) else None
        trades.append((ticker, shares, price, stop, target))
    return trades


# -- Page config -------------------------------------------------------------
st.set_page_config(page_title="LTD Trading Bot", layout="wide")
st.title("LTD Trading Bot 📈")
st.caption("ระบบคัดหุ้นและซื้อหุ้นอัตโนมัติ (Alpaca Paper Account)")

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
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Screener (คัดหุ้น)", "🤖 Bot (ซื้อหุ้น)", "📊 Positions (พอร์ต)", "📋 EOD Report"])


# ---------------------------------------------------------------------------
# TAB 1 - Screener
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("คัดหุ้น (Stock Screener)")
    st.caption("ดึงข้อมูลจาก Alpaca แล้วจัดอันดับหุ้นใน watchlist ตามคะแนน")

    col_left, col_right = st.columns([1, 2])
    with col_left:
        screen_mode = st.radio(
            "โหมด (Mode)",
            ["Momentum (แรงส่ง)", "Reversal (ต้นรอบ)"],
            horizontal=True,
        )
        top_n = st.slider("แสดงกี่ตัว (Top N)", min_value=5, max_value=25, value=10, step=1)
        run_btn = st.button("🔍 คัดหุ้น (Run Screen)", type="primary")

    if run_btn:
        is_reversal = screen_mode.startswith("Reversal")
        cmd = [PYTHON, SCREENER, "--json", "--top", str(top_n)]
        if is_reversal:
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
                st.warning("ไม่พบหุ้นที่ผ่านเกณฑ์")
            else:
                st.success("พบ " + str(len(results)) + " ตัว | โหมด: " + screen_mode)

                if not is_reversal:
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
                    "🟢 เขียว = ผ่านกรอง  |  🟡 เหลือง = ระวัง (WARN)  |  🔴 แดง = ห้ามซื้อ (FAIL)  "
                    "|  Score = RS_vs_SPY × clamp(VolRatio, 0.5, 3.0)"
                )

                # --- Save to vault ---
                try:
                    vault_save_screener(results, screen_mode)
                    st.success("บันทึกลง vault/daily/" + date.today().strftime("%Y-%m-%d") + ".md แล้ว")
                except Exception as e:
                    st.warning("บันทึก vault ไม่สำเร็จ: " + str(e))

        if stderr:
            with st.expander("Screener log (stderr)"):
                st.code(stderr, language="text")


# ---------------------------------------------------------------------------
# TAB 2 - Bot
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("ซื้อหุ้นอัตโนมัติ (Auto-Buy Bot)")
    st.caption("คัดหุ้นแล้วส่ง order ไป Alpaca Paper Account")

    budget = st.radio(
        "งบประมาณ (Budget)",
        ["Paper ($100k) — ทดสอบกลยุทธ์", "Real (~$1,400 / 50k THB) — จำลอง budget จริง"],
        horizontal=True,
    )
    if budget.startswith("Paper"):
        size_pct = 0.05
        max_top = 4
        st.info("Paper mode: position ละ ~$5,000 (5%) | สูงสุด 4 ตัว")
    else:
        size_pct = 0.0035
        max_top = 2
        st.warning("Real budget mode: position ละ ~$350 (25% ของ 50k THB) | สูงสุด 2 ตัว — ยังเป็น paper เท่านั้น ไม่มีเงินจริง")

    strategy = st.radio(
        "กลยุทธ์ (Strategy)",
        ["Momentum (แรงส่ง — หุ้นวิ่งแรง)", "Reversal (ต้นรอบ — หุ้นเพิ่งกลับตัว)"],
        horizontal=True,
    )
    order_type = st.radio(
        "ประเภท Order",
        ["Market (ซื้อทันที)", "Bracket (ซื้อ + ตั้ง stop -15% / เป้า +30% อัตโนมัติ)"],
        horizontal=True,
    )
    top_picks = st.slider("จำนวนหุ้นที่จะซื้อ (Top N picks)", min_value=1, max_value=max_top, value=min(2, max_top))

    def build_autobuy_cmd(dry_run=True):
        cmd = [PYTHON, AUTOBUY, "--top", str(top_picks), "--size", str(size_pct)]
        if strategy.startswith("Reversal"):
            cmd.append("--reversal")
        if "Bracket" in order_type:
            cmd.append("--bracket")
        if dry_run:
            cmd.append("--dry-run")
        return cmd

    col_preview, col_confirm = st.columns([1, 1])

    with col_preview:
        if st.button("👁 ดูก่อน (Dry Run)", type="secondary"):
            st.session_state["previewed"] = False
            cmd = build_autobuy_cmd(dry_run=True)
            st.session_state["preview_cmd"] = cmd

            with st.spinner("กำลังคัดหุ้นและคำนวณ... (อาจใช้เวลา 30 วิ)"):
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
            st.error("เกิดข้อผิดพลาด (exit " + str(rc) + ")")
            if stderr:
                st.code(stderr, language="text")
        else:
            st.code(stdout, language="text")
            if stderr:
                with st.expander("Log (รายละเอียด)"):
                    st.code(stderr, language="text")

        with col_confirm:
            st.markdown("###")
            if rc == 0:
                st.warning("ตรวจสอบผล preview ด้านซ้ายก่อนกดยืนยัน")
                if st.button("✅ ยืนยันซื้อ (CONFIRM BUY)", type="primary"):
                    cmd_live = build_autobuy_cmd(dry_run=False)
                    with st.spinner("กำลังส่ง order..."):
                        out2, err2, rc2 = run_subprocess(cmd_live, timeout=120)
                    if rc2 != 0:
                        st.error("ส่ง order ไม่สำเร็จ (exit " + str(rc2) + ")")
                        if err2:
                            st.code(err2, language="text")
                    else:
                        st.success("ส่ง order สำเร็จแล้ว!")
                        st.code(out2, language="text")
                        # --- Save trades to vault ---
                        strat_label = "Reversal" if strategy.startswith("Reversal") else "Momentum"
                        trades = parse_buys(out2)
                        saved = []
                        for (tk, sh, px, stp, tgt) in trades:
                            try:
                                fname = vault_save_trade(tk, sh, px, stp, tgt, strat_label)
                                saved.append(fname)
                            except Exception as e:
                                st.warning("บันทึก trade " + tk + " ไม่สำเร็จ: " + str(e))
                        if saved:
                            st.info("บันทึก trade ลง vault แล้ว: " + ", ".join(saved))
                    st.session_state["previewed"] = False


# ---------------------------------------------------------------------------
# TAB 3 - Positions
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("พอร์ตปัจจุบัน (Paper Account)")
    st.caption("ดู positions, P&L, และ buying power จาก Alpaca paper account")

    if st.button("🔄 รีเฟรช (Refresh)", type="primary"):
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
                m1.metric("มูลค่าพอร์ต (Portfolio)", "$" + format(portfolio_value, ",.2f"))
                m2.metric("เงินที่ซื้อได้ (Buying Power)", "$" + format(buying_power, ",.2f"))
                m3.metric("จำนวน Position", str(n_pos) + " / 4")

                if n_pos == 0:
                    st.info("ไม่มี position เปิดอยู่")
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
                    st.caption("🟢 เขียว = กำไร  |  🔴 แดง = ขาดทุน")

                # --- Save snapshot to vault ---
                try:
                    vault_save_positions(positions, portfolio_value, buying_power)
                    st.success("บันทึก snapshot ลง vault/daily/" + date.today().strftime("%Y-%m-%d") + ".md แล้ว")
                except Exception as e:
                    st.warning("บันทึก vault ไม่สำเร็จ: " + str(e))

        except Exception as e:
            st.error("เชื่อมต่อ Alpaca ไม่ได้: " + str(e))


# ---------------------------------------------------------------------------
# TAB 4 - EOD Report
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("EOD Report — สรุปปิดตลาด")
    st.caption("รันหลังตลาด US ปิด (05:00 น. ไทย) — ดู P&L paper + real positions ทั้งหมด")

    if st.button("📋 รัน EOD Report", type="primary"):
        with st.spinner("กำลังดึงข้อมูล positions..."):
            stdout, stderr, rc = run_subprocess([PYTHON, EOD], timeout=60)

        if rc != 0:
            st.error("EOD report ล้มเหลว (exit " + str(rc) + ")")
            if stderr:
                st.code(stderr, language="text")
        else:
            st.success("EOD Report — " + date.today().strftime("%Y-%m-%d"))
            st.markdown(stdout)

            # --- Save to vault daily note ---
            try:
                now = datetime.now().strftime("%H:%M")
                _append_to_daily_note("## EOD Report — " + now + "\n\n" + stdout)
                st.info("บันทึกลง vault/daily/" + date.today().strftime("%Y-%m-%d") + ".md แล้ว")
            except Exception as e:
                st.warning("บันทึก vault ไม่สำเร็จ: " + str(e))

        if stderr:
            with st.expander("Log"):
                st.code(stderr, language="text")
