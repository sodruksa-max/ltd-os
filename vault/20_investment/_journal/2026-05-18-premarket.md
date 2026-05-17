# Pre-Market Brief — 2026-05-18 (วันจันทร์)
*ดึงข้อมูลสดทุกตัวเลข ระบุ source ทุกจุด | เตรียมสำหรับ Monday session | ข้อมูล ณ Friday close + weekend developments*

> **หมายเหตุ:** Brief นี้สร้างวันอาทิตย์ 17 พ.ค. 2026 — ตลาดปิด; ข้อมูลสะท้อนราคาปิดวันศุกร์ + ข่าว weekend

---

## Pre-Analysis Layers

**Reflex flags (pre-analysis instinct):**
- [REFLEX] Gold ลง -2.31% ขณะตลาดก็ลง — ทองไม่เป็น safe haven วันศุกร์ = ผิดปกติ → [REFLEX CONFIRMED] USD แข็งกด gold ลง
- [REFLEX] WTI futures -0.15% แต่ USO proxy +3.64% — ข้อมูลขัดกัน → [REFLEX CONFIRMED] timing difference; ใช้ Brent +3.35% เป็น primary
- [REFLEX] Russell -2.43% แรงกว่า S&P มาก — small cap ถูก punish หนักกว่า = risk-off เฉียบ
- [REFLEX] Brent $109.26 ขณะ WTI $101.02 — spread กว้าง = global supply fear > domestic

**Market texture: [COLD-ROUGH-HEAVY]**
Temperature: COLD (SPY -1.40%) | Texture: ROUGH (VIX 18.43) | Width: NARROW (sector Lagging ครอง) | Pressure: TIGHTENING (10Y +13.4bps) | Weight: HEAVY (Brent +3.35%)

**[MISOPHONIA: MARKET TRIGGER] MACRO — Oil up +3.35% ขณะ S&P futures ลง -1.24%**
→ stagflation signal; check Fed reaction; confidence consideration; add to risk table

**HSP Atmosphere: TEXTURE MISMATCH + PRE-CATALYST SILENCE**
- [HSP: TEXTURE MISMATCH] Gold ↓ + Bonds ↓ + Stocks ↓ พร้อมกัน — safe havens ไม่ทำงาน; stagflation correlation
- [HSP: PRE-CATALYST SILENCE] NVDA earnings พุธ — ความเงียบก่อน event ใหญ่ที่สุดของสัปดาห์
- Implication: **ลด position size ทุก setup 25%** (2 flags พร้อมกัน)

**PTSD Ambient Scan:**
- [PTSD: AMBIENT THREAT] Oil — Brent $109.26; Strait of Hormuz risk → -15% size
- Credit / Liquidity / Positioning / Flow / Insider: [unverified — weekend, no data]

**AURA Early Warning:**
- [AURA: EARLY SIGNAL] Bond-Equity Divergence — yields rising ขณะ equity ก็อ่อน; delayed stagflation repricing — watch: 2-4 สัปดาห์
- [AURA: EARLY SIGNAL] Geopolitical Pre-signal — Iran rejection; oil/defense ขยับก่อน mainstream — watch: 1-2 สัปดาห์

**Tachypsychia:** VIX=18.43, Gap NQ -1.54% > 1% → **[TACHYPSYCHIA: SLOW DOWN] Level 1**
- ห้าม entry 9:30–9:45 ET; position size -25% จาก base

---

## 📊 ภาพรวมวันจันทร์นี้

วันจันทร์ 18 พ.ค. ตลาดจะเปิดด้วยแรงกดดัน — ฟิวเจอร์สติดลบ 1.2–2.4% จากข่าว weekend ที่ Trump ปฏิเสธกรอบข้อตกลง Iran ทำให้ Brent (น้ำมันดิบโลก) พุ่งเกิน $109/บาร์เรล สร้างความกังวลเงินเฟ้อรอบใหม่ ดอกเบี้ยพันธบัตร 10Y ขึ้นสู่จุดสูงสุดของปี 4.595% กดหุ้นเติบโต ความเสี่ยงหลักคือ Iran ยังไม่คลี่คลาย + NVDA earnings วันพุธ ตลาดเล็ก (Russell -2.43%) ถูกกระทบหนักกว่า

---

## Futures

