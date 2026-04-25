---
type: project-roadmap
created: 2026-04-25
status: active
tags: [trading, roadmap, paper-trading]
---

# Trading Foundations — 6-Month Roadmap

## Overview

เป้าหมายของ 6 เดือนนี้คือสร้าง foundation ที่แข็งพอจะ trade เงินจริงได้อย่างมีระบบ ไม่ใช่แค่รู้ศัพท์หรือดูกราฟออก แต่หมายถึง execute trade ตาม rule ของตัวเองได้ซ้ำๆ โดยไม่ตัดสินใจด้วยอารมณ์

**ทุน trading**: 100K (แยกจาก QQQM — ถ้าหายหมดได้ ห้ามใส่เพิ่ม 12 เดือนแรก)

**Target market**: US stocks — momentum + small/mid cap + sector rotation

**กฎ paper trading ตลอด 6 เดือน**:
- ใช้ simulator เท่านั้น ห้ามกดซื้อเงินจริงแม้แต่ครั้งเดียว
- Track ทุก trade ใน `vault/20_investment/_journal/` ตั้งแต่วันแรกที่เปิด simulator
- Max 4 positions พร้อมกัน
- Risk per trade ≤5% ของ capital จำลอง
- Stop loss: -25% hard cut ไม่มีข้อยกเว้น, -15% review
- Profit taking: ขาย 50% ที่ +50%, trail ส่วนที่เหลือ
- ห้ามเด็ดขาด: leverage, options, averaging down, all-in, revenge trading

---

## Month 1 — ภาษาพื้นฐาน + เปิด Paper Account

### Focus
อ่านกราฟออก รู้ว่าแต่ละตัวเลขบนหน้าจอหมายความว่าอะไร และเริ่ม observe market ทุกวัน

### Daily Routine (จันทร์-ศุกร์ ~15 ชม/วัน ใช้ ~4-5 ชม)
- **6:30 น.**: เปิด pre-market ดูว่า futures และ major indices เป็นยังไง (15 นาที)
- **9:30-16:00 น.**: เปิด simulator ไว้ดู real-time — ไม่ต้องกดซื้ออะไร แค่ดู (30-60 นาที)
- **หลังตลาดปิด**: เรียน 2-3 ชั่วโมง ตามหัวข้อด้านล่าง
- **ก่อนนอน**: เขียน daily note สั้นๆ ใน vault — วันนี้เห็นอะไร สังเกตอะไร

### Resources
- **หนังสือ**: *How to Make Money in Stocks* — William O'Neil (อ่าน Part 1 และ Appendix รูป chart pattern ก่อน)
- **YouTube channel**: "Investors Underground" (Free Trading Course playlist ของ Nate Michaud) — ดู session 1-5 ก่อน
- **YouTube channel**: "StocksToTrade" — playlist "Stock Market Basics"
- **Simulator**: Thinkorswim paperMoney (ฟรี เปิด account TD Ameritrade/Schwab) หรือ Webull Paper Trading
- **ศัพท์อ้างอิง**: Investopedia.com — search ทุกคำที่ไม่รู้ ไม่ต้องจำทุกอย่างตอนนี้

### หัวข้อที่ต้องรู้ปลาย M1
- Market hours: pre-market (4:00-9:30), regular (9:30-16:00), after-hours (16:00-20:00) ET
- Bid / Ask / Spread — ต่างกันยังไง เสียค่าอะไร
- Volume — ทำไมถึงสำคัญ วันที่ volume สูงคือวันที่เกิดอะไร
- Candlestick: อ่านได้ว่า open/close/high/low อยู่ที่ไหน, แยก bullish/bearish candle
- Market cap: small cap (< $2B), mid cap ($2-10B), large cap (> $10B)
- Float: คืออะไร ทำไม low-float ถึง volatile กว่า
- Ticker, lot, share, position — ศัพท์พื้นฐาน

