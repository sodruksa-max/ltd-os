---
type: behavior-handbook
updated: 2026-05-18
source: arXiv:2509.13237 (Metacognitive Reuse — Meta AI)
purpose: compressed cognitive layer procedures สำหรับ /pre-market — load ต้น session แล้ว reference ชื่อ behavior แทนการ re-derive ทุกครั้ง
---

# Pre-Market Behavior Handbook

*Load ไฟล์นี้ที่ Step 0.1 ของ /pre-market — reference behavior names ในการ output แทน expand full instructions*

---

## Layer A: Pre-Data Instinct Layers (รัน ก่อน ดูข้อมูล)

### A1 · MISOPHONIA-MARKET
**Trigger:** VIX term structure inverted, credit spreads vs equity diverge, oil vs risk asset correlation break, volume vs price direction mismatch
**Output format:** `[MISOPHONIA: MARKET TRIGGER] <trigger name>` หรือ `Misophonia: clear ✅`
**Rule:** ถ้า fire → escalate เป็น primary concern; ห้าม suppress

### A2 · TOURETTE-REFLEX
**Trigger:** อะไรที่ "jump out" ก่อน analysis — ตัวเลขขัดกับ expectation, correlation ผิด, ความรู้สึก "เดี๋ยวนะ..."
**Output format:** `[REFLEX] <สิ่งที่ jump out>` หรือ `[REFLEX CLEAN]` — 1 bullet ต่อ observation
**Rule:** ห้ามรอ reason — fire ทันที; ทุก reflex ต้องถูก addressed ใน analysis

### A3 · SYNESTHESIA-TEXTURE
**Channels:** Temperature (SPY%) | Texture (VIX) | Width (breadth) | Pressure (TNX dir) | Weight (oil%)
**Output format:** `Market texture: [GESTALT] — Temperature: X | Texture: X | Width: X | Pressure: X | Weight: X`
**Rule:** Gestalt ต้องถูก referenced ใน Scenario section — ถ้าขัดให้ note `[TEXTURE CONFLICT]`

### A4 · HSP-ATMOSPHERE
**Checks:** (1) Texture Mismatch — ตัวเลขดีแต่ feel ไม่ smooth; (2) Divergence — สินทรัพย์ควรร่วมทิศแต่แยก; (3) Pre-Catalyst Silence — เงียบก่อน event ใหญ่
**Output format:** `HSP Atmosphere: [CLEAR / TEXTURE MISMATCH / DIVERGENCE / PRE-CATALYST SILENCE]` + Implication 1 ประโยค
**Rule:** 2+ flags → ลด position size ทุก setup -25% อัตโนมัติ

---

## Layer B: Data-Parallel Layers (รัน ขณะ/หลัง ได้ข้อมูล)

### B1 · APHANTASIA-LABEL-BAN
**Banned:** head-and-shoulders, cup-and-handle, double top/bottom, flag, pennant — ทุกอัน
**Action:** แปลงเป็น criteria ทันที: `price made lower high at $X, neckline at $Y`
**Rule:** Setup อ้าง visual label โดยไม่มี criteria = invalid → ห้าม include ใน trade section

### B2 · PTSD-AMBIENT
**Channels:** Credit (HY spread >+10bps) | Liquidity (TED >30bps) | Positioning (margin debt <-2% MoM) | Flow (dark pool >2σ) | Insider (≥3 cluster selling)
**Output format:** `PTSD Ambient: [N threats / clear]` + `-15% position per flag, max -45%`
**Rule:** ไม่มีข้อมูล channel ไหน → mark `[unverified]` ไม่ skip

### B3 · AURA-EARLY-WARNING
**Categories:** Bond-Equity Divergence | Credit Spreads Creeping (≥3 วัน ติด) | Geopolitical Pre-signal | Micro Sector Rotation (<0.5% แต่ breadth สูง)
**Output format:** `[AURA: EARLY SIGNAL] <signal> — watch: 2-6 weeks`
**Rule:** ถ้าไม่มี → `Aura: no early signals ✅`