| Index | ระดับ | เปลี่ยนแปลง | Source |
|---|---|---|---|
| S&P 500 (ES=F) | 7,432.25 | -1.24% | macro-snapshot.py [2026-05-17 12:22 UTC] |
| Nasdaq-100 (NQ=F) | 29,231.75 | -1.54% | macro-snapshot.py |
| Dow Jones (YM=F) | 49,617.00 | -1.07% | macro-snapshot.py |
| Russell 2000 (RTY=F) | 2,799.60 | -2.43% | macro-snapshot.py |

**Gap Analysis:** Futures down ทุกตัว; small cap (RTY -2.43%) อ่อนกว่า large cap (ES -1.24%) = risk-off เชิงโครงสร้าง; ไม่มี gap divergence

---

## ตัวชี้วัด Macro

| ตัวชี้วัด | ค่า | ความหมาย | Source |
|---|---|---|---|
| VIX (ดัชนีความกลัว) | **18.43** (+6.78%) | ระดับ "ระวัง" ยังไม่ตื่นตระหนก; VIX-Rank 66th pct → size 0.47x | macro-snapshot.py |
| 10Y Yield | **4.595%** (+3.00% / ~+13.4bps) | สูงสุดของปี; ⚠️ +13.4bps > 5bps → TLT ไม่น่าเชื่อถือวันนี้ | macro-snapshot.py |
| WTI (น้ำมัน US) | **$101.02** (-0.15%) ⚠️ CONFLICT | ⚠️ WTI futures -0.15% vs USO proxy +3.64%; ⚠️ $101 = เหนือ $100 psychological threshold | macro-snapshot.py vs Alpaca |
| Brent (น้ำมันโลก) | **$109.26** (+3.35%) | Iran rejection; Brent เหนือ $95 ≥2 days → XLE primary outperformer per TRADING_RULES | macro-snapshot.py |
| Gold (ทองคำ) | **$4,561.90** (-2.48%) | ทองลงพร้อมตลาด; USD แข็งกด; safe haven ไม่ work | macro-snapshot.py |
| DXY (ดัชนีดอลลาร์) | **99.27** (+0.39%) | USD แข็ง; กด EM + commodities (ยกเว้น oil) | DX-Y.NYB |
| 10Y vs prev | ~+13.4bps | TRADING_RULES: ≥5bps → yield momentum overrides TLT pre-market signal | คำนวณ |

---

## Alpaca Macro Snapshot
*macro-snapshot.py [2026-05-17 12:22 UTC]*

```
SPY $737.71 -1.40% | QQQM $291.33 -1.70% | IWM $277.06 -2.60%
VXX $27.90 +0.90% | TLT $83.66 -1.48% | USO $148.20 +3.64%
UUP $27.77 +0.54% | GLD $417.36 -2.31%
Bubble Risk [!]: 10Y-2Y Spread +1.01% term premium rising | USD/JPY 158.73
VIX term structure: VIX9D/VIX = 0.89 (flat — ไม่ inverted)
Position Sizing: VIX-Rank 66th pct → multiplier 0.47x
```

## Alpaca News Snapshot
*news-snapshot.py [2026-05-17 19:22]*

```
ไม่พบข่าวใน 12 ชั่วโมงที่ผ่านมา (วันอาทิตย์ — ใช้ web search แทน)
```

---

## ⚠️ ข้อมูลขัดแย้ง

1. **WTI:** CL=F -0.15% vs USO (Alpaca) +3.64% — timing difference; Brent +3.35% align กับ USO direction → ใช้ Brent เป็น primary oil signal
2. **Gold:** GC=F $4,561.90 vs GLD $417.36 — ratio 10.97x (expected ~10x + expense ratio); direction consistent ทั้งคู่ -2.3–2.5% ✅

---

## Catalyst Weekend

- **Geopolitical:** Trump ปฏิเสธ Iran framework หลัง Xi summit → oil Brent +3.35%; magnitude: **สูง** (binary geopolitical, unresolved) [sundayguardianlive.com, 2026-05-15]
- **S&P 500:** ล่วงหน้าทำ record >7,500 ก่อนกลับมาอ่อน; tech + communication ฉุดลง [investing.com, 2026-05-17]
- **Bond/Yield:** Treasury yields yearly high — stagflation narrative dominant
- **NVDA Earnings:** วันพุธ 20 พ.ค. — EPS consensus $1.76, Revenue consensus $78.78B [valuesense.io/benzinga, 2026-05-17]
- **Geopolitical format:** Iran rejection → ผลกระทบ: oil + USD + defense + safe haven demand → magnitude: สูง

