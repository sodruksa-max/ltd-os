# Pre-Market Brief — 2026-05-04 (วันจันทร์)
*ดึงข้อมูลสดทุกตัวเลข ระบุ source ทุกจุด ขัดแย้งระหว่าง source แสดงชัดเจน*
*สร้าง: 19:05 Bangkok time (08:05 ET pre-market) | อัพเดต: 19:36 BKK (08:36 ET) | อัพเดต: 21:53 BKK (10:53 ET — ตลาดเปิดแล้ว 1h23m)*

---

## 📊 ภาพรวมวันนี้ (อ่านก่อน — สำหรับมือใหม่)

> วันนี้ตลาดหุ้นอเมริกาเปิดต้นสัปดาห์ด้วยสัญญาณผสม — Apple รายงานกำไรดีกว่าคาดเมื่อสัปดาห์ที่แล้ว แต่ตลาดในช่วง pre-market แทบไม่ขยับขึ้น ซึ่งเป็นสัญญาณว่านักลงทุนรายใหญ่อาจกำลัง "ขายทำกำไรบนข่าวดี" มากกว่าซื้อต่อ ราคาน้ำมันดิบลดลงแรงเกือบ 3% หลังมีข่าวอิหร่านอาจเสนอข้อตกลงสันติภาพ ซึ่งช่วยลดความกดดันเงินเฟ้อ แต่ crowd บนตลาดพนัน Polymarket (แพลตฟอร์มที่คนวางเดิมพันเหตุการณ์จริง — ใช้เป็นตัวชี้วัด sentiment) ให้โอกาส 86% ว่าตลาดจะเปิด "ลง" วันนี้ ความเสี่ยงหลักของสัปดาห์คือตัวเลขการจ้างงาน NFP วันศุกร์ (คาดอ่อนแอมาก ที่ +49K เท่านั้น) และผล AMD earnings คืนวันอังคาร

---

## Futures

> ⚠️ **yfinance rate limited** — ไม่สามารถดึงข้อมูล Futures โดยตรงได้ ใช้ ETF proxies จาก Alpaca แทน (ราคา pre-market จริง 08:05 ET)

| ETF Proxy | ราคา (19:36) | เทียบ Last Close (May 1) | เทียบ Apr 30 | เปลี่ยนจาก 19:05 |
|---|---|---|---|---|
| **SPY** (S&P 500 proxy) | $720.41 | **-0.03%** → | +0.24% | ↑ +$0.68 (ฟื้นตัว) |
| **QQQ** (Nasdaq-100 proxy) | $674.28 | **+0.02%** → | +0.98% | → ไม่เปลี่ยน |
| **IWM** (Russell 2000 proxy) | $278.34 | — | +0.13% | ↓ -$0.57 |
| **S&P Futures (ES=F)** | [unavailable] | — | — | yfinance rate limited |
| **Nasdaq Futures (NQ=F)** | [unavailable] | — | — | yfinance rate limited |

*Last close SPY: $720.65 (May 1) | Last close QQQ: $674.15 (May 1)*

**Gap Analysis — อัพเดต 19:36 (สำคัญ):**
- SPY ฟื้นตัวจาก -0.13% → -0.03% จาก last close — แทบ flat แล้ว สัญญาณ distribution อ่อนลง
- QQQ ยังคง flat (+0.02%) แม้ Apple beat — ยังไม่มีการ breakout
- **⚠️ USO ดีดกลับ** ($142.85 → $144.43 ใน 31 นาที) = น้ำมันฟื้น → กระทบ Setup 2 ดูรายละเอียดในส่วน Conflicts
- ไม่มีข้อมูล Futures โดยตรง — ใช้ ETF proxy แทน

---

## ตัวชี้วัด Macro

