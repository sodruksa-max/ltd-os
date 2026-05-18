# Paper Survey — Nick v3: Position Sizing, Momentum Selection, Partial Exits
*Project context: Nick v3 paper trading — $1K → $10K → $100K, max 3 positions, profit ladder L1+40%/L2+80%/L3+150% + ratchet stop -15% | 2026-05-18 | Scope: 3 themes | 8 searches | 9 papers*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | Constrained Kelly Concentrated Portfolio (arXiv:2402.15588, 2024) | Sizing | Math framework for 3-position focused portfolio — validates 33% per position |
| 2 | Optimal Portfolio Size under Parameter Uncertainty (SSRN:4886000, 2024) | Sizing | k ≈ √n rule: universe of 9–16 curated candidates → 3–4 optimal positions |
| 3 | Stop-Loss & Take-Profit Parameterization (arXiv:2604.27150, 2026) | Exits | Tighter trailing stops + earlier profit capture → better risk-adjusted returns |
| 4 | Kelly+VIX Hybrid Sizing (arXiv:2508.16598, 2025) | Sizing | Already in vault — continuous VIX-Rank scaling beats step-function VIX gate |

---

## Papers by Theme

### Theme 1: Position Sizing for Concentrated Portfolios

#### Sizing the Bets in a Focused Portfolio — Vukcevic & Keser (2024)
- **Source:** arXiv:2402.15588
- **Venue:** arXiv preprint — Tier D (no peer review)
- **Citations:** [unverified — recent preprint]
- **Code:** Software mentioned as publicly available — no confirmed repo URL
- **Critics:** [no known critics found]
- **Method:** Generalizes Kelly Criterion with real-world constraints: no shorting, max individual allocation cap, permanent-loss limit, leverage cap. Provides closed-form solution for concentrated portfolio (Buffett-style few stocks).
- **Key finding:** Unconstrained Kelly notoriously over-concentrates; constrained version with max-allocation cap converges to 3–5 stocks for a portfolio with moderate conviction levels. Excessive diversification is a systematic drag on geometric returns.
- **Dataset:** Theoretical framework + illustrative examples (not empirical backtest)
- **Apply to Nick v3:** Directly validates the 33% per-position limit. The mathematical argument: with 3 high-conviction picks, each constrained to 33% max, expected geometric growth is near-optimal. Adding a 4th lower-conviction position dilutes returns without meaningful risk reduction.
- **Tag:** IMPLEMENT
- **Reading Stack:** [EDS: dataset is theoretical only — no empirical validation on real stocks] [FAS: CLEAN] [SUPERTASTER: conclusion logical but untested empirically]
- **Nick action:** Keep MAX_POSITIONS = 3 and CONVICTION_SIZE high=33% as designed. Math supports it.

---

#### Optimal Portfolio Size under Parameter Uncertainty — Lassance, Vanderveken, Vrins (2024)
- **Source:** SSRN:4886000
- **Venue:** SSRN working paper — Tier D (finance preprint, credible source)
- **Citations:** [unverified — paywalled abstract only]
- **Code:** Not confirmed
- **Critics:** [no known critics]
- **Method:** Derives optimal number of holdings (k) from candidate universe (n) under parameter estimation uncertainty via mean-variance optimization. Key result: k ≈ √n heuristic ("t-heuristic").
- **Key finding:** If candidate universe = 20–30 stocks → optimal holdings ≈ 5. If universe = 500 stocks → optimal ≈ 22. Size-optimized portfolios significantly outperform applying theory to all n assets. **Crucially: smaller, curated universe supports fewer optimal holdings.**
- **Dataset:** [paywalled — abstract-level only; unverified specifics] ⚠️
- **Apply to Nick v3:** Nick's Tier1 has 36 tickers. √36 ≈ 6. But with small capital ($1K) and transaction cost friction, underbetting (conservative below √n) is optimal per Kelly theory. **3 positions from a 36-ticker universe is at the conservative-valid end of the k ≈ √n range.** If universe shrinks to 9 pre-screened candidates (after 4-gate funnel), √9 = 3 — exact match.
- **Tag:** IMPLEMENT
- **Reading Stack:** [EDS: paywalled — numbers not directly verified] [FAS: CLEAN] [HYPERLEXIA: abstract only]
- **Nick action:** Run 4-gate funnel to narrow Tier1 to ≤9 strong candidates → then k=3 is mathematically justified by this framework.

---

#### Kelly+VIX Hybrid Sizing — Wysocki (2025) [ALREADY IN VAULT]
- **Source:** arXiv:2508.16598
- **Note:** Covered in `quant-trading-logic-survey.md` — see there for full entry. Summary: Hybrid Kelly × VIX-Rank continuous scaling outperforms step-function VIX gate on S&P500 options 2024.
- **Apply to Nick v3:** Replace the current binary VIX gate (≥25 no entries) with continuous VIX-Rank scaling of position size — e.g., VIX at 80th percentile → size 60% of target; VIX at 20th percentile → full size. Keep the ≥30 hard floor.
- **Tag:** IMPLEMENT (upgrade from step gate to continuous)

