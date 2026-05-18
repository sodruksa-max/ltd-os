# LTD-OS System Improvement Papers — 2026-05
*5 searches | 9 papers | 2026-05-19*

Cross-ref: [[nick-v3-sizing-exits-survey]] | [[thesis-convergence]]

---

## TL;DR — Top Picks (implement first)

| # | Paper | Area | Why first |
|---|---|---|---|
| 1 | ERL (arXiv:2603.24639) | Self-improvement | ปิด weakest link — OUTCOMES.md 2 entries ไม่มี feedback loop |
| 2 | Financial Anomaly Multi-Agent (arXiv:2403.19735) | Kill monitor | Nick ไม่มี automated kill condition check ระหว่าง sessions |
| 3 | ChatGPT Systematic Investing (arXiv:2510.26228) | Signal quality | Low effort — news sentiment layer ต่อ /screen |
| 4 | KARMA KG Enrichment (openreview:k0wyi4cOGy) | KB quality | thesis-convergence.py นับ count ไม่ weight quality |
| 5 | Council Stability Detection (arXiv:2510.12697) | Council | /council วิ่ง fixed rounds — ไม่รู้ว่า debate จบหรือยัง |

---

## Papers by Area

### Area 1 — LLM Self-Improvement from Outcomes

#### Experiential Reflective Learning (ERL)
- **Source:** arXiv:2603.24639
- **Method:** สร้าง heuristic จาก single-attempt experience แล้วสะสมเป็น transferable rules
- **Key finding:** +7.8% on Gaia2 benchmark vs baseline
- **Apply to LTD-OS:** /post-market และ /nick-weekly extract "prediction vs reality" → append structured heuristic ลง OUTCOMES.md อัตโนมัติ → ERL loop = outcomes → rules → apply next session. ปิด gap ที่ /weekly-calibration ไม่มีอะไร calibrate บน
- **Complexity:** medium
- **Tag:** IMPLEMENT

#### SAGE — Self-Evolving Agents
- **Source:** arXiv:2409.00872
- **Method:** Reflection + memory augmentation — agents self-adjust จาก historical trajectory
- **Apply to LTD-OS:** Nick kill-condition miss log → weekly reflection อัปเดต nick-soul.md จาก failures โดยตรง ไม่ใช่แค่ append manual
- **Complexity:** medium
- **Tag:** REFERENCE

---

### Area 2 — Financial Signal Quality

#### ChatGPT in Systematic Investing
- **Source:** arXiv:2510.26228
- **Method:** LLM-extracted news sentiment เป็น cross-sectional momentum signal; strongest effect ใน concentrated high-conviction portfolio
- **Apply to LTD-OS:** เพิ่ม news-sentiment scoring ต่อ watchlist ticker ใน /screen — LLM score ข่าวล่าสุดเป็น bullish/neutral/bearish แล้ว combine กับ RS score ที่มีอยู่
- **Complexity:** low
- **Tag:** IMPLEMENT

#### From Hypotheses to Factors (Crypto)
- **Source:** arXiv:2604.26747
- **Method:** LLM agent iterate propose+backtest factor combos จนได้ compact factor set (size/liquidity/range/momentum) — Sharpe 1.55 OOS
- **Apply to LTD-OS:** แทน manual RSI/MA20/RS ด้วย LLM-driven factor discovery — แต่ต้องมี backtesting infra ก่อน
- **Complexity:** high
- **Tag:** REFERENCE (park จนกว่า Nick มี 6+ months data)

---

### Area 3 — Multi-Agent Debate Quality

#### Multi-Agent Adaptive Stability Detection
- **Source:** arXiv:2510.12697
- **Method:** ตรวจว่า debate converge แล้วหรือยัง — ถ้า stabilize แล้ว → stop early; ถ้ายัง diverge → escalate
- **Apply to LTD-OS:** /council ปัจจุบัน run fixed rounds เสมอ — เพิ่ม stability check: ถ้า 4/5 proposals ชี้ทิศทางเดียวกัน → flag "HIGH CONFIDENCE, stop early" ประหยัด token
- **Complexity:** medium
- **Tag:** IMPLEMENT

