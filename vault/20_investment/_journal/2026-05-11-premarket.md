# Pre-Market Brief — 2026-05-11 (วันจันทร์)
*ดึงข้อมูลสดทุกตัวเลข | ระบุ source ทุกจุด | ขัดแย้งระหว่าง source แสดงชัดเจน*
*เวลารัน scripts: 19:22 ICT (08:22 ET) — ก่อนตลาดเปิด*

---

## 📊 ภาพรวมวันนี้ (อ่านก่อน)

วันนี้มีภาพแบ่ง 2 ขั้ว: หุ้นกลุ่ม AI/Semicon/Space วิ่งขึ้นแรงมาก (MU +15%, AMD +11%, RKLB +34%) ขณะที่ตลาดรวม (Futures) ยังแทบไม่ขยับ (-0.1%) การที่ Trump ปฏิเสธข้อเสนอสันติภาพอิหร่านทำให้ราคาน้ำมันพุ่งใกล้ $100 — สร้างแรงกดต้นทุน แต่ยังไม่ panic ตลาด VIX (ดัชนีความกลัว) อยู่ที่ 18.18 ระดับ "ระวัง" ไม่ใช่ panic และอยู่ใน backwardation (ความกลัวระยะสั้นสูงกว่าระยะยาว) ความเสี่ยงหลักวันนี้คือ ASTS มีผลประกอบการ และ **พรุ่งนี้มีตัวเลข CPI (เงินเฟ้อ)** ที่อาจกระทบตลาดหนัก — ให้ระวังการเพิ่ม position ใหม่ก่อนข้อมูลนั้นออก

---

## Futures (ราคาที่ตลาดคาดก่อนเปิดจริง)

| Index | ระดับ | เปลี่ยนแปลง | Source |
|---|---|---|---|
| S&P 500 (ES=F) | 7,410.00 | **-0.12%** | macro-snapshot.py / direct HTTP |
| Nasdaq-100 (NQ=F) | 29,301.75 | **-0.10%** | macro-snapshot.py |
| Dow Jones (YM=F) | 49,645.00 | **-0.09%** | macro-snapshot.py |
| Russell 2000 (RTY=F) | 2,866.30 | **-0.05%** | macro-snapshot.py |

**Gap Analysis:**
ราคาปิดวันก่อน (close): SPY $737.62, QQQM $292.82 — ทั้งคู่แข็งแกร่ง
Futures วันจันทร์: ลบเล็กน้อย -0.1%
→ Cash ปิดดี แต่ Futures เปิดอ่อน → สัญญาณว่า Iran news กดทับ sentiment ข้ามสุดสัปดาห์ — **ไม่ใช่ institutional selling แต่เป็น geopolitical caution** ระวังอย่า over-read ความอ่อนนี้

---

## ตัวชี้วัด Macro

| ตัวชี้วัด | ค่า | ความหมายในทางปฏิบัติ | Source |
|---|---|---|---|
| VIX (ดัชนีความกลัว — ยิ่งสูงยิ่งตื่นตระหนก) | **18.18 (+5.76%)** | ระดับ "ระวัง" (15-25) ไม่ใช่ panic แต่กำลังสูงขึ้น → VIX-Rank 63rd pct → ลด position size เป็น 0.49x | macro-snapshot.py / ^VIX |
| 10Y Yield (ผลตอบแทนพันธบัตรรัฐบาล 10 ปี — สูง = ดอกเบี้ยแพง กดหุ้นเติบโต) | **4.364% (-0.64%)** | Yield ลดลงเล็กน้อย = ผ่อนแรงกดหุ้น growth ระยะสั้น; แต่ term premium ยังสูง (+0.77%) | macro-snapshot.py / ^TNX |
| WTI (น้ำมันดิบสหรัฐ) | **$98.57 (+3.30%)** | ใกล้ $100 แล้ว! Iran tension หนุน; ยิ่งแพงยิ่งเพิ่มต้นทุนธุรกิจทุกประเภท | macro-snapshot.py / CL=F |
| Brent (น้ำมันดิบโลก) | **$104.40 (+3.07%)** | สอดคล้องกับ WTI — global oil แพง; ไม่ conflict | macro-snapshot.py / BZ=F |
| Gold (ทองคำ) | **$4,676.70 (-0.93%)** ⚠️ | ทองลงแม้ risk-off — ผิดปกติ; ดู conflict section | macro-snapshot.py / GC=F |
| DXY (ดัชนีความแข็งค่าของดอลลาร์ — สูง = ดอลลาร์แข็ง กด EM) | **98.02 (+0.18%)** | ดอลลาร์แข็งขึ้นเล็กน้อย; Iran-driven safe haven bid; UUP ETF $27.33 (-0.29%) ⚠️ conflict | macro-snapshot.py / DX-Y.NYB |

