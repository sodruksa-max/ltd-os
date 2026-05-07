---
title: "Paper Survey — Momentum Screening & Early Trend Detection"
tags: [research, screener, momentum, relative-strength, sector-rotation, volume]
created: 2026-05-07
context: "พัฒนา universe-screen.py และ etf-discovery.py ให้จับ setup 'ก่อนวิ่ง' ได้แม่นขึ้น — focus sectors: semicon, AI infra, datacenter, space, memory"
scope: "4 themes | 9 searches | 11 papers (3 IMPLEMENT, 6 REFERENCE, 1 SKIP)"
---

# Paper Survey — Momentum Screening & Early Trend Detection
*2026-05-07 | สำหรับพัฒนา screener ที่ไม่ตกรถ*

---

## TL;DR — Top Picks (implement ก่อน)

| # | Paper | Theme | ทำอะไรกับ screener |
|---|---|---|---|
| 1 | Chen, Stivers, Sun (2024) — 52-Week High + Turnover | Relative Strength | เพิ่ม PTH metric: close / 52w-high > 0.90 + volume สูง = momentum likely persist |
| 2 | VP-MACD (arXiv:2604.26063) | Volume Compression | P* formula capture volume conviction ก่อน breakout — อยู่ใน vault แล้ว |
| 3 | Deep Learning Behavior Factors (arXiv:2508.14656) | Pre-Momentum | 3 behavioral filter: volume-price divergence, bottom reversal conviction, momentum-herding confirm |

---

## Papers by Theme

### Theme 1: Pre-Momentum / Early Breakout Detection

#### Deep Learning for Short-Term Equity Trend Forecasting — Yuqi Luan (2025)
- **arXiv:** 2508.14656
- **Method:** Dual-task MLP predict 5-day return + direction โดยใช้ 40 behavioral finance factors — 3 pattern หลัก: volume-price divergence, bottom reversal, momentum-driven herding
- **Key finding:** MLP resilient ในช่วง market downturn มกราคม 2025; directional learning ทำให้ signal แม่นทุก regime
- **Dataset:** US equities, 5-day horizon
- **Apply:** เพิ่ม 3 filter ใน screener: (1) ราคาขึ้นแต่ volume ต่ำกว่า avg → false breakout warning; (2) intraday close ใกล้ high → conviction สูง; (3) volume spike + RSI trending + above MA → confirm entry
- **Tag: IMPLEMENT**

#### Breaking the Trend: Avoid Cherry-Picked Signals — Valeyre (2025)
- **arXiv:** 2504.10914
- **Method:** พิสูจน์ทาง theoretical ว่า single EMA optimal captures trend; stack indicator หลายตัวมักเป็น overfitting
- **Key finding:** RSI + MACD + Volume + ATR พร้อมกันไม่ได้ดีขึ้น — cherry-picking ย้อนหลัง
- **Dataset:** Multi-asset futures
- **Apply:** ระวัง over-filter ใน tier system — test แต่ละ signal แยกก่อน ค่อย combine; ถ้า EARLY threshold เข้มเกินจะ miss setup จริง
- **Tag: REFERENCE**

---

### Theme 2: Relative Strength as Leading Indicator

#### Short-term Momentum, Turnover, and Price-to-52-Week-High — Chen, Stivers, Sun (2024)
- **DOI:** 10.1016/j.jempfin.2024.101556 | SSRN:4122300
- **Method:** วิเคราะห์ US equities แบ่งตาม PTH (price-to-52-week-high) × share turnover
- **Key finding:** PTH สูง + turnover สูง = momentum persists (under-react ต่อ news); PTH ต่ำ + turnover ต่ำ = reversal; mechanism คือ anchoring bias ที่ investors ไม่ fully price-in good news จนกว่า price จะ break higher
- **Dataset:** US equities, monthly, multi-subperiod
- **Apply:** เพิ่ม `PTH = close / max(close[-252:])` ใน screener → หุ้นที่ PTH > 0.90 + vol_ratio > 1 = empirically supported momentum setup; ใช้เสริม RS vs SPY ที่มีอยู่แล้ว
- **Tag: IMPLEMENT**

