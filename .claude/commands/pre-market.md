---
description: US pre-market brief with live data — futures, VIX, 10Y, oil, scenario playbook, risk framework, trade setups (educational). Use only on days planning to trade US markets.
---

# /pre-market

Produce a verified pre-market brief for US trading. All numbers must come from live searches — never use recalled data without re-verifying.

## Language

**เขียน brief เป็นภาษาไทยทั้งหมด** — ยกเว้น:
- ชื่อ ticker / index (S&P 500, VIX, XLE ฯลฯ) — ใช้ภาษาอังกฤษตามเดิม
- ตัวเลขและหน่วย ($, %, bps) — ใช้ตัวเลขอังกฤษตามเดิม
- DISCLAIMER ในส่วน Trade Setups — ใช้ภาษาอังกฤษทั้งหมด (ข้อกำหนดทางกฎหมาย)
- source URLs — ใช้ภาษาอังกฤษตามเดิม

**กฎภาษาสำหรับมือใหม่ (บังคับทุก section):**
- ทุกครั้งที่ใช้คำเทคนิค ให้อธิบายวงเล็บสั้นๆ ครั้งแรกที่ปรากฏ เช่น: VIX (ดัชนีความกลัวตลาด — ยิ่งสูงยิ่งตื่นตระหนก), Futures (ราคาที่ตลาดคาดก่อนเปิดจริง), Yield (ผลตอบแทนพันธบัตรรัฐบาล — สูง = ดอกเบี้ยแพง), Brent/WTI (ราคาน้ำมันดิบ), DXY (ดัชนีความแข็งค่าของดอลลาร์)
- อธิบาย "ตัวเลขนี้หมายความว่าอะไรในทางปฏิบัติ" ไม่ใช่แค่รายงานตัวเลข
- ห้ามใช้คำเทคนิคแบบ bare เช่น "institutional buying" หรือ "momentum confirmation" โดยไม่มีคำอธิบายภาษาธรรมดากำกับ

## When invoked

- Manually via `/pre-market` in Claude Code
- Use only on days planning to trade US markets (heavier than /daily-brief)

## Distinction from /daily-brief

| | /daily-brief | /pre-market |
|---|---|---|
| Frequency | Every day | Trading days only |
| Data source | Vault-only | Live web fetch |
| Weight | Lean (≤400 words) | Full brief (~800 words) |
| Purpose | Task focus | Market readiness |

---

## Steps

### 0. Get correct weekday (ALWAYS first)

Run this bash command before writing anything — never guess the day of week:

```bash
date '+%A %Y-%m-%d'
```

Map English → Thai: Monday=วันจันทร์, Tuesday=วันอังคาร, Wednesday=วันพุธ, Thursday=วันพฤหัสบดี, Friday=วันศุกร์

Use the output for the brief header: `# Pre-Market Brief — YYYY-MM-DD (วัน__)`

### 0.5 Surface yesterday's lessons (read-only, skip if not found)

ลอง read: `vault/20_investment/_journal/<yesterday>-review.md` (yesterday = `date -d "yesterday" '+%Y-%m-%d'`)
- ถ้าพบ → extract section "Lessons for Next Brief" → แสดงก่อนเริ่ม brief:
  ```
  📋 Lessons from [yesterday]: [lesson 1] | [lesson 2] | [lesson 3]
  ```
- ถ้าไม่พบ → skip โดยไม่แจ้ง

### 1. Fetch live news data in parallel

Macro numbers (futures, VIX, yields, oil, gold, DXY) come from Step 1.5 scripts — only news and sentiment need web searches here.

**Search queries (run all at once):**
- `overnight news market catalyst [TODAY'S DATE] earnings Fed geopolitical oil` — **fallback only** ถ้า news-snapshot.py ทำงาน ให้ข้ามข้อนี้ ประหยัด 1 search slot
- `Polymarket prediction markets stocks S&P 500 [TODAY'S DATE] sentiment odds`
- If barometer earnings today: `[TICKER] earnings [TODAY'S DATE] results EPS`

**WebFetch (fallback only — use if Step 1.5 scripts fail):**
- `https://finance.yahoo.com/markets/stocks/live/` — extract futures, VIX, key numbers
- Note: CNBC pre-markets returns 403 — skip, use search instead

