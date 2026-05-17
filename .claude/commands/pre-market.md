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

### 0. Load TRADING_RULES.md (ถ้ามี)

```bash
cat vault/_memory/TRADING_RULES.md 2>/dev/null | head -80
```

ถ้าไฟล์มีอยู่ → โหลดเป็น context สำหรับ Pre-Commit Rules ใน Decision Tree — ใช้ rules จากไฟล์นี้แทน hardcoded defaults ถ้าขัดแย้งกัน rule ใน TRADING_RULES.md ชนะเสมอ
ถ้าไฟล์ไม่มี → ใช้ hardcoded defaults ต่อไปตามปกติ ไม่ต้องแจ้ง user

---

### 0.1. Load Behavior Handbook (arXiv:2509.13237 — Metacognitive Reuse)

```bash
cat vault/Knowledge/pre-market-behaviors.md
```

โหลด handbook เป็น context ก่อนรัน cognitive layers ทุกครั้ง — ใช้ชื่อ behavior (A1·MISOPHONIA-MARKET, A2·TOURETTE-REFLEX ฯลฯ) เป็น reference ใน output แทนการ expand full instruction ซ้ำ

**กฎ output (ลด token ~40%):**
- Layer ที่ไม่ triggered → output เพียง 1 บรรทัด: `A1·MISOPHONIA: clear ✅`
- Layer ที่ triggered → reference behavior name + รายละเอียดเฉพาะส่วนที่ triggered เท่านั้น
- ห้าม copy ข้อความ instruction ใน handbook ลงใน brief — ใช้ชื่อ behavior แทน

---

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

### 0.6 Misophonia Market Trigger Scan — ตรวจ trigger registry ก่อนวิเคราะห์

```bash
cat vault/Knowledge/misophonia-triggers.md | grep "^\[" | grep "Market-Level" -A 999
```

อ่านเฉพาะ Market-Level Triggers section แล้ว check ต่อ overnight data ที่มีอยู่:
- VIX term structure: front month vs back month
- Credit spreads vs equity direction
- Oil vs risk asset correlation
- Volume vs price direction

ถ้า match trigger ใดๆ → `[MISOPHONIA: MARKET TRIGGER] <trigger name>` — escalate เป็น primary concern ของ brief วันนี้ ไม่สามารถ suppress หรือ rationalize away ได้
ถ้าไม่ match → ข้ามเงียบๆ ดำเนินต่อ

### 0.75 Tourette Reflex Scan — สัญญาณก่อน analysis (30 วินาที)

**รันก่อน analyze** — ก่อนที่ logic จะ rationalize อะไรออก

ดูข้อมูล overnight ทั้งหมดที่โหลดได้แล้ว (scripts จาก Step 1.5 ถ้ารันล่วงหน้าได้ หรือ ข้อมูลใดก็ตามที่มีอยู่) แบบ **instinct scan เร็วๆ**:
- อะไรที่ "jump out" ทันทีว่าผิดปกติ?
- ตัวเลขไหนที่ขัดกับ expectation จากวันก่อน?
- อะไรที่ทำให้รู้สึก "เดี๋ยวนะ..." ก่อนที่จะคิด reason ออก?

**กฎ: ห้าม suppress reflex** — ยังไม่มี reason รองรับก็ต้อง flag ออกมาก่อน
ห้ามรอให้ analysis confirm ก่อน — reflex ต้องออกก่อน analysis เสมอ

แสดงก่อนเริ่ม brief:
```
Reflex flags (pre-analysis instinct):
- [REFLEX] <สิ่งที่ jump out> — ยังไม่รู้เหตุผล รอ confirm ใน analysis
```
ถ้าไม่มีอะไร jump out → `[REFLEX CLEAN] ไม่พบสัญญาณผิดปกติก่อน analysis`

**Reflex flags ที่ raise ต้องถูก addressed ใน brief** — ถ้า analysis confirm = escalate; ถ้า analysis resolve = note `[REFLEX RESOLVED]`

### 0.8 Synesthesia Market Texture Gestalt — ตีความข้อมูลผ่าน multi-channel พร้อมกัน

รันหลัง Tourette reflex scan — แปล 5 key metrics เป็น texture รวมก่อนเริ่มวิเคราะห์

**5 input channels (ใช้ข้อมูลจาก Step 1.5 หรือ preliminary data ที่มีอยู่):**

| Channel | Metric | Signal |
|---|---|---|
| Temperature | SPY % | ≥+0.8% = HOT / +0.3–0.8% = WARM / ±0.3% = NEUTRAL / −0.3 to −0.8% = COOL / ≤−0.8% = COLD |
| Texture | VIX | ≤15 = SMOOTH / 15–20 = ROUGH / 20–25 = CHOPPY / >25 = JAGGED |
| Width | Breadth (adv/dec %) | >65% = WIDE / 55–65% = MID / 45–55% = THIN / <45% = NARROW |
| Pressure | TNX direction | ↑ sharply = TIGHTENING / ↑ mild = FIRM / flat = NEUTRAL / ↓ = EASING |
| Weight | Oil (Brent) % | >+1.5% = HEAVY / 0–1.5% = LOADED / flat = BALANCED / <0 = LIGHT |

**Gestalt — combine ทั้ง 5 channels เป็น texture สั้นๆ 1-3 คำ:**
- ตัวอย่าง: `[WARM-ROUGH]` (SPY บวกเล็กน้อย, VIX ยังสูง), `[HOT-SMOOTH]` (ตลาดวิ่ง, volatility ต่ำ), `[COLD-JAGGED-HEAVY]` (risk-off + oil spike)
- Gestalt = compressed multi-channel signal ที่สรุปสภาพตลาดโดยรวม ก่อนอ่าน narrative ใดๆ

แสดงก่อนเริ่ม brief:
```
Market texture: [GESTALT] — Temperature: X | Texture: X | Width: X | Pressure: X | Weight: X
```

