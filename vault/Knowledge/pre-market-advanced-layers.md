---
type: pre-market-handbook
description: Advanced faint-signal cognitive layers for /pre-market Tier 3 (Active day). Referenced from pre-market.md steps 0.985–0.994. Load only when Tier 3 gate triggered.
updated: 2026-05-18
---

# Pre-Market Advanced Layers — Tier 3 Only

> Extracted from pre-market.md 2026-05-18 (token-audit fix — saves ~10,000 tok/session on Tier 2 days)
> Load only when: Tier 3 (Active day: SPY range ≥1.5% OR VIX >18 OR major catalyst)

Run each layer with script output from Step 1.5. Suppress empty outputs — show only triggered flags.

---

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

ถ้าไม่พบ → suppress (ไม่ต้องเขียน)

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

ถ้าไม่มีข้อมูลเพียงพอ → suppress

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

ถ้าไม่พบ label ใด → suppress

---

### 0.991 Narcolepsy — Flash Insight + Market Drop Detection

Narcolepsy = สลับระหว่าง hyperfocus กับ sudden clarity flash ที่ตัดผ่านทุกอย่าง

**Narcolepsy Flash (รัน 1 ครั้งก่อน generate brief — บังคับเสมอแม้ Tier 2):**

> "ถ้าต้องสรุปสภาพตลาดวันนี้เป็น 1 ประโยค โดยไม่อ่าน analysis อีกครั้ง — ประโยคนั้นคืออะไร?"

```
Narcolepsy Flash: "[1-sentence market read — raw, unfiltered]"
```

หลัง brief เสร็จ → เปรียบเทียบ flash กับ scenario:
- ตรงกัน → `[NARCOLEPSY: FLASH CONFIRMED]`
- ขัดกัน → `[NARCOLEPSY: FLASH-BRIEF CONFLICT]` — ระบุ dimension ที่ต่าง

**Market Narcoleptic Drop:** Sudden volume collapse > 40% จาก 5-day avg โดยไม่มี catalyst + price flat = institutional withdrawal เงียบๆ
→ flag `[NARCOLEPSY: MARKET DROP]`

---

### 0.992 Dermatographia — Market Hypersensitivity Scan

ตรวจ 3 hypersensitivity signals:
1. **VIX-move ratio**: VIX implies daily range X% — SPY เคลื่อนจริง Y% ใน 24h (ถ้า Y > 1.5× X = amplified)
2. **News-to-move ratio**: headline ระดับ minor (<0.5% event) ทำให้ sector move >1.5% = dermatographic session
3. **Breadth amplification**: SPY move เล็ก แต่ advance/decline spread ≥ 65/35 = sentiment leading price

→ flag `[DERMATOGRAPHIA: HYPERSENSITIVE] — reduce all setup sizes 30%`

กฎ: amplification ratio >2× → ลด position size ทุก setup 30% โดยอัตโนมัติวันนี้

ถ้าปกติ → suppress

---

### 0.993 Supertaster — Pre-Market Bitter Signal Scan

สแกน 4 bitter channels ใน script output data:
1. **Credit pre-signal**: HY spreads ขยาย <5bps แต่ equity ยังไม่ปรับ
2. **Options quiet flow**: unusual put volume ในindex/sector โดยไม่มีข่าว
3. **Volume-price mismatch**: SPY/QQQ ราคา flat แต่ volume เบา >20% ของ 5-day avg
4. **Currency micro-shift**: DXY ±0.3%+ โดยไม่มีข่าว macro

→ flag `[SUPERTASTER: FAINT BITTER] <channel>`

ถ้าทุก channel clean → suppress

---

### 0.994 Foreign Accent Syndrome — Communication Shift Scan

ตรวจ 3 sources จาก news-snapshot + web:
1. **Fed accent**: FOMC keyword shift (เช่น "patient" → "vigilant")
2. **Earnings pre-announcement**: guidance specificity drop
3. **Analyst language**: new vocabulary ใน conservative sector = narrative adoption = possible peak

→ flag `[FAS: LANGUAGE SHIFT] <source> — prior: "<old>" → current: "<new>"`

ถ้าไม่พบ → suppress

---

## Suppress-clean output rule

**ถ้า layer ไม่ triggered → ไม่ต้องเขียนผลออกมา**
Summary เมื่อทุก layer clean:
```
Advanced layers (0.985–0.994): no flags ✅
```

เมื่อมี flag:
```
Advanced layer flags:
- [HYPEROSMIA: FAINT SIGNAL] ...
- [DERMATOGRAPHIA: HYPERSENSITIVE] ...
```