#### Momentum on Historical High — Finance Research Letters (2024)
- **Source:** ScienceDirect DOI:10.1016/j.frl.2024.xxx [unverified full content — paywalled]
- **Method:** Momentum portfolio sort ตามความใกล้ historical high (52-week หรือ all-time high)
- **Key finding:** หุ้นใกล้ historical high คิดเป็น 45% ของ momentum portfolio แต่สร้าง 70% ของ returns; 6.2% alpha vs 1.3% สำหรับหุ้นที่ห่าง historical high
- **Apply:** หุ้นที่ใกล้ 52-week high + setup ดี → upgrade tier; สอดคล้องกับ Chen et al. 2024
- **Tag: IMPLEMENT** (verify full paper ก่อน implement)

#### Explaining and Predicting Momentum Shifts Across Sectors — Mamais (2025)
- **Journal:** Journal of Forecasting | [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/for.3232) [unverified full content]
- **Method:** วิเคราะห์ NASDAQ + sector components ผ่าน economic events; out-of-sample 2018-2024
- **Key finding:** Framework สามารถ forecast ว่า sector ไหนจะมี momentum shift ล่วงหน้า
- **Apply:** ก่อน assign tier ให้ stock ให้ check sector ETF momentum (SMH, XLK) ก่อน — stock momentum แรงสุดเมื่อ sector momentum rising พร้อมกัน
- **Tag: REFERENCE**

---

### Theme 3: Volume Compression / ATR Contraction Before Breakout

#### VP-MACD — Lin et al. (2025) [อยู่ใน vault แล้ว]
- **arXiv:** 2604.26063 | **Location:** `vault/10_research/papers/2604.26063-vp-macd.md`
- **Method:** แทน close price ใน MACD ด้วย P* = Σ(P × Volume × σ × r) / Σ(Volume); λ ทำให้ entry เร็วขึ้นก่อน crossover
- **Key finding:** Signal น้อยลงแต่แม่นขึ้น; tested S&P500/Nasdaq 2018-2026
- **Apply:** ช่วง ATR contraction = σ ต่ำ → P* react ช้า → เมื่อ ATR expand P* surge → VP-MACD crossover เร็วกว่า MACD ปกติ; ใช้เป็น volume conviction signal
- **Tag: IMPLEMENT** (code พร้อมแล้วใน vault)

#### VCP (Volatility Contraction Pattern) — ไม่มี peer-reviewed paper
- ไม่พบ academic paper เฉพาะสำหรับ VCP (Minervini) บน US equities
- Evidence ทางอ้อม: volatility clustering literature + ATR-based exits (2511.08571)
- ถ้าต้องการ → search เพิ่มใน SSRN: "volatility contraction consolidation breakout US equity"
- **Tag: SKIP** (ใช้ VP-MACD แทน)

---

### Theme 4: Sector Rotation as Early Signal

#### Sector Rotation by Factor Model — Yang, Shi (2023)
- **arXiv:** 2401.00001
- **Method:** Factor model + fundamental metrics (PE, PB, EV/EBITDA) predict sector shifts
- **Key finding:** Momentum และ short-term reversion เป็น primary drivers ของ sector shifts; predictive framework มี "noteworthy predictive capabilities"
- **Dataset:** US equity sectors
- **Apply:** ใช้ sector-level 12M momentum rank ก่อน rank individual stocks — เลือก stock ใน sector ที่ momentum กำลัง accelerate
- **Tag: REFERENCE**

#### Network Momentum across Asset Classes — Pu, Roberts, Dong, Zohren (2023)
- **arXiv:** 2308.11294
- **Method:** Graph learning บน 64 futures เพื่อ identify momentum spillover; pricing data only
- **Key finding:** Network momentum Sharpe 1.5, return 22%; cross-asset spillover ทำงานได้จริง
- **Dataset:** 64 futures, 2000-2022
- **Apply:** Concept สำหรับ semiconductor ecosystem — SMH/SOX momentum → spillover มา MU/NVDA/AMD; เพิ่ม "sector ETF momentum check" ก่อน promote individual stock ไป tier EARLY
- **Tag: REFERENCE** (concept ดี แต่ implementation ซับซ้อน — ใช้ simplified version)

