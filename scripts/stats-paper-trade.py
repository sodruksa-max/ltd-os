#!/usr/bin/env python3
"""
Paper trade stats calculator — stdlib only, no pip required.

Usage:
    python scripts/stats-paper-trade.py

Reads all .md files in vault/20_investment/_journal/trades/
Calculates R-multiple for closed trades, updates paper-trade-stats.md
"""

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRADES_DIR = ROOT / "vault/20_investment/_journal/trades"
STATS_FILE = ROOT / "vault/20_investment/paper-trade-stats.md"

TARGET_TRADES = 12
TARGET_WIN_RATE = 40.0
TARGET_R = 1.5


def parse_frontmatter(filepath: Path) -> dict:
    """Parse simple key: value YAML frontmatter between --- delimiters."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if val in ("~", "", "null", "None"):
            val = None
        data[key] = val
    return data


def to_float(val) -> float | None:
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def calc_r(entry: float, stop: float, exit_price: float, direction: str) -> float:
    risk = abs(entry - stop)
    if risk == 0:
        return 0.0
    if direction == "long":
        return round((exit_price - entry) / risk, 2)
    return round((entry - exit_price) / risk, 2)


def main():
    if not TRADES_DIR.exists():
        print(f"Trades directory not found: {TRADES_DIR}")
        return

    closed_trades = []

    for f in sorted(TRADES_DIR.glob("*.md")):
        data = parse_frontmatter(f)
        if data.get("status") != "closed":
            continue

        entry = to_float(data.get("entry"))
        stop = to_float(data.get("stop"))
        exit_p = to_float(data.get("exit"))
        direction = str(data.get("direction", "long")).lower()
        size = to_float(data.get("size"))

        r = None
        if entry is not None and stop is not None and exit_p is not None:
            r = calc_r(entry, stop, exit_p, direction)

        result = data.get("result")
        if not result and r is not None:
            result = "win" if r > 0 else ("loss" if r < 0 else "breakeven")

        closed_trades.append({
            "ticker": data.get("ticker", "?"),
            "direction": direction,
            "date_close": str(data.get("date_close", "?")),
            "entry": entry,
            "stop": stop,
            "exit": exit_p,
            "size": size,
            "r_multiple": r,
            "result": result,
        })

    total = len(closed_trades)
    wins = sum(1 for t in closed_trades if t["result"] == "win")
    losses = sum(1 for t in closed_trades if t["result"] == "loss")
    breakevens = total - wins - losses
    win_rate = round(wins / total * 100, 1) if total else 0.0

    r_values = [t["r_multiple"] for t in closed_trades if t["r_multiple"] is not None]
    avg_r = round(sum(r_values) / len(r_values), 2) if r_values else 0.0

    def pnl(t):
        try:
            shares = t["size"] / t["entry"]
            if t["direction"] == "long":
                return (t["exit"] - t["entry"]) * shares
            return (t["entry"] - t["exit"]) * shares
        except (TypeError, ZeroDivisionError):
            return 0.0

    total_pnl = sum(pnl(t) for t in closed_trades)

    meets_trades = total >= TARGET_TRADES
    meets_wr = win_rate >= TARGET_WIN_RATE
    meets_r = avg_r >= TARGET_R
    eligible = meets_trades and meets_wr and meets_r

    if eligible:
        phase_status = "✅ พร้อม go-live — ผ่านทุก metric แล้ว"
    else:
        gaps = []
        if not meets_trades:
            gaps.append(f"trades {total}/{TARGET_TRADES}")
        if not meets_wr:
            gaps.append(f"win rate {win_rate}%/{TARGET_WIN_RATE}%")
        if not meets_r:
            gaps.append(f"avg R {avg_r}/{TARGET_R}")
        phase_status = f"❌ ยังไม่พร้อม — ขาด: {', '.join(gaps)}"

    rows = []
    for t in closed_trades:
        r_str = f"{t['r_multiple']:+.2f} R" if t["r_multiple"] is not None else "?"
        wl = {"win": "W", "loss": "L", "breakeven": "B"}.get(t["result"] or "", "?")
        size_str = f"${int(t['size']):,}" if t["size"] else "?"
        entry_str = f"${t['entry']}" if t["entry"] else "?"
        exit_str = f"${t['exit']}" if t["exit"] else "?"
        rows.append(
            f"| {t['date_close']} | {t['ticker']} | {t['direction']} "
            f"| {entry_str} | {exit_str} | {size_str} | {r_str} | {wl} |"
        )

    table = "\n".join(rows) if rows else "| — | — | — | — | — | — | — | — |"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# Paper Trading Stats Dashboard
*Updated: {now} | คำนวณอัตโนมัติจาก `scripts/stats-paper-trade.py`*

---

## Phase Status

{phase_status}

| Metric | ค่าปัจจุบัน | เป้าหมาย | ผ่าน? |
|---|---|---|---|
| Trades ทั้งหมด | {total} | ≥{TARGET_TRADES} | {"✅" if meets_trades else "❌"} |
| Win rate (อัตราชนะ) | {win_rate}% | ≥{TARGET_WIN_RATE}% | {"✅" if meets_wr else "❌"} |
| Avg R-multiple (คุณภาพ trade เฉลี่ย) | {avg_r} R | ≥{TARGET_R} R | {"✅" if meets_r else "❌"} |
| Total P/L (กำไรขาดทุนสมมติ) | ${total_pnl:+,.0f} | — | — |
| Wins / Losses / B/E | {wins}W / {losses}L / {breakevens}B | — | — |

*ต้องผ่านทั้ง 3 metric พร้อมกัน (AND ไม่ใช่ OR) และต้อง ≥{TARGET_TRADES} trades ก่อนประเมิน*

---

## Trade Log

| วันปิด | Ticker | Dir | Entry | Exit | Size | R | W/L |
|---|---|---|---|---|---|---|---|
{table}

---

## วิธีใช้

1. Copy `vault/_templates/paper-trade-template.md`
   → บันทึกเป็น `vault/20_investment/_journal/trades/YYYY-MM-DD-TICKER.md`
2. กรอก frontmatter (บรรทัดบน): ticker, direction, entry, stop, size, date_open
3. ตอนปิด trade: กรอก exit, date_close, แล้วเปลี่ยน status → closed
4. รัน script: `python scripts/stats-paper-trade.py`
   → ไฟล์นี้อัปเดตอัตโนมัติ

**R-multiple คืออะไร:**
`R = (ราคาออก − ราคาเข้า) ÷ (ราคาเข้า − stop loss)` สำหรับ long
- R = +1.5 หมายความว่าได้กำไร 1.5 เท่าของความเสี่ยงที่รับ
- R = −1.0 หมายความว่าเสียเท่ากับที่ตั้ง stop ไว้พอดี
"""

    STATS_FILE.write_text(content, encoding="utf-8")
    print(f"Stats updated → {STATS_FILE.relative_to(ROOT)}")
    print(f"  Trades: {total} | Win rate: {win_rate}% | Avg R: {avg_r} | P/L: ${total_pnl:+,.0f}")
    print(f"  {phase_status}")


if __name__ == "__main__":
    main()
