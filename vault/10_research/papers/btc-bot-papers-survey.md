# BTC Trading Bot — Paper Survey
*สำหรับ BTC/USDT bot บน Binance เท่านั้น | อัพเดต: 2026-05-04*
*links: [[_index-crypto-bot-papers]] | [[project-btc-bot]]*

---

## Tier 1 — Implement ก่อน (rule ชัด, backtest verified)

### 1. MA 20/100 Day Crossover — Grayscale Research (2023)
- **Source:** [The Trend is Your Friend](https://research.grayscale.com/reports/the-trend-is-your-friend-managing-bitcoins-volatility-with-momentum-signals)
- **Key finding:** Long BTC when price > 20d MA + 20d MA trending up; cash otherwise → Sharpe 1.7, ann. return 116% (2012–2023)
- **Signal:** price vs. MA20; MA20 vs. MA100 direction
- **Implementable:** ✅ ตรงไปตรงมา — MA windows ชัด, exit rule ชัด
- **Warning:** Decay post-2022 → ต้องรัน walk-forward re-optimization ทุก quarter

### 2. EMA Walk-Forward Optimization — arXiv 2602.10785 (2026)
- **Source:** [arXiv:2602.10785](https://arxiv.org/abs/2602.10785) | [GitHub code](https://github.com/tmr-crypto/wf_optim_crypto_analysis)
- **Key finding:** BTC intraday 1m–60m EMA — performance depends heavily on window; B&H + EMA combo ลด drawdown 50% vs. EMA alone; breakeven transaction cost ~0.4% (Binance 0.1% ✅)
- **Implementable:** ✅ GitHub มี code ครบ — walk-forward optimization framework พร้อมใช้

### 3. Intraday Momentum & Reversal — SSRN 4080253 (2022)
- **Source:** [SSRN 4080253](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4080253) | Journal of Financial Markets
- **Key finding:** Momentum ระยะ 1–4 ชั่วโมง (lagged return predict next hour), reversal ระยะ 6–24 ชั่วโมง
- **Signal:** ใช้ 1h lagged return → momentum; 6h+ lagged → expect reversal
- **Implementable:** ✅ window ชัด — code ได้เลย

### 4. Realized GARCH + Jump-Robust (Vol Sizing) — North American J. Econ. Finance (2020)
- **Source:** [ScienceDirect](https://ideas.repec.org/a/eee/ecofin/v52y2020ics1062940820300620.html)
- **Key finding:** BTC jump ถี่มาก → standard GARCH underestimate; RGARCH(1,1) + tri-power variation ชนะ OOS vol forecasting
- **Application:** ใช้สำหรับ **position sizing** — ให้ vol estimate ที่ robust กว่า GARCH ธรรมดา
- **Implementable:** ✅ คำนวณได้จาก OHLCV intraday, `arch` library Python รองรับ

---

## Tier 2 — ใช้เป็น supporting layer (regime + filter)

### 5. HMM Regime Detection — Preprints 202603.0831 (2026)
- **Source:** [Preprints.org](https://www.preprints.org/manuscript/202603.0831)
- **Key finding:** 3-state HMM (Bull/Bear/Neutral) บน BTC ด้วย daily returns + realized vol; HMM > ANN ใน regime transition prediction
- **Implementable:** ⚠️ บางส่วน — state definitions ชัด แต่ hyperparameters ต้อง calibrate
- **Note:** vault มีแล้ว: [[2604.20949-lob-microstructure-regimes]] ทำ intraday LOB version — daily version นี้ complement กัน

### 6. Bayesian HMM 4-State + Macro Covariates — MDPI Mathematics (2025)
- **Source:** [MDPI Mathematics 13(10):1577](https://www.mdpi.com/2227-7390/13/10/1577)
- **Key finding:** 4-state non-homogeneous HMM ที่ใช้ macro covariates (Fed rate, VIX, Gold) ร่วมกับ BTC price → best one-step-ahead forecasting
- **Implementable:** ⚠️ บางส่วน — macro covariate structure code ได้ แต่ไม่มี Sharpe report → ไม่รู้ trading PnL
- **Application:** ใช้เป็น macro regime filter ให้ momentum strategy (เปิด long เฉพาะตอน Bull regime)

### 7. BTC Trend-Following Decay Study — SSRN 4955617 (2024)
- **Source:** [SSRN 4955617](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4955617)
- **Key finding:** Trend-following strategies ที่ work ดีใน 2015–2021 decay ลงชัดใน 2022–2024; mean-reversion แย่กว่า; ต้องใช้ walk-forward
- **Application:** ⚠️ ใช้เป็น warning ไม่ใช่ implementation — validate ว่าทุก strategy ต้องมี walk-forward OOS test

---

## Tier 3 — Reference / ใช้บางส่วน

### 8. On-Chain + CNN-LSTM Price Direction — ScienceDirect (2025)
- **Source:** [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S266682702500057X)
- **Key finding:** MVRV-related on-chain features มี highest predictive power ต่อ next-day BTC direction; CNN-LSTM ให้ Sharpe 6.47
- **Warning:** ⚠️ Sharpe 6.47 สูงผิดปกติ — สงสัย lookahead bias; ใช้ on-chain feature list เป็น reference เท่านั้น
- **Application:** ดู feature list สำหรับ on-chain inputs (MVRV, realized cap, unrealized value)

### 9. Whale Txns + CryptoQuant → Vol Spikes — arXiv 2211.08281 (2022)
- **Source:** [arXiv:2211.08281](https://arxiv.org/abs/2211.08281)
- **Key finding:** Exchange net inflow spikes + large whale movements predict extreme vol spikes; Synthesizer Transformer ชนะ baseline
- **Application:** ใช้ CryptoQuant exchange flow data เป็น vol spike warning filter
- **Implementable:** ⚠️ CryptoQuant API ต้องการ subscription; whale alert ต้อง build Twitter listener

### 10. Cross-Sectional Momentum (BTC time-series component) — SSRN 4322637 (2023)
- **Source:** [SSRN 4322637](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4322637)
- **Key finding:** 30-day lookback → 7-day hold momentum มี consistent excess return; สำหรับ BTC โดดๆ: time-series momentum (BTC vs. cash) signal ชัดเจน
- **Implementable:** ✅ rule ตรงไปตรงมา แต่ full PDF ยังไม่ได้อ่านครบ — ยืนยัน thresholds ก่อน implement

---

## Vault Papers ที่มีอยู่แล้ว (สอดคล้องกับ BTC bot)

| Paper | Relevance |
|---|---|
| [[2604.26063-vp-macd]] | VP-MACD momentum signal — Tier 1, ready to code |
| [[2604.20949-lob-microstructure-regimes]] | HMM intraday LOB regime (38s lead time) — Tier 1 |
| [[2604.26747-constrained-llm-crypto-factors]] | LLM factor discovery daily crypto, Sharpe 2.4 |
| [[2604.01431-kalshi-macro-crypto-vol]] | Kalshi → BTC vol 5-day forecast |
| [[2603.25217-caviar-tail-risk-spillover]] | Tail risk spillover (cross-asset) |

---

## Build Order แนะนำ

```
Phase 1 — Core signal (implement ก่อน):
  VP-MACD (vault มีแล้ว) + MA 20/100 crossover (Grayscale)
  → สองตัวนี้ให้ momentum signal ทั้ง intraday และ daily

Phase 2 — Vol-based position sizing:
  RGARCH + tri-power variation (Hung et al. 2020)
  → ลด position ตาม realized vol, absorb jump risk

Phase 3 — Regime filter:
  HMM daily (Preprints 2026) หรือ LOB intraday (vault)
  → เปิด long เฉพาะตอน Bull regime

Phase 4 — Optional enhancement:
  On-chain filters (MVRV, exchange flows) ถ้า CryptoQuant accessible
```

---

*Sources: Grayscale Research, SSRN, arXiv, MDPI, ScienceDirect, Preprints.org*
*Researched: 2026-05-04 | 5 searches, 7 fetches*

---

## Update — 2026-05-05 | Phase 2 & 3 gaps

*Themes: Funding Rate Signal · Fear & Greed Index · Backtest Methodology | 8 searches | 9 papers*

---

### TL;DR — Top Picks (Phase 2 & 3)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | He et al. (2024) arXiv:2212.06888 | Funding Rate | Basis = crowding indicator; ccxt รองรับ fetch_funding_rate() ได้เลย |
| 2 | Finance Research Letters (2025) | Fear & Greed | FGI > 75 = overpriced ลด long; free API alternative.me |
| 3 | Bailey & Lopez de Prado (2014) SSRN:2460551 | Backtest | DSR — ต้อง implement ก่อน optimize param ใดๆ |
| 4 | Arian et al. (2024) SSRN:4686376 | Backtest | CPCV ชนะ walk-forward ทุก metric — upgrade validation |

---

### Theme A: Funding Rate / Perpetual Futures Signal

#### Fundamentals of Perpetual Futures — He, Manela, Ross, von Wachter (2024)
- **Source:** arXiv:2212.06888
- **Method:** No-arbitrage pricing model สำหรับ perpetual futures; แสดงว่า basis (perp − spot) co-move ข้าม exchanges และสอดคล้องกับ crowded momentum positions
- **Key finding:** Positive basis = momentum speculators crowded long → เกิด predictable mean-reversion; implied arbitrage strategy ให้ Sharpe สูง
- **Dataset:** Multiple crypto exchanges, daily + intraday [period unverified]
- **Apply to project:** ใช้ `ccxt.fetch_funding_rate("BTC/USDT:USDT")` บน Binance; คำนวณ basis z-score (30-day rolling); z-score > 2 = longs crowded → ลด position 50%
- **Tag:** IMPLEMENT

#### Funding Rate Mechanism in Perpetual Futures — Zhang (2026)
- **Source:** SSRN:6185958
- **Method:** Equilibrium model กับ risk-constrained arbitrageurs + momentum speculators; วิเคราะห์ Binance clamp-style funding rule
- **Key finding:** Binance clamp-style funding ให้ tail fatter กว่า linear rule → extreme funding rates (±0.1%/8h) เป็น contrarian signals ไม่ใช่ trend signals
- **Dataset:** Binance BTC/ETH perp [unverified — SSRN blocked]
- **Apply to project:** ที่ funding > +0.1%/8h → contrarian short bias; ที่ funding < −0.1%/8h → contrarian long bias; อย่าใช้เป็น momentum signal
- **Tag:** REFERENCE

#### Predictability of Funding Rates — Emre Inan (2025)
- **Source:** SSRN:5576424
- **Method:** DAR (Dynamic Autoregressive) models + Lyapunov exponents วิเคราะห์ out-of-sample predictability ของ funding rate บน Binance และ Bybit BTC perp
- **Key finding:** Funding rate (ไม่ใช่ price returns) มี out-of-sample predictability — สามารถ forecast "next funding print" ได้ → ใช้ predict ทิศทาง BTC ต่อไป
- **Dataset:** Binance + Bybit BTCUSDT perpetual; October 2025 [period/frequency unverified — SSRN ยัง blocked แต่ abstract verified via web]
- **Apply to project:** แทน AR(1) ธรรมดา → ใช้ DAR model บน 8h funding observations; ถ้า predicted next funding > 0 (longs pay) → ลด long 30 นาทีก่อน settlement; ถ้า predicted < 0 (shorts pay) → bias long
- **Tag:** IMPLEMENT

---

### Theme B: Fear & Greed Index as Trading Signal

#### Investor Sentiment and Cross-Section of Cryptocurrency Returns (2025)
- **Source:** Finance Research Letters, ScienceDirect (DOI unverified — author names blocked by paywall)
- **Method:** สร้าง portfolio sorted by "sentiment beta" (sensitivity ต่อ FGI alternative.me); Fama-MacBeth cross-sectional regression; 1,100+ cryptos
- **Key finding:** Coins ที่มี high positive sentiment beta (co-move กับ Greed) underperform ต่อมา — 3.57%/week premium สำหรับ intermediate-beta coins; FGI เป็น contrarian signal ไม่ใช่ momentum
- **Dataset:** 1,100+ cryptos จาก CoinMarketCap + daily FGI (alternative.me); Feb 2018 – Jul 2024
- **Apply to project:** FGI > 75 (Extreme Greed) ติดต่อกัน 3+ วัน → ลด BTC long 25–50%; FGI < 25 (Extreme Fear) → เปิด full position; API: `https://api.alternative.me/fng/` (free, no auth)
- **Tag:** IMPLEMENT

#### U-Shaped Relationship: Crypto Fear-Greed Index + Price Synchronicity (2023)
- **Source:** Finance Research Letters, ScienceDirect (author names unverified)
- **Method:** Panel regression หา relationship ระหว่าง FGI และ price synchronicity (all-coins-move-together)
- **Key finding:** Extreme fear และ extreme greed → synchronicity สูงสุด (BTC correlates ~1 กับ altcoins); moderate sentiment → idiosyncratic movement
- **Dataset:** Multi-coin panel [period/frequency unverified]
- **Apply to project:** เมื่อ FGI < 20 หรือ > 80 → treat portfolio as single-asset risk (ห้าม hedge BTC ด้วย crypto อื่น); ใช้เป็น regime flag ไม่ใช่ timing signal
- **Tag:** REFERENCE

---

### Theme C: Backtest Methodology / CPCV / Deflated Sharpe

#### Backtest Overfitting in the Machine Learning Era — Arian, Norouzi, Seco (2024)
- **Source:** SSRN:4686376 / Knowledge-Based Systems
- **Method:** Synthetic controlled environment (known ground truth) benchmark: K-Fold, Purged K-Fold, Walk-Forward, CPCV, Bagged CPCV, Adaptive CPCV; metrics = PBO + DSR
- **Key finding:** CPCV ชนะทุก method ใน minimizing PBO และ maximizing DSR; Walk-forward (industry standard) แพ้ CPCV อย่างชัดเจน
- **Dataset:** Synthetic financial time series (non-stationary, autocorrelated, regime-switching)
- **Apply to project:** Implement CPCV บน BTC 1h data เพื่อ validate parameter configs (VP-MACD windows, HMM states, funding rate thresholds) ก่อน live; ใช้ `mlfinlab` library
- **Tag:** IMPLEMENT

#### DRL for Crypto Trading: Addressing Backtest Overfitting — Gort et al. (2023)
- **Source:** arXiv:2209.05559
- **Method:** Trains multiple DRL agents; estimate PBO per agent using Bailey & Lopez de Prado framework; reject overfitted agents ก่อน deployment; ทดสอบใน crash period (May–Jun 2022)
- **Key finding:** Low-PBO agents outperform high-PBO agents และ equal-weight benchmark ในช่วง crash; filter งานจริง
- **Dataset:** 10 cryptos; May 1 – Jun 27, 2022 (crash period); exchange/frequency unverified
- **Apply to project:** สำหรับทุก hyperparameter config ที่ test (GARCH params, HMM state count), compute PBO score; reject ถ้า PBO > 0.5; ต้องทำก่อน go-live
- **Tag:** IMPLEMENT

#### Interpretable Walk-Forward Validation Framework — Deep, Deep, Lamptey (2025)
- **Source:** arXiv:2512.12924
- **Method:** 34 non-overlapping test windows; rolling expanding training window; full information discipline; realistic transaction costs; RL + interpretable signals
- **Key finding:** Microstructure signals work only ใน high-volatility regimes (2020–2024); fail ใน stable markets (2015–2019); Sharpe 0.33 overall — result น้อยแต่ methodology ดี
- **Dataset:** 100 US equities, 2015–2024, daily (ไม่ใช่ crypto)
- **Apply to project:** ใช้ 34-split protocol เป็น template: BTC 5y hourly data → ~20 non-overlapping 3-month test windows + 12-month expanding training; report Sharpe per regime separately
- **Tag:** REFERENCE (methodology template; equity data ไม่ใช่ crypto)

#### The Deflated Sharpe Ratio — Bailey & Lopez de Prado (2014)
- **Source:** SSRN:2460551 / Journal of Portfolio Management
- **Method:** Extends Sharpe Ratio ให้ account for (1) จำนวน strategies ที่ test, (2) extreme value distribution ของ Sharpe under pure noise, (3) non-normality (skew/kurtosis)
- **Key finding:** สำหรับ N strategies ที่ test, expected max Sharpe จาก random search โตตาม √(log N); ทุก reported Sharpe ต้อง deflate; 100 configs tested → ต้องการ Sharpe 2× สูงกว่า normal threshold
- **Dataset:** Theoretical/illustrative
- **Apply to project:** ทุกครั้งที่ optimize param ใดๆ (funding rate threshold, FGI cutoff, MACD windows) → log N (จำนวน configs tested) → compute DSR; ยอมรับ config เฉพาะ DSR > 0.95; implement ใน ~20 lines Python
- **Tag:** IMPLEMENT

---

### Updated Build Order (Phase 2 & 3)

```
Phase 2a — Deflated Sharpe Ratio utility (IMPLEMENT ก่อนสุด):
  Bailey & Lopez de Prado (SSRN:2460551) → ~20 lines Python
  → ใช้ทุกครั้งที่ optimize parameter ใดๆ

Phase 2b — Walk-forward → CPCV upgrade:
  Arian et al. (SSRN:4686376) → mlfinlab CPCV implementation
  → validate VP-MACD + HMM + GARCH configs OOS

Phase 3a — Funding rate filter (free, Binance native):
  He et al. (arXiv:2212.06888) → ccxt.fetch_funding_rate()
  → basis z-score contrarian signal; reduce long เมื่อ z-score > 2

Phase 3b — Fear & Greed gate (free API):
  Finance Research Letters (2025) → alternative.me/fng API
  → FGI > 75 consecutive 3d = reduce long 25-50%
```

---

### Gaps (Phase 2 & 3)

- SSRN 5576424 (Inan 2025): funding rate predictability — full methodology blocked (paywall); fetch เมื่อ accessible
- FGI academic papers มี author names unverified (ScienceDirect blocked); ต้องยืนยันก่อน cite ใน report
- CPCV implemented on real BTC hourly data — ยังไม่มี paper; ใช้ `mlfinlab` docs แทน
- BTC-specific funding rate regression coefficients — He et al. cover multi-crypto; BTC alone ยังไม่ clear

*Scope: 3 themes | Searches: 8/8 | Papers: 9 total — 5 IMPLEMENT, 3 REFERENCE, 1 SKIP (none)*
