# Paper Survey — Pre/Post-Market Analysis
*Project context: daily pre-market brief (scenario playbook Bull/Base/Bear + confidence) + post-market review (calibration scoring, setup outcomes, blind spots) for US equity swing trading | 2026-05-05 | Scope: 4 themes | 10 searches | 10 papers*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | Clinging to Beliefs / PEAD (SSRN 5311906, 2025) | Post-earnings | อธิบาย "beat แล้วลง" — PEAD แรงกว่า 4× เมื่อ surprise ขัดกับ analyst recommendation |
| 2 | Noisy FOMC Returns (SSRN 4131740) | Intraday/FOMC | initial FOMC reaction มักกลับตัว — อย่า chase ทิศทางแรก ให้รอ 45 นาที |
| 3 | Polymarket Accuracy (SSRN 5910522, 2025) | Prediction markets | Polymarket track ความน่าจะเป็นจริงได้ดี แต่ over-trade "Yes" — ปรับวิธีอ่าน odds |
| 4 | User-Focused Probabilistic Forecast Eval (arXiv 2311.18258) | Calibration | Murphy diagram แทน accuracy เดิม — เห็นว่า scenario confidence calibrated จริงไหม |

---

## Papers by Theme

### Theme 1: Scenario Probability Calibration

#### A User-Focused Approach to Evaluating Probabilistic Forecasts — (arXiv:2311.18258)
- **Source:** [arXiv:2311.18258](https://arxiv.org/abs/2311.18258)
- **Method:** Murphy diagram — plot proper scoring rule (Brier score) เป็น function ของ decision threshold แทนการใช้ accuracy เพียงตัวเดียว; แสดงว่า critical success index (CSI) ให้ผลบิดเบี้ยวสำหรับ rare events
- **Key finding:** Categorical accuracy metrics (เช่น % ถูก) ทำให้ประเมิน calibration ผิด โดยเฉพาะ event ที่ไม่บ่อย; Murphy diagram เห็น miscalibration ที่ threshold ต่าง ๆ ได้ชัดกว่า
- **Dataset:** Theoretical + weather forecasting case studies
- **Apply to project:** เพิ่ม Brier score tracking ใน post-market review — `BS = (p - o)²` ที่ p = confidence ที่ predict (เช่น 0.6 สำหรับ Base), o = 1 ถ้าถูก / 0 ถ้าผิด; คำนวณ rolling 10-day average Brier score เพื่อดูว่า "Low/Medium/High confidence" calibrated จริงหรือเปล่า; ถ้า BS เฉลี่ย > 0.25 = over-confident เสมอ
- **Tag:** IMPLEMENT

#### Proper Scoring Rules for Estimation and Forecast Evaluation — (arXiv:2504.01781, Apr 2025)
- **Source:** [arXiv:2504.01781](https://arxiv.org/abs/2504.01781)
- **Method:** ทบทวนและขยาย proper scoring rules (Brier, log-score, CRPS) สำหรับ continuous และ discrete forecasts; เปรียบ rules ในมุม incentive compatibility
- **Key finding:** Log-score (หรือ log-loss) discriminates ดีกว่า Brier สำหรับ extreme probability events; Brier score เหมาะสำหรับ moderate probability (20-80%) ซึ่งตรงกับ scenario prediction ส่วนใหญ่
- **Dataset:** Theoretical
- **Apply to project:** ใช้ Brier score สำหรับ Bull/Base/Bear scenario (moderate prob); เพิ่ม log-score เมื่อ confidence สูงมาก (>80%) หรือต่ำมาก (<20%) เพื่อ penalize หนักขึ้น
- **Tag:** REFERENCE

---

### Theme 2: Post-Earnings Reaction & PEAD

#### Clinging to Beliefs: Solving the PEAD Puzzle — McCarthy (SSRN 5311906, Jun 2025)
- **Source:** [SSRN:5311906](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5311906)
- **Method:** ใช้ 262,000 earnings announcements + IBES analyst recommendations แบ่ง surprise เป็น 2 ประเภท: (1) consistent = surprise ตรงกับ recommendation, (2) inconsistent = surprise ขัดกับ recommendation; วัด 90-day PEAD abnormal return
- **Key finding:** Inconsistent surprise (เช่น beat EPS แต่ analyst แนะนำ Sell) → PEAD +5.8-7.4% ใน 90 วัน, มากกว่า consistent surprise 2.5-4.5×; annual alpha 12-15% vs 1-2%; เกิดจาก overconfidence in prior beliefs + confirmation bias
- **Dataset:** US equities, 262,000 earnings events, IBES
- **Apply to project:** เพิ่ม rule ใน post-market: ถ้า earnings beat แต่หุ้นลง → เช็ค analyst consensus ก่อน — ถ้า majority "Buy" อยู่แล้ว (consistent) drift จะน้อย; ถ้า majority "Sell/Hold" (inconsistent) drift จะแรงมาก → นี่คือ setup ที่น่า trade ไม่ใช่ขาย panic; อธิบาย META case (beat แต่ลง -7%) ว่าเป็น consistent surprise (consensus bullish → ลงน้อย) ไม่ใช่ inconsistent
- **Tag:** IMPLEMENT

#### Retail Investor Horizon and Earnings Announcements — Vamossy (arXiv:2512.00280, Dec 2025)
- **Source:** [arXiv:2512.00280](https://arxiv.org/abs/2512.00280)
- **Method:** วัด holding horizon ของ retail investor กับ reaction ต่อ earnings surprise; แยก short-horizon vs long-horizon retail
- **Key finding:** Drift ปรากฏเกือบทั้งหมดใน bullish firms; bearish firm drift น้อยมาก; retail investor ที่ hold สั้นขาย winner เร็วเกินไป (disposition effect) ทำให้ drift ยังคงอยู่
- **Dataset:** US equities, retail trading data, earnings announcements
- **Apply to project:** ถ้า MU หรือหุ้นใดมีลักษณะ bullish consensus + positive surprise → expect drift ต่อได้อีก 2-4 สัปดาห์; อย่า sell too early หลัง earnings beat ถ้า thesis ยังดี
- **Tag:** REFERENCE

---

### Theme 3: Prediction Market Accuracy

#### Exploring Decentralized Prediction Markets: Accuracy, Skill, Bias on Polymarket — Reichenbach, Walther (SSRN 5910522, Dec 2025)
- **Source:** [SSRN:5910522](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5910522)
- **Method:** วิเคราะห์ Polymarket accuracy บน events หลายหมวดหมู่; เปรียบกับ realized probability และ bookmaker odds; วัด bias (longshot, Yes-bias)
- **Key finding:** Polymarket prices track realized probabilities ใกล้เคียงมากและดีกว่า bookmaker odds เล็กน้อย; มี Yes-bias (over-trade "Yes") และ default-option bias แต่ไม่มี longshot bias ทั่วไป; skill distribution skewed — กำไรกระจุกที่ผู้เล่นส่วนน้อย
- **Dataset:** Polymarket events, Dec 2025
- **Apply to project:** Polymarket odds ใช้เป็น signal ได้ แต่ต้องปรับ: ถ้า market ถาม "Yes/No" → ลด Yes probability ลง 3-5% เพื่อแก้ Yes-bias; ถ้า Polymarket odds เปลี่ยน >10% ในคืนเดียว → นั่นคือ genuine information signal ไม่ใช่แค่ noise
- **Tag:** IMPLEMENT

#### Price Discovery and Trading in Modern Prediction Markets — Ng, Peng, Tao, Zhou (SSRN 5331995)
- **Source:** [SSRN:5331995](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5331995)
- **Method:** วิเคราะห์ price discovery mechanism ของ prediction markets; เปรียบ liquidity สูง vs ต่ำ
- **Key finding:** Prediction markets ที่ liquid กว่าทำ price discovery ได้เร็วและแม่นกว่า; Polymarket lead Kalshi ใน price discovery เมื่อ volume สูง
- **Dataset:** US prediction markets cross-platform
- **Apply to project:** Polymarket signal น่าเชื่อถือกว่าเมื่อ open interest สูง (>$1M) — ถ้า market เล็กมาก odds อาจ noisy; เพิ่ม "market size" check เมื่อ cite Polymarket ใน pre-market brief
- **Tag:** REFERENCE

#### Anatomy of Polymarket: 2024 Presidential Election — Yang, Tsang (arXiv:2603.03136)
- **Source:** [arXiv:2603.03136](https://arxiv.org/abs/2603.03136)
- **Method:** วิเคราะห์ Polymarket microstructure และ price discovery ใน 2024 US election; เปรียบกับ PredictIt
- **Key finding:** Polymarket ที่ volume สูงสุดและ visible ที่สุดกลับให้ forecast แม่นน้อยที่สุดในกลุ่ม prediction markets; PredictIt (volume น้อยกว่า) แม่นกว่า → high visibility อาจดึงดูด noise traders
- **Dataset:** 2024 US Presidential Election, multiple prediction market platforms
- **Apply to project:** เมื่อ Polymarket odds มี discrepancy กับ Kalshi → ดูว่า platform ไหน volume สูงกว่า และ weight ให้ Kalshi มากกว่าถ้า odds ต่างกัน เพราะ Kalshi มี regulation ที่ดึง informed traders มากกว่า
- **Tag:** REFERENCE

---

### Theme 4: Intraday Timing & FOMC Patterns

#### Noisy FOMC Returns? Post-Announcement Reversals — Boguth, Fisher, Gregoire, Martineau (SSRN 4131740)
- **Source:** [SSRN:4131740](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4131740)
- **Method:** วิเคราะห์ price pressure และ information content ของ return ในช่วง FOMC announcement window; วัด reversal pattern ในระดับ intraday
- **Key finding:** FOMC event-window return มัก reverse ภายในสิ้น announcement cycle; negative relationship แรงระหว่าง pre-FOMC return และ post-announcement return; price pressure (ไม่ใช่ information) เป็นสาเหตุหลักของ initial move; VIX เริ่มลดลงทันทีหลัง announcement และ persist ≈45 นาที
- **Dataset:** US equity market, multiple FOMC cycles
- **Apply to project:** เพิ่ม FOMC Protocol ใน decision tree: (1) ห้าม chase ทิศทางแรกใน 15 นาทีแรก — มักเป็น price pressure ไม่ใช่ signal; (2) รอ 45 นาทีให้ VIX settle แล้วดูทิศทางจริง; (3) ถ้า pre-FOMC ขึ้นแรง → คาด reversal หลัง statement; ยืนยัน lesson จาก 2026-04-29 review (Powell 4 dissenting votes → TLT ลง -0.776%)
- **Tag:** IMPLEMENT

#### The FOMC Announcement Reversal — Baglioni, Ribeiro (SSRN 4182628)
- **Source:** [SSRN:4182628](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4182628)
- **Method:** Predictive regression ของ event-window return กับ post-announcement return; วัด reversal magnitude ตาม announcement type
- **Key finding:** Significant reversal ของ event-window return ภายในสิ้น announcement cycle ได้รับการยืนยัน; hawkish announcements trigger network fragmentation ใน short horizon; neutral ไม่มี immediate impact แต่มี delayed fragmentation
- **Dataset:** US equity market, FOMC announcements
- **Apply to project:** ถ้า FOMC hawkish (dissenting votes ≥3 หรือ tone hawk) → ขั้นตอน: (1) อย่า short TLT ทันที รอ 45 นาที, (2) เช็ค 10Y yield direction หลัง 45 นาที, (3) entry ถ้า yield ยัง climbing; เป็น refinement ของ lesson จาก post-market 2026-04-29
- **Tag:** REFERENCE

#### Overnight-Intraday Return Gap and Retail Ebb and Flow — Ahn et al. (SSRN 4752520, 2024)
- **Source:** [SSRN:4752520](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4752520)
- **Method:** วัด gap ระหว่าง overnight return และ intraday return; เชื่อมกับ retail trading flow
- **Key finding:** Retail selling ในช่วง morning (9:30-11:00) กดดัน opening prices; stocks ที่ retail ขายเช้า tend to rebound intraday — retail ebb and flow predict intraday reversal
- **Dataset:** US equities, retail order flow, daily frequency
- **Apply to project:** ถ้าหุ้นเปิดตลาดขึ้นแรงจาก overnight gap → retail ที่ buy overnight มักขายออกช่วงเช้า (take profit) → expect fade ใน first 30-60 นาที; อย่า chase gap open; รอ price settle หลัง 10:00am ก่อน entry — ยืนยัน rule "ไม่เข้า 11:30-1:30pm" ที่มีอยู่แล้ว
- **Tag:** REFERENCE

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **Brier score tracking (arXiv:2311.18258)** → เพิ่มใน post-market review template: คำนวณ `BS = (confidence - outcome)²` ทุกวัน → rolling 10-day average → complexity: **low** (เพิ่ม 3 บรรทัดใน review template)

2. **FOMC 45-minute rule (SSRN 4131740)** → เพิ่มใน decision tree protocol: "ห้าม chase FOMC initial direction, รอ 45 นาที" → complexity: **low** (rule เพิ่มใน template)

3. **Polymarket Yes-bias correction (SSRN 5910522)** → เมื่ออ้าง Polymarket odds ใน brief: แสดง `adjusted = raw - 3%` สำหรับ Yes questions → complexity: **low**

4. **PEAD inconsistent surprise rule (SSRN 5311906)** → เพิ่มใน post-earnings checklist: เช็ค analyst consensus ก่อนตัดสิน reaction; ถ้า inconsistent surprise → hold หรือ add ไม่ใช่ขาย → complexity: **low** (เพิ่มใน post-market review checklist)

5. **Rolling Brier score visualization** → เพิ่มใน weekly-calibration script: track และ plot BS over time → complexity: **medium**

---

## Gaps

- **Capex guidance overhang** — งานวิจัยเฉพาะเรื่อง AI/tech capex raise → stock reaction ยังไม่มี paper ที่ verify; ใช้ SSRN 5311906 เป็น proxy ไปก่อน
- **Opening gap fill rate** — งานวิจัยเรื่อง % ของ gaps ที่ fill ใน day + conditions; `SSRN 4752520` ครอบบางส่วน
- **Scenario base rate calibration** — empirical base rate ของ Bull/Base/Bear scenario ในตลาดจริง; ยังไม่มี paper specific

---

*Scope: 4 themes | Searches: 10/10 | Papers: 10 total — 4 IMPLEMENT, 6 REFERENCE, 0 SKIP*