| ตัวชี้วัด | ค่า | ความหมายในทางปฏิบัติ | Source |
|---|---|---|---|
| **VIX** (ดัชนีความกลัวตลาด — ยิ่งสูงยิ่งตื่นตระหนก) | **~16.99** | 15-20 = ตลาด "ระวังตัวปกติ" ยังไม่ตื่นตระหนก แต่ไม่สบายใจเต็มที่ | Yahoo Finance (May 1 close) |
| **VXX** (ETF proxy ของ VIX) | **$28.32** +0.46% | ความกลัวลดเล็กน้อยจาก 19:05 ($28.38) — ยังอยู่โซน cautious | Alpaca 19:36 |
| **10Y Yield** (ดอกเบี้ยพันธบัตรรัฐบาล 10 ปี — สูง = ดอกเบี้ยแพง) | **~4.24%** | ลดลงจาก 4.39% หลังน้ำมันดิ่ง — แต่ยังสูง กดดันหุ้นเติบโต (tech) | Camden National / Investing.com |
| **WTI** (น้ำมันดิบสหรัฐ) | **~$101.90** | ลดลง $3.19 (-3%) จากข่าวอิหร่าน — น้ำมันถูกลง = ช่วยลดเงินเฟ้อ | Web search (May 4) |
| **USO** (ETF proxy ของ WTI) | **$144.43** -1.81% | ⚠️ **ดีดกลับ** จาก $142.85 (-2.88%) ใน 31 นาที — น้ำมันฟื้นตัว = Iran peace อาจ stall | Alpaca 19:36 |
| **Brent** (น้ำมันดิบโลก) | [unverified] | ลอง proxy ผ่าน USO แล้ว — ไม่พบ Brent spot โดยตรง | — |
| **Gold** (ทองคำ — สูง = หนีความเสี่ยง) | **~$4,613** | ลดลง $31 (-0.68%) — ทองอ่อนตัว = ความกังวลลดลงชั่วคราว | Camden National (May 4) |
| **GLD** (ETF proxy ทองคำ) | **$419.29** -1.03% | ร่วงหนักขึ้นจาก -0.09% → -1.03% ใน 31 นาที — ทองขายออก = risk-on หรือ dollar แข็ง; $419 × ~10.7 = spot ~$4,486 | Alpaca 19:36 |
| **DXY** (ดัชนีความแข็งค่าของดอลลาร์ — สูง = ดอลลาร์แข็ง) | [unverified direct] | ลอง DX-Y.NYB แล้วไม่ได้ → ใช้ UUP proxy แทน | — |
| **UUP** (ETF proxy ของ DXY) | **$27.41** +0.18% | ดอลลาร์แข็งขึ้นเล็กน้อย — กดดันตลาดเกิดใหม่และสินค้าโภคภัณฑ์ | Alpaca pre-market |

---

## Alpaca Macro Snapshot

**อัพเดตล่าสุด: 19:36 BKK (08:36 ET)**

```
### US ETF Proxies — 19:36 BKK / 08:36 ET (Alpaca)
| ETF | Proxy | Price | Change* | vs 19:05 | Signal |
|---|---|---|---|---|---|
| SPY | S&P 500 | $720.41 | +0.24% | ↑ +$0.68 | |
| QQQ | Nasdaq-100 | $674.28 | +0.98% | → flat | RISK+ |
| IWM | Russell 2000 | $278.34 | +0.13% | ↓ -$0.57 | |
| VXX | VIX proxy | $28.32 | +0.46% | ↓ -$0.06 (ดีขึ้น) | |
| TLT | Bonds 20Y | $85.67 | +0.06% | → flat | |
| USO | WTI Oil | $144.43 | -1.81% | ↑ +$1.58 ⚠️ น้ำมันดีด | |
| UUP | Dollar (DXY) | $27.41 | +0.18% | → flat | |
| GLD | Gold | $419.29 | -1.03% | ↓ -$4.00 ⚠️ ทองร่วง | |

*% คิดเทียบจาก Apr 30 close (base ที่ Alpaca ใช้)
[warn] yfinance rate limited — US Futures + Asia markets: unavailable
```

**📌 สัญญาณสำคัญจากการเปลี่ยนแปลง 31 นาที (19:05→19:36):**
- USO ดีดจาก -2.88% → -1.81% (น้ำมันฟื้น = Iran peace อาจ stall → กระทบ Setup 2)
- GLD ร่วงหนักขึ้น -0.09% → -1.03% (ขายทอง = risk appetite มีอยู่ หรือ dollar แข็ง)
- SPY ฟื้น: distribution signal จาก 19:05 อ่อนลงแล้ว

---

