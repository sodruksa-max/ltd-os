# Pre-Market Brief — 2026-05-05 (วันอังคาร)
*ดึงข้อมูลสดทุกตัวเลข ระบุ source ทุกจุด ขัดแย้งระหว่าง source แสดงชัดเจน*

---

📋 Lessons from 2026-05-04:
1. **Binary geopolitical event = cap confidence at Low เสมอ** — Iran headline สามารถพลิก 180° ข้ามคืนได้ ไม่ว่า signal อื่นจะบอกอะไร
2. **10Y Yield rate-of-change สำคัญกว่าระดับ** — +21bps ในวันเดียวคือ stagflation signal; เพิ่ม bps-change ใน tracker
3. **Gold/TLT อาจร่วงแม้ตลาดลง** — ถ้า DXY แข็ง + oil สูงพร้อมกัน safe haven bid ชนะไม่ได้; correlation breakdown watch

---

## 📊 ภาพรวมวันนี้ (อ่านก่อน — สำหรับมือใหม่)

> วานนี้ (จันทร์) ตลาดหุ้นอเมริการ่วง -0.41% หลังอิหร่านยิงขีปนาวุธ 12 ลูกเข้าโจมตีโครงสร้างพื้นฐานน้ำมันของ UAE ราคาน้ำมันพุ่ง +3.4% และนักลงทุนตื่นตกใจ วันนี้ฟิวเจอร์ส (ราคาที่ตลาดคาดก่อนเปิดจริง) ชี้ขึ้นเล็กน้อย +0.15-0.37% แสดงว่าตลาดพยายามเด้งกลับ แต่น้ำมันยังสูง ($104/บาร์เรล) และสถานการณ์อิหร่าน-UAE ยังไม่จบ ความไม่แน่นอนสูง ไม่ใช่วันที่เหมาะกับการเพิ่ม position ใหม่มากนัก แต่ถ้ามีแผน DCA ระยะยาวอยู่แล้ว วันนี้ไม่ใช่วันที่ต้องตื่นตระหนก

---

## Futures

| Index | ระดับ | เปลี่ยนแปลง | Source |
|---|---|---|---|
| S&P 500 (ES=F) | 7,242.75 | +0.17% | macro-snapshot.py (direct HTTP) |
| Nasdaq-100 (NQ=F) | 27,848.25 | +0.26% | macro-snapshot.py (direct HTTP) |
| Dow Jones (YM=F) | 49,152.00 | +0.15% | macro-snapshot.py (direct HTTP) |
| Russell 2000 (RTY=F) | 2,815.10 | +0.37% | macro-snapshot.py (direct HTTP) |

**Gap Analysis:**
- Futures ทุกตัวชี้ขึ้นเล็กน้อย +0.15-0.37% → สัญญาณตลาดพยายามเด้งกลับหลังวานร่วง
- SPY ETF pre-market: $717.80 (ต่ำกว่า close เมื่อวาน $718.01 เล็กน้อย) แต่ futures ชี้ขึ้น → divergence เล็กน้อย
- โดยรวม Cash และ Futures ชี้ทิศทางเดียวกัน (บวกเล็กน้อย) — ไม่มี gap นัยสำคัญ momentum consistent

---

## ตัวชี้วัด Macro