### Paper Trading Tasks
- เปิด paper account บน Thinkorswim หรือ Webull
- ตั้ง capital จำลองที่ 100,000 USD ให้ตรงกับ plan จริง
- Watch list: เพิ่มหุ้น S&P 500 อย่างน้อย 20 ตัว + small cap 5 ตัว แล้วสังเกตทุกวัน
- ยังไม่กดซื้ออะไรใน M1 — แค่ observe และ annotate

### Milestone ปลาย M1 (pass/fail)
- [ ] อธิบาย bid/ask/spread/volume ให้คนอื่นฟังได้ภายใน 2 นาทีโดยไม่ดูโน้ต
- [ ] อ่าน candlestick chart และบอก open/high/low/close ได้ถูกต้อง ≥9/10 ครั้งที่ทดสอบตัวเอง
- [ ] Paper account เปิดแล้ว มี watch list ≥25 หุ้น
- [ ] เขียน daily note ≥15 วันจาก 20 วันทำการ

---

## Month 2 — Chart Reading + Trend + Support/Resistance

### Focus
อ่านกราฟหลาย timeframe ได้ รู้ว่าราคากำลังทำอะไรอยู่ (uptrend/downtrend/sideways) และระบุ level สำคัญได้

### Daily Routine (~5-6 ชม)
- **Pre-market**: ดู futures + overnight news 15 นาที
- **Market hours**: เปิดดู watch list real-time 1 ชั่วโมง — เน้นดู price action ที่ support/resistance
- **เรียน**: 3 ชั่วโมง ตามหัวข้อ
- **After market**: review chart 5 หุ้นจาก watch list ว่าวันนี้เกิดอะไร เขียน journal

### Resources
- **หนังสือ**: *Technical Analysis of the Financial Markets* — John Murphy (บทที่ 1-6 ก่อน — อย่าอ่านทั้งเล่มพร้อมกัน)
- **YouTube**: "The Chart Guys" — playlist "Technical Analysis Basics"
- **YouTube**: "Rayner Teo" — playlist "Technical Analysis Masterclass" (ดูเฉพาะ trend + S/R ก่อน)
- **Tool เพิ่มเติม**: TradingView (ฟรีแบบพื้นฐาน) — ใช้สำหรับ charting ควบคู่ simulator

### หัวข้อที่ต้องรู้ปลาย M2
- Trend definition: higher highs + higher lows = uptrend, ตรงกันข้าม = downtrend
- Trendline: วาดยังไงให้ถูก touch ≥2 จุด
- Support คือ level ที่ราคามักหยุดลง, Resistance คือ level ที่ราคามักหยุดขึ้น
- เมื่อ S/R แตก — ความหมายคืออะไร (breakout/breakdown)
- Moving average: SMA 20, SMA 50, SMA 200 — แต่ละเส้นใช้บอกอะไร
- Timeframe: weekly สำหรับ trend ใหญ่, daily สำหรับ entry, 15-min สำหรับ timing
- Volume ยืนยัน breakout: volume สูงกว่า average = breakout มีความน่าเชื่อถือ

### Paper Trading Tasks
- เริ่ม paper trade จริง: ≥10 trades ใน M2
- ทุก trade ต้องเขียนใน journal ก่อนกด: เหตุผลที่เข้า, entry price, stop loss ที่ตั้ง, target
- Track ผลลัพธ์ทุก trade: exit price, กำไร/ขาดทุน เป็น % และเป็น R (R = risk ที่ตั้งไว้)

### Milestone ปลาย M2 (pass/fail)
- [ ] Paper trades ≥10 ครั้ง ทุกครั้งมี pre-trade journal ครบ (entry reason, SL, target)
- [ ] วาด trendline และ support/resistance บน chart ได้โดยไม่ต้องดูคำสอน
- [ ] อธิบายได้ว่า uptrend/downtrend/sideways คืออะไร และหุ้นที่ดู 5 ตัวอยู่ใน phase ไหน
- [ ] ใช้ TradingView วาด chart + ติด indicator SMA 20/50/200 ได้

