# Paper Survey — Quantitative Trading Logic
*Project context: equity swing trading system (US stocks, pre-market brief, decision tree) | 2026-05-05 | Scope: 3 themes | 9 searches | 7 papers*
*Note: Execution logic ครอบคลุมแล้วใน vault/10_research/papers/2603.28898-mpc-trade-execution.md (MPC, 40-50% slippage reduction)*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | AlgoXpert IS-WFA-OOS (2603.09219, 2026) | Backtest | protocol 3-stage ป้องกัน overfitting — implement ก่อน backtest อะไรก็ตาม |
| 2 | Kelly+VIX Hybrid Sizing (2508.16598, 2025) | Position Sizing | ปรับ position size ตาม VIX-Rank อัตโนมัติ — ตรงกับที่ทำอยู่แล้ว (VIX caution zone) |
| 3 | Forecast-to-Fill ATR Exits (2511.08571, 2025) | Position Sizing | fractional Kelly + ATR stop-loss ใน 1 framework — Sharpe 2.88 จาก walk-forward จริง |
| 4 | Not All Factors Crowd Equally (2512.11913, 2025) | Alpha Decay | momentum decays hyperbolically — รู้ว่าสัญญาณ momentum จะหมดอายุเร็วแค่ไหน |

---

## Papers by Theme

### Theme 1: Position Sizing

