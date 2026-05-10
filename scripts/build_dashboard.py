"""
build_dashboard.py — generate Nick portfolio dashboard HTML
Output: docs/index.html (served by GitHub Pages)
"""

import os
import json
import re
from datetime import date, datetime
from pathlib import Path

import yfinance as yf

REPO = Path(__file__).resolve().parent.parent
NICK_DIR = REPO / "vault/20_investment/nick"
KB_DIR = REPO / "vault/Knowledge"
DOCS_DIR = REPO / "docs"
DOCS_DIR.mkdir(exist_ok=True)

INCEPTION_DATE = "2026-05-10"
INCEPTION_NAV = 10000.0
TICKER_NAMES = {
    "NVDA": "NVIDIA Corporation",
    "AVGO": "Broadcom Inc.",
    "ASML": "ASML Holding",
    "PLTR": "Palantir Technologies",
    "RKLB": "Rocket Lab USA",
    "ASTS": "AST SpaceMobile",
}
SEED_WEIGHTS = {"NVDA": "30%", "AVGO": "25%", "ASML": "20%", "PLTR": "15%"}


# ── Data loaders ──────────────────────────────────────────────────────────────

def get_alpaca_data():
    try:
        from alpaca.trading.client import TradingClient
        client = TradingClient(
            os.environ["ALPACA_API_KEY"], os.environ["ALPACA_SECRET_KEY"], paper=True
        )
        account = client.get_account()
        nav = float(account.portfolio_value)
        cash = float(account.cash)
        positions = client.get_all_positions()
        holdings = []
        for p in positions:
            ticker = p.symbol
            qty = float(p.qty)
            avg = float(p.avg_entry_price)
            price = float(p.current_price)
            pnl_pct = (price - avg) / avg * 100
            mkt_val = qty * price
            holdings.append({
                "ticker": ticker,
                "company": TICKER_NAMES.get(ticker, ticker),
                "shares": int(qty),
                "cost": round(avg, 2),
                "last": round(price, 2),
                "position": round(mkt_val, 2),
                "weight": round(mkt_val / nav * 100, 1),
                "pnl_pct": round(pnl_pct, 2),
                "pnl_dollar": round(mkt_val - qty * avg, 2),
                "seed_weight": SEED_WEIGHTS.get(ticker, "N/A"),
            })
        return holdings, nav, cash
    except Exception as e:
        print(f"Alpaca error: {e} — using demo data")
        return [], INCEPTION_NAV, INCEPTION_NAV


def get_nav_history():
    nav_log = NICK_DIR / "performance/nav_log.md"
    rows = [{"date": INCEPTION_DATE, "nick": INCEPTION_NAV}]
    if not nav_log.exists():
        return rows
    for line in nav_log.read_text(encoding="utf-8").splitlines():
        if "|" in line and "$" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2 and parts[0] not in ("Date", "---"):
                try:
                    d = parts[0]
                    n = float(parts[1].replace("$", "").replace(",", ""))
                    if d != INCEPTION_DATE:
                        rows.append({"date": d, "nick": n})
                except Exception:
                    pass
    return rows


def get_benchmark_history(start_date: str):
    benchmarks = {"SPY": {}, "QQQ": {}, "SOXX": {}}
    for sym in benchmarks:
        try:
            hist = yf.Ticker(sym).history(start=start_date)["Close"]
            if hist.empty:
                continue
            base = hist.iloc[0]
            for dt, price in hist.items():
                d = dt.strftime("%Y-%m-%d")
                benchmarks[sym][d] = round(float(price / base * INCEPTION_NAV), 2)
        except Exception:
            pass
    return benchmarks


def get_spy_comparison(inception: str, current_nav: float):
    try:
        hist = yf.Ticker("SPY").history(start=inception)["Close"]
        if hist.empty:
            return "N/A"
        spy_ret = (hist.iloc[-1] - hist.iloc[0]) / hist.iloc[0] * 100
        nick_ret = (current_nav - INCEPTION_NAV) / INCEPTION_NAV * 100
        return f"{nick_ret - spy_ret:+.2f}pp"
    except Exception:
        return "N/A"


def get_regime():
    data = {"vix": None, "vix_prev": None, "vix_chg": None, "tnx": None, "soxx_chg": None}
    try:
        v = yf.Ticker("^VIX").history(period="5d")["Close"]
        if not v.empty:
            data["vix"] = round(float(v.iloc[-1]), 2)
            if len(v) >= 2:
                prev = round(float(v.iloc[-2]), 2)
                data["vix_prev"] = prev
                data["vix_chg"] = round(data["vix"] - prev, 2)
    except Exception:
        pass
    try:
        t = yf.Ticker("^TNX").history(period="2d")["Close"]
        data["tnx"] = round(float(t.iloc[-1]), 2) if not t.empty else None
    except Exception:
        pass
    try:
        s = yf.Ticker("SOXX").history(period="5d")["Close"]
        if len(s) >= 2:
            data["soxx_chg"] = round((s.iloc[-1] - s.iloc[0]) / s.iloc[0] * 100, 2)
    except Exception:
        pass
    return data