| ตัวชี้วัด | ค่า | เปลี่ยนแปลง | ความหมายในทางปฏิบัติ | Source |
|---|---|---|---|---|
| VIX (ดัชนีความกลัว — ยิ่งสูงยิ่งตื่นตระหนก) | 18.29 | +7.65%† | โซน "ระวัง" (15-25) ยังไม่ panic แต่ VXX (VIX futures ETF) +1.02% วันนี้ → VIX จะเปิดสูงขึ้นเล็กน้อย | ^VIX / Alpaca |
| 10Y Yield (ผลตอบแทนพันธบัตรรัฐบาล 10 ปี — สูง = ดอกเบี้ยแพง) | 4.446% | +1.55% / ≈+7bps | ดอกเบี้ยยังสูง กดดันหุ้นเติบโต (tech, QQQM) ต่อเนื่อง; วานขึ้น +21bps ครั้งเดียว วันนี้ชะลอลง | ^TNX / Alpaca |
| WTI (น้ำมันดิบสหรัฐ) | $104.33 | **-1.96%** | น้ำมันให้คืน -2% จากที่พุ่ง +3.4% เมื่อวาน — ตลาดเริ่ม price in ความกลัวบางส่วนออก แต่ยังสูงกว่าก่อน Iran attack | CL=F / Alpaca |
| Brent (น้ำมันดิบโลก) | $113.44 | -0.87% | ยังสูง; ⚠️ ดู conflict section ด้านล่าง | BZ=F / Alpaca |
| Gold (ทองคำ — สูง = นักลงทุนหนีความเสี่ยง) | $4,554.70 | +0.78% | ทองเด้งกลับหลังร่วง -2.01% เมื่อวาน; safe haven demand กลับมาบางส่วน; ⚠️ ดู conflict section | GC=F / Alpaca |
| DXY (ดัชนีความแข็งค่าของดอลลาร์ — สูง = ดอลลาร์แข็ง → กดตลาดเกิดใหม่) | 98.54 | +0.07% | ดอลลาร์แข็งนิดหน่อย ยังกดดันหุ้นต่างประเทศและทองบ้าง | DX-Y.NYB / Alpaca |

†VIX +7.65% คือ change ของ close เมื่อวาน (จาก ~16.98 → 18.29); VIX cash index ไม่ trade pre-market → ค่าปัจจุบัน = close ล่าสุด

---

## Alpaca Macro Snapshot

```
## Macro Snapshot
*2026-05-05 13:03 | Alpaca (US ETFs) + Yahoo Finance direct HTTP (macro)*

### US ETF Proxies (Alpaca)
| ETF | Proxy | Price | Change | Signal |
|---|---|---|---|---|
| SPY | S&P 500 | $717.80 | -0.40% | |
| QQQM | Nasdaq-100 | $276.96 | -0.21% | |
| IWM | Russell 2000 | $277.62 | -0.59% | risk- |
| VXX | VIX proxy | $28.69 | +1.02% | fear rising |
| TLT | Bonds 20Y | $84.98 | -0.74% | YIELD+ |
| USO | WTI Oil | $147.56 | +3.33%* | *yesterday's change |
| UUP | Dollar (DXY) | $27.48 | +0.24% | |
| GLD | Gold | $414.26 | -2.11%* | *yesterday's change |

*หมายเหตุ: USO/GLD % change สะท้อน performance เมื่อวาน — ดู conflict section*

Quick read: SPY -0.4% | TLT -0.7% yield up | WTI $104.33 (-2.0%) | VIX 18.3 [CAUTION]
```

---

## Alpaca News Snapshot

```
## News Snapshot
*2026-05-05 13:03 | Alpaca News API | Last 12h*

### Geopolitical (market-relevant)
- [magnitude: สูง] UAE Air Defence Engaged 12 Ballistic Missiles, 3 Cruise Missiles, 4 UAVs
  from Iran on May 4 → 3 moderate injuries | ผลกระทบ: oil, safe haven | 19:06 UTC
- [magnitude: กลาง] Bernie Sanders Calls For Windfall Profits Tax on Oil Companies
  amid Iran War | ผลกระทบ: oil policy | 04:44 UTC
- [magnitude: กลาง] Bitcoin, Ethereum Surge Amid Iran War Flareup | 02:18 UTC
- [magnitude: ต่ำ] Maersk Vessel Exits Persian Gulf Under US Military Escort | 20:15 UTC
- [magnitude: ต่ำ] Chevron 'Concerned' Over Hormuz Transit as US, Iran Trade Fire | 19:17 UTC

### Fed / Macro: ไม่มีข่าวใหม่
### Earnings / Corporate: ไม่มีข่าวใหม่
```

---

## ⚠️ ข้อมูลขัดแย้งที่พบ