#### Sizing the Risk: Kelly, VIX, and Hybrid Approaches — Wysocki (Aug 2025)
- **Source:** [arXiv:2508.16598](https://arxiv.org/abs/2508.16598)
- **Method:** เปรียบ 3 วิธี sizing: (1) Kelly criterion ดั้งเดิม (2) VIX-Rank scaling — normalize VIX เป็น percentile แล้วใช้ scale position size (3) Hybrid = Kelly × VIX-Rank weight; ทดสอบบน SPXW put-writing 0-5 DTE
- **Key finding:** Hybrid method ได้ balance ระหว่าง return กับ drawdown ดีที่สุด โดยเฉพาะใน low-volatility regime (2024); full Kelly อันตรายเพราะ path volatility สูง
- **Dataset:** S&P500 index options (SPXW), 2024
- **Apply to project:** นำ VIX-Rank formula มาแทนการใช้ VIX level เฉยๆ — ตอนนี้ระบบบอก "VIX 18 = ลด 20-30%" แบบ rule of thumb; VIX-Rank ทำให้ position size ปรับเป็น continuous function ตาม percentile ไม่ใช่ step function; เหมาะสำหรับ MU entry sizing โดยตรง
- **Tag:** IMPLEMENT

#### Forecast-to-Fill: Benchmark-Neutral Alpha — (Nov 2025)
- **Source:** [arXiv:2511.08571](https://arxiv.org/abs/2511.08571)
- **Method:** Rolling 10-year train → 6-month test walk-forward (2015-2025); แปลง trend-momentum regime signal เป็น position ด้วย fractional impact-adjusted Kelly sizing; ออกจาก position ด้วย ATR-based adaptive exits
- **Key finding:** Sharpe 2.88, max drawdown 0.52%, CAGR 43%, alpha 37% vs benchmark; beta ≈ 0.03 (market neutral จริง); ATR exits ปรับ stop-loss ตาม volatility ปัจจุบันอัตโนมัติ
- **Dataset:** Gold futures, 2,793 trading days, 2015-2025
- **Apply to project:** เปลี่ยน fixed % stop-loss ใน decision tree ให้เป็น ATR-based — ตอนนี้ระบบใช้ S/R levels แบบ static; ATR stop คือ `entry_price ± (N × ATR14)` ซึ่ง shrink ตาม vol ต่ำ และ widen ตาม vol สูง — ตรงกับ Iran risk environment ที่มีอยู่
- **Tag:** IMPLEMENT

---

### Theme 2: Backtest Methodology & Overfitting Prevention

#### AlgoXpert Alpha Research Framework — (arXiv:2603.09219, Mar 2026)
- **Source:** [arXiv:2603.09219](https://arxiv.org/abs/2603.09219)
- **Method:** 3-stage protocol: **IS** (In-Sample) — หา stable parameter region ไม่ใช่ peak; **WFA** (Walk-Forward Analysis) — rolling windows + purge gaps ลด information leakage + majority pass rule + catastrophic veto; **OOS** (Out-of-Sample) — parameter lock สมบูรณ์ ห้าม tune เพิ่ม; มี circuit breakers + kill switch
- **Key finding:** Protocol ลด transition failure (backtest → live) ได้ชัดเจน; cliff veto และ execution controls ป้องกัน strategies ที่ดูดีแต่ fragile; tested on USDJPY M5 intraday
- **Dataset:** USDJPY M5, intraday
- **Apply to project:** ใช้ IS-WFA-OOS เป็น standard ก่อน deploy rule ใหม่ใดก็ตามใน decision tree — ถ้าจะ add ATR stop หรือ EMA filter ต้อง backtest ผ่าน 3 stage นี้ก่อน ไม่ใช่ optimize แล้ว deploy เลย
- **Tag:** IMPLEMENT

#### Backtest Overfitting in the ML Era — Arian, Norouzi, Seco (SSRN, Jan 2024)
- **Source:** [SSRN:4686376](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4686376)
- **Method:** เปรียบ cross-validation methods บน synthetic controlled environment: K-Fold, Purged K-Fold, Walk-Forward, **Combinatorial Purged Cross-Validation (CPCV)**; วัด Probability of Backtest Overfitting (PBO) และ Deflated Sharpe Ratio (DSR)
- **Key finding:** CPCV ดีสุดในทุก metric — PBO ต่ำสุด, DSR สูงสุด; Walk-Forward ที่นิยมใช้กันยังมี overfitting risk สูงกว่า CPCV อย่างมีนัยสำคัญ; financial data ที่ non-stationary + autocorrelated ต้องการ method พิเศษ
- **Dataset:** Synthetic controlled environments (designed to test overfitting)
- **Apply to project:** ใช้ DSR (Deflated Sharpe Ratio) แทน Sharpe ธรรมดาเมื่อ evaluate backtests — DSR adjust สำหรับ multiple testing และ non-normality; ถ้า DSR < 0 strategy นั้น likely overfit
- **Tag:** IMPLEMENT

---

### Theme 3: Alpha Decay & Factor Signal Quality

#### Not All Factors Crowd Equally — (arXiv:2512.11913, Dec 2025)
- **Source:** [arXiv:2512.11913](https://arxiv.org/abs/2512.11913)
- **Method:** Derive hyperbolic decay form α(t) = K/(1+λt) จาก game-theoretic equilibrium model; test กับ linear และ exponential alternatives บน 8 equity factors; วัด crowding acceleration จาก ETF volume growth
- **Key finding:** Momentum decay hyperbolically (R²=0.65 vs linear 0.51); value/quality ไม่ fit model — decay ต่างกันมาก; ETF growth post-2015 เร่ง crowding (ρ=−0.63 กับ ETF volume); model over-predict remaining alpha หลัง 2015
- **Dataset:** US equity factors (momentum, value, reversal, quality), 1995-2024
- **Apply to project:** MU momentum ที่เห็นวันนี้มี half-life จำกัด — hyperbolic form บอกว่า alpha ร่วงเร็วช่วงแรกแล้วค่อย plateau; อย่า hold momentum trade นานเกิน 1-2 สัปดาห์โดยไม่ re-evaluate; value signal (V/P จาก equity-valuation-survey) decay ช้ากว่า — hold ได้นานกว่า
- **Tag:** IMPLEMENT

#### On the Effect of Alpha Decay and Transaction Costs — (arXiv:2502.04284, Feb 2025)
- **Source:** [arXiv:2502.04284](https://arxiv.org/abs/2502.04284)
- **Method:** Multi-period optimal trading model ที่รวม alpha decay (past signal values มี predictive power) กับ transaction costs; derive optimal trading strategy ภายใต้ signal decay
- **Key finding:** ถ้า alpha decay เร็ว optimal strategy คือ trade aggressively เร็วๆ แล้วออก; ถ้า decay ช้า optimal คือ trade ช้าลงเพื่อลด transaction costs; transaction costs บังคับให้ underreact ต่อ signal แม้รู้ว่า decay
- **Dataset:** Theoretical (closed-form solutions)
- **Apply to project:** เมื่อ signal แรง (เช่น MU momentum วันนี้) แต่ commission + spread สูงเทียบกับ expected alpha ที่เหลือ → optimal คือลดขนาด trade หรือรอ entry ที่ดีกว่า ไม่ใช่ไล่ราคา
- **Tag:** REFERENCE

---

### Existing Vault Papers ที่ Relevant (ไม่ต้อง search ซ้ำ)

| Paper | Theme | Location |
|---|---|---|
| MPC Trade Execution (2603.28898) | Execution / Slippage | `vault/10_research/papers/2603.28898-mpc-trade-execution.md` |
| Interpretable Hypothesis-Driven Trading (2512.12924) | Backtest / Walk-Forward | `vault/10_research/papers/equity-valuation-trading-survey.md` |

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **Deflated Sharpe Ratio metric (SSRN 4686376)** → ใช้ DSR แทน Sharpe ทุกครั้งที่ evaluate backtest — complexity: **low** (formula พร้อมใช้)

2. **ATR-based stop-loss (2511.08571)** → แทนที่ fixed S/R stop ใน decision tree ด้วย `stop = entry ± (2 × ATR14)` — complexity: **low** (เพิ่ม ATR calculation ใน sr-levels.py)

3. **VIX-Rank position sizing (2508.16598)** → แทน "VIX 18 = ลด 20-30%" ด้วย continuous VIX percentile scaling — complexity: **low** (เพิ่มใน macro-snapshot.py)

4. **IS-WFA-OOS protocol (2603.09219)** → ใช้ทุกครั้งก่อน deploy rule ใหม่ใน system — complexity: **medium** (ต้องมี backtest framework)

5. **Momentum decay half-life (2512.11913)** → เพิ่ม rule: momentum signal > 1 สัปดาห์ → re-evaluate; อย่า hold momentum trade นาน — complexity: **low** (rule เพิ่มใน decision tree)

---

## Gaps

- **Optimal hold period per signal type** — งานวิจัยเฉพาะเรื่อง holding period optimization สำหรับ swing trade (2-10 วัน)
- **Multi-asset correlation in position sizing** — Kelly ใน portfolio context (ไม่ใช่ single stock)
- **Regime detection** — งานวิจัยเรื่องการ identify market regime อัตโนมัติ (HMM, changepoint detection)

---

*Scope: 3 themes | Searches: 9/9 | Papers: 7 total (5 new IMPLEMENT, 1 new REFERENCE, 1 SKIP) + 2 existing vault papers referenced*