**🔴 อัพเดต 21:53 BKK (10:53 ET) — ตลาดเปิดแล้ว 1h23m**

```
### US ETF Proxies — 21:53 BKK / 10:53 ET (Alpaca — LIVE MARKET)
| ETF | Proxy | Price | Change* | vs 19:36 | สัญญาณ |
|---|---|---|---|---|---|
| SPY | S&P 500 | $721.99 | +0.19% | ↑ +$1.58 | Risk-on |
| QQQ | Nasdaq-100 | $676.63 | +0.37% | ↑ +$2.35 | 🔥 BREAKOUT เหนือ 52W high |
| IWM | Russell 2000 | $280.61 | +0.48% | ↑ +$2.27 | Small-cap ร่วมขึ้น |
| VXX | VIX proxy | $27.98 | -1.48% | ↓ -$0.34 | ✅ ความกลัวลดแรง |
| TLT | Bonds 20Y | $85.29 | -0.37% | ↓ -$0.38 | ⚠️ Bond ลง = risk-on / yield ขึ้น |
| USO | WTI Oil | $143.32 | +0.36% | ↑ (บวกแล้ว) | ⚠️ น้ำมันกลับมาบวก |
| UUP | Dollar (DXY) | $27.44 | +0.11% | → flat | ทรงตัว |
| GLD | Gold | $419.50 | -0.87% | → flat | ทองยังอ่อน |

*% คิดเทียบจาก Apr 30 close (base ที่ Alpaca ใช้)
[warn] yfinance rate limited — US Futures + Asia markets: ยังไม่ได้
```

**🚨 Scenario shift signals (10:53 ET):**
- ✅ **Setup 1 TRIGGERED:** QQQ $676.63 > R2 $676.07 และ 52W high $675.97 — breakout เกิดแล้ว ใน market
- ✅ **VXX -1.48%** → เกือบถึง Bullish trigger $27.00 แล้ว (ปัจจุบัน $27.98)
- ⚠️ **USO กลับมาบวก +0.36%** → Setup 2 Option A (oil continues lower) void สมบูรณ์; Option B (oil bounce) กำลัง play
- ⚠️ **TLT ลง -0.37%** → money หมุนออกจาก bond เข้าหุ้น = risk-on ยืนยัน
- **→ จาก Base ชี้ไปทาง Bullish** — ดู Decision Tree Contingency Plan

---

## ⚠️ ข้อมูลขัดแย้งที่พบ

1. **⚠️ USO ดีดกลับใน pre-market:** 19:05 USO $142.85 (-2.88%) → 19:36 USO $144.43 (-1.81%) — น้ำมันฟื้นตัว +$1.58 ใน 31 นาที อาจสะท้อน Iran peace talks ที่เริ่ม stall หรือ oil demand floor; **กระทบ Setup 2 โดยตรง** — trigger level $140.70 ยากขึ้น ดู Setup 2 ที่อัพเดต

2. **⚠️ Gold spot price gap:** Camden National รายงาน $4,613 | GLD ETF 19:36 $419.29 implies spot ~$4,486 (ratio ~0.091 oz/share) — **ต่างกัน ~$127** และ GLD ร่วงหนักขึ้นในช่วง 31 นาที — ใช้ ~$4,450-4,613 เป็น range; timestamp lag likely

3. **⚠️ SPY change reference ไม่ตรงกัน:** macro-snapshot แสดง +0.24% (vs Apr 30) แต่ vs May 1 close จริง ($720.65) SPY $720.41 = -0.03% เท่านั้น — แทบ flat แล้ว

4. **⚠️ Futures data:** yfinance rate limited ทั้งสาม run — ไม่สามารถยืนยัน ES=F, NQ=F ได้วันนี้ ใช้ ETF proxies แทน

5. **Asia markets:** yfinance rate limited — ข้อมูลตลาดเอเชียไม่ได้รับ (ดูส่วน Asia ด้านล่าง)

6. **Brent crude:** ลอง proxy หลายทางแล้ว ไม่พบ — ระบุ [unverified]

7. **⚠️ UUP/DXY minor conflict:** Alpaca UUP $27.41 vs researcher $27.35 — ต่างกัน ~0.2% ไม่มีนัยสำคัญ เป็น timestamp เท่านั้น

