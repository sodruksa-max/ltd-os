---
description: Self-improving layer — reads all post-market reviews, finds recurring patterns, proposes updates to trading rules and brief approach. User approves every change before saving.
---

# /weekly-calibration

อ่าน review สะสม → หา pattern → เสนอ update กฎและ brief → คุณ approve ก่อน save ทุกครั้ง

## Usage

```
/weekly-calibration [N]
```

- `N` = จำนวนวันย้อนหลัง (default: 7)
- ตัวอย่าง: `/weekly-calibration 14` = ดู 2 สัปดาห์ย้อนหลัง

---

## Steps

### 1. Load source files (read-only ทั้งหมด)

อ่านไฟล์เหล่านี้ — **ห้ามแก้ไขในขั้นตอนนี้:**

```
vault/20_investment/_journal/*-review.md    (N วันย้อนหลัง)
vault/_memory/OUTCOMES.md                   (Trading Calibration Log)
vault/_memory/PREFERENCES.md               (กฎปัจจุบัน)
vault/_memory/HYPERTHYMESIA_LOG.md          (full-context history — ถ้ามี)
```

หลังโหลดไฟล์แล้ว รัน Brier Score เพื่อได้ quantitative baseline ของ calibration accuracy:

```bash
code/python/.venv/Scripts/python scripts/brier-score.py
```

Output: rolling 10-day Brier Score + over-confidence flag — ใช้เป็น evidence เพิ่มใน Step 3a (Calibration trend)

ถ้าไม่พบ review ไฟล์เลย → หยุดและแจ้ง:
> ❌ ไม่พบ review ไฟล์ — รัน `/post-market` ก่อนอย่างน้อย 1 วัน

**ถ้าพบ review บางวันแต่ขาดหายไปบางวัน** (วันที่อยู่ในช่วง N วัน แต่ไม่มี review file) → ดึงข้อมูลตลาดของวันที่ขาดหายด้วย script แทน web search:

```bash
code/python/.venv/Scripts/python scripts/post-snapshot.py --date <MISSING_DATE>
```

ใช้ output เป็น context ของวันนั้น (scenario = ดู SPY % ใน verdict section) — **ไม่ต้อง web search**

### 2. Extract raw data จากทุก review

สำหรับแต่ละ review ไฟล์ที่พบ ดึง:

- **Date + Scenario:** Predicted vs Actual + Match (Yes/Partial/No)
- **Calibration verdict:** well-calibrated / over-confident / under-confident
- **Setups:** แต่ละ setup — trigger เกิด?, ทิศทาง, ผล (win/loss/pending)
- **Blind spots:** แต่ละ item ใน "What Was Missed"
- **Lessons:** แต่ละ lesson ใน "Lessons for Next Brief"
- **Regime label:** classify วันนั้นเป็น 1 ใน 4:
  - `trending-up` — SPY +0.5%+ ต่อเนื่อง, VIX ลด, breadth กว้าง
  - `trending-down` — SPY -0.5%+ ต่อเนื่อง, VIX สูงขึ้น
  - `choppy` — SPY ±0.5% หรือ intraday reversal ชัดเจน
  - `risk-off` — VIX spike >20%, sector rotation เข้า defensives, bonds bid
  ใช้ข้อมูลจาก verdict section ของ review (SPY %, VIX ที่บันทึกไว้) — ห้าม web search เพิ่ม

### 3. Analyze patterns

วิเคราะห์ข้อมูลทั้งหมดและหา pattern ใน 5 มิติ:

**3a. Calibration trend**
- สัดส่วน well-calibrated / over-confident / under-confident
- มี bias ซ้ำไหม (เช่น over-confident ทุกครั้งที่มี earnings)

**3b. Blind spot patterns**
- blind spot ไหนโผล่ซ้ำ ≥ 2 ครั้ง
- หมวดไหนพลาดบ่อย (geopolitical / macro surprise / earnings reaction / Fed)

**3c. Setup performance**
- แต่ละ setup type (XLE, TLT, QQQ ฯลฯ) — win rate จากข้อมูลที่มี
- setup ไหน trigger แต่ผลแย่ vs ไม่ trigger แต่ถ้าเข้าน่าจะดี

**3d. Lesson adoption**
- lesson จาก review ก่อนหน้า → ถูกนำไปใช้ใน brief ถัดไปหรือเปล่า
- lesson ไหนโผล่ซ้ำโดยไม่ได้ถูก implement