| # | ตัวชี้วัด | ค่า Source A | ค่า Source B | สาเหตุ | ใช้ค่าไหน |
|---|---|---|---|---|---|
| 1 | Gold | GLD ETF -2.11% ($414.26) | GC=F futures +0.78% ($4,554.70) | GLD สะท้อน performance เมื่อวาน (May 4 gold ร่วง); GC=F คือ pre-market วันนี้ (ทองเด้งกลับ) | ใช้ GC=F +0.78% เป็นทิศทางปัจจุบัน |
| 2 | Oil | USO ETF +3.33% ($147.56) | CL=F (WTI) -1.96% ($104.33) | USO สะท้อน Iran surge เมื่อวาน; WTI futures วันนี้กำลัง give back | ใช้ CL=F -1.96% เป็นทิศทางปัจจุบัน |
| 3 | VIX | ^VIX 18.29 (+7.65%) | VXX +1.02% วันนี้ | VIX cash close เมื่อวาน; VXX futures trade pre-market → VIX จะเปิดสูงกว่า 18.29 เล็กน้อย | ใช้ 18.29 เป็น base; คาด open ~18.5-19 |

---

## Catalyst คืนที่ผ่านมา

- **Geopolitical:** อิหร่านยิง 12 ขีปนาวุธ + 3 cruise missile + 4 UAV เข้าโจมตี UAE เมื่อ May 4 → ผลกระทบ: oil (WTI +3.4% เมื่อวาน) / safe haven demand / Strait of Hormuz risk → magnitude: **สูง** (ยังไม่ resolved)
- **Hormuz shipping:** Maersk ออกจาก Persian Gulf ภายใต้การคุ้มกันทหารสหรัฐ; Chevron แสดงความกังวล → shipping disruption เริ่มส่งผลจริง
- **Policy risk:** Bernie Sanders เรียกร้อง windfall profits tax บริษัทน้ำมัน → ถ้า pass จะกด XLE ระยะกลาง
- **Fed / Macro:** ไม่มีข่าวใหม่ — ตลาดรอ NFP วันศุกร์ May 8
- **Earnings:** ไม่มีรายงานสำคัญวันนี้

---

## Polymarket Sentiment (อ้างอิงเท่านั้น)

| ตลาด / คำถาม | Odds ปัจจุบัน | หมายเหตุ |
|---|---|---|
| Strait of Hormuz traffic กลับปกติ ภายใน May 31 | **Yes: 16% / No: 84%** | crowd คิดว่าการปิดกึ่งๆ จะยืดยาว — risk ยังอยู่ |
| Iran ตกลง shipping ปกติ ภายใน May 31 | **Yes: 9% / No: 91%** | crowd ไม่เชื่อว่า Iran จะถอย |
| SPX May 5 daily direction | ไม่พบ market live สำหรับวันนี้ | ดู polymarket.com/finance/daily |

*Polymarket = crowd sentiment proxy เท่านั้น — ไม่ใช่การพยากรณ์; ใช้เป็น sanity check กับ scenario ด้านล่าง*
*Crowd: Hormuz จะ disrupted ต่อไป 84% → consistent กับ scenario oil ยังแพง*

---

## Earnings วันนี้

ไม่มีรายงาน earnings สำคัญ (barometer stocks) วันนี้ — ตลาดรอ NFP วันศุกร์ May 8

---

## ปฏิทินสัปดาห์นี้

- **วันนี้ (อังคาร May 5):** ไม่มี major event; จับตา Iran-UAE headlines
- **พุธ May 6:** ตรวจ geopolitical updates; อาจมี Fed speakers
- **พฤหัส May 7:** ISM Services data (ถ้าออก)
- **ศุกร์ May 8:** **NFP (Non-Farm Payrolls — รายงานการจ้างงาน)** — event สำคัญที่สุดสัปดาห์นี้; ผลจะกำหนด Fed path
- **ยาวๆ:** Iran-UAE ceasefire หรือ escalation ใหม่ — watch closely

---

## Scenario Playbook

สามสถานการณ์สำหรับวันนี้ — ไม่ใช่การพยากรณ์ แต่เป็นกรอบเตรียมรับมือ

### กรณี Bullish (ตลาดขึ้น)
- **Trigger:** ข่าว Iran-UAE ceasefire / การเจรจา; WTI หล่นใต้ $100; VIX ลงใต้ 17; Nasdaq futures ยืนเหนือ NQ 28,000
- **Sectors ที่ได้ประโยชน์:** QQQM/QQQ (tech กลับมา risk-on) — XLK (เทคโนโลยี); QQQM ที่ตอนนี้ใกล้ PP $277.07 จะ break R1 $278.77 ขึ้นไป
- **Sectors ที่เสียประโยชน์:** XLE (พลังงาน — น้ำมันร่วงถ้า Iran risk จบ); GLD (ทอง — safe haven demand หด)
- **ตัวชี้วัดที่ต้องดู:** WTI ยืนใต้ $100 | VIX ลงใต้ 17 | QQQM ทะลุ R1 $278.77
- **สรุปสำหรับมือใหม่:** ตลาดกลับมามีความหวัง หุ้น tech ฟื้นตัว เหมาะกับการเข้า DCA ตามแผน