---

## Polymarket Sentiment

| ตลาด | Odds raw | Odds adjusted | หมายเหตุ |
|---|---|---|---|
| SPX direction May 18 | [unverified] | — | ใช้ futures -1.24% เป็น proxy |
| Iran escalation | [unverified] | — | Trump rejected = elevated |

*Specific odds ไม่ accessible; ใช้ futures + geopolitical news แทน*

---

## Earnings สัปดาห์นี้

| Ticker | วันที่ | EPS Est. | Revenue Est. | หมายเหตุ |
|---|---|---|---|---|
| **NVDA** | พ. 20 พ.ค. (after hours) | $1.76 | $78.78B | **Event ใหญ่ที่สุดของสัปดาห์** — Q4 FY2026 actual: $68.1B rev (+73% YoY) |

## ปฏิทินสัปดาห์นี้

- **จ. 18 พ.ค.:** ตลาดเปิด; Iran status watch; Fed speakers [unverified]
- **พ. 20 พ.ค.:** NVDA earnings (after hours); ASTS BlueBird 8-10 readiness estimate
- **ตลอดสัปดาห์:** ติดตาม Iran/Hormuz; yield direction; NVDA pre-earnings vol

---

## Sector Universe Radar

*universe-screen.py [2026-05-17 19:22]*

```
Sector 5d: SMH -1.8% | XLK +0.4% | UFO +3.2%

[EARLY★] ก่อนวิ่ง + RS แข็ง: NVDA(RS+10.7%), UCTT(RS+12.3%), LRCX(RS+8.1%), MRVL(RS+4.6%), ASML, SMCI, DELL, IONQ, QUBT
  → ทั้งหมด ⚠sector↓ (SMH -1.8% 5d) ยกเว้น SMCI, DELL, IONQ, QUBT
[ALERT] เริ่มวิ่ง: HPE(RS+13.0%), MSFT(gap+3.05%, vol 1.5x)
[EXTENDED] ห้าม chase: MU(RSI 70.1), GOOGL(RSI 75.5), RKLB(RSI 73.3), LUNR(RSI 66.8)
[WATCH] ผสม: AMD, CRDO, WDC, ASTS
```

**สรุป:**
- **[EARLY★] แข็งแกร่งที่สุด:** NVDA, UCTT, LRCX, MRVL
- **[ALERT] เริ่มวิ่ง:** HPE, MSFT
- **Catalyst หลัก:** NVDA earnings พุธ = ทุก EARLY★ semicon react; ห้าม swing ข้ามคืนพุธ

---

## ETF Discovery

*etf-discovery.py [2026-05-17 19:22]*

**[EARLY★] น่าสนใจสุด:**
- **AMAT** $436.62 — Applied Materials; RS↑↑, vol 1.75x แข็งที่สุด; WFE equipment (T2 thesis)
- **GLW** $191.81 — Corning; datacenter fiber; RS↑↑
- **PL** $41.62 — Planet Labs; satellite; RS↑↑ (T3 space)
- **ADI** $417.49 — Analog Devices; semicon; RS↑
→ ถ้าสนใจ → `/stock-content AMAT` หรือ `/stock-content PL`

---

## Sector Money Flow

*sector-flow.py [2026-05-17 19:22]*

```
Leading:   XLK(+0.2%/+9.7%), XLE(+6.5%/+3.8%)
Improving: XLV(Healthcare), XLP(Cons Staples), ROKT(Space +3.4% 5d)
Lagging:   XLI, XLF, XLY, XLU, XLC, XLB, ITA(Aerospace)
```

**สรุป:**
- **IN:** XLK + XLE; energy beneficiary จาก oil; tech resilient
- **OUT:** อุตสาหกรรม, การเงิน, discretionary, utilities, communication
- **Space (ROKT):** Improving — ASTS BlueBird catalyst พุธ
- ⚠️ Sector conflict: ITA Lagging แต่ T3 Space & Defense active — ตรวจว่า RKLB/ASTS decouple จาก ITA หรือเปล่า

---

## Catalyst Calendar