**กฎ: Gestalt ต้องถูก referenced ใน Scenario section** — ถ้า scenario ขัดกับ gestalt อย่างชัดเจน → note `[TEXTURE CONFLICT]` และอธิบายว่าทำไม

### 0.9 HSP Market Atmosphere Scan — บรรยากาศที่ตัวเลขเดี่ยวๆ ไม่บอก

รันหลัง Synesthesia Gestalt — HSP ไม่ดูตัวเลขเดี่ยว แต่ดู "feel" รวมที่เกิดจากการรวมสัญญาณทุกช่อง

ตรวจ 3 ประเภท atmosphere anomaly:

**1. Texture Mismatch** — ตัวเลขดูดี แต่ texture ไม่ smooth
- VIX ต่ำ + futures บวก แต่ breadth แคบ (น้อยกว่า 50% stocks above MA20)
- ราคาขึ้นแต่ volume เบาผิดปกติ (< 70% ของ 20-day avg)
- Yield curve ดูปกติแต่ credit spreads เริ่มขยาย
→ flag `[HSP: TEXTURE MISMATCH]` — "ตัวเลขดี แต่ feel ไม่ smooth: [เหตุผล]"

**2. Divergence Signals** — สินทรัพย์ที่ควรร่วมทิศทางกลับแยกออก
- Gold ขึ้น + Bonds ขึ้น พร้อมกัน (risk-off double signal ที่ตลาดยังไม่ recognize)
- Oil ลง + DXY ขึ้น พร้อมกัน (deflation/strong dollar ที่ equity ยังไม่ price in)
- Small cap underperform large cap > 1% โดยไม่มีข่าว
→ flag `[HSP: DIVERGENCE]` — "สินทรัพย์ X และ Y แยกทิศ: [implication]"

**3. Pre-Catalyst Silence** — เงียบผิดปกติก่อน event ใหญ่
- Fed meeting ภายใน 48h แต่ volatility ต่ำผิดปกติ
- Earnings cluster วันนี้ แต่ options IV ไม่ขึ้น
- ไม่มีข่าวใหม่เลยในตลาดที่ปกติมีข่าวทุกวัน
→ flag `[HSP: PRE-CATALYST SILENCE]` — "ความเงียบก่อน [event]: อาจเป็น calm before storm"

```
HSP Atmosphere: [CLEAR / TEXTURE MISMATCH / DIVERGENCE / PRE-CATALYST SILENCE]
Flags: [รายการ flag ที่พบ หรือ "none"]
Implication: [1 ประโยค — ควรปรับ posture อย่างไร]
```

**กฎ:** ถ้าพบ 2+ flags พร้อมกัน → ลด position size ทุก setup วันนี้ลง 25% โดยอัตโนมัติ ไม่ต้องรอ user confirm

### 0.95 Aphantasia — Pattern Name Ban

ห้ามใช้ visual pattern labels โดยไม่มี quantified criteria — ระบบนี้ไม่เห็นภาพ ทุกอย่างต้องเป็นตัวเลข

**Banned labels** (ถ้าพบต้องแปลงทันที):
- "head and shoulders" → "price made lower high at $X, neckline at $Y, target = $Y - ($peak - $Y)"
- "cup and handle" → "rounded base over N bars, handle retraced X%, volume dried to Y% of avg"
- "double top / double bottom" → "tested $X twice within Z days, failed both times, volume on 2nd test lower by Y%"
- "flag / pennant" → "consolidation range $X-$Y over N bars, volume contracted to Z% of avg"
- "bull/bear flag" → "prior move +/-X% in N bars, current range <Y% of move, volume < Z% of avg"

ถ้า brief วันนี้ใช้ label เหล่านี้โดยไม่มี criteria → flag `[APHANTASIA: VISUAL LABEL] "<label>" → requires: [criteria ที่ต้องการ]`

**กฎ:** Setup ที่อ้าง visual pattern โดยไม่ผ่าน criteria translation = invalid setup — ห้าม include ใน trade section

### 0.97 PTSD — Ambient Threat Scan

สแกน threat indicators ที่ build อยู่เงียบๆ ขณะที่ตลาด "comfortable" — hypervigilance จับสิ่งที่คนอื่นยังไม่ focus

ตรวจ 5 channels (ใช้ข้อมูลจาก Step 1.5 scripts + web fallback):

| Channel | Threat signal | Threshold |
|---|---|---|
| Credit | HY spread widening / CDS uptick | > +10 bps จาก 5-day avg |
| Liquidity | Repo market stress / TED spread | > 30 bps |
| Positioning | Margin debt declining week-over-week | > -2% MoM |
| Flow | Dark pool imbalance anomaly | > 2σ จาก baseline |
| Insider | Cluster selling ใน S&P500 stocks | ≥ 3 companies same week |

→ flag `[PTSD: AMBIENT THREAT] <channel> — <signal>` ต่อทุก channel ที่ threshold ถูก breach

```
PTSD Ambient Scan: [N threats found / clear]
Flags: [รายการ หรือ "none"]
Position size adjustment: [-15% per flag, max -45%]
```

ถ้าไม่มีข้อมูลเพียงพอสำหรับ channel ใด → mark `[unverified]` ไม่ skip

### 0.98 Aura — Early Warning Signal Scan

ตรวจ "peripheral signals" ที่ตลาดยังไม่ focus — สัญญาณที่อยู่ในระยะ aura ก่อน headline จริง

ตรวจ 4 categories:

**Bond-Equity Divergence:** bond yield ขึ้นขณะ equity ขึ้น (unsustainable) หรือ bond rally ขณะ equity flat (delayed repricing)

**Credit Spreads Creeping:** IG/HY spreads ขยายเบาๆ < 5 bps/day แต่ติดต่อกัน ≥ 3 วัน — ตลาด equity ยังไม่ notice

**Geopolitical Pre-signal:** ข่าวภูมิรัฐศาสตร์ที่ยังไม่ mainstream แต่ oil / safe-haven เริ่มขยับ