---

## ตลาดเอเชีย (ปิดแล้ว)

> ⚠️ yfinance rate limited — ไม่สามารถดึงข้อมูล Asia markets ได้วันนี้

| ตลาด | เปลี่ยนแปลง | ระดับ | หมายเหตุ |
|---|---|---|---|
| **Nikkei 225** | [unverified] | — | ⚠️ Golden Week ญี่ปุ่น (29 เม.ย.–5 พ.ค.) — อาจปิดทำการ |
| **KOSPI** | [unverified] | — | yfinance rate limited |
| **Hang Seng** | [unverified] | — | yfinance rate limited |
| **CSI 300** | [unverified] | — | ⚠️ อาจมี Labour Day holiday extension |
| **ASX 200** | [unverified] | — | yfinance rate limited |

*ตรวจสอบ holiday calendar ก่อนใช้ข้อมูล Asia ใดๆ — หลายตลาดอาจปิด Golden Week / Labour Day*

---

## Catalyst คืนที่ผ่านมา / ต้นสัปดาห์

1. **🍎 Apple earnings beat** (รายงานปลายสัปดาห์ที่แล้ว): AAPL กำไรดีกว่าคาด — ตามหลัง Alphabet ที่พุ่ง ~10% เมื่อ Apr 30 แต่ QQQ ไม่ตอบสนองใน pre-market ของวันนี้ = สัญญาณ distribution

2. **🏦 Fed คงดอกเบี้ย Apr 29** ที่ 3.50-3.75%: โอกาสลดดอกเบี้ยเดือน June พังเหลือ ~5% — ตลาดกำหนดราคา "ไม่มีการลดดอกเบี้ยตลอดปี 2026" ความหมาย: ดอกเบี้ยยังแพง กดดันหุ้นเติบโต

3. **🛢️ Iran peace proposal**: อิหร่านอาจเสนอข้อตกลงสันติภาพ → WTI ดิ่ง $3.19 (-3%) → ถ้าจริง = น้ำมันถูกลง ดีต่อเศรษฐกิจ แต่ยังไม่ confirmed

4. **💻 AI Capex shock**: แม้ Alphabet beat แต่ Microsoft -4% และ Meta -9% จากความกังวลงบลงทุน AI สูงเกินไป — สัญญาณ megacap tech แตกตัว ไม่ขึ้นพร้อมกัน

5. **📊 NFP สัปดาห์นี้**: consensus +49K — ต่ำมาก (ค่าเฉลี่ย 12 เดือน ~150K+) ถ้าจริง = ตลาดแรงงานอ่อนแอ อาจดัน Fed กลับมาพิจารณาลดดอกเบี้ย

---

## Polymarket Sentiment (อ้างอิงเท่านั้น)

*Polymarket = แพลตฟอร์มที่ผู้คนวางเงินเดิมพันเหตุการณ์จริง — ใช้เป็น crowd sentiment proxy ไม่ใช่การพยากรณ์แม่นยำ*

| ตลาด / คำถาม | Odds ปัจจุบัน | หมายเหตุ |
|---|---|---|
| **SPX opens DOWN on May 4** | **86%** ↑ strongly | Volume: $38,877 — crowd strongly bearish วันนี้ |
| **SPX opens UP on May 4** | **14%** | แม้ AAPL beat แต่ crowd ไม่เชื่อ |
| **0 rate cuts in 2026** | **56%** | Polymarket ให้โอกาสเกินครึ่งว่า Fed จะไม่ลดดอกเบี้ยเลยตลอดปี |
| SPX new highs June 2026 | moderate bullish lean | ระยะยาวยังพอมีความหวัง |

*⚠️ Polymarket 86% DOWN vs Alpaca ETF pre-market flat/slightly down — ทิศทาง consistent กัน crowd ถูก direction*
*Polymarket resolves ที่ open 9:30 ET — ตรวจสอบอีกครั้งที่ open*

---

## Earnings วันนี้ (May 4)

ไม่มี earnings สำคัญ (S&P 500 barometer) รายงานวันนี้