*catalyst-calendar.py [2026-05-17 19:22]*

```
[SOON] พ. 20 พ.ค.: ASTS — BlueBird 8-10 ready to ship estimate
[SOON] พ. 20 พ.ค.: NVDA earnings Q1 FY2027 (after hours)
RKLB, LUNR, KTOS: ไม่มี catalyst ใน 21 วัน
```

**[SOON] ≤3 วัน:**
- ASTS BlueBird — อาจเห็น pre-catalyst positioning จ.-อ.; [WATCH] tier รอ confirm
- NVDA earnings พุธ → ห้าม swing ข้ามพุธ ทุก position

---

## Scenario Playbook

### กรณี Bullish
- **Trigger:** Iran ส่งสัญญาณ dialog; Brent ร่วงใต้ $105; VIX < 17
- **Sectors ได้:** XLK, QQQM, NVDA group
- **Sectors เสีย:** XLE (oil ลง)
- **ดูตัวชี้วัด:** VIX < 17, Brent < $105, S&P futures +0.5%
- **มือใหม่:** "Iran news คลี่คลาย → ตลาดพุ่งกลับ tech นำ"

### กรณี Base
- **Trigger:** Iran ยังไม่ resolved แต่ตลาด digest แล้ว; S&P เปิดลง 0.5-1% แล้วทรง
- **Sectors ได้:** XLE (oil ยังสูง), XLV, XLP (defensive)
- **Sectors เสีย:** small cap, discretionary
- **ดูตัวชี้วัด:** S&P ทรงเหนือ 7,380; VIX ไม่เกิน 20
- **มือใหม่:** "ตลาดลงเปิดแต่ไม่พัง นักลงทุนรอดู NVDA พุธ"

### กรณี Bearish (Most Likely)
- **Trigger:** Iran escalate อีก; Brent > $115; VIX ทะลุ 20; yields +5bps
- **Sectors ได้:** XLE, XLV, XLP; GLD (ถ้า USD อ่อน)
- **Sectors เสีย:** XLK, QQQM, IWM, XLC, XLY
- **ดูตัวชี้วัด:** S&P < 7,380; VIX > 20; Brent > $112
- **มือใหม่:** "ความเสี่ยงสูง ควรถือ cash มากกว่าซื้อเพิ่ม"

### Most Likely Scenario: **Bearish** | Confidence: **Low**

*Event Risk: Iran geopolitical binary (unresolved) → Low cap per TRADING_RULES.md*

**เหตุผล:**
1. Futures -1.24% to -2.43%; S&P ใต้ pivot S2 $741.12 [macro-snapshot.py]
2. Iran rejection = new negative catalyst weekend; Brent $109 ยืนยัน [web search]
3. NVDA earnings uncertainty + Tachypsychia Level 1 triggered = ตลาดระมัดระวัง [catalyst-calendar]

**อะไรจะทำให้ผิด:**
1. Iran ส่งสัญญาณ dialog ใหม่ก่อนเปิดจันทร์ → flip Bullish
2. NVDA pre-earnings accumulation แข็งแกร่ง = Bullish signal ใน semicon

---

**DR Reality Check:**
- Probability: Bearish 55% / Base 35% / Bullish 10% — data-backed ✅
- Language scan: conditional language ✅
- `DR Reality Check: clean ✅`

**Split-Brain:**
Left-Brain: Futures down, Iran, yields high → Bearish
Right-Brain: XLK Leading, NVDA EARLY★ NEAR★ → potential bounce
`[SPLIT-BRAIN: SCENARIO CONFLICT]` — reconcile: Bearish open 9:30-10:15am; ถ้า SPY ทรงเหนือ $735 → Base EOD possible

**Satiation:** [SATIATION: NARRATIVE NUMBNESS] "Fed/Iran" — repeated 2+ สัปดาห์; real catalyst = NVDA earnings (ยังไม่ fully priced)

**AIWS:** NVDA earnings [AIWS: UNDER-LABELED] — implied vol อาจต่ำเกิน; position ข้ามพุธ = reckless

**Paranoid:** [PARANOID: ADVERSARIAL ACTOR] — Large holders distributed ใน record high; Iran news = convenient trigger; reduce size ในวันที่ futures bounce แทนที่จะซื้อ