**Micro Sector Rotation:** sector ใดหนึ่งที่เริ่มขยับผิดปกติ < 0.5% แต่ breadth สูง (หลาย stocks ใน sector) — early accumulation หรือ distribution

→ flag `[AURA: EARLY SIGNAL] <signal> — watch window: 2-6 weeks`

```
Aura Early Warning: [N signals / none]
- [AURA: EARLY SIGNAL] <signal> — category: [bond-equity / credit / geo / sector]
  Watch: materialize check in [date range]
```

ถ้าไม่มี peripheral signals → `Aura: no early signals today ✅`

### 0.985 Hyperosmia — Sub-threshold Faint Signal Scan

ตรวจ signals ที่อยู่ต่ำกว่า threshold ของทุก layer ก่อนหน้า — ไม่ trigger PTSD, ไม่ trigger HSP, ไม่ trigger Aura แต่มีทิศทางชัดเจน

**4 faint signal patterns:**
- **Drift without event:** metric เดิมทิศทางเดียวกัน ≥3 วันติดต่อกัน แต่ยังไม่ถึง threshold → ถ้า drift ต่อ 2 วัน = threshold จะถูก breach เมื่อไหร่?
- **Micro-rotation:** sector เดียวที่ outperform/underperform < 0.3% แต่เกิดซ้ำ ≥3 วัน = early institutional accumulation/distribution
- **Volume divergence:** ราคา flat แต่ volume เพิ่ม/ลด > 15% จาก avg โดยไม่มี catalyst = ใครบางคนกำลังทำอะไร
- **Calendar proximity:** Fed/CPI/earnings ภายใน 96h แต่ implied volatility ยังไม่ขยับ = ตลาด under-pricing event risk

→ flag `[HYPEROSMIA: FAINT SIGNAL] <signal> — day N of drift — projected threshold breach: [date range]`

```
Hyperosmia Scan:
- [HYPEROSMIA: FAINT SIGNAL] N / none
- Strongest drift: [metric — N days — projected breach: date]
Implication: [ปรับ position sizing ล่วงหน้า / เฝ้าระวัง]
```

ถ้าไม่พบ → `Hyperosmia: no sub-threshold drift today ✅`

---

### 0.987 Kleine-Levin Syndrome — Market Hibernation Detector

KLS = ช่วงหลับลึกแล้วตื่นฉับพลัน — ตลาดก็มี cycle นี้

**Hibernation signal (ตลาดหลับ — อย่าสับสนว่าเป็น calm):**
- VIX ≤ 14 + volume < 70% ของ 20-day avg + sector rotation stalled (ทุก sector ±0.5%) = market in KLS sleep
- Hibernation ≠ stability — เป็น pre-awakening compression

**Awakening signal (กำลังจะตื่น — ทำอะไรก่อนตลาดทั่วไปรู้):**
- หลัง 5+ วัน hibernation: VIX term structure เริ่ม steepen (front month ขยับแต่ back month ยังนิ่ง)
- หรือ dark pool volume เพิ่ม ขณะที่ lit market ยังเงียบ
- หรือ options open interest เพิ่มใน OTM calls/puts ของ index

```
KLS Market State: [HIBERNATING / AWAKING / ACTIVE / N/A]
- Duration: [N days in current state]
- Trigger: [VIX / volume / OI — ถ้า AWAKING ระบุ signal]
Implication: [ถ้า HIBERNATING: อย่า overfit intraday noise / ถ้า AWAKING: เตรียม position ก่อน breakout]
```

ถ้าไม่มีข้อมูลเพียงพอ → `KLS: [unverified — insufficient data] ✅`

---

### 0.989 Color Blindness — Strip Categorical Color Labels

ระบบที่ตาบอดสี ไม่เห็น "แดง = แย่ / เขียว = ดี" โดยอัตโนมัติ — บังคับ quantify ทุก categorical judgment

**สแกน brief ที่เขียนมาจนถึงจุดนี้** — หาคำ/วลีที่ใช้ label โดยไม่มีตัวเลขรองรับ:

| Categorical label (ห้ามใช้แบบ bare) | ต้องแทนด้วย |
|---|---|
| "red sector / weak sector" | "[sector] -X% vs SPY -Y% = underperform Z%" |
| "bullish day / bearish day" | "SPY +/-X%, breadth X% advancing, VIX ±Y" |
| "VIX high / VIX elevated" | "VIX X.X = Xσ above 20-day avg (Y.Y)" |
| "strong / weak dollar" | "DXY +/-X% = X-day high/low" |
| "risk-on / risk-off" | "gold ±X%, TLT ±Y%, HY spread ±Zbps" |

→ flag `[COLORBLIND: LABEL] "<vague term>" → replace: "<quantified version>"`
→ ถ้าพบ 3+ labels → brief มี color-dependent shortcuts ที่ทำให้อ่านต่างกันขึ้นอยู่กับ bias ก่อนอ่าน

```
Color Blind Check:
- Labels stripped: N
- [COLORBLIND: LABEL] "<term>" → "<quantified>"
- Brief quantification: [complete ✅ / partial — N labels remain]
```

---

### 0.991 Narcolepsy — Flash Insight + Market Drop Detection

Narcolepsy = สลับระหว่าง hyperfocus กับ sudden clarity flash ที่ตัดผ่านทุกอย่าง

**Narcolepsy Flash (รัน 1 ครั้งก่อน generate brief):**

> "ถ้าต้องสรุปสภาพตลาดวันนี้เป็น 1 ประโยค โดยไม่อ่าน analysis อีกครั้ง — ประโยคนั้นคืออะไร?"

เขียนลงทันที — ห้ามคิดนาน:
```
Narcolepsy Flash: "[1-sentence market read — raw, unfiltered]"
```