---

## Month 3 — Momentum Indicators

### Focus
เข้าใจและใช้ indicator ที่เหมาะกับ momentum trading: MACD, RSI, Volume — ไม่ใช่ใช้ครบทุกตัวพร้อมกัน แต่เข้าใจว่าแต่ละตัวบอกอะไรและมี false signal ยังไง

### Daily Routine (~5-6 ชม)
- **Pre-market**: ดู pre-market movers + ข่าวที่กระทบตลาดวันนี้ (30 นาที)
- **Market hours**: ดู live และเริ่ม identify setup ที่เห็น indicator confirm — จด แต่ยังไม่กดซื้อถ้ายังไม่แน่ใจ
- **เรียน**: 2-3 ชั่วโมง
- **Journal**: review trade ของวัน + บันทึก setup ที่พลาดหรือที่ดูแล้วใช่แต่ไม่เข้า

### Resources
- **YouTube**: "Trade Like a Stock Market Wizard" — Mark Minervini talks (YouTube ฟรี ค้นหาชื่อเขา)
- **หนังสือ**: *Trade Like a Stock Market Wizard* — Mark Minervini (เน้นบท SEPA methodology)
- **YouTube**: "SMB Capital" — "Momentum Trading Strategies" playlist
- **Investopedia**: RSI, MACD, Volume indicators — อ่าน article ทีละตัว ไม่พร้อมกัน

### หัวข้อที่ต้องรู้ปลาย M3
- RSI: overbought (>70), oversold (<30) — แต่ทำไมใน strong uptrend RSI ค้างที่ 70+ ได้นาน
- MACD: histogram, signal line crossover หมายความว่าอะไร
- Volume: volume surge ตอน breakout vs. volume dry-up ตอน consolidation — ต่างกันยังไง
- Momentum setup พื้นฐาน: หุ้นที่ price + volume + indicator align ไปทิศเดียวกันหน้าตาเป็นยังไง
- ทำไม indicator ต้อง confirm กัน — อย่าใช้ตัวเดียว

### Paper Trading Tasks
- Paper trades ≥15 ครั้งใน M3 โดยทุก trade ต้องระบุว่า indicator ไหน confirm
- สร้าง simple scorecard ใน journal: trade ไหนชนะ/แพ้ เพราะ indicator หรือเพราะ execution
- ลองจงใจเข้า 3 trade ที่ indicator ไม่ confirm — บันทึกผลเพื่อเปรียบเทียบ

### Milestone ปลาย M3 (pass/fail)
- [ ] Paper trades ≥15 ครั้ง ทุก trade ระบุ indicator ที่ใช้ confirm
- [ ] อธิบาย momentum setup ที่ตัวเองใช้ได้ภายใน 30 วินาที (entry condition, stop logic, target)
- [ ] Win rate จาก paper trades รวม M2+M3 ≥30% (ยังไม่ถึงเป้า แต่ต้องมีข้อมูล)
- [ ] สร้าง trade journal template ใน vault ที่ใช้จริงทุก trade — ไม่ใช่แค่มีไฟล์ว่าง

---

## Month 4 — Small Cap Specifics

### Focus
Small cap มีกฎเล่นที่ต่างจาก large cap ชัดเจน — เรื่อง float, catalyst, gap-and-go pattern เป็นหัวข้อที่ต้องรู้ก่อนเล่นจริงเพราะ small cap volatile มากและ spread กว้าง

### Daily Routine (~5-6 ชม)
- **Pre-market (4:00-9:30 ET)**: ดู pre-market gappers — หุ้นที่ gap up/down ≥5% พร้อม catalyst คืออะไร
- **Market open (9:30-10:30 ET)**: ช่วงที่ small cap volatile ที่สุด — สังเกต price action หนึ่งชั่วโมงแรก ห้ามกดซื้อในนาทีแรก
- **เรียน**: 2-3 ชั่วโมง
- **Journal**: ดู gappers ที่สังเกตไว้ว่า end-of-day ปิดที่ไหน — gap hold หรือ fade?