**Sources to prioritize (in order of trust for macro data):**
1. `macro-snapshot.py` output (Alpaca ETF proxies + direct HTTP oil + yfinance) — primary for futures, VIX, yields, oil (WTI/Brent direct), gold, DXY
2. Yahoo Finance live article — fallback only if scripts unavailable
3. CNBC live updates article
4. Bloomberg Markets
5. Trading Economics (yields, VIX history)
6. Benzinga / Polymarket (sentiment only)

### 1.5 Run Alpaca scripts (parallel with searches)

While web searches are running, execute all three in parallel:

```bash
code/python/.venv/Scripts/python scripts/macro-snapshot.py
code/python/.venv/Scripts/python scripts/news-snapshot.py
code/python/.venv/Scripts/python scripts/sr-levels.py SPY QQQM NVDA AMD MU AVGO PLTR
code/python/.venv/Scripts/python scripts/universe-screen.py
```

`universe-screen.py` สแกนหา MU pattern (gap>=2% + vol>=1.5x + above MA20 + RSI 45-70) ใน universe ทุกวัน — output แสดงใน "Sector Universe Radar" section ด้านล่าง

เพิ่ม SMCI MRVL ARM ใน sr-levels ถ้ามีข่าว/catalyst วันนั้น:

```bash
code/python/.venv/Scripts/python scripts/sr-levels.py SPY QQQM NVDA AMD MU AVGO PLTR SMCI MRVL
```

**How to use the output:**
- `macro-snapshot.py` → embeds into "Alpaca Macro Snapshot" section; use to cross-check VIX proxy (VXX), oil (USO), dollar (UUP), bonds (TLT) against web search results. If web and Alpaca conflict, flag ⚠️ CONFLICT as usual.
- `news-snapshot.py` → embeds into "Alpaca News Snapshot" section; **replaces the overnight news search** — use Geopolitical / Fed / Earnings sections directly to populate Catalyst section. Only run the overnight news web search if news-snapshot fails.
- `sr-levels.py` → embeds into "Key S/R Levels" section; use to populate trigger/stop/target prices in Trade Setups.

If any script fails, note `[unavailable]` and continue without it.

### 2. Verify and flag conflicts

For every data point, note the source. If two sources give different numbers for the same metric:

- Mark with **⚠️ CONFLICT**
- Show both values and sources
- State the likely reason (timestamp difference, contract month, data lag)
- Do NOT average or pick one — show both and let user decide

Metrics that commonly conflict:
- Brent crude (spot vs front-month futures)
- VIX (prior close vs pre-market reading)
- Futures % change (different timestamps)

If a number cannot be verified from any live source today, write: `[unverified — last confirmed: DATE, VALUE]`

**DXY fallback (ห้ามข้ามไป [unverified] โดยตรง):** ถ้า DXY live ไม่ได้จาก search → ลอง fetch proxy ก่อนเสมอ:
1. Search: `DX-Y.NYB dollar index [TODAY'S DATE]` (ICE Dollar Index futures)
2. Search: `UUP ETF price [TODAY'S DATE]` (Invesco DB US Dollar Bullish Fund — proxy ที่ดี)
3. ถ้าทั้งสองไม่ได้ → ค่อยระบุ `[unverified]` พร้อมบอกว่าลอง proxy แล้ว

### 3. Generate brief

---