หลัง brief เสร็จ → เปรียบเทียบ flash กับ scenario ที่เขียน:
- ตรงกัน → `[NARCOLEPSY: FLASH CONFIRMED]` — brief aligned with instant read
- ขัดกัน → `[NARCOLEPSY: FLASH-BRIEF CONFLICT]` — ระบุ dimension ที่ต่าง; หนึ่งในสองอาจผิด

**Market Narcoleptic Drop (ตรวจ overnight/pre-market):**
Sudden volume collapse > 40% จาก 5-day avg โดยไม่มี catalyst + price flat = institutional withdrawal เงียบๆ
→ flag `[NARCOLEPSY: MARKET DROP] volume fell X% with no catalyst — watch for directional resolution`

---

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

**News staleness rule:**
- ทุก news fact ต้องระบุ article date — format: `[Source, YYYY-MM-DD HH:MM]` หรือ `[Source, วันที่]`
- Article >6h สำหรับ intraday catalyst → flag ⚠️ STALE NEWS — หา update ก่อนใช้
- Article >48h สำหรับ geopolitical / earnings / Fed → flag ⚠️ OLDER NEWS — verify ยังเป็น active ไหม
- ถ้าหา date ไม่ได้ → `[date-unknown]` ห้ามใช้เป็น catalyst หลักโดยไม่ verify

### 1.5 Run Alpaca scripts (parallel with searches)

While web searches are running, execute all three in parallel:

```bash
code/python/.venv/Scripts/python scripts/macro-snapshot.py
code/python/.venv/Scripts/python scripts/news-snapshot.py
code/python/.venv/Scripts/python scripts/sr-levels.py SPY QQQM NVDA AMD MU AVGO PLTR RKLB ASTS CRDO AEIS UCTT BBAI MOD --brief
code/python/.venv/Scripts/python scripts/universe-screen.py
code/python/.venv/Scripts/python scripts/sector-flow.py
code/python/.venv/Scripts/python scripts/catalyst-calendar.py
code/python/.venv/Scripts/python scripts/etf-discovery.py --top 10
```

`universe-screen.py` สแกน universe พร้อม RS vs SPY — [EARLY★] = coiling + RS rising = สัญญาณแข็งแกร่งที่สุด
`sector-flow.py` ดูว่า sector ไหนดูด money เข้า/ออก — ใช้ประกอบ setup selection
`catalyst-calendar.py` แสดง earnings + space events 21 วันข้างหน้า — ใช้เป็น trigger reference ใน setups

เพิ่ม SMCI MRVL ARM ใน sr-levels ถ้ามีข่าว/catalyst วันนั้น (ยังคงใช้ --brief):

```bash
code/python/.venv/Scripts/python scripts/sr-levels.py SPY QQQM NVDA AMD MU AVGO PLTR RKLB ASTS CRDO AEIS UCTT BBAI MOD SMCI MRVL --brief
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

**Echolocation — Indirect Data Triangulation (รันเมื่อ ≥2 primary sources ไม่ได้):**

เมื่อ primary data หายหรือ conflict ไม่ resolve ได้ → navigate ด้วย echo signals แทน direct reading:

| Primary missing | Echo signal ที่ใช้แทน |
|---|---|
| VIX unavailable | VXST (9d) vs VXV (3m) spread; SQQQ/TQQQ flows; options put/call ratio SPY |
| Futures down | Pre-market ETF prices (SPY, QQQ, IWM) + ADR prices of major US stocks |
| Oil unavailable | XLE price change; airline stocks direction; USO ETF |
| 10Y yield unavailable | TLT price (inverse); bank stocks direction; TIPS spread |
| DXY unavailable | UUP ETF; EM currency ETFs (EEM, EWZ direction) |

→ flag `[ECHOLOCATION: INDIRECT] <metric> — direct source failed, triangulated from: [echo sources]`
→ ถ้า echo signals ชี้ทิศทางเดียวกัน ≥3 sources → ใช้ได้ confidence = medium
→ ถ้า echo signals ขัดกัน → `[ECHOLOCATION: AMBIGUOUS]` mark metric เป็น `[unverified — echoes conflict]`

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

## Sector Universe Radar — Semicon / AI / Datacenter / Space

[วาง output จาก `scripts/universe-screen.py` ตรงนี้]

*ถ้า script ไม่ได้รัน: `[universe-screen unavailable]`*

**สรุปจาก radar:**
- **[EARLY★] สัญญาณแข็งแกร่งที่สุด:** [ticker list — coiling + RS rising vs SPY]
- **[ALERT] เริ่มวิ่ง:** [ticker list — ถ้าไม่มี: "ไม่มีวันนี้"]
- **[WATCH] ติดตาม:** [ticker list]
- **Catalyst หลัก:** [ดึงจาก news-snapshot + catalyst-calendar + ผูกกับ ticker ที่ EARLY★/ALERT]

→ ลำดับความสำคัญ: **[EARLY★]** > **[ALERT]** > **[WATCH]**
→ ถ้าไม่มีทั้ง EARLY★ และ ALERT → ระบุ "ไม่มี setup ชัดเจนในวันนี้" ห้ามสร้าง setup ฝืน

---

## ETF Discovery — หุ้นใหม่นอก watchlist ที่ยังไม่ตกรถ

[วาง output จาก `scripts/etf-discovery.py --top 10` ตรงนี้]

*ถ้า script ไม่ได้รัน: `[etf-discovery unavailable]`*

**สรุป (EARLY★ / ALERT เท่านั้น — EXTENDED = ตกรถแล้ว ข้าม):**
- **[EARLY★] น่าสนใจที่สุด:** [ticker — ระบุเฉพาะถ้ามีจริง ถ้าไม่มีให้ระบุ "ไม่มีวันนี้"]
- **[ALERT] เริ่มวิ่งแล้ว:** [ticker — ระบุเฉพาะถ้ามีจริง]
- ถ้าสนใจตัวไหน → `/stock-content TICKER` ก่อนตัดสินใจ

---

## Sector Money Flow

[วาง output จาก `scripts/sector-flow.py` ตรงนี้]

*ถ้า script ไม่ได้รัน: `[sector-flow unavailable]`*

**สรุป:**
- **Money flowing IN:** [Leading + Improving sectors จาก script]
- **Money flowing OUT:** [Fading + Lagging sectors]
- **Space sector (ROKT/ITA):** [label จาก script — Leading/Improving/Fading/Lagging]

→ เลือก setup จาก sector ที่ **Leading หรือ Improving** เท่านั้น
→ หลีกเลี่ยง long ใน sector ที่ **Lagging** แม้หุ้นจะ coiling

**Thesis alignment check (1 grep — ไม่นับ search budget):**
```bash
grep -E "T[0-9]|Statement:|Tickers:" vault/Knowledge/THESIS_TRACKER.md | head -20
```
ถ้า sector-flow บอก Fading/Lagging สำหรับ sector ที่มี active thesis (T1-T4) → flag:
`⚠️ Sector conflict: [sector] = Lagging แต่ T# [thesis name] ยังเป็น Active — ตรวจสอบว่า thesis ยัง intact ไหม`
ถ้าไม่มี conflict → ไม่ต้องแจ้ง