### Resources
- **YouTube channel**: "Investors Underground" (Nate Michaud) — ดู small cap specific content ทั้งหมด
- **YouTube channel**: "Ross Cameron / Warrior Trading" — เน้น gap-and-go strategies
- **เว็บ**: Finviz.com — ใช้ screener ดู gappers + news catalyst ฟรี
- **เว็บ**: SEC EDGAR (edgar.sec.gov) — ฝึกดู filing ที่ trigger catalyst (8-K, S-1, dilution)

### หัวข้อที่ต้องรู้ปลาย M4
- Float คืออะไร: ทำไม low float (< 20M shares) ถึง move ได้แรงกว่า
- Catalyst types ที่ drive small cap: earnings surprise, FDA approval, partnership announcement, short squeeze
- Gap-and-go pattern: เงื่อนไขที่ gap มักจะ hold และ extend ไปต่อ
- Gap fill pattern: เงื่อนไขที่ gap มักจะ fade กลับ
- Dilution risk: S-1 filing, ATM offering คืออะไร ทำไม small cap เจ้าของมักขายหุ้นใส่
- Halt: circuit breaker halt คืออะไร และทำไมมันอันตรายสำหรับ position ที่ถืออยู่

### Paper Trading Tasks
- เพิ่ม small cap screener เข้า routine — ทุกเช้า screen หา gappers ≥5% ก่อนตลาดเปิด
- Paper trade เฉพาะ small cap ≥10 ครั้งใน M4 โดย entry ต้องมี catalyst ระบุในทุก trade
- Track ว่า trade ที่ชนะ vs. แพ้ — catalyst type ไหนทำงานได้ดีกว่า

### Milestone ปลาย M4 (pass/fail)
- [ ] Paper trades small cap ≥10 ครั้ง ทุกครั้งระบุ catalyst ก่อน entry
- [ ] ใช้ Finviz screener screen pre-market gappers ได้ทุกวันโดยไม่ต้องดูคู่มือ
- [ ] อธิบาย gap-and-go vs. gap fade ได้พร้อมเงื่อนไขที่ทำให้ต่างกัน
- [ ] รวม paper trades M1-M4 ≥35 ครั้ง ทุกครั้งมี journal ครบ

---

## Month 5 — Sector Rotation + Screening Workflow

### Focus
เรียนรู้ว่า capital ไหลระหว่าง sector อย่างไร และสร้าง daily workflow ที่ทำซ้ำได้ — ตั้งแต่ตื่นนอนถึงตลาดปิด ทำอะไร ดูอะไร เรียงลำดับยังไง

### Daily Routine — สร้าง workflow จริง (~4-5 ชม)
- **6:30 น.**: macro check — ดู US futures, dollar index (DXY), 10Y yield, VIX
- **7:00 น.**: ดูข่าว pre-market จาก Benzinga หรือ MarketWatch — sector ไหนถูก mention มากที่สุด
- **8:00 น.**: run screener — gappers + sector leaders
- **9:20 น.**: finalize watch list สำหรับวัน — ≤5 ตัว
- **9:30-16:00 น.**: manage positions + observe
- **16:30 น.**: journal review — trade ที่ทำวันนี้ + setup ที่พลาด + ปรับ watch list พรุ่งนี้

### Resources
- **หนังสือ**: *Intermarket Analysis* — John Murphy (บทที่เกี่ยวกับ sector rotation)
- **เว็บ**: Finviz.com — Sector Map (ดู heat map รายวันว่า sector ไหน green/red)
- **เว็บ**: SPDR Sector ETFs (XLK, XLE, XLF, XLV, etc.) — ใช้ดู sector performance relative
- **YouTube**: "ZipTrader" — "Sector Rotation Strategy" content
- **Tool**: TradingView — ตั้ง watchlist แยก sector