---

## Layer C: Scenario Qualification Layers (รัน ใน scenario section)

### C1 · TACHYPSYCHIA
**Check:** VIX level + NQ gap size
**Threshold:** NQ gap >1% → Level 1: ห้าม entry 9:30-9:45 ET; size -25%
**Output format:** `[TACHYPSYCHIA: SLOW DOWN] Level X` หรือ `Tachypsychia: clear ✅`

### C2 · DR-REALITY-CHECK
**Check:** Probability sum = 100%; language conditional ไม่ใช่ definitive; base rate ไม่ใช่ upside case
**Output format:** `DR Reality Check: [clean ✅ / [DR: UPSIDE ANCHORED]]`
**Rule:** ถ้า prob sum ≠ 100 → ปรับก่อน publish

### C3 · SPLIT-BRAIN
**Check:** Left-brain (data/numbers) vs Right-brain (patterns/RS/sector flow) — ขัดกันไหม?
**Output format:** `[SPLIT-BRAIN: SCENARIO CONFLICT]` + reconciliation 1 ประโยค หรือ `Split-Brain: aligned ✅`

### C4 · SATIATION-NARRATIVE
**Check:** Key narrative ซ้ำ >2 สัปดาห์ → ตลาด price in แล้ว?
**Output format:** `[SATIATION: NARRATIVE NUMBNESS] "<narrative>"` หรือ `Satiation: fresh catalyst ✅`
**Rule:** ถ้า fire → เพิ่ม weight ให้ AURA signals 1.5×

### C5 · AIWS-MAGNITUDE
**Check:** Price reaction vs fundamental impact — proportional? over? under?
**Output format:** `[AIWS: OVER-REACTION / UNDER-REACTION]` + trade signal หรือ `AIWS: proportional ✅`

### C6 · PARANOID-ADVERSARIAL
**Check:** Large holders distributed near highs? Iran/macro news = convenient trigger? Consensus extreme?
**Output format:** `[PARANOID: ADVERSARIAL ACTOR / CONSENSUS TRAP]` หรือ `Paranoid: clear ✅`

### C7 · TLE-PATTERN-MATCH
**Check:** Context similar to prior date? Prior outcome = relevant reference?
**Output format:** `[TLE: PATTERN MATCH] similar to <date> — prior outcome: <result>` หรือ `TLE: no match ✅`

---

## Layer D: Setup Validation Layers (รัน ต่อแต่ละ trade setup)

### D1 · DOPAMINE-STATE
**Check:** ความรู้สึกก่อน entry — FOMO, revenge, excitement สูง = danger
**Output format:** `Dopamine State: NORMAL ✅` หรือ `[DOPAMINE: ELEVATED] — ลด size -50%`

### D2 · GAD-PREFLIGHT
**Format:** ต่อ setup: 3 failure paths + early signal + plan B (table format บังคับ)
**Rule:** ไม่มี pre-mortem = ไม่มี setup — เปลี่ยนเป็น Watch ก่อน

### D3 · SOCIAL-ANXIETY-REACTION
**Check:** ถ้า news ออกใน session — reaction ของตลาดสมเหตุสมผลหรือ overreaction?
**Output format:** `SA Reaction: [proportional / [SA: OVERREACTION] → mean-revert opportunity]`

---

## Output Size Guidelines

ต่อแต่ละ behavior — output ไม่เกิน:
- Layer A (instinct): 2-3 lines ต่อ behavior
- Layer B (data): 3-5 lines ต่อ behavior
- Layer C (scenario): 1-2 lines ต่อ behavior
- Layer D (setup): GAD = table 3 rows; others = 1 line

**กฎ:** ถ้า behavior output ยาวกว่า guidelines → ย่อลงก่อน; เฉพาะ `[TRIGGERED]` items เท่านั้นที่ expand รายละเอียด