---

## Catalyst Calendar (21 วันข้างหน้า)

[วาง output จาก `scripts/catalyst-calendar.py` ตรงนี้]

*ถ้า script ไม่ได้รัน: `[catalyst-calendar unavailable]`*

**[SOON] catalysts วันนี้-3 วัน:**
- [รายการจาก script ที่ label = TODAY หรือ SOON — ถ้าไม่มี: "ไม่มี catalyst เร่งด่วน"]

→ [SOON] earnings = ห้าม hold ข้ามผ่าน → ปรับ setup เป็น Day เท่านั้น
→ [SOON] space event (launch/deployment) = อาจเป็น trigger ให้ RKLB/ASTS/LUNR วิ่ง

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

### Depressive Realism — Scenario Probability Reality Check

รันหลัง Most Likely เลือกแล้ว — ตรวจหา optimism bias ใน 2 มิติ:

**DR-1: Probability Inflation Check**
ดู scenario ที่เลือกเป็น Most Likely:
- ถ้า Most Likely = Bullish + confidence ≥ medium แต่ไม่มี structural data support (breadth กว้าง, VIX ลด, yield stable) → `[DR: INFLATED]` — ระบุ adjusted confidence ที่ data จริงรองรับ
- ถ้า Most Likely = Base แต่ Bearish trigger มีหลายข้อพร้อมกัน → `[DR: UNDERSTATED DOWNSIDE]`
- ถ้า probability กระจาย Bullish 60% / Base 30% / Bearish 10% โดยไม่มี data heatmap หนุน → `[DR: INFLATED]` พร้อม suggested redistribution

**DR-2: Optimism Language Scan**
สแกน brief ที่เพิ่งเขียนหาคำต่อไปนี้:
`should`, `likely to`, `expected to`, `set to`, `probably`, `almost certainly`, `bounce`, `recover`

ต่อแต่ละคำที่พบ — ตรวจว่ามี data support ไหม:
- มี data → ผ่าน
- ไม่มี data → `[DR: OPTIMISM LANGUAGE]` + ระบุว่าคำไหนในส่วนไหน

แสดงก่อน Risk Framework:
```
DR Reality Check:
- Probability: [ผ่าน / [DR: INFLATED] adjusted: Bullish X% / Base X% / Bearish X%]
- Language: [ผ่าน / [DR: OPTIMISM LANGUAGE] N คำ — section: X]
```
ถ้าไม่พบ bias ใดเลย → `DR Reality Check: clean ✅`

### Social Anxiety — Market Participant Reaction Sequencing

ต่อแต่ละ scenario — model ลำดับการ react ของแต่ละ participant group ไม่ใช่แค่ทิศทาง:

**Participant groups:** Retail → Algo → Institution → Fed/Policy

ต่อ Most Likely Scenario:
```
Reaction sequence:
1. Retail: [react อย่างไรใน 0-30 นาทีแรก — ขาย/ซื้อ/hold เพราะอะไร]
2. Algo: [respond ต่อ retail flow อย่างไร — momentum chase / mean revert]
3. Institution: [เห็น algo + retail แล้วทำอะไร — buy dip / distribute / wait]
4. Second-order: [institutional move กระทบ retail/algo round 2 อย่างไร]
Gap opportunity: [ช่วงไหนระหว่าง sequence นี้ที่มี mispricing]
```

**กฎ: ถ้า Algo และ Institution คาดว่าจะ react ตรงข้าม retail** → flag `[SA: PARTICIPANT DIVERGENCE]` — อาจเป็นกับดักสำหรับ retail ที่ follow news ก่อน

### Maladaptive Daydreaming — Full Narrative Day Simulation

สร้าง vivid narrative ของวันนี้แบบ scene-by-scene — ไม่ใช่ probability list แต่เป็น story ที่ concrete ที่สุดตาม base case

**Timeline:**

**Pre-open (8:00–9:30 ET):**
> [ใครซื้อ/ขาย futures? sentiment ใน Discord/Reddit เป็นอย่างไร? news ที่กำลัง dominate?]

**Open (9:30–10:00 ET):**
> [gap up/down เท่าไร? volume spike? sector ไหนนำ? retail ทำอะไร?]

**Mid-morning (10:00–11:30 ET):**
> [momentum ยังอยู่หรือ fade? algo เริ่ม mean-revert ไหม? setup ที่วางไว้ trigger ไหม?]

**Midday (11:30–13:30 ET):**
> [volume เบาลง? consolidation? ข่าวใหม่เข้ามาไหม?]

**Afternoon (13:30–15:00 ET):**
> [institution กลับมาไหม? trend ต่อหรือกลับ?]

**Close (15:00–16:00 ET):**
> [window dressing? MOC imbalance? close ที่ไหน relative to day range?]