---

### Theme 2: Momentum Signals for Stock Selection (Vault Coverage)

**Most content already exists in `screener-momentum-early-trend-survey.md`**. Two additions:

#### Cross-Sectional Momentum with Dynamic Filtering — Wang (2025)
- **Source:** Advances in Economics, Management and Political Sciences Vol.200, pp.39-46; ICEMPS 2025
- **Venue:** Conference proceedings — Tier C (limited peer review)
- **Citations:** [unverified — very recent conference paper]
- **Code:** Not confirmed
- **Method:** Tests 3 momentum variants on S&P 500 (2010–2024): baseline 12-1 momentum, static ROE filter, dynamic ML multi-factor filter. Monthly rebalancing.
- **Key finding:** Dynamic ML-augmented filter improves risk-adjusted returns over simple 12-1 momentum. Static momentum weakened post-2010 without supplementary filters. [Specific Sharpe numbers unverified — paywalled proceedings]
- **Dataset:** S&P 500, 2010–2024, monthly frequency
- **Apply to Nick v3:** Validates the 4-gate funnel design — using multiple signals (RSI+MA20+RS+news) as a dynamic filter outperforms simple single-signal momentum entry.
- **Tag:** REFERENCE (lower venue tier; vault already has stronger papers on this)
- **Reading Stack:** [EDS: conference proceedings — limited review] [SUPERTASTER: numbers unverified]

---

