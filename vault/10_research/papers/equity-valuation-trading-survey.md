# Paper Survey — Equity Valuation & Trading Logic
*Project context: stock research system (MU, pre-market brief, decision tree) | 2026-05-05 | Scope: 4 themes | 10 searches | 10 papers*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | Residual Income Valuation (2506.00206, 2025) | Valuation | คำนวณ intrinsic value แทน P/E ดิบ — V/P ratio ทำนาย return 1-3 ปีได้จริง |
| 2 | Does Overnight News Explain Overnight Returns? (2507.04481, 2025) | Pre-market | ระบุว่า news topic ไหนทำให้หุ้นขึ้นข้ามคืน — ต่อยอด pre-market brief ได้ทันที |
| 3 | Generating Alpha: Hybrid AI Trading (2601.19504, 2026) | Entry/Exit | blueprint ครบ: EMA+MACD+RSI+XGBoost+regime filter — 135% / 24 เดือน บน S&P500 |
| 4 | SAE-FiRE Earnings Surprise (2505.14420, 2025) | Forward EPS | ใช้ earnings call + 10Q + news → predict surprise ก่อน consensus — ช่วยประเมิน forward EPS แม่นขึ้น |

---

## Papers by Theme

### Theme 1: Valuation Accuracy (P/E, Intrinsic Value)