def parse_thesis_data():
    """Returns (thesis_by_ticker dict, clist list)."""
    result = {}
    clist = []
    tracker = KB_DIR / "THESIS_TRACKER.md"
    if not tracker.exists():
        return result, clist
    content = tracker.read_text(encoding="utf-8")

    for block in re.split(r'(?=###\s+T\d+)', content):
        title_m = re.match(r'###\s+(T\d+)\s*[—\-]\s*(.*?)\n', block)
        if not title_m:
            continue
        thesis_id = title_m.group(1).strip()
        thesis_title = title_m.group(2).strip()

        stmt_m = re.search(r'\*\*Statement:\*\*\s*(.*?)(?=\n\*\*|\Z)', block, re.DOTALL)
        statement = stmt_m.group(1).strip() if stmt_m else ""

        tickers_m = re.search(r'\*\*Tickers:\*\*\s*(.*?)(?=\n\*\*|\Z)', block)
        tickers = [t.strip() for t in tickers_m.group(1).split(',')] if tickers_m else []

        kill_m = re.search(r'\*\*Kill condition[s]?:\*\*\s*(.*?)(?=\n\*\*|\Z)', block, re.DOTALL)
        kill = kill_m.group(1).strip() if kill_m else ""

        status_m = re.search(r'\*\*Status:\*\*\s*(.*?)(?=\n\*\*|\Z)', block)
        t_status = status_m.group(1).strip() if status_m else ""

        for ticker in tickers:
            if ticker and ticker not in result:
                result[ticker] = {
                    "thesis": statement,
                    "kill_conditions": [kill] if kill else [],
                    "thesis_id": thesis_id,
                    "thesis_title": thesis_title,
                    "status": t_status,
                    "seed_weight": SEED_WEIGHTS.get(ticker, "N/A"),
                }

    clist_m = re.search(r'## C-List.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if clist_m:
        for line in clist_m.group(1).splitlines():
            if '|' in line and line.count('|') >= 3:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 3 and parts[0] not in ('Ticker', '---', ''):
                    clist.append({"ticker": parts[0], "reason": parts[1], "trigger": parts[2]})

    return result, clist


def get_weekly_summary():
    weekly_dir = NICK_DIR / "weekly"
    files = sorted(weekly_dir.glob("*_weekly-rec.md"), reverse=True)
    if not files:
        return "ยังไม่มีคำแนะนำ — รันอัตโนมัติทุกวันศุกร์", "", 0
    content = files[0].read_text(encoding="utf-8")
    changes_m = re.search(r"## Changes recommended\n(.*?)(?=##|\Z)", content, re.DOTALL)
    summary = changes_m.group(1).strip()[:200] if changes_m else "ไม่มีการเปลี่ยนแปลงสัปดาห์นี้"
    note_m = re.search(r"## Nick's note\n(.*?)(?=##|\Z)", content, re.DOTALL)
    note = note_m.group(1).strip()[:300] if note_m else ""
    actions_count = 0
    orders_m = re.search(r'```json\s*(\[.*?\])\s*```', content, re.DOTALL)
    if orders_m:
        try:
            orders = json.loads(orders_m.group(1))
            actions_count = sum(1 for o in orders if o.get("action", "NONE") != "NONE")
        except Exception:
            pass
    return summary, note, actions_count


def get_trade_log():
    log = NICK_DIR / "trade-log.md"
    if not log.exists():
        return []
    rows = []
    for line in log.read_text(encoding="utf-8").splitlines():
        if "|" in line and line.count("|") >= 10:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 10 and parts[0] not in ("Date", "---", ""):
                try:
                    rows.append({
                        "date": parts[0], "ticker": parts[1], "action": parts[2],
                        "shares": parts[3], "price": parts[4], "nav_pct": parts[5],
                        "conviction": parts[6], "vix": parts[7], "tnx": parts[8],
                        "soxx": parts[9], "reason": parts[10] if len(parts) > 10 else "",
                    })
                except Exception:
                    pass
    return rows


def get_ipo_radar():
    inbox = REPO / "vault/00_inbox"
    files = sorted(inbox.glob("ipo-radar-*.md"), reverse=True)
    return files[0].read_text(encoding="utf-8") if files else ""


def compute_risk_stats(nav_history, holdings, nav, thesis_data):
    """Returns dict of risk metrics calculated from available data."""
    stats = {
        "max_drawdown": None,
        "sharpe": None,
        "sharpe_note": "",
        "largest_position": None,
        "largest_ticker": "",
        "thesis_hhi": None,
        "weeks_of_data": 0,
    }

    # Max drawdown from nav history
    if len(nav_history) >= 2:
        navs = [r["nick"] for r in nav_history]
        peak = navs[0]
        max_dd = 0.0
        for n in navs:
            if n > peak:
                peak = n
            dd = (n - peak) / peak * 100
            if dd < max_dd:
                max_dd = dd
        stats["max_drawdown"] = round(max_dd, 2)
        stats["weeks_of_data"] = len(navs) - 1

        # Sharpe (annualized weekly) — needs >=4 data points
        if len(navs) >= 4:
            import statistics
            returns = [(navs[i] - navs[i-1]) / navs[i-1] * 100 for i in range(1, len(navs))]
            avg_r = statistics.mean(returns)
            std_r = statistics.stdev(returns) if len(returns) > 1 else 0
            if std_r > 0:
                stats["sharpe"] = round((avg_r / std_r) * (52 ** 0.5), 2)
                stats["sharpe_note"] = f"({len(returns)} สัปดาห์)"
            else:
                stats["sharpe_note"] = "stddev=0"
        else:
            stats["sharpe_note"] = f"ต้องการ 4+ สัปดาห์ (มี {len(navs)-1})"

    # Largest position
    if holdings:
        top = max(holdings, key=lambda h: h["weight"])
        stats["largest_position"] = top["weight"]
        stats["largest_ticker"] = top["ticker"]

    # Thesis HHI — concentration by thesis cluster
    if holdings:
        clusters: dict[str, float] = {}
        for h in holdings:
            tid = thesis_data.get(h["ticker"], {}).get("thesis_id", "Other")
            clusters[tid] = clusters.get(tid, 0) + h["weight"]
        total = sum(clusters.values()) or 1
        hhi = sum((v / total * 100) ** 2 for v in clusters.values())
        stats["thesis_hhi"] = round(hhi)

    return stats


def risk_stats_html(stats):
    # Max drawdown
    dd = stats["max_drawdown"]
    if dd is None:
        dd_val, dd_cls = "N/A", "stat-muted"
    elif dd == 0:
        dd_val, dd_cls = "0.00%", "stat-ok"
    elif dd > -10:
        dd_val, dd_cls = f"{dd:.2f}%", "stat-ok"
    elif dd > -20:
        dd_val, dd_cls = f"{dd:.2f}%", "stat-warn"
    else:
        dd_val, dd_cls = f"{dd:.2f}%", "stat-danger"

    # Sharpe
    sh = stats["sharpe"]
    sh_note = stats["sharpe_note"]
    if sh is None:
        sh_val, sh_cls = "—", "stat-muted"
        sh_sub = sh_note
    elif sh >= 1.5:
        sh_val, sh_cls = f"{sh:.2f}", "stat-ok"
        sh_sub = sh_note
    elif sh >= 0.5:
        sh_val, sh_cls = f"{sh:.2f}", "stat-warn"
        sh_sub = sh_note
    else:
        sh_val, sh_cls = f"{sh:.2f}", "stat-danger"
        sh_sub = sh_note

    # Largest position
    lp = stats["largest_position"]
    lt = stats["largest_ticker"]
    if lp is None:
        lp_val, lp_cls = "N/A", "stat-muted"
        lp_sub = ""
    elif lp >= 35:
        lp_val, lp_cls = f"{lp}%", "stat-danger"
        lp_sub = f"{lt} — เกินขีดจำกัด 30%"
    elif lp >= 25:
        lp_val, lp_cls = f"{lp}%", "stat-warn"
        lp_sub = f"{lt} — ระดับ high-conviction"
    else:
        lp_val, lp_cls = f"{lp}%", "stat-ok"
        lp_sub = lt

    # HHI
    hhi = stats["thesis_hhi"]
    if hhi is None:
        hhi_val, hhi_cls = "N/A", "stat-muted"
        hhi_sub = ""
    elif hhi >= 5000:
        hhi_val, hhi_cls = str(hhi), "stat-danger"
        hhi_sub = "Concentrated สูงมาก"
    elif hhi >= 2500:
        hhi_val, hhi_cls = str(hhi), "stat-warn"
        hhi_sub = "Moderately concentrated"
    else:
        hhi_val, hhi_cls = str(hhi), "stat-ok"
        hhi_sub = "Diversified ดี"

    return f"""<div class="risk-panel">
      <div class="risk-stat">
        <div class="risk-lbl">Max Drawdown</div>
        <div class="risk-val {dd_cls}">{dd_val}</div>
        <div class="risk-sub">จาก peak ตั้งแต่เริ่ม</div>
      </div>
      <div class="risk-stat">
        <div class="risk-lbl">Sharpe Ratio</div>
        <div class="risk-val {sh_cls}">{sh_val}</div>
        <div class="risk-sub">{sh_sub}</div>
      </div>
      <div class="risk-stat">
        <div class="risk-lbl">Largest Position</div>
        <div class="risk-val {lp_cls}">{lp_val}</div>
        <div class="risk-sub">{lp_sub}</div>
      </div>
      <div class="risk-stat">
        <div class="risk-lbl">Thesis HHI</div>
        <div class="risk-val {hhi_cls}">{hhi_val}</div>
        <div class="risk-sub">{hhi_sub}</div>
      </div>
    </div>"""


def get_earnings_calendar(tickers: list[str]):
    """Fetch next earnings date for each ticker. Returns sorted list of dicts."""
    today = date.today()
    results = []
    for sym in tickers:
        try:
            info = yf.Ticker(sym).calendar
            if info is None:
                continue
            if hasattr(info, "get"):
                edate = info.get("Earnings Date")
            else:
                edate = None
            if edate is None and hasattr(info, "columns"):
                col = info.columns[0] if len(info.columns) > 0 else None
                if col and "Earnings Date" in str(col):
                    edate = col
                elif hasattr(info, "iloc"):
                    row = info[info.index == "Earnings Date"]
                    if not row.empty:
                        edate = row.iloc[0, 0]
            if edate is None:
                continue
            if hasattr(edate, "__iter__") and not isinstance(edate, str):
                edate = list(edate)[0]
            if hasattr(edate, "date"):
                edate = edate.date()
            elif isinstance(edate, str):
                edate = datetime.strptime(edate[:10], "%Y-%m-%d").date()
            days_away = (edate - today).days
            if -7 <= days_away <= 90:
                results.append({"ticker": sym, "date": str(edate), "days": days_away})
        except Exception:
            pass
    return sorted(results, key=lambda x: x["days"])


def get_kb_gaps():
    weekly_dir = NICK_DIR / "weekly"
    files = sorted(weekly_dir.glob("*_weekly-rec.md"), reverse=True)
    if not files:
        return []
    content = files[0].read_text(encoding="utf-8")
    m = re.search(r"## KB Gaps.*?\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        if '|' in line and line.count('|') >= 3:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 3 and parts[0] not in ("Priority", "---", ""):
                rows.append({
                    "priority": parts[0], "topic": parts[1],
                    "why": parts[2], "cmd": parts[3] if len(parts) > 3 else "",
                })
    return rows


def weeks_alive():
    start = datetime.strptime(INCEPTION_DATE, "%Y-%m-%d").date()
    return max(0, (date.today() - start).days // 7)


# ── HTML fragment builders ─────────────────────────────────────────────────────

THESIS_COLORS = {
    "T1": "#00c896",
    "T2": "#58a6ff",
    "T3": "#d29922",
    "T4": "#bc8cff",
    "Cash": "#30363d",
    "Other": "#8b949e",
}

THESIS_SHORT = {
    "T1": "T1 AI Capex",
    "T2": "T2 Semis",
    "T3": "T3 Space",
    "T4": "T4 AI Software",
}


def thesis_exposure_html(holdings, nav, cash, thesis_data):
    """Horizontal stacked bar + breakdown list for thesis exposure."""
    clusters: dict[str, float] = {}

    for h in holdings:
        tid = thesis_data.get(h["ticker"], {}).get("thesis_id", "Other")
        clusters[tid] = clusters.get(tid, 0) + h["weight"]

    cash_pct = round(cash / nav * 100, 1) if nav else 0
    if cash_pct > 0:
        clusters["Cash"] = cash_pct

    if not clusters:
        clusters = {"T1": 30.0, "T2": 45.0, "T4": 15.0, "Cash": 10.0}
        seed_mode = True
    else:
        seed_mode = False

    total = sum(clusters.values())
    if total == 0:
        return ""

    seg_html = ""
    for tid, pct in sorted(clusters.items(), key=lambda x: -x[1]):
        color = THESIS_COLORS.get(tid, THESIS_COLORS["Other"])
        w = round(pct / total * 100, 1)
        label = THESIS_SHORT.get(tid, tid)
        seg_html += (
            f'<div class="exp-seg" style="width:{w}%;background:{color}" '
            f'title="{label}: {pct:.1f}%"></div>'
        )

    rows_html = ""
    for tid, pct in sorted(clusters.items(), key=lambda x: -x[1]):
        color = THESIS_COLORS.get(tid, THESIS_COLORS["Other"])
        label = THESIS_SHORT.get(tid, tid)
        warn = ' <span class="exp-warn">⚠ Concentration</span>' if pct >= 50 and tid != "Cash" else ""
        rows_html += (
            f'<div class="exp-row">'
            f'<span class="exp-dot" style="background:{color}"></span>'
            f'<span class="exp-name">{label}</span>'
            f'<span class="exp-bar-wrap"><div class="exp-mini-bg">'
            f'<div class="exp-mini-fill" style="width:{min(pct,100)}%;background:{color}"></div>'
            f'</div></span>'
            f'<span class="exp-pct">{pct:.1f}%</span>{warn}'
            f'</div>'
        )

    seed_note = '<div class="exp-seed-note">* Seed weights — Alpaca positions ยังไม่มี</div>' if seed_mode else ""

    return f"""<div class="card" style="margin-bottom:16px">
      <div class="card-hdr">
        <span class="card-title">Thesis Exposure</span>
        <span class="card-sub">% NAV ต่อ thesis cluster</span>
      </div>
      <div class="card-body">
        <div class="exp-bar">{seg_html}</div>
        <div class="exp-list">{rows_html}</div>
        {seed_note}
      </div>
    </div>"""


def status_label(pnl_pct):
    if pnl_pct >= 50:
        return ("ถึงเป้า", "pill pill-target")
    elif pnl_pct <= -20:
        return ("ใกล้ Stop", "pill pill-stop")
    elif pnl_pct < 0:
        return ("ขาดทุน", "pill pill-loss")
    return ("ปกติ", "pill pill-ok")


def early_gate_html(r):
    vix = r.get("vix")
    chg = r.get("vix_chg")

    if vix is None:
        return """  <div class="gate gate-unknown">
    <div class="gate-status">EARLY GATE <span class="gate-icon">?</span></div>
    <div class="gate-detail">ไม่สามารถดึงข้อมูล VIX ได้</div>
    <div class="gate-rule">กฎ: ซื้อใหม่ได้เมื่อ VIX &lt; 20</div>
  </div>"""

    if chg is not None:
        arrow = "↑" if chg > 0 else ("↓" if chg < 0 else "→")
        chg_cls = "gate-chg-up" if chg > 0 else ("gate-chg-down" if chg < 0 else "")
        chg_str = f'<span class="gate-vix-chg {chg_cls}">{arrow} {chg:+.2f} จากเมื่อวาน</span>'
    else:
        chg_str = ""

    if vix < 18:
        cls, icon, label, note = "gate-open", "✓", "เปิด", "ซื้อหุ้นใหม่ได้"
    elif vix < 20:
        cls, icon, label, note = "gate-caution", "⚠", "เปิด — ใกล้เส้น", f"VIX ห่างจากเส้น {20 - vix:.1f} จุด — ระวังกลับตัว"
    elif vix < 28:
        cls, icon, label, note = "gate-closed", "✗", "ปิด", "ห้ามซื้อหุ้นใหม่ รอ VIX ต่ำกว่า 20"
    else:
        cls, icon, label, note = "gate-panic", "✗", "ปิด — ตลาดตื่นตระหนก", "ห้ามซื้อเด็ดขาด รอความสงบก่อน"

    return f"""  <div class="gate {cls}">
    <div class="gate-left">
      <div class="gate-label">EARLY GATE</div>
      <div class="gate-status">{label} <span class="gate-icon">{icon}</span></div>
    </div>
    <div class="gate-center">
      <div class="gate-vix-num">{vix}</div>
      <div class="gate-vix-label">VIX {chg_str}</div>
    </div>
    <div class="gate-right">
      <div class="gate-note">{note}</div>
      <div class="gate-rule">กฎ: ซื้อใหม่เมื่อ VIX &lt; 20 เท่านั้น</div>
    </div>
  </div>"""


def build_chart_data(nav_history, benchmarks):
    dates = [r["date"] for r in nav_history]
    return {
        "dates": dates,
        "nick": [r["nick"] for r in nav_history],
        "SPY": [benchmarks["SPY"].get(d, INCEPTION_NAV) for d in dates],
        "QQQ": [benchmarks["QQQ"].get(d, INCEPTION_NAV) for d in dates],
        "SOXX": [benchmarks["SOXX"].get(d, INCEPTION_NAV) for d in dates],
    }


def holdings_rows_html(holdings, nav, cash):
    cash_pct = round(cash / nav * 100, 1) if nav else 0
    rows = ""
    for h in holdings:
        pnl_class = "pnl-pos" if h["pnl_pct"] >= 0 else "pnl-neg"
        sign = "+" if h["pnl_pct"] >= 0 else ""
        bar_w = min(100, h["weight"])
        label, pill_cls = status_label(h["pnl_pct"])
        rows += f"""
        <tr onclick="selectHolding('{h['ticker']}')" id="row-{h['ticker']}">
          <td><div class="tn">{h['ticker']}</div><div class="tc">{h['company']}</div></td>
          <td><span class="{pill_cls}">{label}</span></td>
          <td>{h['shares']}</td>
          <td>${h['cost']:.2f}</td>
          <td>${h['last']:.2f}</td>
          <td>${h['position']:,.0f}</td>
          <td><div class="wbar-wrap"><div class="wbar-bg"><div class="wbar-fill" style="width:{bar_w}%"></div></div><span>{h['weight']}%</span></div></td>
          <td class="{pnl_class}">{sign}{h['pnl_pct']:.2f}%<br><small>${h['pnl_dollar']:+,.0f}</small></td>
        </tr>"""
    cb = min(100, cash_pct)
    rows += f"""
        <tr style="opacity:0.6;">
          <td><div class="tn">CASH</div></td>
          <td>—</td><td>—</td><td>—</td><td>—</td>
          <td>${cash:,.0f}</td>
          <td><div class="wbar-wrap"><div class="wbar-bg"><div class="wbar-fill" style="width:{cb}%"></div></div><span>{cash_pct}%</span></div></td>
          <td>—</td>
        </tr>"""
    return rows


def timeline_steps_html(weeks):
    labels = ["เริ่ม", "สป.1", "สป.2", "สป.4", "สป.8", "สป.12"]
    thresholds = [0, 1, 2, 4, 8, 12]
    return "".join(
        f'<div class="timeline-step{" active" if weeks >= t else ""}">{l}</div>'
        for l, t in zip(labels, thresholds)
    )


def regime_html(r):
    tnx = r.get("tnx")
    soxx = r.get("soxx_chg")

    tnx_h = f'<span class="regime-val">{tnx}%</span>' if tnx else '<span class="regime-val">N/A</span>'

    if soxx is None:
        soxx_h = '<span class="regime-val">N/A</span>'
    elif soxx >= 0:
        soxx_h = f'<span class="regime-val pnl-pos">+{soxx}%</span>'
    else:
        soxx_h = f'<span class="regime-val pnl-neg">{soxx}%</span>'

    return f"""  <div class="regime-bar">
    <div class="regime-item"><span class="regime-lbl">10Y Yield</span>{tnx_h}</div>
    <span class="regime-sep">|</span>
    <div class="regime-item"><span class="regime-lbl">SOXX (5 วัน)</span>{soxx_h}</div>
  </div>"""


def clist_rows_html(clist):
    if not clist:
        return '<tr><td colspan="3" class="empty-cell">ยังไม่มี watchlist</td></tr>'
    rows = ""
    for c in clist:
        rows += f'<tr><td><strong>{c["ticker"]}</strong></td><td class="muted-cell">{c["reason"]}</td><td class="small-cell">{c["trigger"]}</td></tr>'
    return rows


def trade_rows_html(trades):
    if not trades:
        return '<tr><td colspan="8" class="empty-cell">ยังไม่มีการเทรด — execute.py จะบันทึกที่นี่หลัง order แรก</td></tr>'
    rows = ""
    action_pill = {"BUY": "pill-ok", "SELL": "pill-stop", "TRIM": "pill-loss"}
    for t in reversed(trades[-20:]):
        pc = action_pill.get(t["action"], "pill-ok")
        rows += f'<tr><td style="white-space:nowrap">{t["date"]}</td><td><strong>{t["ticker"]}</strong></td><td><span class="pill {pc}" style="font-size:9px">{t["action"]}</span></td><td>{t["shares"]}</td><td>{t["price"]}</td><td class="muted-cell">{t["conviction"]}</td><td class="muted-cell">{t["vix"]}</td><td class="small-cell" style="max-width:160px">{t["reason"]}</td></tr>'
    return rows


def kb_rows_html(gaps):
    if not gaps:
        return '<tr><td colspan="4" class="empty-cell">ยังไม่มี KB gaps — จะแสดงหลัง nick-weekly รันครั้งแรก</td></tr>'
    pmap = {"High": "pill-stop", "Med": "pill-loss", "Low": "pill-ok"}
    rows = ""
    for g in gaps:
        pc = pmap.get(g["priority"], "pill-ok")
        rows += f'<tr><td><span class="pill {pc}" style="font-size:9px">{g["priority"]}</span></td><td><strong>{g["topic"]}</strong></td><td class="muted-cell small-cell">{g["why"]}</td><td style="font-size:11px;color:var(--accent)">{g["cmd"]}</td></tr>'
    return rows


def earnings_calendar_html(earnings):
    if not earnings:
        return """<div class="card" style="margin-bottom:16px">
      <div class="card-hdr"><span class="card-title">Earnings Calendar</span><span class="card-sub">90 วันข้างหน้า</span></div>
      <div class="card-body"><p class="empty-cell">ไม่พบข้อมูล earnings — yfinance อาจไม่มีข้อมูลสำหรับหุ้นเหล่านี้</p></div>
    </div>"""

    today = date.today()
    items = ""
    for e in earnings:
        days = e["days"]
        sym = e["ticker"]
        edate = e["date"]
        company = TICKER_NAMES.get(sym, sym)

        if days < 0:
            urgency = "earn-past"
            badge = f'<span class="earn-badge earn-done">รายงานแล้ว {abs(days)} วัน</span>'
        elif days == 0:
            urgency = "earn-today"
            badge = '<span class="earn-badge earn-now">วันนี้!</span>'
        elif days <= 7:
            urgency = "earn-urgent"
            badge = f'<span class="earn-badge earn-soon">อีก {days} วัน</span>'
        elif days <= 14:
            urgency = "earn-near"
            badge = f'<span class="earn-badge earn-near-b">อีก {days} วัน</span>'
        else:
            urgency = ""
            badge = f'<span class="earn-badge earn-far">อีก {days} วัน</span>'

        bar_pct = max(0, min(100, round((1 - days / 90) * 100)))
        items += f"""
        <div class="earn-item {urgency}">
          <div class="earn-sym">{sym}<div class="earn-co">{company}</div></div>
          <div class="earn-timeline">
            <div class="earn-bar-bg"><div class="earn-bar-fill" style="width:{bar_pct}%"></div></div>
          </div>
          <div class="earn-date">{edate}</div>
          {badge}
        </div>"""

    return f"""<div class="card" style="margin-bottom:16px">
      <div class="card-hdr">
        <span class="card-title">Earnings Calendar</span>
        <span class="card-sub">90 วันข้างหน้า — {len(earnings)} หุ้น</span>
      </div>
      <div class="card-body" style="padding:12px 20px">{items}</div>
    </div>"""


def ipo_content_html(md_text):
    if not md_text:
        return '<p class="empty-cell" style="padding:24px 0;text-align:center;">ยังไม่มีข้อมูล IPO — scanner รันทุกวันจันทร์</p>'
    lines = []
    in_table = False
    for line in md_text.splitlines():
        if line.startswith("## "):
            lines.append(f'<h3 style="font-size:13px;margin:16px 0 8px;color:var(--accent)">{line[3:]}</h3>')
        elif line.startswith("# "):
            lines.append(f'<h2 style="font-size:14px;margin:0 0 12px">{line[2:]}</h2>')
        elif "|" in line and "---" not in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if parts:
                is_hdr = any(p in ("Ticker", "Company", "Date", "Size", "Sector") for p in parts)
                tag = "th" if is_hdr else "td"
                if is_hdr and not in_table:
                    lines.append("<table class='htable'><thead>")
                    in_table = True
                elif not is_hdr and in_table and "<thead>" in "\n".join(lines[-3:]):
                    lines.append("</thead><tbody>")
                lines.append("<tr>" + "".join(f"<{tag}>{p}</{tag}>" for p in parts) + "</tr>")
        elif "|" not in line and in_table:
            lines.append("</tbody></table>")
            in_table = False
            if line.strip():
                lines.append(f'<p style="font-size:12px;color:var(--muted);margin:4px 0">{line}</p>')
        elif line.strip():
            lines.append(f'<p style="font-size:12px;color:var(--muted);margin:4px 0">{line}</p>')
    if in_table:
        lines.append("</tbody></table>")
    return "\n".join(lines)


# ── Main HTML assembler ────────────────────────────────────────────────────────

def build_html(holdings, nav, cash, nav_history, benchmarks, thesis_data, clist,
               weeks, action_summary, nick_note, actions_count, vs_spy,
               regime, trade_log, ipo_radar, kb_gaps, earnings):

    cash_pct = round(cash / nav * 100, 1) if nav else 0
    total_return = round((nav - INCEPTION_NAV) / INCEPTION_NAV * 100, 2)
    chart_data = build_chart_data(nav_history, benchmarks)
    today_str = str(date.today())
    timeline_pct = min(100, weeks * 8)

    note_html = (
        f'<div class="ab"><div class="ab-title">บันทึกของ Nick</div>'
        f'<div class="ab-text">{nick_note}</div></div>'
        if nick_note else ""
    )

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>พอร์ตของ Nick</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {{
  --bg:#0d1117; --accent:#00c896; --text:#e6edf3;
  --muted:#8b949e; --border:#30363d; --card:#161b22;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'IBM Plex Mono','Courier New',monospace;background:var(--bg);color:var(--text);font-size:15px;line-height:1.7}}
.wrap{{max-width:1280px;margin:0 auto;padding:0 24px 60px}}
/* Header */
.hdr{{border-bottom:2px solid var(--border);padding:22px 0 0;margin-bottom:24px}}
.hdr-top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px}}
.site-title{{font-size:24px;font-weight:700;letter-spacing:-.5px}}
.site-sub{{font-size:13px;color:var(--muted);margin-top:4px}}
.hdr-meta{{font-size:13px;color:var(--muted);text-align:right;line-height:1.9}}
.tabs{{display:flex}}
.tab{{padding:10px 26px;border:2px solid var(--border);border-bottom:none;font-family:inherit;font-size:13px;font-weight:700;letter-spacing:.5px;background:transparent;color:var(--muted);cursor:pointer;margin-right:-2px}}
.tab.on{{background:var(--accent);color:#0d1117;border-color:var(--accent)}}
/* Metrics */
.metrics{{background:var(--accent);color:var(--text);border:2px solid var(--border);display:grid;grid-template-columns:repeat(3,1fr)}}
.mc{{padding:18px 24px;border-right:1px solid rgba(255,255,255,.18)}}
.mc:last-child{{border-right:none}}
.mc-lbl{{font-size:10px;text-transform:uppercase;letter-spacing:1px;opacity:.65;margin-bottom:5px}}
.mc-val{{font-size:24px;font-weight:700;letter-spacing:-1px;color:#0d1117}}
.mc-sub{{font-size:11px;opacity:.8;margin-top:3px;color:#0d1117}}
.mc-badge{{display:inline-block;background:rgba(0,0,0,.15);padding:2px 9px;font-size:11px;margin-top:5px;color:#0d1117}}
/* EARLY Gate Banner */
.gate{{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:0;padding:14px 28px;border:2px solid var(--border);margin-bottom:0;border-bottom:none}}
.gate-open{{background:rgba(0,200,150,.10);border-color:#00c896}}
.gate-caution{{background:rgba(210,153,34,.10);border-color:#d29922}}
.gate-closed{{background:rgba(248,81,73,.10);border-color:#f85149}}
.gate-panic{{background:rgba(248,81,73,.18);border-color:#f85149;animation:pulse-red 1.8s ease-in-out infinite}}
.gate-unknown{{background:rgba(139,148,158,.08);border-color:var(--border);grid-template-columns:auto 1fr auto}}
@keyframes pulse-red{{0%,100%{{box-shadow:0 0 0 0 rgba(248,81,73,0)}}50%{{box-shadow:0 0 0 6px rgba(248,81,73,.15)}}}}
.gate-left{{padding-right:32px;border-right:1px solid rgba(255,255,255,.08)}}
.gate-label{{font-size:9px;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin-bottom:3px}}
.gate-status{{font-size:18px;font-weight:700;letter-spacing:-.3px}}
.gate-open .gate-status{{color:#00c896}}
.gate-caution .gate-status{{color:#d29922}}
.gate-closed .gate-status,.gate-panic .gate-status{{color:#f85149}}
.gate-icon{{font-style:normal}}
.gate-center{{text-align:center;padding:0 32px;border-right:1px solid rgba(255,255,255,.08)}}
.gate-vix-num{{font-size:36px;font-weight:700;letter-spacing:-2px;line-height:1}}
.gate-open .gate-vix-num{{color:#00c896}}
.gate-caution .gate-vix-num{{color:#d29922}}
.gate-closed .gate-vix-num,.gate-panic .gate-vix-num{{color:#f85149}}
.gate-vix-label{{font-size:10px;color:var(--muted);margin-top:3px;text-transform:uppercase;letter-spacing:1px}}
.gate-vix-chg{{margin-left:6px;font-size:11px}}
.gate-chg-up{{color:#f85149}}.gate-chg-down{{color:#00c896}}
.gate-right{{padding-left:32px}}
.gate-note{{font-size:13px;font-weight:600;margin-bottom:4px}}
.gate-rule{{font-size:11px;color:var(--muted)}}
/* Regime */
.regime-bar{{border:2px solid var(--border);border-top:none;padding:10px 24px;display:flex;align-items:center;gap:20px;background:var(--card)}}
.regime-item{{display:flex;align-items:center;gap:8px}}
.regime-sep{{color:var(--border);font-size:18px}}
.regime-lbl{{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--muted)}}
.regime-val{{font-size:16px;font-weight:700}}
.regime-note{{font-size:11px;padding:1px 8px}}
.regime-note.ok{{background:rgba(0,200,150,.15);color:var(--accent)}}
.regime-note.warn{{background:rgba(255,180,0,.12);color:#d29922}}
.regime-note.danger{{background:rgba(248,81,73,.15);color:#f85149}}
.vix-low{{color:var(--accent)}}.vix-mid{{color:#d29922}}.vix-high{{color:#f85149}}
/* Timeline */
.tl{{border:2px solid var(--border);border-top:none;padding:11px 24px;margin-bottom:24px;display:flex;align-items:center;gap:14px}}
.tl-lbl{{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--muted);white-space:nowrap}}
.tl-track{{flex:1;height:4px;background:var(--border)}}
.tl-fill{{height:100%;background:var(--accent)}}
.tl-steps{{display:flex}}
.timeline-step{{font-size:10px;padding:4px 10px;border:1px solid var(--border);margin-left:-1px;color:var(--muted);font-weight:600}}
.timeline-step.active{{background:var(--accent);color:#0d1117;border-color:var(--accent)}}
/* Grid & Card */
.g2{{display:grid;grid-template-columns:60fr 40fr;gap:16px;margin-bottom:16px}}
.card{{background:var(--card);border:2px solid var(--border)}}
.card-hdr{{padding:12px 20px;border-bottom:2px solid var(--border);display:flex;justify-content:space-between;align-items:center}}
.card-title{{font-size:10px;text-transform:uppercase;letter-spacing:1px;font-weight:700}}
.card-sub{{font-size:11px;color:var(--muted)}}
.card-body{{padding:20px}}
/* Bench buttons */
.bbtns{{display:flex;margin-bottom:16px}}
.bbtn{{padding:5px 13px;border:1px solid var(--border);margin-right:-1px;font-family:inherit;font-size:11px;font-weight:600;background:transparent;color:var(--muted);cursor:pointer}}
.bbtn.on{{background:var(--accent);color:#0d1117;border-color:var(--accent)}}
.chart-wrap{{height:230px;position:relative}}
/* Actions */
.act-feed{{max-height:260px;overflow-y:auto;border-top:1px solid var(--border);padding-top:14px}}
.ab{{margin-bottom:16px}}
.ab-title{{font-weight:700;font-size:12px;margin-bottom:4px}}
.ab-text{{color:var(--muted);font-size:12px;line-height:1.75}}
.act-badge{{background:var(--accent);color:#0d1117;font-size:10px;font-weight:700;padding:3px 10px}}
/* Pills */
.pill{{display:inline-block;font-size:9px;font-weight:700;padding:2px 8px;letter-spacing:.4px;text-transform:uppercase}}
.pill-ok{{background:rgba(0,200,150,.15);color:var(--accent)}}
.pill-target{{background:rgba(88,166,255,.15);color:#58a6ff}}
.pill-stop{{background:rgba(248,81,73,.15);color:#f85149}}
.pill-loss{{background:rgba(210,153,34,.15);color:#d29922}}
/* Table */
.htable{{width:100%;border-collapse:collapse}}
.htable th{{font-size:10px;text-transform:uppercase;letter-spacing:.8px;color:var(--muted);padding:8px 12px;text-align:left;border-bottom:2px solid var(--border);font-weight:600}}
.htable td{{padding:11px 12px;border-bottom:1px solid var(--border);vertical-align:middle;font-size:12px}}
.htable tbody tr{{cursor:pointer}}
.htable tbody tr:hover{{background:#1f2937}}
.htable tbody tr.sel{{background:#243447;outline:2px solid var(--accent)}}
.tn{{font-weight:700;font-size:13px}}.tc{{font-size:10px;color:var(--muted);margin-top:1px}}
.wbar-wrap{{display:flex;align-items:center;gap:6px;white-space:nowrap}}
.wbar-bg{{width:52px;height:5px;background:var(--border);flex-shrink:0}}
.wbar-fill{{height:100%;background:var(--accent)}}
.pnl-pos{{color:#3fb950;font-weight:600}}.pnl-neg{{color:#f85149;font-weight:600}}
.empty-cell{{text-align:center;color:var(--muted);padding:24px}}
.muted-cell{{color:var(--muted);font-size:12px}}.small-cell{{font-size:11px}}
/* Thesis panel */
.th-empty{{text-align:center;padding:56px 16px;color:var(--muted)}}
.th-empty-t{{font-size:15px;font-weight:700;margin-bottom:8px;color:var(--text)}}
.th-empty-s{{font-size:12px;line-height:1.7}}
.th-ticker{{font-size:22px;font-weight:700;letter-spacing:-1px}}
.th-co{{color:var(--muted);font-size:12px;margin:4px 0 12px}}
.th-seed{{display:inline-block;border:1px solid var(--border);padding:2px 10px;font-size:11px;margin-bottom:8px}}
.th-tid{{display:inline-block;border:1px solid var(--accent);padding:2px 10px;font-size:11px;color:var(--accent);margin-bottom:8px;margin-left:6px}}
.th-sec{{font-size:10px;text-transform:uppercase;letter-spacing:1px;font-weight:700;color:var(--muted);margin:16px 0 8px}}
.th-text{{font-size:12px;line-height:1.85;color:var(--text)}}
.kill-list{{list-style:none}}
.kill-list li{{padding:8px 12px;border-left:3px solid var(--accent);margin-bottom:8px;font-size:12px;background:rgba(0,200,150,.05);line-height:1.65}}
/* Risk Stats Panel */
.risk-panel{{display:grid;grid-template-columns:repeat(4,1fr);border:2px solid var(--border);background:var(--card);margin-bottom:16px}}
.risk-stat{{padding:16px 20px;border-right:1px solid var(--border)}}
.risk-stat:last-child{{border-right:none}}
.risk-lbl{{font-size:9px;text-transform:uppercase;letter-spacing:1.2px;color:var(--muted);margin-bottom:6px}}
.risk-val{{font-size:22px;font-weight:700;letter-spacing:-.5px;margin-bottom:3px}}
.risk-sub{{font-size:10px;color:var(--muted);line-height:1.4}}
.stat-ok{{color:#3fb950}}.stat-warn{{color:#d29922}}.stat-danger{{color:#f85149}}.stat-muted{{color:var(--muted)}}
@media(max-width:760px){{.risk-panel{{grid-template-columns:repeat(2,1fr)}}.risk-stat{{border-bottom:1px solid var(--border)}}}}
/* Earnings Calendar */
.earn-item{{display:grid;grid-template-columns:140px 1fr 100px 110px;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);font-size:12px}}
.earn-item:last-child{{border-bottom:none}}
.earn-item.earn-urgent{{background:rgba(248,81,73,.04);margin:0 -20px;padding:10px 20px}}
.earn-item.earn-today{{background:rgba(248,81,73,.10);margin:0 -20px;padding:10px 20px}}
.earn-sym{{font-weight:700;font-size:13px;line-height:1.2}}
.earn-co{{font-size:10px;color:var(--muted);font-weight:400;margin-top:2px}}
.earn-bar-bg{{height:4px;background:var(--border);border-radius:1px}}
.earn-bar-fill{{height:100%;background:var(--accent);border-radius:1px;transition:width .3s}}
.earn-date{{font-size:11px;color:var(--muted);text-align:right}}
.earn-badge{{display:inline-block;font-size:10px;font-weight:700;padding:3px 10px;text-align:center;white-space:nowrap}}
.earn-done{{background:rgba(139,148,158,.15);color:var(--muted)}}
.earn-now{{background:rgba(248,81,73,.2);color:#f85149;animation:pulse-red 1s ease-in-out infinite}}
.earn-soon{{background:rgba(248,81,73,.15);color:#f85149}}
.earn-near-b{{background:rgba(210,153,34,.15);color:#d29922}}
.earn-far{{background:rgba(0,200,150,.1);color:var(--accent)}}
/* Thesis Exposure */
.exp-bar{{display:flex;height:18px;border-radius:2px;overflow:hidden;margin-bottom:18px;gap:2px}}
.exp-seg{{height:100%;transition:opacity .2s;cursor:default}}
.exp-seg:hover{{opacity:.75}}
.exp-list{{display:flex;flex-direction:column;gap:8px}}
.exp-row{{display:grid;grid-template-columns:12px 120px 1fr 52px auto;align-items:center;gap:8px;font-size:12px}}
.exp-dot{{width:10px;height:10px;border-radius:1px;flex-shrink:0}}
.exp-name{{color:var(--text);font-weight:600}}
.exp-bar-wrap{{flex:1}}
.exp-mini-bg{{height:4px;background:var(--border);border-radius:1px}}
.exp-mini-fill{{height:100%;border-radius:1px}}
.exp-pct{{text-align:right;font-weight:700;font-size:13px;white-space:nowrap}}
.exp-warn{{font-size:9px;color:#f85149;white-space:nowrap}}
.exp-seed-note{{font-size:10px;color:var(--muted);margin-top:12px;border-top:1px solid var(--border);padding-top:8px}}
/* Bottom tabs */
.btabs{{display:flex;margin-top:24px;border-bottom:2px solid var(--border)}}
.btab{{padding:8px 20px;font-family:inherit;font-size:12px;font-weight:700;background:transparent;color:var(--muted);border:none;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px}}
.btab.on{{color:var(--accent);border-bottom-color:var(--accent)}}
.bpane{{display:none;padding:20px 0}}.bpane.on{{display:block}}
/* About */
.about{{max-width:620px;padding:36px 0}}
.about h2{{font-size:15px;margin-bottom:10px;border-bottom:1px solid var(--border);padding-bottom:6px}}
.about p{{font-size:12px;line-height:1.9;color:var(--text);margin-bottom:14px}}
.about ul{{margin:0 0 14px 16px;font-size:12px;line-height:2;color:var(--text)}}
@media(max-width:760px){{
  .g2{{grid-template-columns:1fr}}
  .metrics{{grid-template-columns:1fr}}
  .mc{{border-right:none;border-bottom:1px solid rgba(255,255,255,.18)}}
  .regime-bar{{flex-wrap:wrap;gap:12px}}
  .gate{{grid-template-columns:1fr;gap:12px;text-align:center}}
  .gate-left,.gate-center,.gate-right{{border:none;padding:0}}
  .gate-vix-num{{font-size:28px}}
}}
</style>
</head>
<body>
<div class="wrap" style="padding-top:22px">

<div class="hdr">
  <div class="hdr-top">
    <div>
      <div class="site-title">พอร์ตของ Nick</div>
      <div class="site-sub">พอร์ตทดลอง $10K &bull; วินัยสไตล์ Nick Sleep</div>
    </div>
    <div class="hdr-meta">วันเริ่ม: {INCEPTION_DATE}<br>อัปเดตล่าสุด: {today_str}</div>
  </div>
  <div class="tabs">
    <button class="tab on" onclick="showTab('dash',this)">แดชบอร์ด</button>
    <button class="tab" onclick="showTab('about',this)">เกี่ยวกับ Nick</button>
  </div>
</div>

<div id="pane-dash">

{early_gate_html(regime)}

  <div class="metrics">
    <div class="mc">
      <div class="mc-lbl">วันที่</div>
      <div class="mc-val">{today_str}</div>
      <div class="mc-sub">สัปดาห์ที่ {weeks} นับจากเริ่ม</div>
    </div>
    <div class="mc">
      <div class="mc-lbl">มูลค่าพอร์ต</div>
      <div class="mc-val">${nav:,.2f}</div>
      <div class="mc-sub">{total_return:+.2f}% นับจากเริ่ม</div>
      <div class="mc-badge">เทียบ SPY: {vs_spy}</div>
    </div>
    <div class="mc">
      <div class="mc-lbl">สถานะ</div>
      <div class="mc-val">{weeks} สัปดาห์</div>
      <div class="mc-sub">{actions_count} รายการสัปดาห์นี้</div>
      <div class="mc-badge">{len(holdings)} หุ้นในพอร์ต</div>
    </div>
  </div>

{regime_html(regime)}

  {risk_stats_html(compute_risk_stats(nav_history, holdings, nav, thesis_data))}

  <div class="tl">
    <span class="tl-lbl">ไทม์ไลน์</span>
    <div class="tl-track"><div class="tl-fill" style="width:{timeline_pct}%"></div></div>
    <div class="tl-steps">{timeline_steps_html(weeks)}</div>
  </div>

  <div class="g2">
    <div class="card">
      <div class="card-hdr">
        <span class="card-title">ผลตอบแทนเทียบ Benchmark</span>
        <span class="card-sub">ผลตอบแทนสะสมนับจากเริ่ม</span>
      </div>
      <div class="card-body">
        <div class="bbtns">
          <button class="bbtn on" onclick="setBench('SPY',this)">SPY S&amp;P 500</button>
          <button class="bbtn" onclick="setBench('QQQ',this)">QQQ Nasdaq-100</button>
          <button class="bbtn" onclick="setBench('SOXX',this)">SOXX Semiconductor</button>
        </div>
        <div class="chart-wrap"><canvas id="perf"></canvas></div>
      </div>
    </div>
    <div class="card">
      <div class="card-hdr">
        <span class="card-title">คำแนะนำสัปดาห์นี้</span>
        <span class="act-badge">{actions_count} รายการ</span>
      </div>
      <div class="card-body">
        <div style="font-size:13px;font-weight:600;line-height:1.4;margin-bottom:14px">{action_summary[:120]}</div>
        <div class="act-feed">
          <div class="ab">
            <div class="ab-title">Kill Conditions</div>
            <div class="ab-text">ไม่มี kill condition ถูกกระตุ้นสัปดาห์นี้ ทุก thesis ยังคงสถานะปกติตามข้อมูลราคาล่าสุด</div>
          </div>
          <div class="ab">
            <div class="ab-title">เงินสด</div>
            <div class="ab-text">เงินสด {cash_pct:.1f}% ของ NAV รอโอกาส — กฎ EARLY-only ซื้อใหม่ได้เมื่อ VIX &lt; 20 เท่านั้น</div>
          </div>
          {note_html}
        </div>
      </div>
    </div>
  </div>

  {earnings_calendar_html(earnings)}

  {thesis_exposure_html(holdings, nav, cash, thesis_data)}

  <div class="g2">
    <div class="card">
      <div class="card-hdr">
        <span class="card-title">พอร์ตหุ้น</span>
        <span class="card-sub">{len(holdings)} หุ้น + เงินสด</span>
      </div>
      <div class="card-body" style="padding:0">
        <table class="htable">
          <thead><tr>
            <th>หุ้น</th><th>สถานะ</th><th>จำนวน</th>
            <th>ต้นทุน</th><th>ราคาล่าสุด</th><th>มูลค่า</th>
            <th>น้ำหนัก</th><th>กำไร/ขาดทุน</th>
          </tr></thead>
          <tbody>{holdings_rows_html(holdings, nav, cash)}</tbody>
        </table>
      </div>
    </div>
    <div class="card">
      <div class="card-hdr">
        <span class="card-title">Thesis &amp; Kill Conditions</span>
        <span class="card-sub" id="th-label">—</span>
      </div>
      <div class="card-body">
        <div id="th-empty" class="th-empty">
          <div class="th-empty-t">เลือกหุ้น</div>
          <div class="th-empty-s">คลิกแถวในตารางเพื่อดู thesis<br>และ kill conditions ของ Nick</div>
        </div>
        <div id="th-content" style="display:none">
          <div class="th-ticker" id="th-ticker"></div>
          <div class="th-co" id="th-co"></div>
          <span class="th-seed" id="th-seed"></span><span class="th-tid" id="th-tid"></span>
          <div class="th-sec">Thesis เดิม</div>
          <div class="th-text" id="th-thesis"></div>
          <div class="th-sec">Kill Conditions</div>
          <ul class="kill-list" id="th-kills"></ul>
          <div class="th-sec" id="th-status-sec" style="display:none">สถานะ Thesis</div>
          <div class="th-text" id="th-status" style="color:var(--muted)"></div>
        </div>
      </div>
    </div>
  </div>

  <div class="btabs">
    <button class="btab on" onclick="showBtab('clist',this)">C-List (Watchlist)</button>
    <button class="btab" onclick="showBtab('tradelog',this)">Trade Log</button>
    <button class="btab" onclick="showBtab('ipo',this)">IPO Radar</button>
    <button class="btab" onclick="showBtab('kbgaps',this)">KB Gaps</button>
  </div>

  <div id="bpane-clist" class="bpane on">
    <div class="card">
      <div class="card-hdr"><span class="card-title">C-List — รอ Trigger</span><span class="card-sub">จาก THESIS_TRACKER.md</span></div>
      <div class="card-body" style="padding:0">
        <table class="htable">
          <thead><tr><th>หุ้น</th><th>เหตุผลที่ดู</th><th>Trigger ที่รอ</th></tr></thead>
          <tbody>{clist_rows_html(clist)}</tbody>
        </table>
      </div>
    </div>
  </div>

  <div id="bpane-tradelog" class="bpane">
    <div class="card">
      <div class="card-hdr"><span class="card-title">Trade Log</span><span class="card-sub">20 รายการล่าสุด</span></div>
      <div class="card-body" style="padding:0">
        <table class="htable">
          <thead><tr><th>วันที่</th><th>หุ้น</th><th>Action</th><th>จำนวน</th><th>ราคา</th><th>Conviction</th><th>VIX</th><th>เหตุผล</th></tr></thead>
          <tbody>{trade_rows_html(trade_log)}</tbody>
        </table>
      </div>
    </div>
  </div>

  <div id="bpane-ipo" class="bpane">
    <div class="card">
      <div class="card-hdr"><span class="card-title">IPO Radar</span><span class="card-sub">$500M+ / buzz detection</span></div>
      <div class="card-body">{ipo_content_html(ipo_radar)}</div>
    </div>
  </div>

  <div id="bpane-kbgaps" class="bpane">
    <div class="card">
      <div class="card-hdr"><span class="card-title">KB Gaps</span><span class="card-sub">Research ที่ขาด — จาก nick-weekly</span></div>
      <div class="card-body" style="padding:0">
        <table class="htable">
          <thead><tr><th>Priority</th><th>หัวข้อ</th><th>เหตุผล</th><th>คำสั่ง</th></tr></thead>
          <tbody>{kb_rows_html(kb_gaps)}</tbody>
        </table>
      </div>
    </div>
  </div>

</div><!-- pane-dash -->

<div id="pane-about" style="display:none">
  <div class="about">
    <h2>Nick คือใคร?</h2>
    <p>Nick คือ AI portfolio manager ที่อ่านได้เฉพาะ knowledge base — thesis tracker, insight atoms และราคาปัจจุบัน ไม่รู้เกี่ยวกับการเทรดจริงหรือพอร์ตจริง</p>
    <p>Nick ได้รับแรงบันดาลใจจาก Nick Sleep นักลงทุนชื่อดังที่เน้น concentration สูง ถือยาว และวินัยตาม thesis</p>
    <h2>กฎ</h2>
    <ul>
      <li>EARLY-only: ซื้อใหม่ได้เมื่อ VIX &lt; 20 เท่านั้น</li>
      <li>ถือสูงสุด 10 หุ้น (ปกติ 4–6 high-conviction)</li>
      <li>Stop แข็ง: –25% ต่อหุ้น (ออกทั้งหมด)</li>
      <li>Partial exit: ขายครึ่งเมื่อ +50% ถือส่วนที่เหลือต่อ</li>
      <li>Benchmark: 50% QQQM + 50% SOXX ไม่ใช่ SPY</li>
      <li>ไม่เขียน KB เอง — Nick แค่แจ้ง gap ให้ทราบ</li>
    </ul>
    <h2>วงจรพัฒนาตนเอง</h2>
    <p>Nick Weekly รันทุกวันศุกร์ผ่าน GitHub Actions (Gemini 2.0 Flash) Trade log บันทึก regime tags (VIX, 10Y, sector ETF trend) ทุก entry หลัง 30+ trade ที่ปิดแล้ว pattern จะป้อนกลับเข้า KB</p>
    <p style="color:var(--muted);font-size:11px">ที่มา: github.com/sodruksa-max/ltd-os &bull; เทรดจำลองเท่านั้น &bull; ไม่ใช่คำแนะนำทางการเงิน</p>
  </div>
</div>

<script>
const CD = {json.dumps(chart_data)};
const TD = {json.dumps(thesis_data)};
const HD = {json.dumps(holdings)};

function showTab(name, btn) {{
  document.getElementById('pane-dash').style.display = name==='dash' ? '' : 'none';
  document.getElementById('pane-about').style.display = name==='about' ? '' : 'none';
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('on'));
  btn.classList.add('on');
}}

function showBtab(name, btn) {{
  document.querySelectorAll('.bpane').forEach(p => p.classList.remove('on'));
  document.querySelectorAll('.btab').forEach(t => t.classList.remove('on'));
  document.getElementById('bpane-'+name).classList.add('on');
  btn.classList.add('on');
}}

function selectHolding(ticker) {{
  document.querySelectorAll('.htable tbody tr').forEach(r => r.classList.remove('sel'));
  const row = document.getElementById('row-'+ticker);
  if (row) row.classList.add('sel');
  const h = HD.find(x => x.ticker===ticker) || {{}};
  const t = TD[ticker] || {{}};
  document.getElementById('th-label').textContent = ticker;
  document.getElementById('th-empty').style.display = 'none';
  document.getElementById('th-content').style.display = '';
  document.getElementById('th-ticker').textContent = ticker;
  document.getElementById('th-co').textContent = h.company || '';
  document.getElementById('th-seed').textContent = 'น้ำหนักเริ่มต้น: ' + (t.seed_weight || 'N/A');
  const tid = t.thesis_id ? t.thesis_id + (t.thesis_title ? ' — ' + t.thesis_title : '') : '';
  document.getElementById('th-tid').textContent = tid;
  document.getElementById('th-thesis').textContent = t.thesis || 'รัน /stock-research ' + ticker + ' เพื่อบันทึก thesis ใน KB';
  const ul = document.getElementById('th-kills');
  ul.innerHTML = '';
  (t.kill_conditions || []).forEach(k => {{ const li = document.createElement('li'); li.textContent = k; ul.appendChild(li); }});
  if (!t.kill_conditions || !t.kill_conditions.length) ul.innerHTML = '<li>รัน /stock-research ' + ticker + ' เพื่อบันทึก kill conditions</li>';
  const sec = document.getElementById('th-status-sec');
  const sta = document.getElementById('th-status');
  if (t.status) {{ sec.style.display = ''; sta.style.display = ''; sta.textContent = t.status; }}
  else {{ sec.style.display = 'none'; sta.style.display = 'none'; }}
}}

let chart;
const COLORS = {{nick:'#00c896', SPY:'#8b949e', QQQ:'#58a6ff', SOXX:'#d29922'}};
function initChart() {{
  chart = new Chart(document.getElementById('perf').getContext('2d'), {{
    type:'line',
    data:{{
      labels:CD.dates,
      datasets:[
        {{label:'Nick',data:CD.nick,borderColor:COLORS.nick,backgroundColor:'rgba(0,200,150,.08)',borderWidth:2.5,fill:true,tension:.3,pointRadius:3}},
        {{label:'SPY',data:CD.SPY,borderColor:COLORS.SPY,borderWidth:1.5,borderDash:[5,4],fill:false,tension:.3,pointRadius:0}}
      ]
    }},
    options:{{
      responsive:true,maintainAspectRatio:false,
      plugins:{{legend:{{labels:{{font:{{family:'monospace',size:11}},color:'#e6edf3'}}}},tooltip:{{mode:'index',intersect:false}}}},
      scales:{{
        x:{{grid:{{color:'#30363d'}},ticks:{{font:{{family:'monospace',size:10}},color:'#8b949e'}}}},
        y:{{grid:{{color:'#30363d'}},ticks:{{font:{{family:'monospace',size:10}},color:'#8b949e',callback:v=>'$'+v.toLocaleString()}}}}
      }}
    }}
  }});
}}
function setBench(b, btn) {{
  document.querySelectorAll('.bbtn').forEach(x=>x.classList.remove('on'));
  btn.classList.add('on');
  chart.data.datasets[1].label = b;
  chart.data.datasets[1].data = CD[b] || [];
  chart.data.datasets[1].borderColor = COLORS[b] || '#aaa';
  chart.update();
}}
initChart();
</script>
</body>
</html>"""


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Fetching data...")
    holdings, nav, cash = get_alpaca_data()
    nav_history = get_nav_history()
    benchmarks = get_benchmark_history(INCEPTION_DATE)
    thesis_data, clist = parse_thesis_data()
    action_summary, nick_note, actions_count = get_weekly_summary()
    weeks = weeks_alive()
    vs_spy = get_spy_comparison(INCEPTION_DATE, nav)
    regime = get_regime()
    trade_log = get_trade_log()
    ipo_radar = get_ipo_radar()
    kb_gaps = get_kb_gaps()

    watch_tickers = list({h["ticker"] for h in holdings} | set(SEED_WEIGHTS.keys()))
    earnings = get_earnings_calendar(watch_tickers)

    print(f"NAV: ${nav:,.2f} | Holdings: {len(holdings)} | Weeks: {weeks} | VIX: {regime.get('vix')} | Earnings: {len(earnings)}")

    html = build_html(
        holdings, nav, cash, nav_history, benchmarks,
        thesis_data, clist, weeks, action_summary, nick_note, actions_count,
        vs_spy, regime, trade_log, ipo_radar, kb_gaps, earnings
    )

    out = DOCS_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Dashboard saved: {out}")


if __name__ == "__main__":
    main()
