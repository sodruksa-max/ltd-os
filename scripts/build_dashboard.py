"""
build_dashboard.py — generate Nick portfolio dashboard HTML
Output: docs/index.html (served by GitHub Pages)
Data: Alpaca paper account + vault KB files
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
        nav = INCEPTION_NAV
        return [], nav, nav


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
                    nav = float(parts[1].replace("$", "").replace(",", ""))
                    if d != INCEPTION_DATE:
                        rows.append({"date": d, "nick": nav})
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
        spy_return = (hist.iloc[-1] - hist.iloc[0]) / hist.iloc[0] * 100
        nick_return = (current_nav - INCEPTION_NAV) / INCEPTION_NAV * 100
        diff = nick_return - spy_return
        return f"{diff:+.2f}pp"
    except Exception:
        return "N/A"


def parse_thesis_data():
    result = {}
    tracker = KB_DIR / "THESIS_TRACKER.md"
    if not tracker.exists():
        return result
    content = tracker.read_text(encoding="utf-8")

    for ticker in TICKER_NAMES:
        pattern = rf"#{1,4}\s*{ticker}(.*?)(?=#{1,4}\s+[A-Z]{{2,6}}|\Z)"
        m = re.search(pattern, content, re.DOTALL)
        if not m:
            continue
        block = m.group(1)
        thesis_m = re.search(r"(?:thesis|why|narrative)[:\s]*(.*?)(?=kill|##|\Z)", block, re.DOTALL | re.IGNORECASE)
        thesis = thesis_m.group(1).strip()[:400] if thesis_m else ""
        kill_m = re.search(r"kill condition[s]?[:\s]*(.*?)(?=##|\Z)", block, re.DOTALL | re.IGNORECASE)
        kills = []
        if kill_m:
            kills = [l.strip().lstrip("-•*1234567890. ") for l in kill_m.group(1).splitlines() if l.strip() and not l.startswith("#")]
            kills = [k for k in kills if len(k) > 10][:5]
        result[ticker] = {
            "thesis": thesis,
            "kill_conditions": kills,
            "seed_weight": SEED_WEIGHTS.get(ticker, "N/A"),
        }
    return result


def get_weekly_summary():
    weekly_dir = NICK_DIR / "weekly"
    files = sorted(weekly_dir.glob("*_weekly-rec.md"), reverse=True)
    if not files:
        return "No weekly rec yet — runs automatically every Friday.", ""
    content = files[0].read_text(encoding="utf-8")
    changes_m = re.search(r"## Changes recommended\n(.*?)(?=##|\Z)", content, re.DOTALL)
    summary = changes_m.group(1).strip()[:200] if changes_m else "No changes this week."
    note_m = re.search(r"## Nick's note\n(.*?)(?=##|\Z)", content, re.DOTALL)
    note = note_m.group(1).strip()[:300] if note_m else ""
    return summary, note


def weeks_alive():
    start = datetime.strptime(INCEPTION_DATE, "%Y-%m-%d").date()
    return max(0, (date.today() - start).days // 7)


# ── HTML builder ──────────────────────────────────────────────────────────────

def build_chart_data(nav_history, benchmarks):
    dates = [r["date"] for r in nav_history]
    nick_vals = [r["nick"] for r in nav_history]
    spy_vals = [benchmarks["SPY"].get(d, INCEPTION_NAV) for d in dates]
    qqq_vals = [benchmarks["QQQ"].get(d, INCEPTION_NAV) for d in dates]
    soxx_vals = [benchmarks["SOXX"].get(d, INCEPTION_NAV) for d in dates]
    return {"dates": dates, "nick": nick_vals, "SPY": spy_vals, "QQQ": qqq_vals, "SOXX": soxx_vals}


def holdings_rows_html(holdings, nav, cash):
    cash_pct = round(cash / nav * 100, 1) if nav else 0
    rows = ""
    for h in holdings:
        pnl_class = "pnl-pos" if h["pnl_pct"] >= 0 else "pnl-neg"
        pnl_sign = "+" if h["pnl_pct"] >= 0 else ""
        bar_w = min(100, h["weight"])
        rows += f"""
        <tr onclick="selectHolding('{h['ticker']}')" id="row-{h['ticker']}">
          <td><div class="ticker-name">{h['ticker']}</div><div class="ticker-company">{h['company']}</div></td>
          <td><span class="status-pill">ปกติ</span></td>
          <td>{h['shares']}</td>
          <td>${h['cost']:.2f}</td>
          <td>${h['last']:.2f}</td>
          <td>${h['position']:,.0f}</td>
          <td>
            <div class="wbar-wrap">
              <div class="wbar-bg"><div class="wbar-fill" style="width:{bar_w}%"></div></div>
              <span>{h['weight']}%</span>
            </div>
          </td>
          <td class="{pnl_class}">{pnl_sign}{h['pnl_pct']:.2f}%<br><small>${h['pnl_dollar']:+,.0f}</small></td>
        </tr>"""
    cash_bar = min(100, cash_pct)
    rows += f"""
        <tr style="opacity:0.6;">
          <td><div class="ticker-name">CASH</div></td>
          <td>—</td><td>—</td><td>—</td><td>—</td>
          <td>${cash:,.0f}</td>
          <td>
            <div class="wbar-wrap">
              <div class="wbar-bg"><div class="wbar-fill" style="width:{cash_bar}%"></div></div>
              <span>{cash_pct}%</span>
            </div>
          </td>
          <td>—</td>
        </tr>"""
    return rows


def timeline_steps_html(weeks):
    labels = ["เริ่ม", "สป.1", "สป.2", "สป.4", "สป.8", "สป.12"]
    thresholds = [0, 1, 2, 4, 8, 12]
    html = ""
    for i, (label, thresh) in enumerate(zip(labels, thresholds)):
        active = " active" if weeks >= thresh else ""
        html += f'<div class="timeline-step{active}">{label}</div>'
    return html


def build_html(holdings, nav, cash, nav_history, benchmarks, thesis_data, weeks, action_summary, nick_note, vs_spy):
    cash_pct = round(cash / nav * 100, 1) if nav else 0
    total_return = round((nav - INCEPTION_NAV) / INCEPTION_NAV * 100, 2)
    actions_count = 0
    chart_data = build_chart_data(nav_history, benchmarks)
    rows_html = holdings_rows_html(holdings, nav, cash)
    timeline_html = timeline_steps_html(weeks)
    timeline_pct = min(100, weeks * 8)
    today_str = str(date.today())

    note_html = ""
    if nick_note:
        note_html = f'<div class="ab"><div class="ab-title">บันทึกของ Nick</div><div class="ab-text">{nick_note}</div></div>'

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>พอร์ตของ Nick</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {{
  --bg: #0d1117; --accent: #00c896; --accent-l: #00a87e;
  --text: #e6edf3; --muted: #8b949e; --border: #30363d;
  --card: #161b22; --white: #e6edf3;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'IBM Plex Mono', 'Courier New', monospace; background: var(--bg); color: var(--text); font-size: 15px; line-height: 1.7; }}
a {{ color: inherit; text-decoration: none; }}
.wrap {{ max-width: 1280px; margin: 0 auto; padding: 0 24px 60px; }}

/* Header */
.hdr {{ border-bottom: 2px solid var(--border); padding: 22px 0 0; margin-bottom: 24px; }}
.hdr-top {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }}
.site-title {{ font-size: 24px; font-weight: 700; letter-spacing: -.5px; }}
.site-sub {{ font-size: 13px; color: var(--muted); margin-top: 4px; }}
.hdr-meta {{ font-size: 13px; color: var(--muted); text-align: right; line-height: 1.9; }}
.tabs {{ display: flex; }}
.tab {{ padding: 10px 26px; border: 2px solid var(--border); border-bottom: none; font-family: inherit; font-size: 13px; font-weight: 700; letter-spacing: .5px; background: transparent; color: var(--muted); cursor: pointer; margin-right: -2px; }}
.tab.on {{ background: var(--accent); color: #0d1117; border-color: var(--accent); }}

/* Metrics */
.metrics {{ background: var(--accent); color: var(--white); border: 2px solid var(--border); display: grid; grid-template-columns: repeat(3,1fr); margin-bottom: 0; }}
.mc {{ padding: 18px 24px; border-right: 1px solid rgba(255,255,255,.18); }}
.mc:last-child {{ border-right: none; }}
.mc-lbl {{ font-size: 10px; text-transform: uppercase; letter-spacing: 1px; opacity: .65; margin-bottom: 5px; }}
.mc-val {{ font-size: 24px; font-weight: 700; letter-spacing: -1px; }}
.mc-sub {{ font-size: 11px; opacity: .8; margin-top: 3px; }}
.mc-badge {{ display: inline-block; background: rgba(255,255,255,.15); padding: 2px 9px; font-size: 11px; margin-top: 5px; }}

/* Timeline */
.tl {{ border: 2px solid var(--border); border-top: none; padding: 11px 24px; margin-bottom: 24px; display: flex; align-items: center; gap: 14px; }}
.tl-lbl {{ font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: var(--muted); white-space: nowrap; }}
.tl-track {{ flex: 1; height: 4px; background: var(--border); }}
.tl-fill {{ height: 100%; background: var(--accent); }}
.tl-steps {{ display: flex; }}
.timeline-step {{ font-size: 10px; padding: 4px 10px; border: 1px solid var(--border); margin-left: -1px; color: var(--muted); font-weight: 600; }}
.timeline-step.active {{ background: var(--accent); color: white; border-color: var(--accent); }}

/* Grid */
.g2 {{ display: grid; grid-template-columns: 60fr 40fr; gap: 16px; margin-bottom: 16px; }}

/* Card */
.card {{ background: var(--card); border: 2px solid var(--border); }}
.card-hdr {{ padding: 12px 20px; border-bottom: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
.card-title {{ font-size: 10px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }}
.card-sub {{ font-size: 11px; color: var(--muted); }}
.card-body {{ padding: 20px; }}

/* Benchmark btns */
.bbtns {{ display: flex; margin-bottom: 16px; }}
.bbtn {{ padding: 5px 13px; border: 1px solid var(--border); margin-right: -1px; font-family: inherit; font-size: 11px; font-weight: 600; background: transparent; color: var(--muted); cursor: pointer; }}
.bbtn.on {{ background: var(--accent); color: white; border-color: var(--accent); }}
.chart-wrap {{ height: 230px; position: relative; }}

/* Actions */
.act-hdr {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }}
.act-sum {{ font-size: 13px; font-weight: 600; line-height: 1.4; max-width: 200px; }}
.act-badge {{ background: var(--accent); color: white; font-size: 10px; font-weight: 700; padding: 3px 10px; white-space: nowrap; }}
.act-feed {{ max-height: 260px; overflow-y: auto; border-top: 1px solid var(--border); padding-top: 14px; }}
.ab {{ margin-bottom: 16px; }}
.ab-title {{ font-weight: 700; font-size: 12px; margin-bottom: 4px; }}
.ab-text {{ color: var(--muted); font-size: 12px; line-height: 1.75; }}

/* Table */
.htable {{ width: 100%; border-collapse: collapse; }}
.htable th {{ font-size: 10px; text-transform: uppercase; letter-spacing: .8px; color: var(--muted); padding: 8px 12px; text-align: left; border-bottom: 2px solid var(--border); font-weight: 600; }}
.htable td {{ padding: 11px 12px; border-bottom: 1px solid var(--border); vertical-align: middle; font-size: 12px; }}
.htable tbody tr {{ cursor: pointer; }}
.htable tbody tr:hover {{ background: #1f2937; }}
.htable tbody tr.sel {{ background: #243447; outline: 2px solid var(--accent); }}
.tn {{ font-weight: 700; font-size: 13px; }}
.tc {{ font-size: 10px; color: var(--muted); margin-top: 1px; }}
.pill {{ display: inline-block; background: var(--accent); color: white; font-size: 9px; font-weight: 700; padding: 2px 8px; letter-spacing: .4px; text-transform: uppercase; }}
.wbar-wrap {{ display: flex; align-items: center; gap: 6px; white-space: nowrap; }}
.wbar-bg {{ width: 52px; height: 5px; background: var(--border); flex-shrink: 0; }}
.wbar-fill {{ height: 100%; background: var(--accent); }}
.pnl-pos {{ color: #2d6a2d; font-weight: 600; }}
.pnl-neg {{ color: #8b2222; font-weight: 600; }}

/* Thesis */
.th-empty {{ text-align: center; padding: 56px 16px; color: var(--muted); }}
.th-empty-t {{ font-size: 15px; font-weight: 700; margin-bottom: 8px; color: var(--text); }}
.th-empty-s {{ font-size: 12px; line-height: 1.7; }}
.th-ticker {{ font-size: 22px; font-weight: 700; letter-spacing: -1px; }}
.th-co {{ color: var(--muted); font-size: 12px; margin: 4px 0 12px; }}
.th-seed {{ display: inline-block; border: 1px solid var(--border); padding: 2px 10px; font-size: 11px; margin-bottom: 18px; }}
.th-sec {{ font-size: 10px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; color: var(--muted); margin: 16px 0 8px; }}
.th-text {{ font-size: 12px; line-height: 1.85; color: var(--text); }}
.kill-list {{ list-style: none; }}
.kill-list li {{ padding: 8px 12px; border-left: 3px solid var(--accent); margin-bottom: 8px; font-size: 12px; background: rgba(0,200,150,.05); line-height: 1.65; }}

/* About */
.about {{ max-width: 620px; padding: 36px 0; }}
.about h2 {{ font-size: 15px; margin-bottom: 10px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }}
.about p {{ font-size: 12px; line-height: 1.9; color: var(--text); margin-bottom: 14px; }}
.about ul {{ margin: 0 0 14px 16px; font-size: 12px; line-height: 2; color: var(--text); }}

@media(max-width:760px) {{
  .g2 {{ grid-template-columns: 1fr; }}
  .metrics {{ grid-template-columns: 1fr; }}
  .mc {{ border-right: none; border-bottom: 1px solid rgba(255,255,255,.18); }}
}}
</style>
</head>
<body>
<div class="wrap" style="padding-top:22px;">

<div class="hdr">
  <div class="hdr-top">
    <div>
      <div class="site-title">พอร์ตของ Nick</div>
      <div class="site-sub">พอร์ตทดลอง $10K &bull; วินัยสไตล์ Nick Sleep</div>
    </div>
    <div class="hdr-meta">
      วันเริ่ม: {INCEPTION_DATE}<br>
      อัปเดตล่าสุด: {today_str}
    </div>
  </div>
  <div class="tabs">
    <button class="tab on" onclick="showTab('dash',this)">แดชบอร์ด</button>
    <button class="tab" onclick="showTab('about',this)">เกี่ยวกับ Nick</button>
  </div>
</div>

<div id="pane-dash">

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

  <div class="tl">
    <span class="tl-lbl">ไทม์ไลน์</span>
    <div class="tl-track"><div class="tl-fill" style="width:{timeline_pct}%"></div></div>
    <div class="tl-steps">{timeline_html}</div>
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
        <span class="act-badge" style="font-size:10px;background:var(--accent);color:white;padding:3px 10px;">{actions_count} รายการ</span>
      </div>
      <div class="card-body">
        <div class="act-hdr">
          <div class="act-sum">{action_summary[:80]}</div>
        </div>
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

  <div class="g2">
    <div class="card">
      <div class="card-hdr">
        <span class="card-title">พอร์ตหุ้น</span>
        <span class="card-sub">{len(holdings)} หุ้น + เงินสด</span>
      </div>
      <div class="card-body" style="padding:0;">
        <table class="htable">
          <thead>
            <tr>
              <th>หุ้น</th><th>สถานะ</th><th>จำนวน</th>
              <th>ต้นทุน</th><th>ราคาล่าสุด</th><th>มูลค่า</th>
              <th>น้ำหนัก</th><th>กำไร/ขาดทุน</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
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
        <div id="th-content" style="display:none;">
          <div class="th-ticker" id="th-ticker"></div>
          <div class="th-co" id="th-co"></div>
          <div class="th-seed" id="th-seed"></div>
          <div class="th-sec">Thesis เดิม</div>
          <div class="th-text" id="th-thesis"></div>
          <div class="th-sec">Kill Conditions</div>
          <ul class="kill-list" id="th-kills"></ul>
        </div>
      </div>
    </div>
  </div>

</div><!-- pane-dash -->

<div id="pane-about" style="display:none;">
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
    <p style="color:var(--muted); font-size:11px;">ที่มา: github.com/sodruksa-max/ltd-os &bull; เทรดจำลองเท่านั้น &bull; ไม่ใช่คำแนะนำทางการเงิน</p>
  </div>
</div>

<script>
const CD = {json.dumps(chart_data)};
const TD = {json.dumps(thesis_data)};
const HD = {json.dumps(holdings)};

// Tabs
function showTab(name, btn) {{
  document.getElementById('pane-dash').style.display = name==='dash' ? '' : 'none';
  document.getElementById('pane-about').style.display = name==='about' ? '' : 'none';
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('on'));
  btn.classList.add('on');
}}

// Holdings row select
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
  document.getElementById('th-thesis').textContent = t.thesis || 'รัน /stock-research '+ticker+' เพื่อบันทึก thesis ใน KB';
  const ul = document.getElementById('th-kills');
  ul.innerHTML = '';
  (t.kill_conditions || []).forEach(k => {{
    const li = document.createElement('li');
    li.textContent = k;
    ul.appendChild(li);
  }});
  if (!t.kill_conditions || !t.kill_conditions.length) {{
    ul.innerHTML = '<li>รัน /stock-research '+ticker+' เพื่อบันทึก kill conditions</li>';
  }}
}}

// Chart
let chart;
const COLORS = {{nick:'#00c896', SPY:'#8b949e', QQQ:'#58a6ff', SOXX:'#d29922'}};
function initChart() {{
  chart = new Chart(document.getElementById('perf').getContext('2d'), {{
    type: 'line',
    data: {{
      labels: CD.dates,
      datasets: [
        {{ label:'Nick', data:CD.nick, borderColor:COLORS.nick, backgroundColor:'rgba(0,200,150,.08)', borderWidth:2.5, fill:true, tension:.3, pointRadius:3 }},
        {{ label:'SPY', data:CD.SPY, borderColor:COLORS.SPY, borderWidth:1.5, borderDash:[5,4], fill:false, tension:.3, pointRadius:0 }}
      ]
    }},
    options: {{
      responsive:true, maintainAspectRatio:false,
      plugins:{{ legend:{{ labels:{{ font:{{family:'monospace',size:11}}, color:'#e6edf3' }} }}, tooltip:{{ mode:'index', intersect:false }} }},
      scales:{{
        x:{{ grid:{{color:'#30363d'}}, ticks:{{font:{{family:'monospace',size:10}}, color:'#8b949e'}} }},
        y:{{ grid:{{color:'#30363d'}}, ticks:{{font:{{family:'monospace',size:10}}, color:'#8b949e', callback:v=>'$'+v.toLocaleString()}} }}
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
    thesis_data = parse_thesis_data()
    action_summary, nick_note = get_weekly_summary()
    weeks = weeks_alive()
    vs_spy = get_spy_comparison(INCEPTION_DATE, nav)

    print(f"NAV: ${nav:,.2f} | Holdings: {len(holdings)} | Weeks: {weeks}")

    html = build_html(
        holdings, nav, cash, nav_history, benchmarks,
        thesis_data, weeks, action_summary, nick_note, vs_spy
    )

    out = DOCS_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Dashboard saved: {out}")


if __name__ == "__main__":
    main()