### กรณี Base (น่าจะเป็นไปได้สุด — ตลาดทรงตัว)
- **Trigger:** ไม่มีข่าว Iran ใหม่; น้ำมันให้คืนช้าๆ; futures บวกเล็กน้อยตามที่เห็นตอนนี้
- **Sectors ที่ได้ประโยชน์:** ไม่มีตัวชัดเจน; defensives (XLP, XLU — สินค้าจำเป็นและสาธารณูปโภค) อาจ hold ดีกว่า
- **Sectors ที่เสียประโยชน์:** XLY (สินค้าฟุ่มเฟือย — yield สูงกดดัน); IWM (small-cap อ่อนแอกว่า)
- **ตัวชี้วัดที่ต้องดู:** SPY ยืนเหนือ S2 $717.60 | QQQM ยืนเหนือ S1 $275.85 | VIX ใต้ 20
- **สรุปสำหรับมือใหม่:** ตลาดรอข่าว Iran ไม่มีทิศทางชัด เหมาะกับการนั่งดูก่อนมากกว่าลงมือ

### กรณี Bearish (ตลาดลง)
- **Trigger:** ข่าว Iran escalation ใหม่ (Hormuz ปิดจริง / โจมตีเพิ่ม); WTI พุ่งเหนือ $108; VIX ทะลุ 22; yield 10Y เกิน 4.55%
- **Sectors ที่ได้ประโยชน์:** XLE (พลังงาน — น้ำมันแพง); GLD (ทอง — safe haven); UVXY (VIX leveraged — อ้างอิงเท่านั้น)
- **Sectors ที่เสียประโยชน์:** QQQM/QQQ (tech โดนหนัก — high valuation + yield สูง); XLY; IWM
- **ตัวชี้วัดที่ต้องดู:** WTI เหนือ $108 | VIX เหนือ 22 | SPY หลุด S2 $717.60
- **สรุปสำหรับมือใหม่:** ถ้าเกิดขึ้น ควรระวัง ลดความเสี่ยง อย่าเพิ่ม position ใหม่ รอความชัดเจนก่อน

### Most Likely Scenario

**Event Risk Check:**
- Iran-UAE war / Hormuz (geopolitical ยัง unresolved) = 1 event
- ไม่มี FOMC, ไม่มี Mag7 earnings, ไม่มี CPI/NFP วันนี้
→ **1 event active** → ปกติ confidence สูงสุด medium ได้
→ **แต่ yesterday's lesson:** binary geopolitical = cap ที่ Low เสมอ → **confidence = Low**

- **เลือก: Base**
- **Confidence: Low** (ตาม lesson: Iran ยัง binary — Polymarket 84% บอก Hormuz disrupted ต่อ แต่ตลาดยังพยายามเด้ง)
- **เหตุผล 3 ข้อ:**
  1. Futures +0.15-0.37% ทุก index; oil ให้คืน -2% → แรงกดดันหลักของวานเริ่มคลาย (Macro / Futures)
  2. Polymarket 84% ว่า Hormuz disrupted → crowd ยัง risk-off แต่ไม่ panic; ไม่มี earnings catalyst วันนี้ (Catalyst / Polymarket)
  3. VIX 18.29 ไม่ขยับมาก; VXX +1.02% เล็กน้อย → fear เพิ่มขึ้นช้า ไม่ใช่ surge (Macro / Event Calendar)
- **อะไรจะทำให้ผิด:**
  1. ข่าวอิหร่านโจมตี Hormuz หรือ UAE เพิ่มเติม → flip ไป Bearish ทันที
  2. Yield 10Y ทะลุ 4.55% + oil กลับขึ้นเหนือ $108 พร้อมกัน → stagflation signal → flip Bearish

---

## กรอบความเสี่ยง (Risk Framework)

### ความเสี่ยงสูงสุด 3 อันดับวันนี้ + Correlation Breakdown