### หัวข้อที่ต้องรู้ปลาย M5
- Business cycle phases: expansion/peak/contraction/trough — sector ไหน outperform ในแต่ละ phase
- Leading vs. lagging sectors: Tech และ Consumer Discretionary มักนำ, Utilities และ Consumer Staples มักตาม
- Relative strength: เปรียบ sector ETF กับ SPY — ถ้า XLE outperform SPY หมายความว่าอะไร
- Screening criteria ที่ใช้จริงของตัวเอง: ระบุได้ว่าใช้ parameter อะไรใน screener ทุกเช้า

### Paper Trading Tasks
- ทุก trade ใน M5 ต้องมี sector context ในjournal: sector นี้กำลัง outperform หรือ underperform ตลาดรวม
- สร้าง sector watch list แยก — track ว่าสัปดาห์นี้ sector ไหนนำ
- Paper trades ≥15 ครั้งใน M5

### Milestone ปลาย M5 (pass/fail)
- [ ] Paper trades ≥15 ครั้ง ทุก trade มี sector context ในjournal
- [ ] เขียน sector rotation summary ประจำสัปดาห์ลง vault ≥3 สัปดาห์ติดต่อกัน (ใน `vault/20_investment/_journal/`)
- [ ] มี screening workflow เขียนเป็น checklist ใน vault — ทำซ้ำได้ทุกวันโดยไม่ลืมขั้นตอน
- [ ] อธิบายได้ว่าทำไม trade แต่ละครั้งในเดือนนี้ถึงเลือก sector นั้น

---

## Month 6 — Full Simulation + Review + Graduation Prep

### Focus
เทรดเหมือนใช้เงินจริงทุกประการ ทบทวนทุกสิ่งที่เรียนมา วัด metrics จริง และตัดสินว่าพร้อมเริ่มเงินจริงหรือยัง

### Daily Routine — Full trading day (~5-6 ชม)
- ใช้ workflow จาก M5 ทุกวัน — ไม่มีการ skip ขั้นตอน
- **Weekly review ทุกเย็นวันศุกร์**: pull journal ทุก trade ของสัปดาห์ คำนวณ win rate + R-multiple + ดู pattern ที่ได้ผลและไม่ได้ผล
- **Monthly review ปลาย M6**: รวม metrics ทั้ง 6 เดือน prepare graduation checklist

### Resources
- **หนังสือ**: *The Disciplined Trader* — Mark Douglas (เน้นเรื่อง psychology — อ่านรวดเดียว)
- **หนังสือ**: *Trading in the Zone* — Mark Douglas (sequel ที่ลึกกว่า)
- **เว็บ**: Edgewonk หรือ Tradervue (trade journal software — ฟรีบางส่วน) สำหรับ visualize stats
- **Journal ใน vault**: `vault/20_investment/_journal/` — ทุก trade

### Paper Trading Tasks
- Paper trades ≥20 ครั้งใน M6
- คำนวณ metrics ทุกสัปดาห์ — win rate, average R-multiple, largest loss, largest win
- ทำ "worst case review": หา 3 trade ที่ขาดทุนหนักที่สุด — เกิดอะไรขึ้น ป้องกันได้ไหม
- Stress test: จำลองว่าถ้าใช้เงินจริง 100K ตอนนี้ current drawdown คือเท่าไร

