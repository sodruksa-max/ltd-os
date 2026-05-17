---
type: compression-guidelines
updated: 2026-05-18
source: arXiv:2510.00615 (ACON — Oct 2025)
purpose: ระบุ section ที่ compress ได้ vs ห้าม compress — load ก่อน /condense หรือ agent summary
---

# Compression Guidelines

*Load ก่อนใช้ /condense หรือก่อน agent summarize context ที่ยาว — ห้าม compress ส่วนที่ mark UNSAFE*

---

## UNSAFE to Compress (ห้ามตัด ห้าม paraphrase)

| Section type | เหตุผล |
|---|---|
| Kill conditions (metric + threshold) | Paraphrase เปลี่ยน threshold → decision error |
| Exact prices (entry, stop, target) | ตัวเลขต้อง exact — approximation = wrong trade |
| TRADING_RULES.md rules | กฎที่อ้างอิง source paper — อย่า rephrase |
| Contradiction registry entries | ข้อขัดแย้งต้อง verbatim ไม่ then สรุปใหม่ |
| Savant numbers (verified exact metrics) | verified once — ห้ามลดความ exact |
| Behavior names (A1-D3 codes) | reference codes — ถ้า compress หาย = ไม่รู้ว่าหมายถึงอะไร |
| Earnings dates + EPS estimates | วันและตัวเลข precise — compression error = wrong timing |
| API keys / secret references | ไม่ต้องอธิบาย |

---

## SAFE to Compress (compress ได้ — ลด token โดยไม่เสีย fidelity)

| Section type | วิธี compress |
|---|---|
| Narrative explanation ใน pre-market | ตัดเหลือ 1-2 ประโยค — ใจความหลักเท่านั้น |
| Technical term definitions (parenthetical) | ตัดออกหลังนิยามครั้งแรก — ไม่ต้องซ้ำทุก section |
| Repeated headers + boilerplate | ตัดออกถ้าซ้ำกัน (เช่น "Source: macro-snapshot.py" ไม่ต้องทุกบรรทัด) |
| Script output raw text | keep ตัวเลข + labels, ตัด verbose description |
| Polymarket section ถ้า unverified | `[Polymarket: unverified — skip]` แทน table ว่าง |
| EXTENDED tickers (RSI >70) | group เป็น 1 บรรทัด แทนรายการ |
| Scenario playbook narrative | ตัดเหลือ trigger + sectors + indicator (ตัด "มือใหม่" explanation) |
| Catalyst descriptions ที่ไม่มี impact วันนี้ | ตัดลงเหลือ ticker + date + event name เท่านั้น |

---

## Session Context Compression (เมื่อ context >70%)

**ลำดับการ compress:**

1. ตัด script raw output ที่ embedded ใน brief (macro-snapshot, news-snapshot text blocks) — ข้อมูลนี้ใช้แล้ว ไม่ต้อง keep
2. ตัด cognitive layer outputs ที่ clean/clear (1-line entries) — เก็บแต่ triggered items
3. ตัด sector flow narrative — เก็บแค่ Leading/Improving labels
4. ตัด scenario playbook narrative ให้เหลือ bullet สั้น
5. Keep: kill conditions, exact prices, Most Likely scenario, position size modifier, setup triggers

**ห้ามตัด:** kill conditions, exact prices, TRADING_RULES references, setup triggers/stops

---

## Vault File Compression (เมื่อ /condense)

| File | Compressible | Keep verbatim |
|---|---|---|
| THESIS_TRACKER.md | narrative sections | T# name + tickers + kill conditions |
| OUTCOMES.md | context/narrative | entry/exit prices + P&L + lessons |
| DECISIONS.md | rationale prose | decision date + outcome + rule added |
| nick-soul.md | examples/anecdotes | principles + standing rules |
| insight-atoms/ | context sentences | insight statement + source |

---

## ACON Update Protocol

เมื่อ compressed output fail (agent ตัดสินใจผิดเพราะ context ขาด):
1. ระบุ section ที่ถูกตัดออกและทำให้ fail
2. เพิ่ม section นั้นใน UNSAFE table ด้านบน
3. commit: `memory: update compression-guidelines — add unsafe section [date]`
