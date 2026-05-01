---
description: Weekly market review — ดึงข้อมูลตลาดรายสัปดาห์, sector rotation, key events, earnings. ไม่ต้องมี daily pre/post files. รันทุกต้นสัปดาห์หรือเมื่อต้องการ.
---

# /weekly-market

Weekly market data review แบบ standalone — ไม่ต้องมี daily pre/post market files. บันทึก market performance, sector rotation, key events ของสัปดาห์ และ observations สำหรับสัปดาห์ถัดไป.

## Usage

```
/weekly-market [YYYY-Www]
```

- Argument เป็น ISO week format (เช่น `2026-W18`)
- ถ้าไม่ระบุ → default คือ **สัปดาห์ที่แล้ว** (Mon–Fri ที่เพิ่งปิด)
- ตัวอย่าง: `/weekly-market 2026-W17`

---

## Steps

### 1. Resolve target week

ถ้าไม่มี argument — หา date range ของสัปดาห์ที่แล้ว:

```bash
# หา Monday และ Friday ของสัปดาห์ที่เพิ่งปิด (last completed Mon-Fri)
python -c "
from datetime import date, timedelta
today = date.today()
wd = today.weekday()  # 0=Mon, 5=Sat, 6=Sun
# ถ้า Sat(5) หรือ Sun(6) → สัปดาห์ที่เพิ่งปิดคือสัปดาห์ปัจจุบัน (Mon ของสัปดาห์นี้)
# ถ้า Mon-Fri → สัปดาห์ที่เพิ่งปิดคือสัปดาห์ก่อนหน้า
if wd >= 5:
    last_monday = today - timedelta(days=wd)
else:
    last_monday = today - timedelta(days=wd + 7)
last_friday = last_monday + timedelta(days=4)
week_num = last_monday.isocalendar()[1]
print(f'{last_monday.year}-W{week_num:02d}')
print(f'{last_monday} to {last_friday}')
"
```

แสดง: `Target week: YYYY-Www (YYYY-MM-DD to YYYY-MM-DD)`

### 2. Check overwrite

ถ้า `vault/20_investment/_journal/<week>-weekly-market.md` มีอยู่แล้ว → หยุดและถาม:
> ⚠️ พบ `<week>-weekly-market.md` อยู่แล้ว — overwrite? (y/n)

ถ้า n → จบโดยไม่แตะไฟล์

### 3. Check existing daily reviews (optional context)

ลองอ่าน daily review files ของสัปดาห์นั้น (ถ้ามี) — **read-only:**

```
vault/20_investment/_journal/<YYYY-MM-DD>-review.md  (วันจันทร์–ศุกร์)
```

ถ้าพบ → ใช้เป็น context เพิ่มเติม (อย่า re-summarize, แค่ extract key points)
ถ้าไม่พบ → ดำเนินต่อได้ปกติ ไม่ต้องแจ้ง

### 4. Fetch weekly market data

Fire searches **in parallel:**

**Search queries:**
- `S&P 500 Nasdaq Dow Jones weekly performance <WEEK> <YEAR> stock market`
- `VIX weekly close high low <WEEK> <YEAR>`
- `XLE XLK XLP XLU XLY GLD TLT weekly performance <WEEK> <YEAR>`
- `Brent WTI crude oil weekly change <WEEK> <YEAR>`
- `US 10-year Treasury yield weekly change <WEEK> <YEAR>`
- `key market events earnings results week of <START_DATE>`

**Data to collect:**

| Metric | Target |
|---|---|
| S&P 500 | weekly open, close, % change, high, low |
| Nasdaq-100 | weekly close, % change |
| Dow Jones | weekly close, % change |
| Russell 2000 | weekly close, % change |
| VIX | weekly close + intraday high |
| XLE, XLK, XLP, XLU, XLY | % change each |
| GLD, TLT | % change each |
| US 10Y yield | end of week level + weekly change |
| Brent crude | end of week close |
| WTI crude | end of week close |
| DXY (USD index) | end of week close + % change |

**Conflict rule:** ถ้า 2 sources ให้ค่าต่างกัน → flag ⚠️ CONFLICT แสดงทั้งสองค่า ไม่เลือกข้างใดข้างหนึ่ง

**ถ้าหาตัวเลขไม่ได้:** ใส่ `[unverified]` — ห้าม fabricate

### 5. Determine weekly regime

ใช้ S&P 500 weekly % change:
- > +1.5% → **Risk-On (Strong)**
- +0.3% ถึง +1.5% → **Risk-On (Mild)**
- -0.3% ถึง +0.3% → **Flat / Indecisive**
- -1.5% ถึง -0.3% → **Risk-Off (Mild)**
- < -1.5% → **Risk-Off (Strong)**

จากนั้น cross-check กับ:
- VIX ขึ้นหรือลง? (ยืนยันหรือขัดแย้ง regime)
- TLT ขึ้นหรือลง? (ยืนยัน risk-off หรือเปล่า)
- Sector rotation สอดคล้องกับ regime ไหม?

### 6. Identify best/worst sectors

จาก XLE, XLK, XLP, XLU, XLY:
- **Best 2 sectors:** ระบุ % change + เหตุผล 1 ประโยค
- **Worst 2 sectors:** ระบุ % change + เหตุผล 1 ประโยค
- **Rotation signal:** defensive (XLP, XLU outperform) vs cyclical (XLE, XLY outperform) — สรุป 1 ประโยค

### 7. Generate weekly review file