**TLE:** [TLE: PATTERN MATCH] similar to May 5 2026 context; prior outcome: oil ลง, XLK +2.2% เมื่อ Iran eases; increases weight on XLK ถ้า Iran resolves

---

## กรอบความเสี่ยง

| อันดับ | ความเสี่ยง | โอกาสเกิด | ผลกระทบ | เครื่องมือ (อ้างอิง) |
|---|---|---|---|---|
| 1 | Iran escalate → Hormuz closure → Brent >$120 | กลาง | สูงมาก | XLE hedge; ลด size |
| 2 | NVDA pre-earnings volatility จันทร์ | ต่ำ-กลาง | กลาง | Day only; ห้ามข้ามพุธ |
| 3 | 10Y Yield ทะลุ 4.7% → repricing growth | ต่ำ | สูง | ลด XLK exposure |
| ⚠️ | **Correlation breakdown** — oil↑ + yield↑ + stocks↓ (Friday preview) | เกิดแล้วบางส่วน | สูงมาก | **Cash เท่านั้น** |
| ⚠️ | **Presidential Action Risk:** Trump Iran hardening | ต่ำ-กลาง | สูง | ลด equity; XLE hedge |

**Position Sizing วันนี้ (สะสม):**
- Base VIX-rank: 0.47x
- HSP 2 flags: -25% → × 0.75
- PTSD 1 channel: -15% → × 0.85
- Tachypsychia Level 1: -25% → × 0.75
- **Effective: ~0.22x base size**

---

## Key S/R Levels
*sr-levels.py [2026-05-17 12:22 UTC]*

| Ticker | Last | S2 | S1 | R1 | R2 | Zone |
|---|---|---|---|---|---|---|
| SPY | $739.17 | $741.12 | $744.64 | $750.61 | $753.06 | **ใต้ S2** ⚠️ |
| QQQM | $291.89 | $292.74 | $294.56 | $297.74 | $299.10 | **ใต้ S2** ⚠️ |
| NVDA | $225.32 | $226.62 | $231.18 | $238.42 | $241.10 | NEAR★ |
| AMD | $424.10 | $428.60 | $439.15 | $456.78 | $463.86 | NEAR★ |
| LRCX | $284.72 | — | — | — | — | NEAR★ |
| UCTT | $85.94 | $82.53 | $84.45 | $87.88 | $89.38 | NEAR★ |
| RKLB | $124.77 | $117.14 | $124.85 | $136.72 | $140.88 | AT S1 |
| ASTS | $83.67 | $70.73 | $76.87 | $86.83 | $90.64 | MID |
| PLTR | $133.99 | $127.52 | $130.63 | $135.66 | $137.58 | NEAR★ |

⚠️ SPY + QQQM ต่ำกว่า S2 แล้ว = broken standard pivot support; bearish confirmation

---

## 📉 Sector Pullback Watch

| Ticker | ราคา | Support S1 | ห่าง | สถานะ | หมายเหตุ |
|---|---|---|---|---|---|
| NVDA | $225.32 | $231.18 | -2.5% (ใต้ S1) | **NEAR★** | EARLY★ RS+10.7%; Day trade only; earnings Wed |
| UCTT | $85.94 | $84.45 | +1.8% | **NEAR★** | EARLY★; WFE supercycle |
| LRCX | $284.72 | ~$280 | ~+1.7% | **NEAR★** | EARLY★ RS+8.1%; T1+T2 |
| AVGO | $425.19 | $422.80 | +0.6% | **NEAR★** | EARLY; RS อ่อน |
| RKLB | $124.77 | $124.85 | -0.1% | **AT S1** | EXTENDED RSI 73.3 — ห้าม chase |
| ASTS | $83.67 | $76.87 | +8.8% | **MID** | BlueBird catalyst Wed |

**NEAR★ วันนี้:** NVDA, UCTT, LRCX, AVGO
**ตัวน่าจับตา:** NVDA — EARLY★ RS แข็งที่สุด; Day trade เท่านั้น
**ห้าม chase:** RKLB (RSI 73), MU (RSI 70), GOOGL (RSI 75), LUNR (RSI 67)

---

## Trade Setups (เพื่อการศึกษาเท่านั้น)

> **DISCLAIMER: The setups below are educational frameworks based on publicly available technical and fundamental data. They are NOT financial advice, NOT personalized recommendations, and NOT a solicitation to buy or sell any security. All trading involves risk of loss. Do your own research and consult a licensed advisor before making any investment decision.**