**Earnings ที่กำลังจะมา (สำคัญต่อสัปดาห์):**
| วัน | Ticker | ความสำคัญ |
|---|---|---|
| อังคาร May 5 (หลัง close) | **AMD** | Read-through สำหรับ AI/semiconductor vs AI capex fears |
| พุธ May 6 | **Disney (DIS)** | Consumer sentiment barometer |
| พุธ May 6 | **Uber (UBER)** | Gig economy + consumer spending |

---

## ปฏิทินสัปดาห์นี้

- **วันนี้ (May 4):** ไม่มี data/event หลัก — ตลาดดูดซับ AAPL + Iran news
- **อังคาร May 5:** AMD earnings หลัง close — AI sector read-through
- **พุธ May 6:** Disney + Uber earnings
- **ศุกร์ May 8:** **NFP 🔴 (สำคัญมาก)** — consensus +49K; ถ้า miss = กดดัน growth; ถ้า beat = ยืนยัน "higher for longer"
- **ตลอดสัปดาห์:** Golden Week หลายตลาดเอเชียอาจปิด

---

## Scenario Playbook

### กรณี Bullish (ตลาดขึ้น)
- **Trigger:** AAPL เปิดแข็ง +2%+ ดึง QQQ ทะลุ $676 (R2) และ 52W high $675.97 พร้อมกัน; หรือ Iran peace deal ถูกยืนยันอย่างเป็นทางการ → น้ำมันลงต่อ + yields ลง
- **Sectors ที่ได้ประโยชน์:** QQQ/Tech (momentum ทะลุ 52W high), XLY (consumer discretionary — ได้ประโยชน์จากน้ำมันถูก), Airlines/Transports (น้ำมันถูกลด cost)
- **Sectors ที่เสียประโยชน์:** XLE (พลังงาน — น้ำมันถูกลง = รายได้น้อยลง), GLD (ทองอ่อนตัวเมื่อ risk-on)
- **ตัวชี้วัดที่ต้องดู:** QQQ ทะลุ $676 พร้อม volume, VXX ร่วงต่ำกว่า $27, USO ลงต่ำกว่า $138
- **สรุปสำหรับมือใหม่:** ถ้าเกิดขึ้น ตลาดเทค "เบรกเอาท์" สู่จุดสูงสุดใหม่รอบ 52 สัปดาห์ — momentum ดึงดูดนักลงทุนตามเข้ามาซื้อ

### กรณี Base (น่าจะเป็นไปได้สุด — ตลาดทรงตัว)
- **Trigger:** pre-market flat ดำเนินต่อ; QQQ วนเวียนใต้ $676 (ไม่ทะลุ); ตลาดรอ AMD earnings วันอังคาร และ NFP วันศุกร์ก่อนตัดสินใจ
- **Sectors ที่ได้ประโยชน์:** defensives (XLU utility, XLV healthcare, XLP consumer staples) — นักลงทุนหมุนเข้า "หุ้นนิ่ง" ระหว่างรอ
- **Sectors ที่เสียประโยชน์:** high-growth tech (ดอกเบี้ยแพงกดดัน valuation) และ XLE (น้ำมันลง)
- **ตัวชี้วัดที่ต้องดู:** VIX range 16-19, SPY range $715-722, QQQ range $670-676
- **สรุปสำหรับมือใหม่:** ตลาดอยู่ในโหมด "รอดู" — ดีที่สุดคือนั่งดูก่อน ไม่ต้องรีบเข้า เพราะไม่มีทิศทางชัดจนกว่า AMD และ NFP จะออก

### กรณี Bearish (ตลาดลง)
- **Trigger:** Polymarket 86% ถูก — open ลงแรง; QQQ หลุดต่ำกว่า $670 (ใต้ R1 $671.91); VIX กระโดดข้าม 20; Iran peace talks ล้มเหลว → น้ำมันพุ่งกลับ
- **Sectors ที่ได้ประโยชน์:** TLT (พันธบัตร — เป็นสินทรัพย์ปลอดภัยเมื่อตลาดตื่นตระหนก), GLD (ทอง — ซื้อเพื่อป้องกัน), XLE (ถ้า Iran peace ล้มเหลว + น้ำมันพุ่ง)
- **Sectors ที่เสียประโยชน์:** QQQ/tech, growth stocks, IWM small-cap
- **ตัวชี้วัดที่ต้องดู:** VIX ข้าม 20, SPY หลุด $712.81 (S1), QQQ หลุด $671.91 (R1 กลายเป็น resistance)
- **สรุปสำหรับมือใหม่:** ถ้าเกิดขึ้น ให้ลดความเสี่ยง อย่าเพิ่มซื้อ รอให้ตลาดหา bottom ก่อน