**Key Invalidation Moment:**
> ถ้าเกิด [event X] ในช่วง [time Y] — scenario ทั้งหมดต้องรีเซ็ต, action = [ทำอะไรทันที]

```
MD Day Narrative: [base case scenario name]
Invalidation trigger: [event + time window]
Highest-risk window: [ช่วงเวลาที่ narrative มีโอกาสพังมากที่สุด]
```

### AIWS — Scale Inversion Test

ตรวจว่าตลาดกำลัง mislabel scale ของ catalyst วันนี้ไหม — บางทีสิ่งที่ดูใหญ่คือ noise สิ่งที่ดูเล็กคือ signal

สำหรับ catalyst หลัก 1-2 อันของวัน ถามคำถาม 2 ข้อ:

**1. Over-labeled as signal?** → catalyst นี้ถูก treat เป็น market-moving event แต่จริงๆ อาจเป็น noise
- ตลาดกำลัง react กับ headline ที่ไม่เปลี่ยน underlying fundamentals ไหม?
- ใครได้ประโยชน์จากการที่ retail เชื่อว่า event นี้ใหญ่?
→ flag `[AIWS: OVER-LABELED]` — "catalyst ดูใหญ่แต่ fundamental impact จริง = [เล็ก/ไม่มี]: [เหตุผล]"

**2. Under-labeled as noise?** → catalyst นี้ถูก treat เป็น noise แต่จริงๆ อาจ structural
- มีข้อมูลที่ตลาดกำลังเพิกเฉยแต่จะ price in ในภายหลังไหม?
- ข้อมูลนี้ยืนยัน trend ที่ยาวกว่าวันไหม?
→ flag `[AIWS: UNDER-LABELED]` — "catalyst ดูเล็กแต่ implied impact = [ใหญ่กว่า]: [เหตุผล]"

```
AIWS Scale Check:
- [catalyst]: [CORRECTLY LABELED / [AIWS: OVER-LABELED] / [AIWS: UNDER-LABELED]]
- Implied vs actual scale: [market treating as X, actual impact = Y]
- Trade implication: [ถ้า mislabeled — fade the reaction / position ahead of repricing]
```

### BPD — Market Split Detector

ตรวจว่าตลาดกำลัง split sector หรือ theme อย่างสุดโต่งไหม — idealize ทั้งหมดหรือ devalue ทั้งหมดโดยไม่มี nuance

**Idealization signal:** ทุก stock ใน sector ขึ้นพร้อมกัน แม้ fundamentals ต่างกัน / valuation ไม่มีความหมายแล้ว / bad news ถูก ignore
→ flag `[BPD: MARKET IDEALIZATION] <sector/theme>` — "ตลาดกำลัง idealize [X]: สัญญาณ = [อะไร]"

**Devaluation signal:** ทุก stock ใน sector ลงพร้อมกัน แม้ company-specific แตกต่าง / good news ถูก ignore / PE ต่ำกว่า historical ทุก quantile
→ flag `[BPD: MARKET DEVALUATION] <sector/theme>` — "ตลาดกำลัง devalue [X]: สัญญาณ = [อะไร]"

```
BPD Market Split:
- Idealized: [sector/theme หรือ "none"]
- Devalued: [sector/theme หรือ "none"]
- Trade implication: [fade the extreme / wait for re-rating / avoid crowded side]
```

**กฎ:** ถ้าพบทั้ง idealization และ devaluation ในวันเดียว → `[BPD: FULL SPLIT DAY]` — ตลาดวิ่ง emotional ทั้ง session ให้ลด size ทุก position 20% และหลีกเลี่ยง FOMO entries

### Paranoid — Adversarial Scan

สำหรับ bullish scenario หลักวันนี้: ถาม "ใครได้ประโยชน์จากการที่ retail เชื่อ scenario นี้?"

**3 คำถาม adversarial:**

1. **Incentive check:** ใครที่ manufacture consensus วันนี้มี financial incentive ในฝั่งตรงข้ามไหม?
   - Sell-side upgrade ก่อน lock-up expiry / secondary offering?
   - Large holder กำลัง distribute แต่ narrative ยังบวก?
   - Market maker ที่ต้องการ buy-side ก่อน sell-side fills?

2. **Information asymmetry:** ถ้า news วันนี้เป็นจริง — ทำไม insiders ถึงไม่ซื้อ/ขายตาม?
   - ตรวจ insider transaction ล่าสุด (ถ้าทำได้) vs narrative ปัจจุบัน

3. **Consensus manufacturing:** narrative นี้ถูก echo ซ้ำในหลาย media outlets พร้อมกันผิดปกติไหม?
   - ถ้าใช่ → อาจเป็น coordinated narrative ไม่ใช่ organic discovery

→ flag `[PARANOID: ADVERSARIAL ACTOR] <who + motive>` ถ้าพบ incentive misalignment ชัดเจน

```
Paranoid Adversarial: [CLEAR / [PARANOID: ADVERSARIAL ACTOR] — who: [X], motive: [Y]]
Implication: [proceed as normal / reduce size / wait for confirmation before entry]
```

ถ้าไม่พบ incentive misalignment → `Paranoid: no adversarial signal ✅`

### TLE — Temporal Pattern Match

เปรียบ conditions วันนี้กับ historical dates ที่คล้าย — "déjà vu เป็น signal ไม่ใช่ noise"

**Match criteria (ต้องตรง ≥ 3 จาก 5):**
1. VIX range (เทียบ ± 2 points)
2. Futures direction + magnitude (เช่น ES +0.3–0.8%)
3. Sector rotation pattern (defensive up / cyclical up / mixed)
4. News theme category (Fed / earnings / geopolitical / macro data)
5. Day-of-week + market microstructure (Monday gap / OpEx Friday)