```markdown
# Pre-Market Brief — YYYY-MM-DD (วัน)
*ดึงข้อมูลสดทุกตัวเลข ระบุ source ทุกจุด ขัดแย้งระหว่าง source แสดงชัดเจน*

## 📊 ภาพรวมวันนี้ (อ่านก่อน — สำหรับมือใหม่)

> [เขียน 3-4 ประโยคภาษาธรรมดา ไม่มีคำเทคนิค อธิบายว่าวันนี้ตลาดเป็นยังไง อารมณ์ตลาดเป็นอย่างไร และมีอะไรสำคัญที่ต้องรู้ก่อนตัดสินใจใดๆ ตัวอย่าง: "วันนี้ตลาดหุ้นอเมริกามีแนวโน้มเปิดทรงตัว นักลงทุนกำลังรอดูผลประชุมธนาคารกลาง (Fed) ที่จะออกพรุ่งนี้ ราคาน้ำมันยังสูงจากความขัดแย้งในตะวันออกกลาง ความเสี่ยงหลักวันนี้คือข่าวที่อาจออกมาไม่คาด"]

## Futures

| Index | ระดับ | เปลี่ยนแปลง | Source |
|---|---|---|---|
| S&P 500 (ES=F) | | | |
| Nasdaq-100 (NQ=F) | | | |
| Dow Jones (YM=F) | | | |
| Russell 2000 (RTY=F) | | | |

**Gap Analysis — เปรียบ cash open vs futures direction (ระบุทุกครั้งที่ diverge):**
- Cash open ↑ + Futures ↓ pre-market → สัญญาณ institutional buying (ซื้อขัดกับ futures weakness)
- Cash open ↓ + Futures ↑ pre-market → สัญญาณ distribution (ขายขัดกับ futures strength)
- Cash และ Futures ชี้ทิศทางเดียวกัน → momentum confirmation — ไม่ต้องอธิบายพิเศษ
- ถ้าไม่ diverge: ระบุ "ไม่มี gap — futures และ cash สอดคล้องกัน"

## ตัวชี้วัด Macro

| ตัวชี้วัด | ค่า | ความหมายในทางปฏิบัติ | Source |
|---|---|---|---|
| VIX (ดัชนีความกลัว) | | [ตัวเลขนี้บอกอะไร เช่น "18 = ตลาดค่อนข้างสบายใจ ยังไม่ตื่นตระหนก"] | |
| 10Y Yield (ดอกเบี้ยพันธบัตร 10 ปี) | | [เช่น "4.3% = ดอกเบี้ยสูง กดดันหุ้นกลุ่มเติบโต"] | |
| WTI (น้ำมันดิบสหรัฐ) | | [เช่น "$95 = น้ำมันแพง เพิ่มต้นทุนธุรกิจ"] | |
| Brent (น้ำมันดิบโลก) | | ⚠️ ถ้า conflict | |
| Gold (ทองคำ) | | [เช่น "สูง = นักลงทุนหนีความเสี่ยง"] | |
| DXY (ดัชนีดอลลาร์) | | [เช่น "แข็งค่า = กดหุ้นตลาดเกิดใหม่"] | |

## Alpaca Macro Snapshot

[วาง output จาก `scripts/macro-snapshot.py` ตรงนี้]

*ถ้า script ไม่ได้รัน: `[macro-snapshot unavailable]`*

## Alpaca News Snapshot

[วาง output จาก `scripts/news-snapshot.py` ตรงนี้]

*ถ้า script ไม่ได้รัน: `[news-snapshot unavailable — ใช้ overnight news search แทน]`*

## ⚠️ ข้อมูลขัดแย้งที่พบ
(ระบุทุกจุด — รวม conflict ระหว่าง Alpaca ETF proxies กับ web sources — ถ้าไม่มี: "ไม่พบข้อมูลขัดแย้งระหว่าง source")

## Catalyst คืนที่ผ่านมา
- สรุป 3-5 ประเด็นหลักที่ขับเคลื่อนตลาดคืนนี้
- ต้องมีเสมอ: geopolitical, Fed/macro, earnings ที่ประกาศล่วงหน้า
- **Geopolitical ต้องใช้ format นี้เสมอ (ห้าม free-form):**
  `- **Geopolitical:** [สรุปเหตุการณ์] → ผลกระทบ: [oil / USD / defense / safe haven / ไม่มีนัยต่อตลาด] → magnitude: [ต่ำ/กลาง/สูง]`
  ถ้าไม่มีเหตุการณ์ geopolitical ที่กระทบตลาด → ระบุ: `- **Geopolitical:** ไม่มีเหตุการณ์ใหม่ที่กระทบตลาด`

## Polymarket Sentiment (อ้างอิงเท่านั้น)
*ค้นหา active markets ที่เกี่ยวข้องกับวันนี้จริงๆ — ไม่ hardcode คำถาม เพราะ Polymarket สร้าง market ใหม่แต่ละวัน*

| ตลาด / คำถาม | Odds raw | Odds adjusted | เปลี่ยนจากวาน | หมายเหตุ |
|---|---|---|---|---|
| [active market เกี่ยวกับ SPX/market direction วันนี้ — ถ้ามี] | | | | |
| [active market เรื่อง Fed / geopolitical / earnings ที่เกี่ยวข้อง — ถ้ามี] | | | | |

*Yes-bias correction (Reichenbach & Walther 2025): Polymarket มี systematic over-trade "Yes" — ปรับ `Odds adjusted = Odds raw − 3%` สำหรับทุก Yes/No market ก่อนนำไปใช้*
*Polymarket = crowd sentiment proxy เท่านั้น — ไม่ใช่การพยากรณ์ที่แม่นยำ ใช้เป็น sanity check กับ base scenario*
*ถ้าหา Polymarket data ไม่ได้: ระบุ `[unverified]` และ skip section นี้*

## Earnings วันนี้
ระบุ ticker พร้อม EPS คาด vs ปีก่อน — โน้ตหุ้นที่เคลื่อนไหวก่อนตลาดเปิด

## ปฏิทินสัปดาห์นี้
กิจกรรมสำคัญ (FOMC, CPI, earnings หลัก) — ไม่เกิน 5 bullet

---

## Sector Universe Radar — Semicon / AI / Datacenter

[วาง output จาก `scripts/universe-screen.py` ตรงนี้]

*ถ้า script ไม่ได้รัน: `[universe-screen unavailable]`*

**สรุปจาก radar:**
- **[ALERT] ตัวที่วิ่งแบบ MU:** [ticker list จาก ALERT section ของ script — ถ้าไม่มี: "ไม่มีวันนี้"]
- **[WATCH] ติดตาม:** [ticker list จาก WATCH section]
- **Catalyst หลัก:** [ดึงจาก news-snapshot + ผูกกับ ticker ที่ ALERT]

→ ใช้ตัวที่ **[ALERT]** เป็น candidate หลักสำหรับ Trade Setups ด้านล่าง
→ ถ้าไม่มี ALERT → เช็ค [WATCH] ว่า criteria ที่ขาดจะ trigger ได้ไหมในวันนี้
→ ถ้าไม่มีทั้ง ALERT และ WATCH → ระบุ "ไม่มี setup ชัดเจนในวันนี้" ห้ามสร้าง setup ฝืน

---

## Scenario Playbook

สามสถานการณ์สำหรับวันนี้ — ไม่ใช่การพยากรณ์ แต่เป็นกรอบเตรียมรับมือ

### กรณี Bullish (ตลาดขึ้น)
- **Trigger:** [อะไรต้องเกิดขึ้นให้ scenario นี้เป็นจริง]
- **Sectors ที่ได้ประโยชน์:** [พร้อมอธิบายสั้นว่าทำไม เช่น "XLE (พลังงาน) — เพราะราคาน้ำมันสูง"]
- **Sectors ที่เสียประโยชน์:** [พร้อมเหตุผลสั้น]
- **ตัวชี้วัดที่ต้องดู:** [2-3 ตัว พร้อมระดับที่สำคัญ]
- **สรุปสำหรับมือใหม่:** [1 ประโยค ถ้าเกิด scenario นี้ หมายความว่าอะไรในภาพรวม เช่น "ตลาดกลับมามีความหวัง นักลงทุนกล้าซื้อหุ้นเติบโตอีกครั้ง"]

### กรณี Base (น่าจะเป็นไปได้สุด — ตลาดทรงตัว)
- **Trigger:** [สภาวะปัจจุบันดำเนินต่อไป]
- **Sectors ที่ได้ประโยชน์:** [พร้อมเหตุผลสั้น]
- **Sectors ที่เสียประโยชน์:** [พร้อมเหตุผลสั้น]
- **ตัวชี้วัดที่ต้องดู:**
- **สรุปสำหรับมือใหม่:** [1 ประโยค เช่น "ตลาดรอข่าว ยังไม่มีทิศทางชัด เหมาะสำหรับนั่งดูก่อนมากกว่าลงมือ"]

### กรณี Bearish (ตลาดลง)
- **Trigger:** [อะไรทำให้สมมติฐานปัจจุบันพัง]
- **Sectors ที่ได้ประโยชน์:** [สินทรัพย์ปลอดภัย เช่น ทอง พันธบัตร และเหตุผล]
- **Sectors ที่เสียประโยชน์:** [พร้อมเหตุผลสั้น]
- **ตัวชี้วัดที่ต้องดู:**
- **สรุปสำหรับมือใหม่:** [1 ประโยค เช่น "ถ้าเกิดขึ้น ควรระวังและลดความเสี่ยง อย่าเพิ่งซื้อเพิ่ม"]

### Most Likely Scenario

- **เลือก:** [Bullish / Base / Bearish] — ห้ามตอบ "ไม่แน่ใจ" หรือ "50/50"

**Event Risk Check — ทำก่อนเลือก confidence:**
นับ active event risks วันนี้ (แต่ละข้อ = 1):
  - FOMC meeting หรือ Fed announcement / press conference
  - Earnings จาก Mag7 หรือ barometer stocks (KO, UPS, XOM ฯลฯ)
  - Geopolitical event ที่ยังไม่ resolved (สงคราม, sanctions, strait closure)
  - Major economic data release (NFP, CPI, GDP, PCE)
  - Major Fed speakers ที่ market-moving (Waller, Williams, Barkin ฯลฯ — ไม่นับถ้า routine speech)
→ **0-1 events → ดุลพินิจปกติ (low/medium/high)**
→ **2 events → confidence = medium สูงสุด ห้าม high**
→ **3+ events → confidence = low เสมอ ไม่มีข้อยกเว้น**
*(Lesson จาก 2026-04-28: 3 events พร้อมกัน FOMC + Mag7 + Iran → ควรเป็น low ไม่ใช่ medium)*

- **Confidence:** [low / medium / high]
- **เหตุผล 3 ข้อ:**
  1. [อ้างอิงจาก Macro / Futures data ใน brief นี้]
  2. [อ้างอิงจาก Catalyst / Polymarket ใน brief นี้]
  3. [อ้างอิงจาก Polymarket / Earnings / event calendar ใน brief นี้]
- **อะไรจะทำให้ผิด:**
  1. [event ที่ถ้าเกิดจะ flip scenario ทันที]
  2. [event ที่ถ้าเกิดจะ flip scenario ทันที]

*กฎ: ต้องเลือก 1 scenario เสมอ ไม่ hedge — ถ้า data ไม่พอให้ confidence = low แต่ยังต้องเลือก — เหตุผลต้อง derive จาก data ใน brief เดียวกันเท่านั้น ห้ามขัดแย้งกับ data ของตัวเอง*

---

## กรอบความเสี่ยง (Risk Framework)

### ความเสี่ยงสูงสุด 3 อันดับวันนี้ + Correlation Breakdown (probability × impact)

| อันดับ | ความเสี่ยง | โอกาสเกิด | ผลกระทบ | เครื่องมือป้องกัน (อ้างอิงเท่านั้น) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| ⚠️ | **Correlation breakdown** — oil↑ + Fed hawkish + earnings miss พร้อมกัน | ต่ำ แต่ tail risk | **สูงมาก** — defensive ไม่ช่วย | ถือ cash เท่านั้น; ลด position size ทุกประเภท |

> **หมายเหตุ Row ⚠️:** ในสถานการณ์ correlation breakdown ทุก asset class ร่วงพร้อมกัน (stocks + bonds + gold + defensives) เครื่องมือป้องกันปกติไม่ work — cash คือ hedge เดียวที่เชื่อถือได้

**เครื่องมือป้องกันความเสี่ยงทั่วไป** (อ้างอิงเท่านั้น — ไม่ใช่คำแนะนำให้ซื้อ):
- VIX สูง / tail risk: VIX calls, UVXY
- Yield พุ่ง: TLT puts, financials long
- Oil shock: XLE long, airlines/transports short
- USD แข็ง: EEM short, gold watch
- Broad selloff: หมุนเข้า defensive (XLU, XLV, XLP), ถือ cash

**Reminder เรื่องขนาด position:**
- VIX > 20: ลดขนาด position, ขยาย stop
- วัน event risk (FOMC, CPI, Mag7 earnings): พิจารณาลดขนาดก่อน แล้วรอ reaction
- VIX < 15: ระวัง complacency — อย่า over-leverage ตอนตลาดนิ่ง

---

## Key S/R Levels (จาก sr-levels.py)

*ใช้เป็น reference สำหรับกำหนด trigger / stop / target ใน Trade Setups ด้านล่าง*

[วาง output จาก `scripts/sr-levels.py` ตรงนี้ — pivot points + swing highs/lows ต่อ ticker]

*ถ้า script ไม่ได้รัน: `[sr-levels unavailable]`*

---

## Trade Setups (เพื่อการศึกษาเท่านั้น)

> **DISCLAIMER: The setups below are educational frameworks based on publicly available technical and fundamental data. They are NOT financial advice, NOT personalized recommendations, and NOT a solicitation to buy or sell any security. All trading involves risk of loss. Do your own research and consult a licensed advisor before making any investment decision.**

Setup ทุกอันใช้ logic แบบ IF-THEN — การเข้า position ขึ้นอยู่กับ trigger ไม่ใช่แน่นอนเสมอ

**กฎบังคับก่อนเขียน setup:**

1. **Forward-looking only** — ตรวจสอบว่า "ถ้า" condition ยังไม่เกิด ณ ตอนที่เขียน ถ้าเกิดแล้ว → skip setup นั้น เขียน setup ใหม่แทน
2. **Time horizon consistency** — ระยะเวลาใน body ต้องตรงกับ header:
   - Header = `Day` → body พูดถึงแค่ "วันนี้" เท่านั้น ห้ามพูด "สัปดาห์นี้"
   - Header = `Swing` → body พูดถึง "2-10 วัน" หรือ "สัปดาห์" ได้
   - Header = `Position` → body พูดถึง "หลายสัปดาห์/เดือน" ได้
3. **Event-driven setups ต้องใช้ post-event entry เสมอ** — ถ้า setup ขึ้นอยู่กับผล FOMC / earnings / macro release → "ถ้า" condition ต้องเป็น reaction หลัง event ออกแล้ว ไม่ใช่ positioning ก่อน เช่น: ✅ "ถ้า Powell ใช้ภาษา hawkish ใน press conference → แล้วค่อยดู TLT" ❌ "เข้า TLT ก่อน press conference เพราะคาดว่า dovish"
4. **Day setups ต้องมี time-stop** — "EOD" ไม่พอ ต้องระบุเวลาตัดสิน เช่น "ถ้าไม่เกิด trigger ภายใน 10:30am ET → setup void, ไม่เข้า" ถ้าเข้าแล้วและ trigger ไม่ confirm → ออกภายใน [เวลา] ไม่ hold ต่อ

### Setup 1 — [Ticker / Sector] | ระยะเวลา: [Day / Swing / Position]

**เหตุผล:** [หนึ่งประโยคอธิบายว่าทำไม setup นี้ถึงน่าสนใจ — technical + fundamental สอดคล้องกันอย่างไร]

- **ถ้า:** [เงื่อนไขเข้า — ระดับราคา, catalyst ยืนยัน, สัญญาณ volume]
- **แล้ว:** [ทิศทางที่คาดและช่วงเคลื่อนไหว]
- **ล้มเลิกถ้า:** [ระดับหรือเหตุการณ์ที่ทำให้ setup นี้ไม่ valid]
- **ระยะเวลา:** [Day trade (วันเดียว) / Swing (2-10 วัน) / Position (หลายสัปดาห์)]
- **Time-stop (Day เท่านั้น):** ถ้าไม่เกิด trigger ภายใน [เช่น 10:30am ET] → setup void ไม่เข้า; ถ้าเข้าแล้วและ thesis ไม่ confirm ภายใน [เช่น 12:00pm ET] → ออก
- **Catalyst สนับสนุน:** [เหตุการณ์ fundamental ที่หนุนหรือคุกคาม setup นี้]

### Setup 2 — [Ticker / Sector] | ระยะเวลา: [Day / Swing / Position]

- **ถ้า:**
- **แล้ว:**
- **ล้มเลิกถ้า:**
- **ระยะเวลา:**
- **Time-stop (Day เท่านั้น):** ถ้าไม่เกิด trigger ภายใน [เวลา ET] → setup void ไม่เข้า
- **Catalyst สนับสนุน:**

### Setup 3 — [Ticker / Sector] | ระยะเวลา: [Day / Swing / Position]

- **ถ้า:**
- **แล้ว:**
- **ล้มเลิกถ้า:**
- **ระยะเวลา:**
- **Time-stop (Day เท่านั้น):** ถ้าไม่เกิด trigger ภายใน [เวลา ET] → setup void ไม่เข้า
- **Catalyst สนับสนุน:**

---
*Sources: [ระบุทุก source พร้อม URL]*
```