Save to `vault/20_investment/_journal/<week>-weekly-market.md`:

```markdown
# Weekly Market Review — YYYY-Www (DD Mon – DD Mon YYYY)
*Standalone weekly log | สร้างหลังตลาดปิดวันศุกร์ | ไม่ใช่คำแนะนำลงทุน*

---

## Weekly Regime

- **S&P 500:** [+/-X.XX%] → **[Risk-On Strong / Risk-On Mild / Flat / Risk-Off Mild / Risk-Off Strong]**
- **VIX:** [ขึ้น/ลง] จาก [X.X] → [X.X] → [ยืนยัน / ขัดแย้ง] regime
- **Bond (TLT):** [+/-X.XX%] → [Flight to safety / Risk appetite]
- **สรุป regime:** [1 ประโยค — เช่น "สัปดาห์ risk-off ชัดเจน driven by trade war escalation"]

---

## Index Performance

| Index | Weekly Close | Weekly % | Note |
|---|---|---|---|
| S&P 500 | | | |
| Nasdaq-100 | | | |
| Dow Jones | | | |
| Russell 2000 | | | |
| VIX (close / weekly high) | / | | |

---

## Sector Rotation

| Sector ETF | Weekly % | Signal |
|---|---|---|
| XLK (Tech) | | |
| XLE (Energy) | | |
| XLP (Consumer Staples) | | |
| XLU (Utilities) | | |
| XLY (Consumer Disc.) | | |

- **Best:** [sector] (+X.XX%) — [เหตุผล 1 ประโยค]
- **Worst:** [sector] (-X.XX%) — [เหตุผล 1 ประโยค]
- **Rotation signal:** [Defensive / Cyclical / Mixed — 1 ประโยค]

---

## Macro & Fixed Income

| Metric | End of Week | Weekly Change | Source |
|---|---|---|---|
| US 10Y Yield | | | |
| GLD | | | |
| TLT | | | |
| Brent Crude | | | |
| WTI Crude | | | |
| DXY (USD) | | | |

---

## Key Events This Week

[3-5 events/catalysts ที่ขับเคลื่อนตลาดสัปดาห์นี้ — ระบุวันที่ + ผลกระทบ]
1. [วัน] [Event] → [ผลกระทบจริง]
2. [วัน] [Event] → [ผลกระทบจริง]
3. [วัน] [Event] → [ผลกระทบจริง]

---

## Notable Earnings

[เฉพาะที่ move ตลาดหรือ sector จริง — ถ้าไม่มี → "ไม่มี earnings ที่ notable สัปดาห์นี้"]

| Ticker | EPS (actual vs est.) | After-hours move | Market impact |
|---|---|---|---|
| | | | |

---

## Key Observations

[3-5 observations ที่น่าจดจำของสัปดาห์ — pattern, anomaly, หรือ theme ที่เห็น]
1. [observation]
2. [observation]
3. [observation]

---

## Watch List for Next Week

[3 สิ่งที่ควรติดตามสัปดาห์หน้า — events, data releases, setups ที่กำลัง form]
1. [วัน / event ที่ต้องติดตาม]
2. [วัน / event ที่ต้องติดตาม]
3. [วัน / event ที่ต้องติดตาม]

---

## Sources

*[ระบุทุก source พร้อม URL]*
```

### 8. Append to OUTCOMES.md

Append 1 line ใต้ section `## Weekly Market Log` ใน `vault/_memory/OUTCOMES.md`:

```
<week> — Regime: <X>, S&P <+/-X%>, Best sector: <X>, Worst: <X>, Key event: <Z>
```

ถ้า section `## Weekly Market Log` ยังไม่มี → append section header ก่อน แล้วค่อย append entry

### 9. Print summary + personal note prompt

แสดงให้ user:

```
Weekly market review saved: vault/20_investment/_journal/<week>-weekly-market.md

Regime: [Risk-On/Off + strength]
S&P 500: [+/-X%] | VIX: [level]
Best sector: [X] | Worst: [X]
Next week watch: [top 1 item]
```

จากนั้นถาม:
> **อยาก add note ส่วนตัวลง OUTCOMES ก่อน save? (y/n)**

ถ้า y → รอ user พิมพ์ note → append ต่อท้าย entry:
`... | Note: <user input>`

ถ้า n → จบ

---

## Constraints

- **ทุก market data ต้อง verify จาก source** — flag conflicts, ใส่ `[unverified]` ถ้าหาไม่เจอ
- **ห้าม fabricate ตัวเลข** — ถ้าไม่มีข้อมูลให้ใส่ [unverified]
- **Warn ก่อน overwrite** — ถ้า `<week>-weekly-market.md` มีอยู่แล้วต้องถามก่อนเสมอ
- **Token budget:** ~4K tokens
- **ห้าม re-summarize daily reviews** — ถ้ามี daily files ให้ extract key points เท่านั้น

## Anti-patterns

- ❌ ตัดสิน regime ด้วย "รู้สึก" — ใช้ S&P 500 % change ตาม threshold ที่กำหนดเสมอ
- ❌ Skip OUTCOMES.md append — ทุก review ต้อง append ทุกครั้ง
- ❌ Overwrite โดยไม่ warn — ต้องถามก่อนเสมอ
- ❌ Fabricate earnings data — ถ้าหาไม่ได้ = [unverified]
- ❌ ข้าม Watch List section — ต้องระบุเสมอ แม้จะบอกว่า "ยังไม่มีข้อมูล"