| อันดับ | ความเสี่ยง | โอกาสเกิด | ผลกระทบ | เครื่องมือป้องกัน (อ้างอิงเท่านั้น) |
|---|---|---|---|---|
| 1 | Iran escalation ใหม่ (Hormuz ปิดบางส่วน / โจมตี UAE เพิ่ม) | กลาง | สูง — oil พุ่ง, yield ขึ้น, tech ร่วง | XLE long, ถือ cash; ลด QQQM |
| 2 | 10Y Yield rate-of-change เร่งขึ้น (เหนือ 4.55% วันนี้) | ต่ำ-กลาง | กลาง — กด tech/QQQM ต่อ; ไม่มี catalyst ชัดวันนี้ | TLT puts (อ้างอิงเท่านั้น); ชะลอ DCA QQQM |
| 3 | Windfall profits tax ผ่าน (Bernie Sanders bill) | ต่ำ | กลาง-สูง (เฉพาะ XLE) | หลีกเลี่ยง new XLE long วันนี้ |
| ⚠️ | **Correlation breakdown** — oil↑ + yield↑ + Iran attack ใหม่ พร้อมกัน | ต่ำ แต่ tail risk | **สูงมาก** — defensive ไม่ช่วย (เหมือนเมื่อวาน GLD+TLT+SPY ร่วงพร้อมกัน) | ถือ cash เท่านั้น; ลด position size ทุกประเภท |

> **หมายเหตุ Row ⚠️:** เมื่อวาน GLD -2.01% + TLT -0.75% + SPY -0.41% ร่วงพร้อมกัน เป็น early signal ของ correlation breakdown ถ้าเกิดซ้ำวันนี้ — cash เท่านั้น

**Reminder เรื่องขนาด position:**
- VIX 18.29 → โซนระวัง (15-25); ลดขนาด position ลง 20-30% จากปกติ
- Iran ยัง unresolved → VIX อาจ spike ได้ตลอดเวลา
- วันนี้ไม่มี FOMC/CPI แต่มี geopolitical tail risk → position ขนาดปกติ + wide stop

---

## Key S/R Levels (จาก sr-levels.py)

```
### SPY | Last close: $718.01 | 52W: H=$724.87 / L=$556.04

Pivot Points (Classic):
R3: $727.92 (+1.4%) | R2: $726.40 (+1.2%) | R1: $723.52 (+0.8%)
PP:  $722.00 (+0.6%)
S1:  $719.12 (+0.2%) | S2: $717.60 (-0.1%) | S3: $714.72 (-0.5%)

SPY ปัจจุบัน $717.80 = ต่ำกว่า S2 ($717.60) เล็กน้อย → แนวรับสำคัญอยู่ที่ S3 $714.72

Swing Levels (30 วัน):
High: $712.39 (Apr 17) | Low: $708.37 (Apr 29) | Low: $702.28 (Apr 23)

### QQQM | Last close: $277.05 | 52W: H=$278.65 / L=$196.36

Pivot Points (Classic):
R3: $281.69 (+1.7%) | R2: $279.99 (+1.1%) | R1: $278.77 (+0.6%)
PP:  $277.07 (0.0%)
S1:  $275.85 (-0.4%) | S2: $274.15 (-1.0%) | S3: $272.93 (-1.5%)

QQQM ปัจจุบัน $276.96 = ใกล้ PP $277.07 มาก → neutral pivot zone
Entry DCA ที่นี่: upside R1 $278.77, downside S1 $275.85 (stop ถ้าหลุด)
```

---

## Trade Setups (เพื่อการศึกษาเท่านั้น)

> **DISCLAIMER: The setups below are educational frameworks based on publicly available technical and fundamental data. They are NOT financial advice, NOT personalized recommendations, and NOT a solicitation to buy or sell any security. All trading involves risk of loss. Do your own research and consult a licensed advisor before making any investment decision.**

---

### Setup 1 — QQQM | ระยะเวลา: Position (DCA Entry)

**เหตุผล:** QQQM อยู่ที่ PP $277.07 หลังร่วง -0.21% เมื่อวาน; futures Nasdaq +0.26% ชี้ว่าจะเปิดใกล้ pivot zone; สำหรับ DCA เกษียณระยะยาว นี่คือ entry zone ที่ยอมรับได้