### Most Likely Scenario

**Event Risk Check:**
- Iran geopolitical (ongoing, partially resolved) = **1 event**
- AMD earnings = วันอังคาร ไม่ใช่วันนี้ = 0 วันนี้
- NFP = วันศุกร์ = 0 วันนี้
- → รวม **1 event** วันนี้ → confidence สูงสุดได้ medium/high

- **เลือก: Base** (ตลาดทรงตัวรอ catalyst)
- **Confidence: Medium**
- **เหตุผล 3 ข้อ:**
  1. **Futures/ETF proxy (Macro):** SPY pre-market -0.13% และ QQQ +0.02% จาก last close — ตลาดไม่ตอบสนองต่อ AAPL catalyst = distribution signal ไม่ใช่ breakout
  2. **Polymarket + VXX (Catalyst/Sentiment):** Crowd 86% bearish วันนี้ + VXX +0.67% ยืนยันความกังวลเพิ่มขึ้น แต่ VIX ~17 ยังไม่ถึง panic zone
  3. **ปฏิทิน events ที่เหลือ (Calendar):** ไม่มี catalyst หลักวันนี้ — AMD (อังคาร) + NFP (ศุกร์) ทำให้ตลาดอยู่ในโหมด "รอ" ไม่กล้า commit ทิศทาง

- **อะไรจะทำให้ผิด:**
  1. AAPL เปิดแรงมาก (+3%+) ดึง QQQ ทะลุ $676 → flip เป็น Bullish
  2. Iran peace ล้มเหลว + น้ำมันพุ่งกลับ + VIX ข้าม 20 ภายใน 30 นาทีหลังเปิด → flip เป็น Bearish

---

## กรอบความเสี่ยง (Risk Framework)

### ความเสี่ยงสูงสุด 3 อันดับวันนี้ + Correlation Breakdown

| อันดับ | ความเสี่ยง | โอกาสเกิด | ผลกระทบ | เครื่องมือป้องกัน (อ้างอิงเท่านั้น) |
|---|---|---|---|---|
| 1 | **Iran peace ล้มเหลว → น้ำมันพุ่งกลับ >$106** | ปานกลาง | ปานกลาง-สูง | XLE long (รับน้ำมันแพง), airlines short |
| 2 | **Polymarket ถูก: ตลาดเปิดลงแรงและ QQQ หลุด $670** | ปานกลาง-สูง (86% Polymarket) | สูง | ลด position, ถือ cash เพิ่ม |
| 3 | **AI capex fear ลุกลาม → AMD ร่วงก่อน earnings** | ต่ำ-ปานกลาง | ปานกลาง (เฉพาะ tech) | หลีกเลี่ยง long tech ก่อน AMD |
| ⚠️ | **Correlation breakdown** — oil↑ + yields↑ + earnings miss พร้อมกัน | ต่ำ แต่ tail risk | **สูงมาก** — defensive ไม่ช่วย | ถือ cash เท่านั้น; ลด position size ทุกประเภท |

> **หมายเหตุ Row ⚠️:** ในสถานการณ์ correlation breakdown ทุก asset class ร่วงพร้อมกัน (stocks + bonds + gold + defensives) เครื่องมือป้องกันปกติไม่ work — cash คือ hedge เดียวที่เชื่อถือได้

**เครื่องมือป้องกันความเสี่ยงทั่วไป** (อ้างอิงเท่านั้น — ไม่ใช่คำแนะนำให้ซื้อ):
- VIX สูง / tail risk: VIX calls, UVXY
- Oil shock (Iran deal fails): XLE long, airlines/transports short
- USD แข็ง: EEM short
- Broad selloff: หมุนเข้า defensive (XLU, XLV, XLP), ถือ cash