---

### 4. Save

- Save to: `vault/20_investment/_journal/YYYY-MM-DD-premarket.md`
- ถ้าไฟล์มีอยู่แล้ว → ถาม user:
  > ⚠️ พบ `YYYY-MM-DD-premarket.md` อยู่แล้ว — overwrite? (y/n)
  ถ้า n → แสดง brief ใน chat แต่ไม่ save
- Show full brief in chat

### 5. Reporting

End with:
```
Brief saved to: vault/20_investment/_journal/YYYY-MM-DD-premarket.md
Searches used: X | WebFetch attempts: Y | Conflicts found: Z
Unverified data points: [list or "none"]
```

### 6. Decision Tree (opt-in)

After reporting, ask the user:

> **สร้าง decision tree ต่อเลยไหม? (y/n)** [default: y]

**ถ้า n:** จบ command — แค่ report path ของ brief ที่ save ไว้

**ถ้า y (หรือ user ไม่ตอบ / กด Enter):**

1. **ตรวจสอบไฟล์ก่อน:** ถ้า `vault/20_investment/_journal/YYYY-MM-DD-decision-tree.md` มีอยู่แล้ว → แจ้ง user:
   > ⚠️ พบไฟล์ `YYYY-MM-DD-decision-tree.md` อยู่แล้ว — จะ overwrite หรือไม่? (y/n)
   ถ้า user ตอบ n → จบโดยไม่แตะไฟล์นั้น