**3e. Prediction accuracy**
- scenario accuracy โดยรวม (% ที่ match)
- confidence calibration — low confidence + ถูก vs high confidence + ผิด

**3f. Regime distribution — overfitting guard**

**3g. HSAM Context-Matched Precedent Query (ถ้ามี HYPERTHYMESIA_LOG)**

ถ้า `vault/_memory/HYPERTHYMESIA_LOG.md` มีอยู่และมี entries ≥ 5:

ดู regime + VIX range ของสัปดาห์ปัจจุบัน (จาก review ไฟล์ล่าสุด) แล้วหา entries ใน HYPERTHYMESIA_LOG ที่ context ใกล้เคียงที่สุด:
- Regime ตรงกัน (เช่น choppy)
- VIX อยู่ใน range เดียวกัน (±3 points)
- Catalyst type คล้ายกัน (earnings / Fed / geopolitical)

แสดง top 3 precedents:
```
HSAM Precedent Query — context ใกล้เคียงสัปดาห์นี้:
1. [date]: [regime] VIX=[X] — Predicted [direction] @ [confidence] → Actual [Y], Match [Z]
   Lesson: [top lesson จาก entry นั้น]
2. [date]: ...
3. [date]: ...

Pattern from precedents: "เมื่อ [context] เกิด → outcome คือ [X] ใน Y/Z ครั้ง"
```

ถ้า HYPERTHYMESIA_LOG ยังไม่มี entries พอ → ข้ามเงียบๆ ไม่ต้องแจ้ง
- นับวันแต่ละ regime: trending-up X วัน / trending-down X วัน / choppy X วัน / risk-off X วัน
- ถ้า regime ใด regime หนึ่ง > 70% ของ sample → flag:
  > ⚠️ **Regime-homogeneous sample**: X% ของ review วันเหล่านี้เป็น `[regime]` — pattern ที่เห็นอาจใช้ได้เฉพาะ regime นี้ ไม่ใช่ all-weather rule
- ถ้า sample มีหลาย regime → note ว่า "diverse sample — pattern น่าเชื่อถือกว่า"

**3h. Depressive Realism — Systematic Optimism Bias Tracker**

สแกนทุก brief ใน N วัน หาภาษา optimism bias เปรียบกับผลจริง:

**Optimism language keywords:** `should`, `likely to`, `expected to`, `set to`, `probably`, `almost certainly`, `bounce`, `recover`, `likely`

ต่อแต่ละ keyword ที่พบใน brief:
- บันทึก: วันที่ / section ที่ปรากฏ / Most Likely scenario วันนั้น / ผลจริง (match/no match)

**คำนวณ Optimism Bias Rate:**
```
Optimism Bias Rate = (ครั้งที่ใช้ optimism language + ผลไม่ match) / (ครั้งที่ใช้ optimism language ทั้งหมด)
```

- Rate < 40% → ภาษา optimism มี data support ดี — ผ่าน
- Rate 40–60% → `[DR: MODERATE BIAS]` — แนะนำใช้คำที่ระบุ condition ชัดขึ้น
- Rate > 60% → `[DR: SYSTEMATIC OPTIMISM]` → เสนอ proposal: "ห้ามใช้ optimism language โดยไม่มี data อ้างอิงใน brief section ที่พบบ่อย"

แสดงใน Pattern Summary:
```
DR Optimism Bias: X% (N ครั้งที่ใช้ / M ครั้งที่ผิด)
Top optimism keywords: [keyword] ใน [section] — miss rate X%
Status: [clean / [DR: MODERATE BIAS] / [DR: SYSTEMATIC OPTIMISM]]
```

**3i. Schizotypal — Coincidence Convergence Scanner**

มองหา 3+ data points ที่ดูไม่เกี่ยวกันแต่เกิดพร้อมกันในช่วง N วัน:
- สินทรัพย์ที่ไม่ควร correlate แต่ move together
- sector rotation ที่ไม่ match กับ macro narrative
- timing coincidences: ข่าว A เกิดวันเดียวกับ data B และ C

ต่อแต่ละ cluster ที่พบ → ตั้ง hypothesis:
> "ถ้า 3 สิ่งนี้ไม่ใช่ coincidence — hidden factor คืออะไรที่อธิบายได้ทั้งหมด?"