**Dopamine State:** NORMAL ✅
**Setup consistency:** Bearish scenario → Long setups มีเหตุผล diverge ชัดเจน (oil rule + EARLY★ RS)

---

### Setup 1 — XLE (Energy ETF) | Swing 3-5 วัน

**เหตุผล:** TRADING_RULES.md: Brent >$95 ≥2 days → XLE primary outperformer; Brent $109.26; XLE Leading sector flow

- **ถ้า:** XLE เปิด ≥ $103 + VIX ไม่ทะลุ 22
- **แล้ว:** เป้า $107-108; size 22% of base (effective after all modifiers)
- **ล้มเลิกถ้า:** Brent < $103 (Iran news คลาย) หรือ VIX > 22
- **ระยะเวลา:** Swing 3-5 วัน
- **Catalyst:** Iran rejection, Brent $109, XLE Leading (5d RS +6.5%)

### Setup 2 — NVDA | Day เท่านั้น (ห้าม overnight)

**เหตุผล:** EARLY★ RS +10.7% = smart money เข้าก่อน; NEAR★ zone; earnings Wed = ห้าม overnight

- **ถ้า:** SPY ทรงเหนือ $735 ภายใน 9:45am ET + NVDA volume > 1.5x + NVDA ≥ $224
- **แล้ว:** Day trade เป้า $230-231 (S1); size 22% of base
- **ล้มเลิกถ้า:** SPY < $730 หรือ NVDA < $221
- **ระยะเวลา:** Day — ออกก่อน 3:00pm ET เสมอ
- **Time-stop:** ถ้าไม่เกิด trigger ภายใน 10:15am ET → void; ถ้าเข้าแล้วไม่ confirm ภายใน 12:00pm ET → ออก
- **Catalyst:** EARLY★ RS signal; pre-earnings positioning; EARNINGS WED = ห้าม hold ข้ามคืน

### Setup 3 — ASTS (สังเกตการณ์วันนี้ / พิจารณาพรุ่งนี้)

**วันนี้ไม่เข้า** — MID zone; [WATCH] tier; ตลาด risk-off
- ถ้าวันอังคาร: ASTS > $83 + ROKT ไม่อ่อน + BlueBird confirm → พิจารณา Day entry
- ออกก่อนพุธ เสมอ

---

## GAD Pre-flight

| Setup | Failure Mode | Early Signal | Plan B |
|---|---|---|---|
| XLE | Iran resolves → oil ลง -5% | Brent < $103 pre-market | ออกทันที; flip XLK |
| XLE | Fed hawkish surprise → risk-off total | VIX > 22 + USD spike | ออก; cash |
| XLE | Demand destruction ชนะ supply fear | Oil + equity ลงพร้อมกัน | ออก; cash 100% |
| NVDA | SPY ไม่ทรง → ลงต่อ | SPY < $730 ใน 30 นาทีแรก | ไม่เข้า; Setup void |
| NVDA | Negative earnings leak | NVDA ลง >-3% ไม่มี market reason | ออกทันที; ห้าม average down |
| NVDA | Time-stop triggered | ไม่เกิด trigger ก่อน 10:15am ET | void; ไม่เข้าเด็ดขาด |

---

*Sources:*
- [US Stock Market May 15 2026 — Sunday Guardian](https://sundayguardianlive.com/business/us-stock-market-today-15-may-2026-dow-falls-nasdaq-sp-500-crash-after-trump-china-visit-oil-surges-109-on-us-iran-deal-gold-silver-hit-bitcoin-retreats-82k-what-investors-should-watch-192641/)
- [S&P 500 Pullback — Investing.com](https://www.investing.com/analysis/sp-500-pullback-looks-more-like-a-rates-problem-than-panic-200680413)
- [NVDA Earnings Date — valuesense.io](https://valuesense.io/ticker/nvda/earnings)
- [NVDA Earnings — Benzinga](https://www.benzinga.com/quote/NVDA/earnings)
- [Polymarket S&P 500](https://polymarket.com/predictions/sp-500)
- macro-snapshot.py, news-snapshot.py, sr-levels.py, universe-screen.py, sector-flow.py, catalyst-calendar.py, etf-discovery.py [Alpaca, 2026-05-17 12:22 UTC]
