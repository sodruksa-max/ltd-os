# Paper Survey — Autonomous Portfolio Agent Workflow
*Project context: Nick — blinded portfolio manager ที่ self-research, verify kill conditions ด้วย web search, maintain KB memory atoms | 2026-05-16 | Scope: 5 themes | 6 searches | 14 papers (6 จาก vault + 8 ใหม่)*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | LLM Multi-Agent Anomaly Detection (arXiv:2403.19735) | Kill Condition | Blueprint ตรงที่สุด: flag → web+KB validate → verdict |
| 2 | Orchestration Framework (arXiv:2512.02227) | Architecture | แยก risk agent ออกจาก alpha agent — supports Nick/Vera split |
| 3 | FinDeepResearch HisRubric (arXiv:2510.13936) | Self-Research | Quality rubric สำหรับ Reese research docs |
| 4 | Agentic RAG Fintech (arXiv:2510.25518) | Memory | Keyphrase-indexed retrieval → ปรับปรุง KB lookup ต้นทุนต่ำ |
| 5 | AI Trading Biases (arXiv:2604.18373) | Governance | Prompt rules ลด LLM bias ก่อน deploy — ใส่ใน nick-soul.md |

---

## Papers by Theme

### Theme 1: Kill Condition Verification / Anomaly Detection

