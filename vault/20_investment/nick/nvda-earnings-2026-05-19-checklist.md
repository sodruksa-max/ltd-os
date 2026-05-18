---
type: nick-earnings-checklist
ticker: NVDA
event: Q1 FY2027 Earnings (post-close 2026-05-19)
decision_due: 2026-05-20 pre-market
---

# NVDA Q1 FY2027 Earnings Checklist

**รายงานหลัง market close วันนี้ — ตรวจ checklist นี้คืนนี้หรือเช้าพรุ่งนี้ก่อนตลาดเปิด**

---

## ตัวเลขที่ต้องดูก่อน (ภายใน 5 นาทีแรก)

| ตัวเลข | สิ่งที่ต้องหา | Threshold |
|---|---|---|
| EPS Adjusted | Beat vs consensus | > $0.88 = beat |
| Revenue | Data center segment | > $43B total / DC > $38B = strong |
| Q2 FY2027 Guidance | Revenue guide | > $45B = thesis intact |
| Blackwell mention | Demand language | "strong / accelerating / record" = bullish |
| Hyperscaler language | AWS/Azure/Google/Meta capex | "increasing / committed" = bullish |
| Gross Margin | Trajectory | > 71% = intact; < 69% = concern |
| China/Export | Any new restriction mention | อะไรก็ตาม = flag ทันที |

---

## Decision Tree (รัน /nick-weekly ย่อหลังผลออก)

### Scenario A — NVDA beats + raises (guidance ↑)
- ✅ T1 thesis gate CLEARED
- Action: **BUY NVDA 1 share** ราคา market open May 20 (~$222–$250 range est.)
- Cap ต้องตรวจก่อนซื้อ: HIGH = 15% × NAV × VIX-multiplier
  - NAV ≈ $2,320 | VIX-mult ~0.45x → HIGH cap = ~$157
  - **⚠️ NVDA ~$222 ยังเกิน HIGH cap — ต้องรอ NAV เพิ่มหรือราคา NVDA ลง**
  - หากราคา NVDA ≤ $157 หลัง earnings → BUY 1 share ได้เลย
  - หากราคา NVDA > $157 → WATCH only, เพิ่มใน watchlist สำหรับ NAV ≥ $2,972

### Scenario B — NVDA in-line (meets consensus, neutral guidance)
- ✅ T1 thesis intact (no kill)
- Action: HOLD CASH — ไม่ซื้อจนกว่าจะมี guidance ที่แข็งแกร่งกว่านี้
- ยังคง WATCH NVDA สำหรับ Week 3+ เมื่อ NAV โต

### Scenario C — NVDA miss หรือ guidance cut
- ❌ T1/T2 thesis AT RISK
- Action: **HOLD ALL CASH — ห้ามซื้อชื่อ AI capex ทั้งหมด** (AVGO, CRDO, ARM ฯลฯ)
- Check IONQ: quantum decorrelated จาก AI capex → kill conditions ไม่กระทบโดยตรง → HOLD IONQ
- รัน `/nick-weekly` ทันทีเช้าวัน May 20 พร้อม earnings data

---

## Kill Condition Link — ตรวจจากผล

| Kill Condition | Source thesis | Check |
|---|---|---|
| Hyperscaler capex guidance ↓ | T1 AI Capex | earnings call transcript |
| Blackwell demand miss vs expectations | T1 | earnings release + guidance |
| Gross margin compression < 68% | T2 Semicon Moats | earnings release |

---

## Post-earnings Action (วัน May 20 เช้า)

```
รัน: /stock-content NVDA --focus earnings-kill-check
```

แล้วอัปเดต nick_state.json + nick-soul.md ตาม scenario ที่เกิดขึ้นจริง

---

*Current NVDA signal (2026-05-19): SETUP — RSI NEUTRAL / MA NEAR / RS STRONG*
*Position cap at current NAV ($2,319.88): HIGH = ~$157 | NVDA ~$222 → impractical*
*Do NOT execute NVDA buy without recalculating cap on earnings day*