#### Follow the Leader: Network Momentum — Li, Ferreira (2025)
- **arXiv:** 2501.07135
- **Method:** รวม univariate trend กับ cross-sectional lead-lag signal; 2 วิธี detect lead-lag: correlation-based และ DTW-based
- **Key finding:** Network momentum ทำให้ Sharpe, skewness, downside performance ดีขึ้น statistically significant
- **Dataset:** Commodity futures (bootstrapped)
- **Apply:** Simplified version — SMH/XLK มี trend signal แล้ว → boost tier ของ semicon stocks ที่ setup ดีแต่ยัง ALERT
- **Tag: REFERENCE**

#### Predictive Directional Trading via Causal Inference — Letteri (2025)
- **arXiv:** 2507.09347
- **Method:** GMM cluster + Granger Causality + Effective Transfer Entropy + DTW/KNN สำหรับ optimal lag timing
- **Key finding:** Total return 15.38% vs 10.39% buy-and-hold; Sharpe 2.17 — ระบุ lead-lag ระหว่าง assets ได้ผ่าน causal inference
- **Dataset:** 9 stocks, June-August 2023 (**ระวัง: backtest 2 เดือนเท่านั้น — Sharpe 2.17 น่าสงสัย**)
- **Apply:** Concept — ดู sector ETF ก่อน 1-2 วัน; ถ้า ETF move แล้ว individual stock ยังไม่ตาม = laggard ที่มี lead-lag edge
- **Tag: REFERENCE** (concept ดี แต่อย่า trust ตัวเลข backtest)

---

## Implementation Roadmap

เรียงตาม impact สูง + complexity ต่ำก่อน:

1. **PTH metric (Chen et al. 2024)** → เพิ่ม `PTH = close / max_52w` ใน screener; หุ้นที่ PTH > 0.90 + vol_ratio > 1 → boost early_score +1 — complexity: **low**
2. **Volume-price divergence filter (arXiv:2508.14656)** → ราคาขึ้นแต่ volume < avg → warning tag ใน EARLY tier — complexity: **low**
3. **Sector ETF momentum check (Mamais 2025 + Network Momentum)** → ก่อน promote stock ไป EARLY ให้ check SMH/XLK 5-day trend — complexity: **medium**
4. **VP-MACD P* signal (arXiv:2604.26063)** → ใช้ P* formula แทน close ใน momentum calc — complexity: **medium** (code พร้อมแล้วใน vault)
5. **Historical high proximity booster (Finance Research Letters 2024)** → หุ้น PTH > 0.95 ใกล้ all-time high → star booster — complexity: **low** (verify paper ก่อน)

---

## Gaps ที่ยังขาด

- **RSI optimal threshold**: ไม่พบ paper optimize threshold (50 vs 55 vs 62) สำหรับ early momentum detection — search เพิ่ม: "RSI threshold optimization momentum equity cross-sectional"
- **VCP academic validation**: ไม่พบ peer-reviewed paper เฉพาะ — search เพิ่มใน SSRN: "volatility contraction consolidation breakout US equity"
- **Semiconductor-specific momentum**: ไม่พบ paper เฉพาะ semicon sector momentum — Mamais 2025 ครอบ NASDAQ level เท่านั้น

---

*Scope: 4 themes | Searches: 9 | Papers: 11 (3 IMPLEMENT, 6 REFERENCE, 1 SKIP + 1 vault reuse)*
*Papers verified: 2508.14656, 2504.10914, SSRN:4122300, 2401.00001, 2308.11294, 2501.07135, 2507.09347, 2604.26063*
*Unverified full content: Finance Research Letters 2024 (paywalled), Mamais 2025 (abstract only)*