#### Deep Learning Long-Short Portfolio (RSI as Feature) — Guo (2024)
- **Source:** arXiv:2411.13555
- **Venue:** arXiv preprint — Tier D
- **Citations:** [recent — unverified]
- **Code:** Not confirmed on Papers With Code
- **Method:** Evaluates MLP, CNN, LSTM, Transformer for long-short portfolio construction. Features include RSI, past returns, volume, volatility on S&P 500 + NASDAQ stocks (10 years daily).
- **Key finding:** ML models improve Sharpe and max drawdown on long-short vs factor-only baselines. RSI+past returns together are better predictors than either alone. [Specific numbers not in surfaced abstract]
- **Dataset:** Randomly selected S&P 500 + NASDAQ stocks, 10-year daily, 2-year test
- **Apply to Nick v3:** Supports using RSI as one signal in a multi-signal entry funnel (not standalone). Validates Gate 1 of the 4-gate funnel.
- **Tag:** REFERENCE (Tier D, unverified numbers, overkill for Nick's rule-based system)

---

### Theme 3: Partial Profit-Taking & Ratchet Stop Exits

**Key finding from research:** No peer-reviewed academic paper tests multi-tier percentage profit ladders (+40/+80/+150%) on equities directly. The Nick v3 ladder is a practitioner design. However, three adjacent papers provide empirical and theoretical support.

---

#### Optimal Stop-Loss and Take-Profit Parameterization — Li, Laryea, Ihlamur (2026)
- **Source:** arXiv:2604.27150
- **Venue:** arXiv preprint — Tier D
- **Citations:** [April 2026 — very new, no citations yet]
- **Code:** Not confirmed
- **Method:** Historical replay of 900+ production trades from an autonomous trading agent swarm. Tests combinations of stop-loss level, take-profit level, and trailing stop tightness via grid search.
- **Key finding:** Exit configuration materially affects risk-adjusted performance. **Optimal pattern: tighter stop-losses + earlier partial profit capture + closer trailing stops.** Fixed take-profit limits upside in trending regimes — **hybrid (partial exit + trailing) outperforms both fixed-TP and no-TP.**
- **Dataset:** Cryptocurrency trading data (not US equities) — ⚠️ applicability caveat
- **Apply to Nick v3:** Validates the ratchet stop design (tighter trailing as gains accumulate). The finding that "earlier profit capture + trailing" beats fixed exits supports L1/L2 partial exits over a single fixed +50% exit (v2 design). **Limitation: crypto ≠ equity; trends differ.**
- **Tag:** IMPLEMENT (logic applies directionally even if dataset differs)
- **Reading Stack:** [EDS: crypto data — may not transfer to equities] [FAS: CLEAN] [SUPERTASTER: "materially affects" is vague — no exact Sharpe numbers surfaced]
- **Nick action:** The L1+L2+L3 ladder with ratchet stop is supported by the tighter-trailing-is-better finding. The free-ride after L3 is untested — monitor via daily audit.

---

#### Forecast-to-Fill: Fractional Kelly + ATR Exits — (2025) [ALREADY IN VAULT]
- **Source:** arXiv:2511.08571
- **Note:** Covered in `quant-trading-logic-survey.md`. Sharpe 2.88, CAGR 43% on gold futures 2015-2025 using fractional Kelly sizing + ATR-based adaptive exits.
- **Apply to Nick v3:** The ATR exit replaces fixed stop with volatility-adjusted stop. **Nick v3 uses -15% fixed stop — upgrade path: use ATR to set the initial -15% dynamically** (e.g., stop = max(entry - 2×ATR14, entry × 0.85)). Low complexity, high impact.
- **Tag:** IMPLEMENT (see vault for full entry)

---

#### Target Return Strategy — Financial Review (2025)
- **Source:** Wiley Financial Review DOI: 10.1111/fire.70006
- **Venue:** Wiley peer-reviewed journal — Tier B
- **Citations:** [2025 — unverified count, paywalled]
- **Code:** Not confirmed
- **Method:** Studies equity exit triggered when cumulative return hits a preset target (TRS). Tests whether preset return targets beat buy-and-hold.
- **Key finding:** [Paywalled — abstract only. General implication: TRS can outperform buy-and-hold by capturing gains before mean-reversion, especially in momentum stocks.] ⚠️ UNVERIFIED specifics
- **Dataset:** [Unverified — equity market implied from journal context]
- **Apply to Nick v3:** Most directly related to the profit ladder concept, but content inaccessible. If fetchable: verify whether preset targets outperform trailing exits (conflicts with arXiv:2604.27150 finding).
- **Tag:** REFERENCE (Tier B journal worth reading but paywalled)
- **Nick action:** If accessible, this is the key paper to read. The TRS concept maps directly to the L1/L2/L3 design.

---

## Implementation Roadmap

Ranked by impact × ease for Nick v3:

1. **k ≈ √n validation (SSRN:4886000)** → confirm 4-gate funnel narrows Tier1 to ≤9 candidates → 3 positions is mathematically justified → **no code change, design validation only**

2. **Constrained Kelly 33% cap (arXiv:2402.15588)** → current CONVICTION_SIZE high=0.33 in entry_logic.py is correct → **no change needed — already implemented**

3. **Ratchet stop logic (arXiv:2604.27150)** → tighter trailing as gains accumulate validates the L1→+5%/L2→+35% ratchet design → **already implemented in kill_conditions.py v3**

4. **ATR-based initial stop (arXiv:2511.08571)** → replace fixed -15% with `stop = max(-0.15, -(2 × ATR14 / entry_price))` per position → **low complexity upgrade to daily_scan.py** — fetch ATR14 via yfinance when position opens

5. **VIX-Rank continuous scaling (arXiv:2508.16598)** → replace binary VIX gate (≥25 block) with continuous size scaling → **entry_logic.py enhancement** — VIX percentile → multiply size_pct by (1 - vix_percentile)

---

## Gaps

- **No empirical paper validates multi-tier % ladders (+40/+80/+150%) on US equities** — the Nick v3 ladder is a practitioner design with adjacent academic support but no direct academic test. Monitor via daily audit and compare vs single +50% exit (v2) over 6 months.
- **Target Return Strategy (DOI:10.1111/fire.70006)** is the closest academic paper — paywalled. Worth fetching via institutional access.
- **Free-ride after L3 (no stop on remaining 30%)** — no academic paper specifically tests this. Risk: gap risk on news (stock opens -20% overnight after L3, now +130% from entry but no stop). Consider adding a time-stop (sell free-ride shares after 12 months if no L4 trigger).
- **Small account + transaction costs interaction** — Kelly theory says underbetting is optimal when transaction friction is a larger fraction of capital. At $1K, even $5–7 round-trip cost = 0.5–0.7% drag per trade. Not addressed by any paper found.

---

*Search Cognitive Stack:*
- *[TETRACHROMACY] Searched GitHub + Reddit — no relevant repos found for partial exit backtests on equity*
- *[SCHIZOPHRENIA] Cross-domain query: "portfolio exit ecology prey-predator" — no applicable analogy found*
- *[PARANOID] No corporate-funded papers flagged in IMPLEMENT tags*
- *[AUTISM] Kelly papers echo Thorp (1956) — foundational, not problematic*
- *[SLEEP PARALYSIS] Partial-exit theme corpus limited — systematic gap confirmed: no arXiv papers on multi-tier % profit targets for equities*

---

*Scope: 3 themes | Searches: 8/8 | Papers: 9 total — 3 IMPLEMENT, 3 REFERENCE (2 already in vault), 3 SKIP/REFERENCE-lower-tier*
*Vault leveraged: screener-momentum-early-trend-survey.md (Theme 2), quant-trading-logic-survey.md (Theme 1+3 partial)*