- **ถ้า:** QQQM เปิดเหนือ S1 $275.85 AND VIX ไม่ spike เหนือ 20 ใน 1 ชั่วโมงแรก → entry zone valid
- **แล้ว:** DCA entry ตามแผน; คาดว่าจะเคลื่อนไปทดสอบ R1 $278.77 ถ้าไม่มีข่าว Iran ใหม่
- **ล้มเลิกถ้า:** QQQM หลุด S1 $275.85 อย่างชัดเจน → รอให้ลงไปทดสอบ S2 $274.15 ก่อนแล้ว re-evaluate; ถ้าหลุด S2 $274.15 → hold cash รอ stabilization
- **ระยะเวลา:** Position (DCA ระยะยาว — ไม่มี time-stop สำหรับ position trade)
- **Catalyst สนับสนุน:** Futures Nasdaq +0.26%; oil ให้คืน -2% ลด inflation pressure เล็กน้อย; ถ้า DCA ทุกเดือนไม่ว่าราคาจะเป็นอะไร entry ตรงนี้คือ neutral-to-fair

---

### Setup 2 — XLE (Energy Sector ETF) | ระยะเวลา: Swing (2-3 วัน)

**เหตุผล:** Oil ให้คืน -1.96% วันนี้หลังพุ่ง +3.4% เมื่อวาน; ถ้า Iran escalation ไม่เพิ่ม oil premium จะ fade ต่อ และ XLE จะ underperform

- **ถ้า:** WTI (CL=F) ยืนใต้ $105 หลังเปิดตลาด 30 นาที AND ไม่มีข่าว Iran escalation ใหม่หลัง 09:30am ET
- **แล้ว:** XLE มีแนวโน้ม give back บางส่วนของ +0.92% เมื่อวาน; watch ระดับ $58.50-$59.00 เป็น near-term target
- **ล้มเลิกถ้า:** WTI กลับขึ้นเหนือ $107 (Iran escalation ใหม่) → XLE จะ surge อีกรอบ setup void
- **ระยะเวลา:** Swing (2-3 วัน)
- **Time-stop:** ถ้าไม่เกิด trigger ภายใน 10:30am ET → setup void ไม่เข้า; ถ้าเข้าแล้วและ oil ไม่ fade ภายใน 12:00pm ET → ออก
- **Catalyst สนับสนุน:** Polymarket 84% Hormuz disrupted = oil ยังจะสูง; แต่ short-term oil ให้คืนและ Bernie Sanders tax bill เพิ่ม headwind ให้ XLE

---

### Setup 3 — TLT (พันธบัตรรัฐบาล 20Y ETF) | ระยะเวลา: Swing (Pre-NFP)

**เหตุผล:** 10Y yield ที่ 4.446% สูงกว่าก่อน Iran attack; ถ้าวันนี้ yield stabilize (ไม่เร่งขึ้น) TLT อาจ stabilize ก่อน NFP ศุกร์ May 8 ซึ่งจะเป็น real catalyst

- **ถ้า:** 10Y yield ไม่ขยับเหนือ 4.47% วันนี้ (yield stabilizes) AND oil ยังให้คืน → TLT ($84.98) อาจ hold เหนือ $84.50
- **แล้ว:** รอดูทิศทาง NFP ศุกร์; ถ้า NFP อ่อน → yield ลง → TLT ขึ้น → entry post-NFP
- **ล้มเลิกถ้า:** 10Y yield ทะลุ 4.55% (stagflation acceleration) → TLT จะยังลงต่อ setup void
- **ระยะเวลา:** Swing (2-4 วัน; entry trigger post-NFP ศุกร์)
- **Catalyst สนับสนุน:** NFP วันศุกร์ May 8 คือ event หลัก; ถ้า jobs อ่อน → Fed cut คาดการณ์ → yield ลง → TLT ขึ้น

---

*Sources:*
- *macro-snapshot.py + news-snapshot.py + sr-levels.py — Alpaca API / direct HTTP Yahoo Finance (2026-05-05 13:03)*
- *Polymarket: polymarket.com/finance/daily | polymarket.com/event/strait-of-hormuz-traffic-returns-to-normal-by-end-of-may*
- *Yesterday review: vault/20_investment/_journal/2026-05-04-review.md*