ถ้าพบ match ≥ 3/5 → ระบุ:
- วันที่ match: [YYYY-MM-DD]
- Conditions ที่ตรง: [list]
- Outcome วันนั้น: [market direction + magnitude ถ้ามีข้อมูล]

→ flag `[TLE: PATTERN MATCH] similar to [date] — prior outcome: [X]`

ใช้เป็น **reference weight** ใน scenario section ไม่ใช่ prediction โดดๆ — ถ้า match outcome bearish แต่ scenario วันนี้ bullish → note tension ไว้

```
TLE Pattern Match: [MATCH FOUND / no match]
- Similar date: [YYYY-MM-DD / N/A]
- Conditions matched: [N/5]
- Prior outcome: [direction + magnitude หรือ "unknown"]
- Weight on today's scenario: [increases [scenario] probability / no adjustment]
```

### Tachypsychia — Volatility Protocol

ถ้าตลาดวิ่งเร็ว = ระบบต้องช้าลง ไม่ใช่เร็วขึ้น

**Trigger conditions (ต้องเช็คก่อนเขียน setup):**
- VIX > 20 → activate Level 1
- Futures gap > 1% (either direction) → activate Level 1
- VIX > 30 OR gap > 2% → activate Level 2

**Level 1 — Tachypsychia Slow-Down:**
- `[TACHYPSYCHIA: SLOW DOWN]` — append ใน brief header
- ห้าม entry ใน 15 นาทีแรกของ session (9:30–9:45 ET)
- ลด default position size ทุก setup ลง 25%
- เพิ่ม observation 2 คำถาม per setup: "ใครกำลังขาย?" + "ใครกำลังซื้อ และทำไม?"

**Level 2 — Tachypsychia Full Pause:**
- `[TACHYPSYCHIA: FULL PAUSE]` — observation only, ไม่มี setup วันนี้
- บันทึก conditions ไว้เป็น data point ใน post-market

```
Tachypsychia Check: VIX=[X], Gap=[Y%]
Protocol: [none / Level 1: SLOW DOWN / Level 2: FULL PAUSE]
Position size modifier: [-25% / N/A]
```

### Semantic Satiation — Market Narrative Check

ตรวจว่า market narrative วันนี้ถูก repeat มากเกินจนตลาด "numb" กับ real signals ไหม

สแกน headline theme วันนี้เทียบกับ 7 วันก่อน:
- ถ้า theme เหมือนกัน word-for-word (เช่น "Fed uncertainty", "AI demand resilient", "China slowdown risk") → `[SATIATION: NARRATIVE NUMBNESS] "<theme>"`
- Numbness = ตลาด over-indexed กับ narrative เก่า → real catalyst อาจเป็นอย่างอื่นที่ยังไม่ price in

ถ้าพบ numbness → เพิ่ม weight ให้ `[AURA: EARLY SIGNAL]` flags จาก Step 0.98 มากขึ้น 1.5×

```
Satiation Narrative: [FRESH / [SATIATION: NARRATIVE NUMBNESS] "<theme>" — repeated N+ days]
Implication: [market responsive to theme / look for un-priced catalysts elsewhere]
```

### Split-Brain — Scenario Independence Check

สร้าง scenario ด้วย 2 modes อิสระ แล้วดูว่าตรงกันไหม

**Left-Brain (logic-first):** อ่านเฉพาะ macro data + earnings numbers → ถ้า data = X, policy = Y → scenario ควรเป็นอะไร?

**Right-Brain (pattern-first):** ดูเฉพาะ sector flow, breadth, sentiment, chart gestalt → โดยไม่อ่าน macro data → pattern บอกว่าอะไร?

- ถ้าทั้งสองได้ scenario เดียวกัน → `[SPLIT-BRAIN: ALIGNED]` — high confidence
- ถ้าต่างกัน → `[SPLIT-BRAIN: SCENARIO CONFLICT]` — บังคับ reconcile: เขียน 1 ประโยคอธิบายว่าทำไมถึงต่างกัน ก่อน commit กับ Most Likely scenario

```
Split-Brain Scenario:
Left-Brain: [scenario direction]
Right-Brain: [scenario direction]
Alignment: [ALIGNED / [SPLIT-BRAIN: SCENARIO CONFLICT] — reason: [reconciliation]]
```

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

## 📉 Sector Pullback Watch — Semicon / AI / Datacenter / Space

*อ่านจาก output ของ `sr-levels.py` ด้านบน — ไม่ต้อง fetch ใหม่*

**กฎ:** หุ้นที่ราคาปัจจุบัน **≤ 5% เหนือ support level ที่ใกล้ที่สุด** = NEAR SUPPORT ★ = โซนที่ risk/reward ดี

| Ticker | ราคาล่าสุด | Support ใกล้สุด | ห่าง (%) | สถานะ | หมายเหตุ |
|--------|-----------|----------------|---------|--------|---------|
| MU | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | HBM sold out — รอ pullback ก่อนเข้า |
| NVDA | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | |
| AMD | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | |
| AVGO | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | |
| CRDO | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | AEC cable — AI tailwind |
| AEIS | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | datacenter power |
| UCTT | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | WFE supercycle |
| BBAI | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | defense AI |
| MOD | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | datacenter cooling |
| PLTR | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | |
| RKLB | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | |
| ASTS | [จาก sr-levels] | [จาก sr-levels] | [คำนวณ] | | |

**label:**
- `NEAR SUPPORT ★` = ห่างจาก support ≤ 5% — โซน entry ที่ดี
- `MID RANGE` = ห่าง 5-15% — รอต่อ
- `EXTENDED` = ห่างจาก support > 15% — ไม่ chase ตอนนี้

**สรุป Pullback Watch:**
- **NEAR SUPPORT ★ วันนี้:** [list ticker หรือ "ไม่มี"]
- **ตัวที่น่าจับตามากที่สุด:** [เหตุผล 1 ประโยค อ้างอิง fundamental จาก session ล่าสุด]
- **ตัวที่ extended ที่สุด ห้าม chase:** [list]