#### Residual Income Valuation and Stock Returns — Haboub, Kartsaklas, Sarafidis (2025)
- **Source:** [arXiv:2506.00206](https://arxiv.org/abs/2506.00206)
- **Method:** คำนวณ intrinsic value V ด้วย Ohlson (1995) Residual Income Model (RIM) โดยใช้ book value + analyst EPS forecast 1 ปี แล้วสร้าง V/P ratio เปรียบกับราคาตลาด P
- **Key finding:** High V/P portfolios ชนะ low V/P อย่างมีนัยสำคัญในช่วง 1-3 ปี; บริษัทที่ V/P สูงสุดมักถูก misprice อย่างต่อเนื่อง — Fama-French 3 factors ยังอธิบายไม่ครบ
- **Dataset:** US equities หลายปี (cross-sectional portfolio sorts)
- **Apply to project:** แทนที่การดู P/E ดิบจาก website ให้คำนวณ V = BV + PV(residual income) จาก Micron IR data → ถ้า V > P = undervalued signal ที่มีงานวิจัยรองรับ; ใส่ใน stock-research template เป็น "Intrinsic Value Check"
- **Tag:** IMPLEMENT

#### Volatility of P/E Ratio and Return Predictability — Jiang & Li (SSRN 2025)
- **Source:** [SSRN:5163103](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5163103)
- **Method:** วัด time-series volatility ของ P/E ratio เป็น signal เพิ่มเติม (ไม่ใช่แค่ระดับ P/E)
- **Key finding:** P/E volatility มี predictive power สำหรับ future returns — P/E ที่ไม่นิ่ง (volatile) บ่งชี้ uncertainty สูงกว่าที่ระดับ P/E เพียงอย่างเดียวบอก
- **Dataset:** US equities, multi-year
- **Apply to project:** อธิบายว่าทำไม MU มี P/E ต่างกันระหว่าง source — cyclical stocks มี P/E volatile โดยธรรมชาติ; ใช้เป็น context สำหรับ stock research notes
- **Tag:** REFERENCE

---

### Theme 2: Forward EPS Estimation & Earnings Surprise

#### SAE-FiRE: Enhancing Earnings Surprise Predictions — Zhang et al. (May 2025)
- **Source:** [arXiv:2505.14420](https://arxiv.org/abs/2505.14420)
- **Method:** Sparse Autoencoder (SAE) decompose LLM representations จาก earnings call transcripts + 10Q + news → ANOVA F-test + tree-based importance → เลือก features ที่ discriminative จริง
- **Key finding:** SAE-FiRE outperforms baseline approaches ทั้ง 3 datasets อย่างมีนัยสำคัญ — เก็บ signal จาก text ได้ดีกว่า LLM embedding ดิบ
- **Dataset:** Earnings call transcripts, 10Q reports, financial news (US equities)
- **Apply to project:** เมื่อ MU รายงาน Q3 FY2026 — ดู earnings call transcript แล้วระบุ tone เกี่ยว HBM, guidance, capex; เปรียบกับ pattern ที่ paper ระบุว่า predict surprise ได้ — ช่วยประเมินว่า street consensus จะ beat หรือ miss
- **Tag:** IMPLEMENT

#### FinCall-Surprise: Large Scale Multi-modal Benchmark — Koval, Andrews, Yan (2025)
- **Source:** [arXiv:2510.03965](https://arxiv.org/abs/2510.03965)
- **Method:** Multi-modal benchmark รวม conference call audio/text + tabular financials → forecast earnings surprise direction
- **Key finding:** LSTM/TCN ชนะ naive model 30% และชนะ analyst accuracy ถึง 12-13%; text features สำคัญมากสำหรับ short-horizon surprise
- **Dataset:** Large-scale US earnings calls (multi-year, multi-sector)
- **Apply to project:** ใช้เป็น benchmark สำหรับ MU earnings surprise model; ยืนยันว่าการอ่าน earnings call อย่างมีระบบดีกว่าดู consensus EPS เพียงอย่างเดียว
- **Tag:** REFERENCE

#### Behavioral ML: Computer Predictions Also Overreact — (arXiv:2303.16158, 2025 updated)
- **Source:** [arXiv:2303.16158](https://arxiv.org/abs/2303.16158)
- **Method:** เปรียบ ML forecast (regularized) กับ analyst consensus จาก IBES (1986-2019); วัด overreaction / underreaction
- **Key finding:** ML ได้ accuracy ใกล้เคียง analyst แต่ ML มี systematic overreaction เหมือนกัน — regularization ลด bias ได้บางส่วนแต่ไม่หมด
- **Dataset:** IBES annual EPS forecasts, Compustat/CRSP, 1986-2019
- **Apply to project:** เตือนว่า consensus EPS forecast (และ ML-based) มี bias อยู่เสมอ — ควรใช้ range ไม่ใช่ point estimate เมื่อประเมิน forward P/E ของ MU
- **Tag:** REFERENCE

---

### Theme 3: Entry/Exit Signal Generation

#### Generating Alpha: Hybrid AI-Driven Trading System — (arXiv:2601.19504, Jan 2026)
- **Source:** [arXiv:2601.19504](https://arxiv.org/abs/2601.19504)
- **Method:** 5-layer signal stack: (1) EMA+MACD สำหรับ trend, (2) RSI+BB สำหรับ mean reversion, (3) FinBERT sentiment, (4) XGBoost signal synthesis, (5) market regime filter ตาม volatility/return environment
- **Key finding:** 135.49% return ใน 24 เดือน บน 100 US equities จาก S&P500 (2023-2025); ชนะ S&P500 และ NASDAQ-100 benchmark; lower downside risk
- **Dataset:** 100 US equities, S&P500, 2023-2025
- **Apply to project:** นำ regime filter + multi-layer confirmation มาใส่ใน decision tree — ตอนนี้ใช้แค่ S/R levels + VIX; เพิ่ม EMA trend check + RSI state ก่อน approve entry; แยก "trend day" vs "mean-reversion day"
- **Tag:** IMPLEMENT

#### Interpretable Hypothesis-Driven Trading — Deep, Deep, Lamptey (arXiv:2512.12924, Dec 2025)
- **Source:** [arXiv:2512.12924](https://arxiv.org/abs/2512.12924)
- **Method:** Walk-forward validation (34 independent test periods) + 5 hypothesis types: institutional accumulation, flow momentum, mean reversion, breakouts, range-bound value; strict information set discipline
- **Key finding:** Sharpe 0.33, max drawdown -2.76%, beta 0.058; สำคัญ: works during high-volatility (2020-2024: +2.4% ann.) ไม่ใช่ low-volatility (2015-2019: -0.16%) — microstructure signals จาก daily data ใช้ได้เฉพาะตอน VIX สูง
- **Dataset:** 100 US equities, 2015-2024
- **Apply to project:** ยืนยัน thesis ที่มีอยู่ว่า VIX 18+ เป็น signal ที่ใช้ได้ดีกว่า; เพิ่ม rule: "ถ้า VIX < 15 → ลด confidence ของ microstructure signals ทุกตัว"; ใช้ walk-forward validation เมื่อ backtest system ใหม่
- **Tag:** REFERENCE

#### Increase Alpha: AI-Driven Trading Framework — (arXiv:2509.16707, Sep 2025)
- **Source:** [arXiv:2509.16707](https://arxiv.org/abs/2509.16707)
- **Method:** Minimalist design: ดึง variables ที่ fundamental analyst ให้ความสำคัญ → compact network หา non-linear interactions → daily directional signal สำหรับ 814 US equities
- **Key finding:** Fundamental variables ที่เลือกดีชนะ transformer model ขนาดใหญ่บน unstructured text; interpretability ดีกว่าแบบ black-box
- **Dataset:** 814 US equities, daily
- **Apply to project:** ใช้เป็น checklist ว่า fundamental variables ที่ควรดู (earnings yield, book-to-price, momentum, quality factors) ก่อน entry — แทนที่การดูแค่ P/E เดียว
- **Tag:** REFERENCE

---

### Theme 4: Pre-Market Signals & Price Discovery

#### Does Overnight News Explain Overnight Returns? — (arXiv:2507.04481, Jul 2025)
- **Source:** [arXiv:2507.04481](https://arxiv.org/abs/2507.04481)
- **Method:** Supervised topic analysis บน 2.4M news articles; เลือก topics ที่ explain contemporaneous returns ได้ดีที่สุด; แยก overnight vs intraday news
- **Key finding:** เกือบทั้งหมดของ equity risk premium ใน 30 ปีที่ผ่านมาเกิดขึ้น **overnight** (intraday return เฉลี่ยติดลบ); overnight news topics explain overnight returns → สามารถ forecast ล่วงหน้าได้ว่าหุ้นไหนจะดีข้ามคืน
- **Dataset:** S&P500, 1993-2003 (core); out-of-sample tests
- **Apply to project:** ปรับ pre-market brief — เพิ่ม section "Overnight News Tone" ที่จัดกลุ่ม headline ตาม topic type (earnings, macro, geopolitical, sector) แล้ว assign expected overnight direction; ทำไม MU ขึ้นแรงเช้าวันนี้ = overnight news topic ที่ market ตอบสนองแรง
- **Tag:** IMPLEMENT

#### Dark Side of the Day: Overnight Price Jumps — Bahcivan, Dam, Gonenc (SSRN, Oct 2025)
- **Source:** [SSRN:5648748](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5648748)
- **Method:** ระบุ overnight price jumps ใน 9,283 US stocks; วัด short-term return predictability หลัง jump
- **Key finding:** Cumulative overnight jump returns **negatively predict** short-term returns — นักลงทุน overreact ต่อ overnight information shock ทั้ง positive และ negative; มีการ mean-revert ตามมา
- **Dataset:** NYSE, AMEX, NASDAQ, 9,283 stocks
- **Apply to project:** ถ้า MU (หรือหุ้นใดก็ตาม) ขึ้น/ลงแรงข้ามคืน → expect short-term reversal; เพิ่ม rule ใน decision tree: "overnight gap > X% = overreaction likely → ลด aggression ในทิศทางนั้น หรือรอ retest"
- **Tag:** IMPLEMENT

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **Overnight News Topic Classification (2507.04481)** → เพิ่มใน pre-market brief: จัด news headlines เป็น topic types → assign overnight direction signal → complexity: **low** (เพิ่ม section ใน brief template)

2. **Overnight Gap Reversal Rule (SSRN 5648748)** → เพิ่มใน decision tree: "ถ้า overnight gap > 2% → likely overreaction → ลด size / รอ retest" → complexity: **low** (เพิ่ม rule 1 บรรทัด)

3. **Regime Filter + Multi-layer Confirmation (2601.19504)** → เพิ่ม EMA trend state + RSI zone ใน entry checklist ก่อน approve setup → complexity: **medium** (ต้องเพิ่ม indicator ใน script)

4. **V/P Intrinsic Value Check (2506.00206)** → เพิ่ม section "Intrinsic Value" ใน stock-research template: คำนวณ V = BV + PV(RI) จาก IR data → complexity: **medium** (ต้องดึง book value + EPS forecast จาก IR)

5. **Earnings Surprise Tone Analysis (2505.14420)** → ก่อน Q3 MU earnings: อ่าน call transcript แล้วระบุ HBM/guidance/capex tone → ประเมิน beat/miss probability → complexity: **medium** (manual analysis)

---

## Gaps

หัวข้อที่ยังไม่ครอบคลุม — search เพิ่มถ้าต้องการ:
- **Sector rotation signals** — เมื่อไหรที่ semiconductor cycle เปลี่ยน; leading indicators เฉพาะ memory sector
- **Cyclical stock valuation** — P/E ของ cyclical stocks ควรดูแตกต่างยังไง (normalized earnings, mid-cycle P/E)
- **Position sizing** — Kelly criterion, volatility-adjusted sizing สำหรับ individual stock entry
- **Stop-loss optimization** — งานวิจัยเรื่อง ATR-based vs fixed % stop

---

*Scope: 4 themes | Searches: 10/10 | Papers: 10 total — 4 IMPLEMENT, 6 REFERENCE, 0 SKIP*