2. **สร้าง decision tree** โดยใช้ข้อมูลจาก brief ที่เพิ่งสร้าง (อ้างอิง Most Likely Scenario, Setups, Catalysts):

```markdown
# Pre-Trade Decision Tree — YYYY-MM-DD (วัน)
*อ้างอิงจาก [[YYYY-MM-DD-premarket]] | สร้างต่อจาก brief | ใช้ประกอบการตัดสินใจเท่านั้น ไม่ใช่คำแนะนำลงทุน*

---

> **Context วันนี้:** [VIX | S&P futures | Brent | events หลัก — ดึงจาก brief]
> **Most Likely Scenario: [Bullish/Base/Bearish]** — [เหตุผล 1 ประโยคจาก Most Likely Scenario ใน brief]
> **Risk Level:** [สรุป 1 ประโยค]

---

## Today's Plan ([Most Likely Scenario])

*5 actions สำหรับวันนี้ ถ้า scenario ยังเป็น [Most Likely]*

| # | Action |
|---|---|
| **1** | **[Setup 1 Ticker] — [เข้า/รอ/skip]:** [เงื่อนไขและ action จาก Setup 1 ใน brief] |
| **2** | **[Setup 2 Ticker] — [เข้า/รอ/skip]:** [เงื่อนไขและ action จาก Setup 2 ใน brief] |
| **3** | **[Setup 3 Ticker] — [เข้า/รอ/skip]:** [เงื่อนไขและ action จาก Setup 3 ใน brief] |
| **4** | **Cash buffer [ระดับ]%:** [เหตุผล] |
| **5** | **Time-of-day:** ไม่เข้า new position หลัง 3:00pm ET; หลีกเลี่ยง 11:30am–1:30pm ET (lunch lull) |

---

## Contingency Plans

### ถ้า flip → Bullish
**Triggers ที่ต้องเกิด (อย่างน้อย 2 ใน 3):**
- [trigger 1 — อิงจาก Bullish scenario ใน brief]
- [trigger 2]
- [trigger 3]

**ปรับ action:**
- [การเปลี่ยน Setup 1/2/3 ถ้า Bullish]
- Cash buffer ≥ [ระดับ]%

### ถ้า flip → Bearish
**Triggers ที่ต้องเกิด (อย่างน้อย 1 ใน 3):**
- [trigger 1 — อิงจาก Bearish scenario ใน brief]
- [trigger 2]
- [trigger 3]

**ปรับ action:**
- [การเปลี่ยน Setup 1/2/3 ถ้า Bearish]
- Cash buffer ≥ [ระดับ]%

---

## Pre-Commit Rules
*rules เหล่านี้ยอมรับล่วงหน้า — ถ้าเงื่อนไขเกิดขึ้น ให้ทำตามโดยไม่ต้องคิดใหม่*

**Circuit Breakers (ปิด position ก่อน):**
- `if VIX > 22` → close all positions, ถือ cash 100% ไม่มีข้อยกเว้น
- `if S&P 500 หลุด [support level จาก brief] intraday` → ลด total exposure 50% ทันที
- `if S&P + TLT + GLD ร่วงพร้อมกัน > 1% ใน 30 นาที` → exit ทุก position, cash 100% — correlation breakdown

**Setup Invalidation (ยกเลิก setup ทันที):**
- [invalidation condition จาก Setup 1 ใน brief]
- [invalidation condition จาก Setup 2 ใน brief]
- [invalidation condition จาก Setup 3 ใน brief]

**Earnings Signal:**
- [ถ้ามี earnings barometer วันนี้ เช่น KO+UPS miss → ลด position X%]

**Profit-Taking Rules:**
- [Setup 1 profit-take rule — อิงจาก Setup 1]
- [Setup 2 profit-take rule — อิงจาก Setup 2]
- [Setup 3 profit-take rule — อิงจาก Setup 3]

**Time-of-Day Rules:**
- `ห้ามเข้า new position หลัง 3:00pm ET`
- `11:30am–1:30pm ET (lunch lull)` → ไม่ใช่ entry time

**Event Day Protocol:**
- [ถ้ามี FOMC/CPI/earnings ใหญ่ระหว่างสัปดาห์ — ระบุ condition จาก brief]
- **FOMC 45-min rule (Boguth et al. 2023):** ห้าม chase ทิศทางแรกหลัง FOMC statement — initial move มักกลับตัวภายใน announcement cycle; รอ 45 นาทีให้ VIX settle แล้วดูทิศทางจริงก่อน entry; ถ้า pre-FOMC ขึ้นแรง → คาด reversal; ถ้า dissenting votes ≥ 3 → hawkish signal confirmed → TLT entry ได้หลัง 45 นาที

---

## Decision Confidence Check

*ทำก่อนปิด decision tree — ทุก checkbox ที่ check ต้องมี action เฉพาะ ห้าม vague*

- [ ] Today's Plan ชัดเจนทุก action → ไม่ต้อง council
- [ ] มี dilemma ระหว่าง setups (ไม่รู้จะเลือก Setup ไหน) → `/council <ระบุ dilemma เฉพาะ>`
- [ ] Position size รู้สึกผิดปกติ (ใหญ่เกิน VIX level / เล็กจน meaningless) → `/council --expertise=financial_risk`
- [ ] Setup ขัดกับ Most Likely Scenario (เช่น Long tech ทั้งที่ Most Likely = Bearish) → `/council ทำไม mismatch ระหว่าง [setup] กับ [scenario]`

---

> **DISCLAIMER: ตารางนี้เป็น educational framework เพื่อการวางแผนความคิดเท่านั้น ไม่ใช่คำแนะนำลงทุน ทุกการตัดสินใจขึ้นอยู่กับผู้อ่านแต่เพียงผู้เดียว การลงทุนมีความเสี่ยง**
```