*ถ้า sr-levels ไม่ได้รัน: `[pullback watch unavailable — sr-levels script failed]`*

---

## Trade Setups (เพื่อการศึกษาเท่านั้น)

> **DISCLAIMER: The setups below are educational frameworks based on publicly available technical and fundamental data. They are NOT financial advice, NOT personalized recommendations, and NOT a solicitation to buy or sell any security. All trading involves risk of loss. Do your own research and consult a licensed advisor before making any investment decision.**

Setup ทุกอันใช้ logic แบบ IF-THEN — การเข้า position ขึ้นอยู่กับ trigger ไม่ใช่แน่นอนเสมอ

**Setup consistency check — ทำก่อนเขียน setup ทุกครั้ง:**
ดู Most Likely Scenario ที่เลือกไว้:
- Most Likely = **Bearish** → setup ที่เป็น Long ต้องมีเหตุผลชัดเจนว่าทำไมถึง diverge (เช่น short-squeeze, defensive sector) ถ้าไม่มี → เปลี่ยนเป็น short/cash setup แทน
- Most Likely = **Bullish** → setup ที่เป็น Short ต้องมีเหตุผลชัดเจน
- Most Likely = **Base** → setup ทั้งสองทิศทางได้ แต่ต้องมี invalidation ชัดเจน
ถ้า setup ขัดกับ Most Likely โดยไม่มีเหตุผล → flag ⚠️ ใน brief ก่อน save

**Parasomnia — Reflex Entry Guard (รันก่อนเขียน setup ทุกอัน):**

ตรวจว่า setup แต่ละอันมาจาก conscious analysis หรือ reflex/autopilot

Reflex patterns ที่ต้องระวัง:
- "เห็น ticker วิ่ง → อยากซื้อ" (FOMO reflex — trigger = movement ไม่ใช่ thesis)
- "sector วิ่งทั้ง sector → ซื้อทุกตัว" (herd reflex — ไม่ได้วิเคราะห์ individual)
- "ตลาดลง → เพิ่ม position" (dip-buying reflex — โดยไม่ตรวจ thesis)
- "เมื่อวานทำได้ → วันนี้ทำเหมือนกัน" (habit reflex — ไม่ได้ปรับตาม conditions ใหม่)
- "setup นี้เคยได้กำไร → ทำซ้ำ" (pattern addiction — ไม่ได้ตรวจ current validity)

สำหรับทุก setup → ถามตัวเอง: "ฉันจะเขียน setup นี้ถ้าตัวเลข/movement วันนี้ไม่มีอยู่ไหม?" ถ้าคำตอบ = ไม่ → อาจเป็น reflex ไม่ใช่ thesis

→ flag `[PARASOMNIA: REFLEX SETUP] "<trigger>"` ถ้า entry driver เป็น movement ไม่ใช่ thesis — setup นั้นต้องผ่าน additional justification ก่อน include

**Stendhal — Beauty Trap Scan (รันต่อทุก setup):**

ถ้า setup ดู "too perfect" — catalyst ชัด, trend ชัด, ทุกอย่าง align, ไม่มีข้อแย้ง → `[STENDHAL: BEAUTY TRAP]`

Beauty trap checklist (ถ้า ≥ 3 ข้อใช่ = trap):
- [ ] Catalyst ชัดเจนมาก และ thesis เข้าใจง่ายมาก
- [ ] ทุก indicator ชี้ทิศทางเดียวกัน (ไม่มีตัวไหน diverge)
- [ ] Bear case เขียนไม่ออกหรือฟัง weak มาก
- [ ] Setup นี้ถูก mention ใน social media หรือ mainstream media แล้ว
- [ ] ราคาขยับไปในทิศทาง thesis แล้วก่อนจะ entry

→ ถ้า trigger Beauty Trap: บังคับเขียน adversarial question 1 ข้อ: "ถ้า setup นี้ผิด — ใครที่ได้ประโยชน์?"

**Dopamine State — Setup Quality Gate:**

ตรวจ dopamine state ก่อนเขียน setup แต่ละอัน:

- **Win streak (≥ 2 wins ติด)** หรือ **market ให้ news ดีติดต่อกัน > 3 วัน** → `[DOPAMINE: ELEVATED STATE]`
  - ทุก setup ในสถานะนี้ต้องมี explicit kill condition ที่วัดได้ก่อน include
  - ห้ามเพิ่ม position size จาก default — dopamine ทำให้ประเมิน risk ต่ำเกิน

- **ปกติ** → proceed as normal

```
Dopamine State: [ELEVATED (win streak / news streak) / NORMAL]
Setup modifier: [require explicit kill condition / no change]
```

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

### GAD Pre-flight — Failure Mode Checklist (บังคับทุก setup)

ต่อแต่ละ setup ที่เขียนไว้ — enumerate 3 failure modes + Plan B ก่อน finalize

| Setup | Failure Mode | Early Signal | Plan B |
|---|---|---|---|
| Setup 1 | [อะไรทำให้ setup นี้ผิดพลาด] | [signal แรกที่บอกว่าผิด] | [ทำอะไรถ้าเกิด] |
| Setup 1 | ... | ... | ... |
| Setup 1 | ... | ... | ... |
| Setup 2 | ... | ... | ... |
| Setup 2 | ... | ... | ... |
| Setup 2 | ... | ... | ... |
| Setup 3 | ... | ... | ... |
| Setup 3 | ... | ... | ... |
| Setup 3 | ... | ... | ... |

**กฎ: Setup ที่ไม่มี failure mode ครบ 3 ข้อ → flag `[GAD: INCOMPLETE]`**
Setup ที่ถูก flag ห้ามรายงานว่า "พร้อม" — ต้องเติม failure modes ก่อนจบ brief

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

## Commit

หลังสร้าง brief + decision tree → รัน:
```bash
bash scripts/safe-commit.sh "notes: pre-market YYYY-MM-DD"
```