#### From Debate to Decision — Conformal Social Choice
- **Source:** arXiv:2604.07667
- **Method:** Wrap multi-agent debate output ด้วย conformal prediction set + marginal coverage guarantee; uncertain cases escalate to human
- **Apply to LTD-OS:** /council output ได้ confidence score — high confidence = auto-log ลง DECISIONS.md; low confidence = flag ให้ user review ก่อน act. Track ว่า proposals ไหนถูกต้องจริง
- **Complexity:** medium
- **Tag:** IMPLEMENT

---

### Area 4 — Automated Kill Condition Monitoring

#### Multi-Agent Framework for Financial Anomaly Detection
- **Source:** arXiv:2403.19735
- **Method:** 3-agent pipeline: data agent (signals) → analyst agent (anomaly flag) → report agent (consolidate)
- **Apply to LTD-OS:** 3-agent kill monitor สำหรับ Nick: (1) data-puller ดึง price/earnings/macro daily (2) threshold-checker เทียบกับ kill conditions ใน nick_state.json (3) alert-writer post ลง healthcheck-log.md ถ้า breach. Run เป็น pre-step ของ /nick-weekly
- **Complexity:** medium
- **Tag:** IMPLEMENT

---

### Area 5 — KB Contradiction Detection

#### KARMA — Multi-Agent KG Enrichment
- **Source:** OpenReview:k0wyi4cOGy
- **Method:** Conflict Resolution Agents resolve contradictions via LLM debate; assign conflict weight ต่อ source ไม่ใช่แค่นับ count
- **Apply to LTD-OS:** thesis-convergence.py ตอนนี้นับแค่ source count — KARMA pattern = weight แต่ละ source ตาม corroboration vs contradiction. Source ที่ contradict ลด score; source ที่ corroborate เพิ่ม score. Direct fix ให้ thesis-convergence.py
- **Complexity:** medium
- **Tag:** IMPLEMENT

#### TruthfulRAG — Resolving Factual-level Conflicts via KG
- **Source:** arXiv:2511.10375
- **Method:** Detect factual conflicts เมื่อ KB update; KG resolve temporal/source contradictions
- **Apply to LTD-OS:** เมื่อ Vera flag ⚠️ contradiction → lookup contradiction-registry.md ว่า conflict นี้มี prior resolution ไหม — ป้องกัน re-debate settled facts
- **Complexity:** medium
- **Tag:** REFERENCE

---

## Implementation Roadmap

| Priority | Paper | What to build | Complexity | Impact |
|---|---|---|---|---|
| 1 | ERL arXiv:2603.24639 | /post-market → structured heuristic → OUTCOMES.md | medium | closes feedback loop |
| 2 | Financial Anomaly arXiv:2403.19735 | nick-kill-monitor.py (3-agent) | medium | automates highest-risk check |
| 3 | ChatGPT Systematic arXiv:2510.26228 | news sentiment layer ใน /screen | low | immediate signal quality ↑ |
| 4 | KARMA openreview:k0wyi4cOGy | thesis-convergence.py — add conflict weight | medium | KB quality ↑ |
| 5 | Council Stability arXiv:2510.12697 | stability check ใน /council Phase 3 | medium | token savings + confidence signal |
| 6 | Conformal Social Choice arXiv:2604.07667 | confidence score ใน /council output | medium | outcome tracking ↑ |

## Gaps

- Kill condition monitoring แบบ real-time (intraday) ยังไม่มี paper ที่ตรงกับ personal portfolio scale
- /council outcome tracking (ทำ proposal ไหนแล้วได้ผลยังไง) ยังเป็น open gap ไม่มี paper ครอบคลุมโดยตรง
- Factor selection agent (arXiv:2604.26747) ดีมากแต่ต้องการ backtesting infra ก่อน

*Searches: 5 | Papers: 9 — 6 IMPLEMENT, 3 REFERENCE | Researcher agent: a0d95a52939981b64*