**กฎ: ไม่ต้องพิสูจน์** — แค่ log hypothesis ถ้า pattern ซ้ำ ≥ 3 สัปดาห์ค่อยสอบสวนผ่าน `/wild-thesis`

แสดงใน Pattern Summary:
```
Schizotypal Convergence:
- Cluster: [X] + [Y] + [Z] — date range: [range]
  Hidden factor hypothesis: [1 ประโยค]
  Recurrence: ครั้งแรก / N ครั้งแล้ว → [ถ้า ≥ 3: สอบสวน — /wild-thesis <topic>]
```
ถ้าไม่พบ cluster → ข้ามเงียบๆ

### 4. Generate proposals

สร้าง proposal เฉพาะที่ **มี evidence จาก review อย่างน้อย 2 ครั้ง** — ห้าม fabricate pattern จาก data จุดเดียว

แต่ละ proposal ต้องมี:
- **ประเภท:** `PREFERENCES.md` / `brief approach` / `decision tree rule`
- **การเปลี่ยนแปลง:** เดิมคืออะไร → ใหม่เป็นอะไร
- **Evidence:** อ้างอิง review วันไหน + blind spot/lesson ไหนที่สนับสนุน
- **Impact:** ถ้าใช้กฎนี้ในข้อมูลที่ผ่านมาจะเปลี่ยนผลอะไรได้บ้าง
- **Regime tag:** `all-weather` หรือ `regime-specific: [trending-up/trending-down/choppy/risk-off]`
  - `all-weather` = pattern เกิดใน ≥ 2 regime ที่ต่างกัน
  - `regime-specific` = pattern เกิดเฉพาะใน regime เดียว — ต้องระบุให้ชัด
- **Walk-forward check:** ถ้า regime เปลี่ยนจาก [regime ปัจจุบัน] → [regime ตรงข้าม] กฎนี้ยังใช้ได้ไหม?
  - ถ้าคำตอบคือ "ไม่" หรือ "ไม่แน่ใจ" → tag เป็น `regime-specific` ห้าม tag เป็น `all-weather`

ถ้าไม่พบ pattern ที่ชัดพอ → เขียน:
> "ข้อมูลยังไม่เพียงพอสำหรับ proposal ที่น่าเชื่อถือ — ต้องการ review เพิ่มอีก X วัน"

### 5. Present proposals + ขอ approve

แสดงผลในรูปแบบนี้:

```
Weekly Calibration — YYYY-MM-DD
Reviews analyzed: N ไฟล์ (YYYY-MM-DD ถึง YYYY-MM-DD)

═══════════════════════════════════════
PATTERN SUMMARY
═══════════════════════════════════════

Calibration: X% well-calibrated, X% over-confident, X% under-confident
Scenario accuracy: X/N correct (X%)
Top recurring blind spot: [หมวด]
Top unimplemented lesson: [lesson]

═══════════════════════════════════════
PROPOSALS (N รายการ)
═══════════════════════════════════════

[1] PREFERENCES.md — Trading Rules
  เดิม: [ข้อความเดิม หรือ "ไม่มีกฎนี้"]
  ใหม่: [ข้อความใหม่]
  Evidence: review วันที่ X และ Y — blind spot "[ชื่อ]" โผล่ 2 ครั้ง
  Impact: ถ้าใช้กฎนี้ใน 2 วันที่ผ่านมา จะหลีกเลี่ยง [ผล] ได้

[2] Brief approach — เพิ่ม catalyst category
  เดิม: ไม่มี "Presidential Action Risk" ใน Risk Framework
  ใหม่: เพิ่ม "Presidential Action Risk" เป็น standalone row ใน Risk Table
  Evidence: review 2026-04-29 — Trump naval blockade ทำ oil +7% โดยไม่ได้อยู่ใน brief
  Impact: มี alert ล่วงหน้าสำหรับ executive announcement ที่อาจ move market
  Regime tag: all-weather (เกิดได้ทุก regime)
  Walk-forward: ถ้าตลาดเป็น risk-off — กฎนี้ยังใช้ได้ ✅

...
```

จากนั้นสำหรับแต่ละ proposal — **ก่อนถาม approve** ให้ตรวจ out-of-sample:

**ถ้า regime tag = `all-weather`:**
```bash
ls vault/20_investment/_journal/*-review.md | sort | head -n -N
```
ดูว่ามี review นอก N-day window ที่สนับสนุน pattern เดียวกันไหม (grep blind spot / lesson keyword)
- ถ้ามี evidence นอก window → แสดง ✅ "out-of-sample confirmed (review วันที่ X)"
- ถ้าไม่มี หรือ window ครอบคลุมทุก review ที่มี → แสดง:
  > ⚠️ **Out-of-sample unvalidated** — evidence ทั้งหมดอยู่ใน N-day window เดียวกัน ถ้าต้องการ validate รัน `/weekly-calibration 30` (หรือมากกว่า) ก่อน approve

**ถ้า regime tag = `regime-specific`:** ข้ามขั้นตอนนี้ — ไม่ต้อง validate out-of-sample (เป็น regime-specific อยู่แล้ว)

จากนั้นถามแต่ละ proposal:
> **Proposal [N]: approve? (y/n/แก้ไข)**

- `y` → บันทึกรอ save
- `n` → ข้ามไป proposal ถัดไป
- `แก้ไข` → รอรับข้อความใหม่จาก user แล้วใช้แทน

### 6. Apply approved proposals

หลัง user approve ทุกรายการแล้ว — **ยังไม่ save** — แสดง summary:

```
Approved: X รายการ
Skipped: X รายการ

การเปลี่ยนแปลงที่จะ apply:
- PREFERENCES.md: [รายการ]
- Brief approach: [รายการ] (จะบันทึกเป็น note ใน vault/_memory/WORKFLOWS.md)

บันทึกทั้งหมดเลยไหม? (y/n)
```

ถ้า y → apply ทุก change พร้อมกัน
ถ้า n → ทิ้งทุกอย่าง ไม่แก้ไขไฟล์ใด

### 7. Run Brier Score

```bash
code/python/.venv/Scripts/python scripts/brier-score.py
```

แสดง output ให้ user เห็น extract ค่าสำคัญ 2 อย่าง:
- `latest_bs` = rolling 10d average Brier score ล่าสุด
- `bs_flag` = [ok] / [!] OVER-CONFIDENT / [~] ok

ถ้า `[!] OVER-CONFIDENT` → แจ้ง user ด้วย:
> ⚠️ Brier Score สูงกว่า 0.25 — ระบบ over-confident อย่างเป็นระบบ พิจารณาลด confidence level ใน pre-market brief

### 8. Append calibration entry

Append 1 บรรทัดใต้ `## Trading Calibration Log` ใน `vault/_memory/OUTCOMES.md`:

```
[weekly-calibration YYYY-MM-DD] N reviews analyzed — proposals: X approved, X skipped — top pattern: [pattern] — BS rolling 10d: [latest_bs] [bs_flag]
```

---

## Constraints

- **ห้าม auto-apply** — ทุก change ต้องผ่าน user approve ก่อนเสมอ
- **ห้าม propose จาก data จุดเดียว** — ต้องมี pattern ≥ 2 reviews
- **ห้ามแก้ CLAUDE.md** — แก้ได้แค่ PREFERENCES.md และ WORKFLOWS.md
- **ถ้าข้อมูลน้อยกว่า 3 reviews** → แจ้งว่า pattern ยังไม่น่าเชื่อถือ แต่รันต่อได้ถ้า user ยืนยัน

## Anti-patterns

- ❌ Propose การเปลี่ยนแปลงที่ขัดกับ hard rules ใน PREFERENCES.md (leverage, crypto leverage ฯลฯ)
- ❌ Fabricate pattern — ถ้าไม่เห็นซ้ำจาก evidence จริงๆ ห้ามเสนอ
- ❌ Save โดยไม่ถาม — แม้ผ่าน approve แล้ว ยังต้องถาม final confirm
- ❌ เปลี่ยน position sizing หรือ risk rules โดยไม่มี statistical evidence ชัดเจน
- ❌ Tag rule เป็น `all-weather` ถ้า evidence มาจาก regime เดียว — ต้อง tag เป็น `regime-specific` และแจ้ง user ชัดเจน
- ❌ Approve `regime-specific` rule โดยไม่แสดง warning ว่า "กฎนี้อาจใช้ไม่ได้ถ้า regime เปลี่ยน"

## Commit

หลัง user approve rules → รัน:
```bash
bash scripts/safe-commit.sh "memory: weekly-calibration YYYY-MM-DD (approved YYYY-MM-DD)"
```