### Milestone ปลาย M6 (pass/fail)
- [ ] Paper trades ≥20 ครั้งใน M6 (รวมทั้ง 6 เดือน ≥70 trades)
- [ ] Win rate รวมทุก trade ใน M3-M6 ≥35% (ก่อนเป้าจริง เพื่อ buffer)
- [ ] Average R-multiple ≥1.3 (ก่อนเป้าจริงที่ 1.5)
- [ ] เขียน "Trading Rules Document" ใน vault — ระบุ setup ที่ใช้, entry conditions, SL logic, position sizing rule ได้ครบถ้วนในเอกสารเดียว
- [ ] ไม่มี trade ไหนในเดือนนี้ที่ฝ่าฝืน hard rules (no averaging down, no revenge trade, SL ทุก trade)

---

## Graduation Criteria — เงื่อนไขเริ่มเงินจริง

ทุกข้อต้องผ่านพร้อมกัน ไม่มียกเว้น:

**Quantitative (วัดจาก trade journal)**
- [ ] Paper trades รวม ≥70 ครั้ง ทุกครั้งมี pre-trade และ post-trade journal
- [ ] Win rate จาก trades ≥60 ครั้งล่าสุด: ≥40%
- [ ] Average R-multiple จาก trades ≥60 ครั้งล่าสุด: ≥1.5
- [ ] Max drawdown ตลอด simulation: ≤30% ของ capital จำลอง
- [ ] ไม่มี single trade ที่ lose เกิน 5% ของ capital จำลอง (ผิด position sizing rule)

**Qualitative (self-assessment + journal evidence)**
- [ ] มี written Trading Rules Document ที่ครบถ้วน — อ่านแล้วคนอื่นทำตามได้
- [ ] เขียนสรุปบทเรียนรายเดือน ≥5 เดือนจาก 6 เดือน
- [ ] ไม่มี revenge trade หรือ averaging down ในช่วง 60 trades ล่าสุด

**ถ้าผ่านทุกข้อ**: เริ่มจาก 10K (10% ของ 100K capital) — ไม่ใช่ full capital ทันที

**ถ้ายังไม่ผ่าน**: extend paper trading 1-2 เดือน ไม่มีการ rush

---

## Resources Master List

### หนังสือ (เรียงตาม M ที่ใช้)
- *How to Make Money in Stocks* — William O'Neil (M1)
- *Technical Analysis of the Financial Markets* — John Murphy (M2)
- *Trade Like a Stock Market Wizard* — Mark Minervini (M3)
- *Intermarket Analysis* — John Murphy (M5)
- *The Disciplined Trader* — Mark Douglas (M6)
- *Trading in the Zone* — Mark Douglas (M6)

### YouTube Channels
- **Investors Underground** (Nate Michaud) — small cap, momentum, live trading recaps
- **Warrior Trading** (Ross Cameron) — gap-and-go, morning momentum
- **The Chart Guys** — technical analysis, clean explanation
- **Rayner Teo** — trend trading, S/R, position sizing
- **SMB Capital** — professional trading education
- **ZipTrader** — sector rotation, swing trading

### Simulators
- **Thinkorswim paperMoney** (TD Ameritrade/Schwab) — ดีที่สุดสำหรับ US stocks, ฟรี, real-time data
- **Webull Paper Trading** — UI ใช้ง่าย, ฟรี, mobile-friendly
- **TradingView Paper Trading** — ถ้าใช้ TradingView อยู่แล้ว built-in ได้เลย

### Screening Tools
- **Finviz.com** — screener + sector map + gappers (ฟรีพื้นฐาน)
- **MarketWatch / Benzinga** — pre-market news และ catalyst
- **SEC EDGAR** (edgar.sec.gov) — filings ของ small cap

### Trade Journal
- `vault/20_investment/_journal/` — primary journal ใน vault (ทำตั้งแต่ M1)
- **Edgewonk** หรือ **Tradervue** — software สำหรับ visualize stats (M6)

### Reference
- **Investopedia.com** — ค้นหาทุก term ที่ไม่รู้ตลอด 6 เดือน
- **SPDR Sector ETFs** — XLK, XLE, XLF, XLV, XLI, XLY, XLP, XLRE, XLB, XLU, XLC (sector benchmarks)