#### Enhancing Anomaly Detection in Financial Markets with an LLM-based Multi-Agent Framework — Taejin Park (2024)
- **Source:** [arXiv:2403.19735](https://arxiv.org/abs/2403.19735)
- **Method:** Multi-agent pipeline ที่แต่ละ agent มีบทบาทชัดเจน: data conversion → web research → institutional KB cross-check → report consolidation — ใช้ validate anomaly alerts จาก rule-based system
- **Key finding:** Multi-agent validation ลด false positive ของ anomaly alerts ได้ในชุดข้อมูล S&P 500 พร้อมลด manual analyst workload
- **Apply to Nick:** Blueprint ตรงที่สุดสำหรับ kill condition flow: (1) nick-signals flags abnormality → (2) web research agent ค้น news สด → (3) KB cross-check กับ THESIS_TRACKER atoms → (4) Nick verdict: Intact/Evolving/Invalidated
- **Tag:** **IMPLEMENT**

#### Orchestration Framework for Financial Agents — Li et al. (2025)
- **Source:** [arXiv:2512.02227](https://arxiv.org/abs/2512.02227)
- **Method:** Map ทุก component ของ algo-trading เป็น specialized agent: planner, orchestrator, alpha, risk, portfolio, backtest, execution, audit, memory — orchestrated pipeline ที่ทำงาน end-to-end
- **Key finding:** Stock arm: 20.42% return, 2.63 Sharpe, -3.59% max drawdown. Risk/audit agent แยกออกจาก alpha agent คือ key architectural decision
- **Apply to Nick:** Validates Nick/Vera split (thesis generation ≠ thesis validation). "Memory agent" feeding all others = THESIS_TRACKER-first lookup design ที่มีอยู่แล้ว
- **Tag:** **REFERENCE**

#### AI Agents in Financial Markets: Architecture and Systemic Implications — Hui Gong (2026)
- **Source:** [arXiv:2603.13942](https://arxiv.org/abs/2603.13942)
- **Method:** Four-layer modular architecture: data perception → reasoning → strategy → execution with control; introduces Agentic Financial Market Model ที่เชื่อมโยง agent design กับ systemic risk
- **Key finding:** "Bounded autonomy" (agent recommends, human executes) คือ near-term equilibrium ที่ถูกต้อง; systemic risk ขึ้นกับ coupling และ governance มากกว่า model intelligence
- **Apply to Nick:** Academic backing สำหรับ Nick's no-auto-execute constraint. "Execution with control" layer = kill condition gate ที่ formal
- **Tag:** **REFERENCE**

---

### Theme 2: Multi-Agent Portfolio Architecture (จาก vault)

#### Signal or Noise in Multi-Agent LLM-based Stock Recommendations — Fatouros & Metaxas (2025)
- **Source:** [arXiv:2604.17327](https://arxiv.org/abs/2604.17327)
- **Method:** 4 specialist agents (news, fundamentals, dynamics, macro) → synthesis ด้วย NNLS embedding decomposition → ordinal recommendation
- **Key finding:** Strong-buy portfolio percentile 99.7 vs random (p=0.003); +25.2pp excess return vs equal-weight; agent weights หมุนตาม market regime
- **Apply to Nick:** Nick weekly review เป็น informal version ของ architecture นี้ — formalizing เป็น 4-agent parallel read ก่อน synthesis จะเพิ่ม consistency
- **Tag:** REFERENCE

#### Self-Driving Portfolio — Ang, Azimbayev & Kim (2024)
- **Source:** [arXiv:2604.02279](https://arxiv.org/abs/2604.02279)
- **Method:** ~50 agents: market analysts → portfolio constructors (20+ methods) → critique-and-vote → meta-agent monitor + self-refine
- **Key finding:** Architecture reference — meta-agent learns จาก forecast errors แล้ว refine agent prompts อัตโนมัติ (= nick-soul.md pattern)
- **Apply to Nick:** nick-soul.md feedback loop คือ manual version ของ meta-agent layer; บทเรียน: ลด agents เหลือ 5-10 เพื่อ practical cost
- **Tag:** REFERENCE

#### QRAFTI: Agentic Quant Research — Lim, Muthuraman & Sury (2026)
- **Source:** [arXiv:2604.18500](https://arxiv.org/abs/2604.18500)
- **Method:** 3-agent system (Research Analyst + Quant Dev + Risk Manager) ด้วย reflection-based planning ก่อน execute
- **Key finding:** Reflection เพิ่ม multi-step accuracy จาก 74% → 99%; tool-calling + reflection ดีกว่า dynamic code generation
- **Apply to Nick:** Reflection pattern (draft plan → critique → execute) ควรเพิ่มใน Nick kill condition check: draft verdict → cross-check กับ KB → finalize
- **Tag:** **IMPLEMENT**

---

### Theme 3: Agent Memory Systems / KB Retrieval

#### Memory for Autonomous LLM Agents — Du et al. (2026)
- **Source:** [arXiv:2603.07670](https://arxiv.org/abs/2603.07670)
- **Method:** Survey ด้วย write–manage–read framework; taxonomy 5 ประเภท: context window, episodic store, semantic store, procedural, working memory
- **Key finding:** Field กำลังย้ายจาก static recall → multi-session evaluation; single-context agents ไม่เพียงพอสำหรับ long-horizon tasks
- **Apply to Nick:** vault/_memory/ = semantic store + working memory. ขาด **indexed episodic store** — OUTCOMES.md เก็บ trade outcomes แต่ไม่ได้ retrieval-indexed → Nick ค้น pattern ย้อนหลังไม่ได้
- **Tag:** **REFERENCE** (architecture gap identification)

#### Agentic RAG for Fintech — Cook, Osuagwu et al. (2025)
- **Source:** [arXiv:2510.25518](https://arxiv.org/abs/2510.25518)
- **Method:** Multi-agent RAG ด้วย keyphrase extraction → sub-query decomposition → cross-encoder re-ranking ก่อน return KB context
- **Key finding:** Agentic RAG ชนะ standard RAG บน fintech Q&A; keyphrase extraction ก่อน query คือ key improvement
- **Apply to Nick:** แทนที่ Nick จะ grep ด้วย ticker เปล่าๆ → extract keyphrases ก่อน ("revenue miss", "customer concentration") แล้วค้น atoms — ปรับปรุง recall โดยไม่ต้องเพิ่ม infrastructure
- **Tag:** **IMPLEMENT**

#### Agentic Retrieval from Earnings Calls — Gupta, Bhowmik & Gunow (2025)
- **Source:** [arXiv:2507.07906](https://arxiv.org/abs/2507.07906)
- **Method:** Agent ดึง topics จาก earnings call → จัด hierarchical ontology → track topic evolution ข้าม quarters
- **Key finding:** Traditional topic modeling ไม่จับ emerging topics; hierarchical agent approach adapt ontology แบบ dynamic ได้
- **Apply to Nick:** Indie's atom extraction เป็น simpler version ของนี้. ปรับปรุง: organize atoms ตาม theme cluster ("AI capex pressure", "customer concentration risk") ไม่ใช่แค่ per-ticker → thesis-convergence.py จะ detect patterns ได้ดีขึ้น
- **Tag:** **IMPLEMENT**

---

### Theme 4: Autonomous Self-Research Agents

#### FinDeepResearch: Evaluating Deep Research Agents — Zhu, Ng et al. (2025)
- **Source:** [arXiv:2510.13936](https://arxiv.org/abs/2510.13936)
- **Method:** HisRubric — hierarchical evaluation framework ที่ mirror professional analyst workflow; benchmark 16 methods บน 15,808 grading items, 64 companies, 8 markets, 4 languages
- **Key finding:** ไม่มี deep research agent ที่ perform ดีสม่ำเสมอข้าม markets; failure modes ซ่อนอยู่เมื่อ test single-market English-only เท่านั้น
- **Apply to Nick:** HisRubric grading criteria (data sourcing → reasoning quality → conclusion validity) เป็น quality checklist สำหรับ Reese docs และ Nick's inline research
- **Tag:** **IMPLEMENT**

#### From Web Search towards Agentic Deep Research — (arXiv:2506.18959, 2025)
- **Source:** [arXiv:2506.18959](https://arxiv.org/abs/2506.18959) ⚠️ authors [partially-unverified]
- **Method:** Frames deep research เป็น RL problem — agent เรียน when to search, how to formulate queries, และ how to synthesize ด้วย RL optimize search-reasoning loop
- **Key finding:** RL-optimized search agents ชนะ prompt-engineered agents บน complex multi-hop tasks; biggest gain คือ **query formulation** ไม่ใช่ retrieval infrastructure
- **Apply to Nick:** Reese ปัจจุบันใช้ fixed search template. การ generate 3 candidate queries ต่อ search step แล้วเลือกดีสุดจะเพิ่ม research quality มากกว่าเปลี่ยน search provider
- **Tag:** REFERENCE

---

### Theme 5: LLM Bias & Governance (จาก vault)

#### Dissecting AI Trading Biases — Ouyang & Sui (2025)
- **Source:** [arXiv:2604.18373](https://arxiv.org/abs/2604.18373)
- **Key finding:** LLM trading agents มี 3 biases: disposition effect (ขาย winner เร็ว), extrapolation (เชื่อ trend ล่าสุดมากเกิน), bubble participation (รู้ว่า bubble แต่ยังเข้า); prompt rules ลด bias ได้จริง (-2.23 extrapolation score, t=-6.24)
- **Apply to Nick:** Prompt rules ควรเพิ่มใน nick-soul.md เป็น standing principles — โดยเฉพาะ disposition effect rule ("evaluate ด้วย fundamental ไม่ใช่ entry price")
- **Tag:** **IMPLEMENT**

#### ValueAlpha: Agreement-Gated Stress Testing — Chang, Zhu & Chen (2025)
- **Source:** [arXiv:2604.25224](https://arxiv.org/abs/2604.25224)
- **Key finding:** Agreement gate (Cohen's κ ≥ 0.4) ก่อน execute; single judge ให้ variance สูง — ต้องใช้ ensemble เสมอ
- **Apply to Nick:** Nick's recommendation ปัจจุบันเป็น single-agent output. Agreement gate = ให้ Nick draft verdict แล้ว KB cross-check ก่อน finalize (informal 2-pass validation)
- **Tag:** REFERENCE

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **AI Trading Biases prompt rules (2604.18373)** → append bias-prevention rules ลง nick-soul.md → complexity: **low** — แค่เพิ่ม text ใน soul file
2. **Kill condition multi-agent pattern (2403.19735)** → ใน nick-weekly Step 4: draft verdict → web search → KB cross-check → finalize → complexity: **low** — เพิ่ม sub-step ใน nick.md (เสร็จแล้วบางส่วนจาก session นี้)
3. **Keyphrase-indexed KB retrieval (2510.25518)** → เพิ่ม keyphrase extraction ก่อน grep ใน Nick KB sweep → complexity: **medium** — อาจเพิ่ม python helper ใน nick-monitor.py
4. **Atom theme clustering (2507.07906)** → ปรับ Indie ให้ tag atoms ด้วย theme cluster ด้วย ไม่ใช่แค่ ticker → complexity: **medium** — ปรับ prompt ใน stock-content.md
5. **HisRubric quality checklist (2510.13936)** → เพิ่ม checklist ใน Reese + Chris workflow → complexity: **medium** — ปรับ stock-content.md
6. **Reflection pattern สำหรับ Nick verdict (2604.18500)** → Nick drafts verdict → self-critique → finalize → complexity: **medium** — เพิ่มใน nick.md process
7. **Episodic memory indexing (2603.07670)** → สร้าง retrieval index สำหรับ OUTCOMES.md → complexity: **high** — อาจต้องสร้าง script ใหม่

---

## Gaps

- ยังไม่ครอบคลุม: SSRN practitioner papers on automated stop-loss / thesis invalidation in quant funds
- ยังไม่ครอบคลุม: Papers on kill condition trigger design เป็น formal concept (ระบบของเราอาจ ahead of literature)
- ยังไม่ครอบคลุม: RL-based query formulation implementation details (2506.18959)

---

*Scope: 5 themes | Searches: 6 | Papers: 14 total — 6 IMPLEMENT, 6 REFERENCE, 2 gap | 6 จาก vault + 8 ใหม่*
