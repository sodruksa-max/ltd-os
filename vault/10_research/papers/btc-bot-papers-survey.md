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