3. **Save** to `vault/20_investment/_journal/YYYY-MM-DD-decision-tree.md`

4. **Report:**
```
Decision tree saved to: vault/20_investment/_journal/YYYY-MM-DD-decision-tree.md
```

---

## Constraints

- **Every number needs a source** — no exceptions. If unverifiable, say so.
- **Conflicts must be shown** — never silently pick one number over another.
- **Setups are IF-THEN, never "buy X"** — always conditional, always with invalidation.
- **Disclaimer must appear** before Trade Setups section verbatim — do not shorten.
- **No invented scenarios** — scenarios must be grounded in today's actual catalysts.
- **Token budget:** ~5K tokens for full task (heavier than /daily-brief by design)
- **Search cap:** 2 searches max (Polymarket + earnings) when news-snapshot.py runs successfully; 3 searches if it fails (add overnight news search as fallback)

## Anti-patterns

- ❌ "Based on my knowledge, the VIX is around..." — all numbers must be fetched today
- ❌ Picking one oil price when sources conflict — show both
- ❌ "You should buy X" — always IF-THEN, never imperative
- ❌ Omitting the DISCLAIMER before Trade Setups
- ❌ Running searches sequentially — always parallel
- ❌ Scenarios that don't tie to today's actual catalysts
- ❌ Trade setups without invalidation levels
- ❌ Guessing the weekday — always run `date` bash command first
- ❌ Setup "ถ้า" condition that has already been met — replace with a genuinely forward-looking setup
- ❌ Writing "สัปดาห์นี้" inside a setup labeled `Day` — time horizon must be consistent
- ❌ Omitting the correlation breakdown row (⚠️) from Risk Framework table
- ❌ ใช้คำเทคนิค (institutional buying, momentum, hawkish, dovish ฯลฯ) โดยไม่มีคำอธิบายภาษาธรรมดากำกับ
- ❌ รายงานตัวเลขโดยไม่บอกว่า "ตัวเลขนี้หมายความว่าอะไร" — ทุกตัวเลขต้องมี implication
- ❌ "เข้า TLT ก่อน press conference" — event-driven setups ต้องรอ event ออกก่อนเสมอ
- ❌ Day setup ที่ระบุแค่ "EOD" เป็น time-stop — ต้องระบุเวลาจริง เช่น "10:30am ET"
- ❌ เขียน [unverified] สำหรับ DXY โดยไม่ลอง DX-Y.NYB / UUP proxy ก่อน
- ❌ แสดง cash vs futures divergence โดยไม่อธิบาย implication (institutional buying / distribution)
