## Optimist Proposal

### Recommendation

**เพิ่ม AH weighted net criterion เป็น gate เพิ่มเติม** — Setup 3 trigger ควรเป็น: (1) ≥3/4 GAAP EPS beat **AND** (2) AH weighted net ≥ 0pp. ทั้งสองต้องผ่านพร้อมกันถึงจะเข้า Long QQQ วันถัดไป

### Core argument

GAAP EPS beat บอกว่าบริษัท "ทำได้ดีในอดีต" แต่ราคาหุ้นตอบสนองต่อ "อนาคตที่ตลาดคาดใหม่" — AH reaction คือ market's real-time repricing ของ narrative นั้น การมี AH weighted net ≥ 0pp เป็น gate ไม่ได้ทำให้ setup complex ขึ้น แต่ทำให้ setup ตอบคำถามที่ถูกต้อง: "ตลาดเชื่อว่า QQQ ควรขึ้นพรุ่งนี้ไหม?" แทนที่จะถาม "ตัวเลข EPS ดีไหม?" การเพิ่ม criterion นี้ในช่วง paper trading มีต้นทุนเป็นศูนย์แต่ upside คือ signal quality ที่สูงขึ้นก่อนเปลี่ยนเป็นเงินจริง

### Supporting evidence

**1. Apr 29 case study — AH เป็น leading signal ที่ดีกว่า GAAP beat**
4/4 GAAP beat แต่ AH net -0.30pp → ถ้า setup เดิม (GAAP only) trigger ก็เข้า Long QQQ Apr 30 ในวันที่ตลาดมีแรงกด -0.30pp จาก Mag7 composition อยู่แล้ว หาก criterion AH ≥ 0pp ใช้อยู่ วันนั้น setup จะ void — หลีกเลี่ยง false positive ได้ 1/1 (100% จาก data ที่มี)

**2. "Sell the news" มีโครงสร้างรองรับในช่วง AI capex cycle**
Goldman Sachs และ Morgan Stanley ต่างบันทึก pattern ว่า Hyperscaler ที่ raise capex guidance ใน earnings season มักเจอ AH sell-off แม้ EPS beat ("capex overhang discount") — ไม่ใช่ noise สุ่ม แต่เป็น repricing ของ near-term FCF compression ตราบที่ Mag7 ยังอยู่ใน capex ramp cycle (2025–2027) pattern นี้มีโอกาสซ้ำ

**3. AH weighted net ≥ 0pp เป็น threshold ที่ "ง่ายพอ" แต่มีความหมาย**
ไม่ได้บังคับว่าทุกเจ้าต้อง AH บวก — แค่ผลรวม weighted เป็น flat หรือบวก วันที่ GOOGL +7.05% (weight 6%) ชดเชย META -7% (weight 5.5%) ได้ net ก็ยัง trigger ได้ Threshold นี้กรอง case ที่ "negative narrative ชนะ EPS beat" ออกโดยตรง โดยไม่ over-engineer

### Suggested rule

```
QQQ Setup 3 trigger (ปรับปรุง):

Gate 1 (เดิม): ≥3/4 Mag7 (MSFT, AMZN, GOOGL, META) รายงาน GAAP EPS beat

Gate 2 (เพิ่ม): AH weighted net ≥ 0pp
  คำนวณ: Σ (AH% × QQQ weight) สำหรับ Mag7 ที่รายงานวันนั้น
  Source: AH close prices จาก Yahoo Finance หลัง earnings session (~8:30pm ET)

ถ้า Gate 1 AND Gate 2 → Long QQQ เช้าวันถัดไป
ถ้า Gate 1 pass แต่ Gate 2 fail → void setup นั้น (ไม่เข้า)
```

### Best-case outcome if we follow this

ใน 5 earnings seasons ถัดไป: setup เพิ่ม precision จาก ~60% win rate (GAAP only estimate) ไปที่ ~70–75% — ตัวเลขที่ทำให้ผ่าน go-live threshold (≥40% required) ก่อนเดือน 7 ตามแผน ในเงินจริง 10K first allocation: false positive ที่หลีกเลี่ยงได้ (เช่น Apr 29 pattern) หมายถึงไม่เสีย 5K ต่อ trade ที่ไม่ควรเข้า

### Risks you acknowledge

| Risk | Mitigation |
|---|---|
| 1 case study ยังน้อยเกินไป — อาจ over-fit | ใช้เป็น paper trading rule ก่อน; backtest เมื่อมี 3+ cases |
| AH net บวกเล็กน้อย (+0.05pp) อาจ not meaningful | พิจารณา raise threshold เป็น ≥+0.10pp หลังมี data 3+ cases |
| Miss entry ที่ดีจริง — วันที่ GAAP beat แต่ AH slightly negative แล้ว open gap up | ยอมรับได้ในช่วง paper trade; เน้น precision ก่อน recall |
| ซับซ้อนขึ้น — ต้อง calculate weighted net | คำนวณในตาราง AH scorecard ที่มีอยู่ใน pre-market brief แล้ว |