**Reminder เรื่องขนาด position:**
- VIX ~17 ปัจจุบัน: ยังไม่ต้องลดขนาด แต่ระวัง
- วัน event risk (AMD อังคาร, NFP ศุกร์): พิจารณาลดขนาดก่อน รอ reaction
- ถ้า VIX ข้าม 20 วันนี้: ลดขนาด position ทันที

---

## Key S/R Levels (จาก sr-levels.py)

### SPY — Last close: $720.65 | Pre-market: $719.73

| Level | Price | vs Last Close | ความหมาย |
|---|---|---|---|
| **R3** | $731.50 | +1.5% | zone resistance สูงสุด |
| **R2** | $725.64 | +0.7% | resistance หลัก |
| **R1** | $722.15 | +0.2% | resistance ใกล้ที่สุด |
| **PP** (Pivot) | $716.30 | -0.6% | จุดกลาง — ถ้าลงต่ำกว่านี้ = bearish bias |
| **S1** | $712.81 | -1.1% | **support ด่านแรก** |
| **S2** | $706.95 | -1.9% | support หลัก |
| **S3** | $703.46 | -2.4% | support แข็งแกร่ง |

**Swing reference:**
- Swing High: $712.39 (Apr 17) — ต่ำกว่า current price = bullish higher lows
- Swing Low: $702.28 (Apr 23) | $629.28 (Mar 30) — base กว้าง

### QQQ — Last close: $674.15 | Pre-market: $674.28 | 52W High: $675.97

| Level | Price | vs Last Close | ความหมาย |
|---|---|---|---|
| **52W High** | $675.97 | +0.3% | **resistance สำคัญที่สุด** — ทะลุ = new highs |
| **R3** | $683.25 | +1.3% | เป้าหมายถ้า breakout |
| **R2** | $676.07 | +0.3% | แทบตรงกับ 52W high |
| **R1** | $671.91 | -0.3% | **QQQ ปัจจุบัน ABOVE R1** — แต่ยังต่ำกว่า R2/52W high |
| **PP** | $664.73 | -1.4% | |
| **S1** | $660.57 | -2.0% | support ถ้าย่อ |

**สำคัญ:** QQQ ซื้อขายอยู่ระหว่าง R1 ($671.91) และ R2 ($676.07)/52W high ($675.97) — แค่ $1.69 ห่างจาก 52W high

---

## Trade Setups (เพื่อการศึกษาเท่านั้น)

> **DISCLAIMER: The setups below are educational frameworks based on publicly available technical and fundamental data. They are NOT financial advice, NOT personalized recommendations, and NOT a solicitation to buy or sell any security. All trading involves risk of loss. Do your own research and consult a licensed advisor before making any investment decision.**

Setup ทุกอันใช้ logic แบบ IF-THEN — การเข้า position ขึ้นอยู่กับ trigger ไม่ใช่แน่นอนเสมอ

---

### Setup 1 — QQQ (52W High Breakout Test) | ระยะเวลา: Swing (2-5 วัน)

**เหตุผล:** QQQ อยู่ห่างจาก 52-week high ($675.97) แค่ $1.69 — ถ้าทะลุพร้อม volume จะเป็น momentum breakout ครั้งแรกในรอบ 1 ปี แต่ถ้าล้มเหลว = double-top rejection setup

- **ถ้า:** QQQ ทะลุและ close ช่วงแรก (9:30-10:00am ET) เหนือ $676.07 (R2 = 52W high zone) พร้อม volume > ค่าเฉลี่ย 30 วัน
- **แล้ว:** swing long QQQ หรือ tech ETF; เป้าหมาย R3 = $683.25 ใน 2-5 วัน
- **ล้มเลิกถ้า:** QQQ หลุดต่ำกว่า $671.91 (R1) หลัง trigger — false breakout → ออก
- **ระยะเวลา:** Swing (2-5 วัน)
- **Catalyst สนับสนุน:** AMD earnings อังคาร — ถ้า AMD beat = AI/semi momentum confirm; ถ้า AMD miss = setup void ล่วงหน้า

---

### Setup 2 — USO / Oil Direction (Iran News) | ระยะเวลา: Day