---

## Alpaca Macro Snapshot

```
## Macro Snapshot — 2026-05-11 19:22

### US ETF Proxies (Alpaca)
SPY   $736.48  +0.67%   RISK+
QQQM  $292.45  +2.21%   RISK+
IWM   $284.19  +0.68%   RISK+
VXX   $28.04   +0.50%   fear rising (แต่ต่ำกว่า spot VIX spike)
TLT   $86.07   +0.49%   bond ขึ้น = yield ลง = เล็กน้อย positive growth
USO   $138.80  +2.84%   น้ำมันแพง
UUP   $27.33   -0.29%   ดอลลาร์อ่อน (⚠️ ต่างจาก DX-Y.NYB +0.18%)
GLD   $433.04  +0.32%   implied gold ~$4,330/oz (⚠️ ต่างจาก GC=F $4,676)

### Bubble Risk
- 10Y-2Y Spread: +0.77% [!] term premium สูง
- VIX9D/VIX: 0.78 backwardation [!] — ความกลัวระยะสั้น > ระยะยาว
```

---

## Alpaca News Snapshot

```
## News Snapshot — 2026-05-11 19:22

Geopolitical:
- Trump rejects "totally unacceptable" Iran peace proposal → oil +3.3%
- Yardeni ยกเป้า S&P 500 — เตือน "meltup" อาจจับนักลงทุนออฟการ์ด
- Cathie Wood: เงินเฟ้อจะ "surprise" ลดลง
- Energy Secretary: สหรัฐอยู่ใน "tremendous" position แม้ gas แพง

Fed/Macro: ไม่มีข่าวใหม่

Earnings/Corporate: ไม่มีใหม่ใน 12h ล่าสุด
```

---

## ⚠️ ข้อมูลขัดแย้งที่พบ

| จุดขัดแย้ง | ค่า A | ค่า B | เหตุผลที่น่าจะเป็น |
|---|---|---|---|
| **Gold** | GLD ETF $433.04 (+0.32%) → implied ~$4,330/oz | GC=F futures $4,676.70 (-0.93%) | Timestamp ต่างกัน (ETF = prev close; futures = real-time) + contract month ต่าง |
| **DXY** | UUP ETF -0.29% (ดอลลาร์อ่อน) | DX-Y.NYB +0.18% (ดอลลาร์แข็ง) | ETF vs index ต่าง timing — ใช้ DX-Y.NYB เป็น primary |
| **VIX** | VXX ETF +0.50% | ^VIX spot +5.76% | VXX ติดตาม 1-2 month futures ไม่ใช่ spot — ไม่ใช่ conflict จริง แต่ gap ใหญ่แสดง near-term fear spike |

---

## Catalyst คืนที่ผ่านมา / วันนี้

- **Geopolitical:** Trump ปฏิเสธข้อเสนอสันติภาพอิหร่านว่า "totally unacceptable" → ผลกระทบ: **oil พุ่งแรง (+3.3%)**, USD safe-haven bid เล็กน้อย → magnitude: **กลาง** — ไม่ใช่ escalation ใหม่ แต่ยืดเยื้อต่อ
- **Oil:** WTI ใกล้ $100 — Psychological level สำคัญ; ถ้าทะลุ $100 จะเพิ่มแรงกด inflation
- **Semicon surge:** MU +15%, AMD +11% — ข่าว Micron ใน focus; น่าจะเกี่ยวกับ HBM demand confirmation หรือ outlook แข็งแกร่ง ❓ verify
- **Space surge:** RKLB +34.2% — ใกล้ 52W high $105.62; catalyst ไม่ชัดใน news — คาดว่าเป็น contract หรือ launch milestone ❓ verify
- **ASTS earnings วันนี้:** Q1 2026 — อัปเดตสำคัญ BB7 recovery + BB8-10 timeline ห้าม hold position ข้ามผล

---

## Polymarket Sentiment (อ้างอิงเท่านั้น)

| ตลาด / คำถาม | Odds raw | Odds adjusted (−3%) | หมายเหตุ |
|---|---|---|---|
| SPY ปิดเหนือ $710 วันนี้ | 98% | 95% | ปัจจุบัน $737 — ห่างมาก |
| SPY ปิดเหนือ $735 วันนี้ | 84% | 81% | ใกล้ current price มาก — ตลาดคาดทรงตัว |
| S&P 500 open up or down (May 11) | ไม่มีตัวเลขชัด | [unverified] | Benzinga บอก futures ลงเล็กน้อย → down เล็กน้อย |