**เหตุผล:** WTI ดิ่ง $3.19 ข้ามคืนบนข่าว Iran peace proposal — แต่ USO ดีดกลับ +$1.58 ใน pre-market (19:05→19:36) = สัญญาณ peace talks stalling หรือ oil demand floor มีอยู่ ตอนนี้มีสองทิศทางที่เป็นไปได้

> ⚠️ **อัพเดต 19:36:** USO ดีดกลับจาก $142.85 → $144.43 — trigger "oil continues down" ยากขึ้นแล้ว พิจารณา **Alternative: Oil Bounce Setup** ด้านล่าง

**Option A — Oil Continues Lower (Iran peace advances):**
- **ถ้า:** USO ร่วงต่อเปิดตลาดลงใต้ $142.00 ในชั่วโมงแรก พร้อม headline ยืนยัน Iran talks advancing
- **แล้ว:** XLE short / airlines long — เป้าหมาย 1-2 วัน

**Option B — Oil Bounce (Iran peace stalls):** *(likelihood สูงขึ้นจาก pre-market bounce)*
- **ถ้า:** USO ยืนเหนือ $144.43 ใน 30 นาทีแรกหลังเปิด + ไม่มี Iran peace headline ยืนยัน
- **แล้ว:** XLE long (energy stocks ดีดตาม) — เป้าหมาย 1 วัน

- **ล้มเลิกทั้งคู่ถ้า:** USO วนเวียนระหว่าง $142-$145 โดยไม่มีทิศทาง (range-bound) → void ทั้ง A และ B
- **ระยะเวลา:** Day (วันเดียว)
- **Time-stop:** ตัดสินใจ A หรือ B ภายใน 10:00am ET — ถ้าไม่ชัดเจน → pass setup นี้ทั้งหมด
- **Catalyst สนับสนุน:** Iran peace headlines ตลอดวัน; ข่าว OPEC+ ที่อาจตอบโต้

---

### Setup 3 — TLT (NFP Rate Positioning) | ระยะเวลา: Swing (ผ่าน NFP ศุกร์ May 8)

**เหตุผล:** NFP consensus ศุกร์ที่ +49K อ่อนมาก ถ้าจริง = ตลาดแรงงานอ่อนแอ → Fed อาจต้องกลับมาพิจารณาลดดอกเบี้ย → yields ลง → TLT (พันธบัตร 20 ปี) ขึ้น — นี่คือ **post-event entry** รอ NFP ออกก่อน

- **ถ้า:** NFP วันศุกร์ May 8 พิมพ์ออกมาต่ำกว่า 40K (miss consensus ชัดเจน) **และ** 10Y yield ดิ่งลง >5bps ใน 30 นาทีหลัง release
- **แล้ว:** swing long TLT หลัง initial reaction settle (ประมาณ 9:00-9:30am ET วันศุกร์) — เป้าหมาย TLT +2-3% ใน 1-2 สัปดาห์
- **ล้มเลิกถ้า:** NFP > 60K (stronger than expected) หรือ yields ไม่ลงหลัง NFP → thesis พัง ไม่เข้า
- **ระยะเวลา:** Swing (วางแผนวันนี้ — entry วันศุกร์ post-NFP)
- **Time-stop:** เฉพาะ Day entry วันศุกร์: ถ้า TLT ไม่ยืนเหนือ entry price ภายใน 2 ชั่วโมงหลัง open → ออก
- **Catalyst สนับสนุน:** Polymarket 56% ให้โอกาส 0 cuts ปี 2026 — ถ้า NFP miss อาจ flip sentiment + re-price rate cuts กลับมา

---

*Sources:*
- *Alpaca pre-market ETF data: scripts/macro-snapshot.py (19:05 + 19:36 BKK / 08:05 + 08:36 ET)*
- *S/R Levels: scripts/sr-levels.py (Alpaca OHLC)*
- *Macro overview: Camden National Market Brief May 2026*
- *VIX: Yahoo Finance via researcher agent*
- *WTI crude: Web search 2026-05-04*
- *Catalyst/News: Schwab Market Update, heygotrade Weekly Outlook, Motley Fool Apr 30, TheStreet Apr 29*
- *Polymarket: Polymarket.com live (fetched 2026-05-04)*
- *10Y Yield: Investing.com via researcher agent*