*Yes-bias correction (Reichenbach & Walther 2025): ปรับ −3% สำหรับ Yes/No markets ทุกตัว*
*Source: [Polymarket S&P](https://polymarket.com/event/spy-closes-above-on-may-11-2026) / [Benzinga](https://www.benzinga.com/markets/prediction-markets/26/05/52439256/will-sp-500-open-up-or-down-on-may-11-heres-how-polymarket-traders-lean-as-trump-rejec)*

---

## Earnings วันนี้

| Ticker | Event | หมายเหตุ |
|---|---|---|
| **ASTS** | Q1 2026 Earnings | BB7 loss recovery + BB8-10 timeline — **TODAY [ห้าม hold ข้ามผล]** |

---

## ปฏิทินสัปดาห์นี้

- **May 12 (พรุ่งนี้):** 🔴 **CPI (เงินเฟ้อ เมษายน)** — EVENT RISK ใหญ่ที่สุดสัปดาห์นี้
- **May 13:** PPI (ดัชนีราคาผู้ผลิต)
- **May 14:** LUNR earnings pre-market (rev guide $900M-$1B FY2026); BlueBird 8-10 deployment est. ~May 20
- **สัปดาห์นี้:** JD.com, Alibaba, Cisco earnings (วันไม่ชัด)

---

## Sector Universe Radar — Semicon / AI / Datacenter / Space

```
Sector 5d: SMH +11.1% | XLK +8.4% | UFO +6.1%

[EARLY★] ก่อนวิ่ง + RS แข็งกว่า SPY:
  ASML   $1,592.02  RSI 60.7 | +9.1% above MA20 | -0.2% from 52wH | RS +5.7% vs SPY
  MOD    $273.00    RSI 61.4 | +7.8% above MA20 | -5.0% from 52wH | RS +5.0% vs SPY ⚠vol-div
  BBAI   $4.18      RSI 58.2 | +7.0% above MA20 | -55.5% from 52wH | RS +9.3% vs SPY ⚠vol-div
  IONQ   $49.24     RSI 51.6 | +10.5% above MA20 | -41.8% from 52wH | RS +11.6% vs SPY ⚠vol-div
  RGTI   $18.94     RSI 46.8 | +5.9% above MA20 | -67.4% from 52wH | RS +10.4% vs SPY ⚠vol-div
  QBTS   $22.57     RSI 53.2 | +11.9% above MA20 | -51.7% from 52wH | RS +18.1% vs SPY ⚠vol-div
  QUBT   $9.60      RSI 48.0 | +4.5% above MA20 | -62.8% from 52wH | RS +3.9% vs SPY

[ALERT] เริ่มวิ่ง ยังเข้าได้:
  AVGO  $430.00  gap +4.2% | RSI 62.6 | vol 1.1x | RS -1.6%
  LRCX  $294.05  gap +2.6% | RSI 63.3 | vol 0.9x | RS +6.3% ⚠vol-div
  HPE   $31.35   gap +5.6% | RSI 71.4 | vol 1.2x | RS +7.8%

[EXTENDED] ไปไกลแล้ว ห้ามไล่ราคา:
  AMD $455.19 (+11.4% gap, RSI 80.7 overbought)
  MU  $746.81 (+15.5% gap, RSI 88.0 overbought)
  RKLB $105.47 (+34.2% gap ‼️)
  MRVL $170.13 | WDC $480 | SMCI $35.37 | DELL $260 | UCTT $87.10

[WATCH] สัญญาณผสม:
  PLTR $137.80 | ASTS $75.05 | MSFT $415.12 | KTOS $57.89
```

**สรุปจาก radar:**
- **[EARLY★] สัญญาณแข็งสุด:** ASML (near 52W high, RS ดี), MOD (datacenter cooling, RS↑↑)
- **[ALERT] เริ่มวิ่ง:** AVGO, LRCX, HPE
- **Catalyst หลักวันนี้:** Semicon surge (MU/AMD/NVDA) + Space momentum (RKLB near ATH) + ASTS earnings
- ⚠️ Quantum (IONQ/RGTI/QBTS) ทุกตัว vol-div — RS ดีแต่ volume ไม่ยืนยัน ระวัง

---

## ETF Discovery — หุ้นใหม่นอก watchlist

```
[EARLY★] นอก watchlist ที่น่าสนใจ:
  VSAT  $70.01   +5.6%  RSI 61.8 | RS↑↑ | -0.5% from 52wH (Space)
  FLY   $39.68   +22.6% RSI 44.0 | RS↑↑ | -46.2% from 52wH (Space) — gap ใหญ่ผิดปกติ
  SATS  $127.15  +3.7%  RSI 42.5 | RS↑↑ | -7.5% from 52wH (Space)
  IRDM  $41.46   +3.2%  RSI 49.1 | RS↑   | -6.5% from 52wH (Space)
```

**สรุป ETF Discovery:**
- **[EARLY★] น่าสนใจ:** VSAT — ใกล้ 52W high, RS↑↑, Space sector Improving
- **[ALERT]:** ไม่มีวันนี้ใน discovery list
- FLY +22.6% — EXTENDED แล้ว; ถ้าสนใจรอ `/stock-research FLY` ก่อน
- SATS/IRDM — coiling อยู่ ยังไม่ยืนยัน

---

## Sector Money Flow

```
Leading   : Technology (XLK) — 5d +5.9%, 20d +13.4%
Improving : Space (ROKT) — 5d +0.1%, 20d -4.7%
           Aerospace & Defense (ITA) — 5d +1.0%, 20d -10.4%
Lagging   : ทุก sector อื่น (Energy, Financials, Healthcare, Industrials ฯลฯ)
```

**สรุป:**
- **Money flowing IN:** XLK (Technology) ชัดเจน; ROKT/ITA ฟื้นตัว
- **Money flowing OUT:** XLE (Energy) แม้น้ำมันแพง — แปลก; บอกว่าตลาดไม่เชื่อ oil spike ยั่งยืน
- **Space (ROKT/ITA):** Improving — ดีขึ้น แต่ 20d ยัง negative; ระวัง FOMO

→ Setup วันนี้เลือกจาก **Technology (Leading)** และ **Space (Improving)** เท่านั้น

---

## Catalyst Calendar (21 วันข้างหน้า)

```
[TODAY]  May 11  ASTS  Q1 2026 Earnings — BB7 recovery + BB8-10 timeline
[SOON]   May 14  LUNR  Q1 2026 Earnings (pre-market 8:30am ET)
[AHEAD]  May 20  ASTS  BlueBird 8-10 ready to ship (est. ~30 days from Apr 19)
```

**[SOON] catalysts:**
- **ASTS earnings วันนี้** → ห้าม hold ASTS ข้ามผล; Day trade เท่านั้น (ถ้าจะ trade)
- **LUNR earnings พฤหัส May 14** → ถ้าสร้าง LUNR setup ใดๆ ต้องปิดก่อน May 14 AM

---

## Scenario Playbook

### กรณี Bullish (ตลาดขึ้น)
- **Trigger:** ข่าว Iran de-escalation ออกมา **หรือ** ASTS earnings ดีกว่าคาด + Nvidia/AMD demand outlook แข็งแกร่ง
- **Sectors ได้ประโยชน์:** Technology (XLK), Space (ROKT), Semicon (SMH) — กลุ่มที่ตลาดวิ่งอยู่แล้ว
- **Sectors เสียประโยชน์:** XLE (oil ลง), XLU (utilities ถูกทอดทิ้งเมื่อ risk-on)
- **ตัวชี้วัดที่ต้องดู:** VIX ลงต่ำกว่า 17 | SPY ยืนเหนือ R2 $738.87 | WTI ลงต่ำกว่า $95
- **สรุปมือใหม่:** AI/tech momentum ต่อเนื่อง นักลงทุนกล้าซื้อ หุ้นกลุ่ม semiconductor วิ่งต่อ

### กรณี Base — Most Likely (ตลาดทรงตัว rotation เข้า tech)
- **Trigger:** Futures -0.1% เปิดอ่อน แต่ tech/AI stocks วิ่งแยกตัว; Iran ยังไม่ resolve แต่ไม่ escalate; ตลาดรอ CPI พรุ่งนี้
- **Sectors ได้ประโยชน์:** Technology (Leading), Semicon/AI — rotation ชัดเจน
- **Sectors เสียประโยชน์:** Energy (ขัดสัญชาตญาณ — oil ขึ้นแต่ XLE ลง); Consumer Discretionary
- **ตัวชี้วัดที่ต้องดู:** SPY ยืนแถว PP $732.49–$738.87 | VIX ไม่เกิน 20 | WTI ไม่ทะลุ $102
- **สรุปมือใหม่:** ตลาดรวมทรงตัว แต่หุ้น AI/Semicon/Space วิ่งแยก เลือก sector ให้ถูกก่อนลงมือ

### กรณี Bearish (ตลาดลง)
- **Trigger:** WTI ทะลุ $102+ (psychological level) **และ/หรือ** ASTS earnings แย่กว่าคาดมาก **หรือ** CPI data รั่วออกมาว่าสูงกว่าคาด
- **Sectors ได้ประโยชน์:** Gold (safe haven), TLT (bonds), XLU (utilities)
- **Sectors เสียประโยชน์:** Technology, Consumer Discretionary, Small Caps
- **ตัวชี้วัดที่ต้องดู:** VIX เกิน 21 | SPY หลุด S1 $728.84 | WTI เกิน $102
- **สรุปมือใหม่:** ถ้า oil พุ่ง + CPI fears เพิ่ม → ลดความเสี่ยง อย่าเพิ่ม position

---

### Most Likely Scenario

**Event Risk Check วันนี้:**
1. ✅ ASTS earnings วันนี้ (watchlist stock)
2. ✅ Iran geopolitical ยังไม่ resolve (oil +3.3%)
3. ❌ FOMC — ไม่มี
4. ❌ CPI — พรุ่งนี้ ไม่ใช่วันนี้ (แต่ weighing on sentiment)
→ **2 active events → confidence = medium สูงสุด**

- **เลือก: Base**
- **Confidence: Medium**
- **เหตุผล:**
  1. Futures -0.1% กับ tech stocks +10-15% = rotation เข้า AI/tech ชัดเจน ไม่ใช่ broad selloff (Macro/Futures data)
  2. Iran reject peace = oil ขึ้น แต่ XLE ยัง Lagging = ตลาดไม่ panic ถือเป็น known risk ไม่ใช่ surprise (Catalyst/Polymarket)
  3. Polymarket $735 threshold = 84% → ตลาดคาด SPY ยืนระดับนี้ได้; CPI พรุ่งนี้คือ wild card ที่ป้องกัน full Bullish (Event Calendar)
- **อะไรจะทำให้ผิด:**
  1. ASTS earnings แย่มาก → กด Space sector ทั้งกลุ่ม
  2. น้ำมันทะลุ $102 + ข่าว Iran escalate → flip Bearish ทันที

---

## กรอบความเสี่ยง (Risk Framework)

### ความเสี่ยงสูงสุด 3 อันดับ + Correlation Breakdown

| อันดับ | ความเสี่ยง | โอกาสเกิด | ผลกระทบ | เครื่องมือป้องกัน (อ้างอิงเท่านั้น) |
|---|---|---|---|---|
| 1 | **CPI พรุ่งนี้สูงกว่าคาด** — เงินเฟ้อไม่ลง Fed ไม่ลดดอกเบี้ย | กลาง | สูง — กด growth stocks ทั้งกลุ่ม | TLT puts; ลด tech exposure ก่อน |
| 2 | **WTI ทะลุ $100** — Iran ยิ่งตึงเครียด oil shock | กลาง | กลาง — เพิ่มต้นทุน กด margin ทุกบริษัท | XLE long; airlines short |
| 3 | **ASTS earnings miss** — BB7 ยังไม่ฟื้น + BB8 ล่าช้า | กลาง | กลาง (Space specific) — กด ASTS/LUNR/RKLB | ไม่ hold ASTS ข้ามผล |
| ⚠️ | **Correlation breakdown** — oil $102+ + CPI surprise + Iran escalate พร้อมกัน | ต่ำ แต่ tail risk | **สูงมาก** — defensive ไม่ช่วย | ถือ cash เท่านั้น; ลด position ทุกประเภท |

> **VIX ที่ 18.18 (63rd percentile) → ลด position size เป็น 0.49x ของ base size ทุก setup วันนี้**

---

## Key S/R Levels (จาก sr-levels.py)

```
### SPY — Last close $737.62
R2 $738.87 | R1 $735.22 | PP $732.49 | S1 $728.84 | S2 $726.11
ATR14: $7.04 | Long stop: $723.53

### QQQM — Last close $292.82 (52W HIGH วันนี้)
R3 $292.14 | PP $286.55 | S1 $284.40 | S2 $282.68
ATR14: $4.10

### NVDA — Last close $215.20
R2 $218.43 | R1 $214.97 | PP $210.73 | S1 $207.27 | S2 $203.03
ATR14: $7.36 | 52W high $217.80 (-1.2%)

### AVGO — Last close $430.00
R2 $435.31 | R1 $423.93 | PP $415.12 | S1 $403.74
ATR14: $15.43

### PLTR — Last close $137.80
R1 $140.41 | PP $137.59 | S1 $134.24 | S2 $131.42
ATR14: $6.30

### CRDO — Last close $188.51
R2 $208.67 | R1 $198.48 | PP $192.09 | S1 $181.90
ATR14: $13.69

### AEIS — Last close $357.24
R1 $362.50 | PP $353.94 | S1 $343.38
ATR14: $20.00

### MOD — Last close $273.00
PP $275.21 | S1 $263.12 | S2 $256.59
ATR14: $14.74

### BBAI — Last close $4.18
PP $4.22 | S1 $4.05 | S2 $3.93
ATR14: $0.30

### RKLB — Last close $105.47 (near 52W high $105.62)
PP $80.43 | S1 $76.08 — ห่างมาก ไม่ใช้ pivot
ATR14: $7.66

### ASTS — Last close $75.05
R2 $76.84 | R1 $71.10 | PP $68.00 | S1 $62.26
ATR14: $5.93 — earnings วันนี้ ไม่ trade

### MU — Last close $746.81 (near 52W high $747.21)
ห่างจาก PP ทุกระดับมาก — EXTENDED, ไม่ chase
ATR14: $41.91

### AMD — Last close $455.19
ห่างจาก PP $410.42 (-9.8%) — EXTENDED
ATR14: $26.88

### SMCI — Last close $35.37
R1 $35.16 | PP $34.04 | S1 $32.50
ATR14: $2.24
```

---

## 📉 Sector Pullback Watch — Semicon / AI / Datacenter / Space

| Ticker | ราคา | Support ใกล้สุด | ห่าง (%) | สถานะ | หมายเหตุ |
|--------|------|----------------|---------|--------|---------|
| NVDA | $215.20 | S1 $207.27 | 3.7% | **NEAR SUPPORT ★** | ใกล้ 52W high $217.80; vol-div |
| AVGO | $430.00 | PP $415.12 | 3.5% | **NEAR SUPPORT ★** | Ethernet leader; RS↓ ระยะสั้น |
| PLTR | $137.80 | S1 $134.24 | 2.6% | **NEAR SUPPORT ★** | ห่าง 52W high มาก (-33%); RS↓ |
| CRDO | $188.51 | S1 $181.90 | 3.5% | **NEAR SUPPORT ★** | vol-div ⚠️; AEC thesis intact |
| AEIS | $357.24 | S1 $343.38 | 3.9% | **NEAR SUPPORT ★** | vol-div ⚠️; RS↓ ระยะสั้น |
| MOD | $273.00 | S1 $263.12 | 3.6% | **NEAR SUPPORT ★** | vol-div ⚠️; RSI 61 ยังดี; RS↑↑ |
| BBAI | $4.18 | S1 $4.05 | 3.1% | **NEAR SUPPORT ★** | RS↑↑ แต่ PTH 0.45 ต่ำ |
| RKLB | $105.47 | PP $80.43 | 23.7% | EXTENDED ‼️ | Gap +34% วันนี้ — ห้าม chase |
| ASTS | $75.05 | PP $68.00 | 9.4% | MID RANGE | Earnings วันนี้ — ไม่ trade |
| MU | $746.81 | PP $655.05 | 12.3% | EXTENDED | RSI 88 overbought — รอ pullback |
| AMD | $455.19 | PP $410.42 | 9.8% | EXTENDED | RSI 80.7 — รอ pullback |
| SMCI | $35.37 | S1 $32.50 | 8.1% | MID RANGE | governance risk ยังอยู่ |

**สรุป Pullback Watch:**
- **NEAR SUPPORT ★ วันนี้:** NVDA, AVGO, PLTR, CRDO, AEIS, MOD, BBAI
- **น่าจับตามากที่สุด:** MOD (RSI 61 ยัง healthy, RS↑↑ +5%, datacenter cooling thesis แข็งแกร่ง, sector Leading)
- **ห้าม chase วันนี้:** RKLB (+34%), MU (+15%), AMD (+11%), DELL (+13%)

---

## Trade Setups (เพื่อการศึกษาเท่านั้น)

> **DISCLAIMER: The setups below are educational frameworks based on publicly available technical and fundamental data. They are NOT financial advice, NOT personalized recommendations, and NOT a solicitation to buy or sell any security. All trading involves risk of loss. Do your own research and consult a licensed advisor before making any investment decision.**

*VIX-Rank 63rd pct → ลด position size เป็น 0.49x ทุก setup*

---

### Setup 1 — ASML | ระยะเวลา: Swing (3-7 วัน)

**เหตุผล:** ASML [EARLY★] ใกล้ 52W high (-0.2%) พร้อม RS↑↑ vs SPY (+5.7%) ใน sector Technology ที่ Leading — WFE supercycle thesis: ทุก wafer node transition เพิ่ม etch/litho demand โดยอัตโนมัติ; VIX backwardation warrant ขนาด position ระวัง

- **ถ้า:** ASML ยืนเหนือ $1,590 ในช่วง 30 นาทีแรก **และ** volume ≥ 1.0x average → trigger entry
- **แล้ว:** เป้าหมาย $1,620 (R1 จาก pivot ประมาณ) ถึง new 52W high territory +2-3%
- **ล้มเลิกถ้า:** ราคาหลุดลงต่ำกว่า $1,575 (ATR2 ≈ ~1.1% ใต้ current)
- **ระยะเวลา:** Swing 3-7 วัน — ปิดก่อน CPI ออก (May 12) ถ้าไม่ถึงเป้า
- **Catalyst สนับสนุน:** WFE market $145B 2026 record; GAA ramp; ห่าง 52W high น้อยมาก = breakout candidate

---

### Setup 2 — MOD | ระยะเวลา: Swing (3-5 วัน)

**เหตุผล:** MOD [EARLY★] datacenter cooling — ทุก AI GPU rack ที่ขึ้น TDP (thermal design power สูงขึ้น) ต้องการ liquid cooling มากขึ้น; RS↑↑ +5% vs SPY; ห่างจาก S1 3.6% = zone entry ดี; sector Leading

- **ถ้า:** MOD ยืนเหนือ PP $275.21 บน volume ≥ 0.9x **และ** ไม่มีข่าว negative earnings จาก peers
- **แล้ว:** เป้าหมาย $285 (ใกล้ R2 จากการประมาณ) คืนสู่ระดับ open วันก่อน
- **ล้มเลิกถ้า:** ราคาหลุด S1 $263.12 ชัดเจน
- **ระยะเวลา:** Swing 3-5 วัน — ปิดก่อน CPI พรุ่งนี้ถ้า thesis ยังไม่ confirm
- **Catalyst สนับสนุน:** AI server heat density rising; Blackwell GB200 NVL72 ~14.3kW/rack → liquid cooling necessity

---

### Setup 3 — AVGO | ระยะเวลา: Day (วันนี้เท่านั้น)

**เหตุผล:** AVGO [ALERT] gap +4.2% — Ethernet switch leader 80% market share; RSI 62.6 ยังไม่ overbought; sector Technology Leading; CPI พรุ่งนี้ทำให้ Day เหมาะกว่า Swing

- **ถ้า:** AVGO ยืนเหนือ $425 (ใกล้ R1 $423.93 ที่กลายเป็น support) ในช่วง 10:30am ET แรก
- **แล้ว:** เป้าหมาย $435 (R2 จาก pivot) ในวันเดียวกัน
- **ล้มเลิกถ้า:** ราคาหลุด $423 (R1 เสีย); VIX ทะลุ 21
- **ระยะเวลา:** Day trade — ปิดทั้งหมดก่อน 3:00pm ET
- **Time-stop:** ถ้าไม่ยืนเหนือ $425 ภายใน 10:30am ET → setup void ไม่เข้า
- **Catalyst สนับสนุน:** Ethernet rebellion (UEC 1.0 June 2025) → AVGO ได้ประโยชน์โดยตรง; AI capex $700B+ 2026

---

*Sources:*
- *macro-snapshot.py / news-snapshot.py / sr-levels.py / universe-screen.py / sector-flow.py / catalyst-calendar.py / etf-discovery.py (Alpaca)*
- *[Polymarket S&P May 11](https://polymarket.com/event/spy-closes-above-on-may-11-2026)*
- *[Benzinga Polymarket article](https://www.benzinga.com/markets/prediction-markets/26/05/52439256/will-sp-500-open-up-or-down-on-may-11-heres-how-polymarket-traders-lean-as-trump-rejec)*
- *Web search: market futures VIX premarket May 11 2026*
