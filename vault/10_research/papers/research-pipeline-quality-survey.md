# Paper Survey — Investment Research Pipeline Quality
*Project context: LTD-OS multi-agent pipeline (Researcher→Reese→Chris+Vera→Indie) สำหรับวิเคราะห์หุ้น | 2026-05-17 | Scope: 3 themes (earnings extraction, structured output, debate optimization) | 5 searches | 7 papers*

*Note: Themes 1 (hallucination detection) + 2 (agent eval) + 3 (self-improvement) ครอบคลุมแล้วใน `agent-eval-self-improvement-survey.md` และ `agent-portfolio-autonomy-survey.md` — survey นี้เฉพาะ 3 gaps ที่เหลือ*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | Structuring the Unstructured (arXiv:2505.19197) | Structured Output | Schema-bound KPI extraction layer ระหว่าง Reese → Vera — แก้ root cause ที่ Vera audit free-text ไม่แม่น |
| 2 | LLM Triplet Extraction (arXiv:2602.11886) | Structured Output | SPO triplets = kill conditions เป็น metric+threshold pairs; fix passive-voice hallucination ใน Vera ทันที |
| 3 | MAD Adaptive Stability (arXiv:2510.12697) | Debate Protocol | Stopping rule สำหรับ Chris-Reese debate ด้วย KS-test — หยุดเมื่อ consensus จริง ไม่ใช่ fixed rounds |
| 4 | Can LLM Agents Debate? (arXiv:2511.07784) | Debate Protocol | ให้ Chris และ Vera run parallel (ไม่ share ก่อน) — ลด conformity bias |

---

## Papers by Theme

### Theme A: Earnings Call / SEC Filing Extraction

#### Agentic Retrieval of Topics and Insights from Earnings Calls — Gupta, Bhowmik, Gunow (2025)
- **Source:** arXiv:2507.07906
- **Method:** LLM-agent pipeline ค้นหาและจัด hierarchical topics ข้ามหลาย earnings call quarters; track topics ใหม่ที่ emerging และ topics ที่หายไป โดยไม่ต้องมี labeled ground truth
- **Key finding:** สามารถ detect ว่า management เพิ่ม/ลด risk language ข้าม quarters และ cross-company theme detection (เช่น supply chain risk ที่ emerge ใน sector ทั้งหมด)
- **Dataset:** S&P 500 earnings call transcripts, multi-quarter
- **Apply to pipeline:** ก่อน Reese เขียน narrative → agentic topic-retriever scan 4 quarters ของ earnings calls ก่อน → ส่ง structured topic map (recurring talking points, newly introduced risks, vanished topics) ให้ Reese แทน raw transcript — Reese hallucinate น้อยลงเพราะ input structured แล้ว
- **Tag:** REFERENCE *(upstream ingestion — ดีมากแต่ complex; ทำหลัง B1+B2)*

#### MarketSenseAI 2.0: Enhancing Stock Analysis through LLM Agents — Fatouros et al. (2025)
- **Source:** arXiv:2502.00415
- **Method:** RAG + multi-agent framework ประมวลผล SEC filings, earnings calls, financial news, macro indicators แบบ parallel ด้วย specialized agents; output เป็น investment signal
- **Key finding:** 125.9% cumulative return vs 73.5% index บน S&P 100 (2023-2024) — ⚠️ single-group backtest, lookahead bias not fully ruled out; ดูที่ architecture ไม่ใช่ return figure
- **Dataset:** S&P 100 stocks, 2023-2024
- **Apply to pipeline:** Blueprint สำหรับ SEC/earnings ingestion layer ก่อน Reese: agent interface design, context window structuring, conflict resolution ระหว่าง sources — study Section 3 ของ paper
- **Tag:** REFERENCE

#### A Scalable Framework for Systematic Analysis of SEC 10-K Filings — Daimi & Iqbal (2024)
- **Source:** arXiv:2409.17581
- **Method:** Cohere Command-R+ สร้าง quantitative ratings จาก 10-K text ใน structured dimensions โดยไม่มี verification layer
- **Key finding:** Proof-of-concept ว่า extraction เป็นไปได้ — แต่ขาด schema validation และ hallucination control โดยสิ้นเชิง
- **Dataset:** Corporate 10-K filings
- **Apply to pipeline:** Background only — ยืนยันว่าทำไม Vera ถึงต้องมีอยู่ใน pipeline (paper นี้ไม่มี Vera = มี error มาก)
- **Tag:** ⚠️ AGING (2024 — superseded by B1+B2 below)

---

### Theme B: Structured Claim Extraction / Constrained LLM Output

#### Structuring the Unstructured: Multi-Agent KPI and Guidance Extraction — Choi, Lopez-Lira et al. (2025)
- **Source:** arXiv:2505.19197
- **Method:** Agent 1 (Extraction Agent) แปลง free-text financial disclosure เป็น fixed schema + financial-logic validation (reject EPS ที่ unit ไม่ match historical series); Agent 2 (Text-to-SQL) ให้ query structured output ด้วย natural language — 95% schema accuracy, 91% retrieval accuracy
- **Key finding:** Schema compliance + financial-logic validation ร่วมกันคือ requirement หลัก — ขาดอันใดอันหนึ่ง accuracy ตกชัดเจน
- **Dataset:** Financial earnings releases + SEC disclosures, multiple companies
- **Apply to pipeline:** **Insertion point ที่ leverage สูงสุด** — เพิ่ม Extraction Agent ระหว่าง Reese กับ Vera: Reese เขียน narrative → Extraction Agent แปลง bull/bear claims เป็น schema records (claim text, metric name, threshold, time horizon, source reference) → Vera audit schema records แทน free text = reliable มากกว่ามาก Bonus: Text-to-SQL = `/query-thesis` command ในอนาคต
- **Tag:** **IMPLEMENT** *(priority 1)*

#### LLM-based Triplet Extraction from Financial Reports — Wesslund et al. (2026)
- **Source:** arXiv:2602.11886
- **Method:** Extract Subject-Predicate-Object (SPO) triplets จาก corporate financial documents โดยไม่ต้อง annotated ground truth; ใช้ ontology-driven evaluation + hybrid LLM-as-judge + regex verification; พบว่า passive voice constructions ทำให้ subject hallucination สูงอย่างมีระบบ
- **Key finding:** Automated ontology ได้ 100% schema conformance; passive voice = root cause หลักของ subject hallucination ใน financial text
- **Dataset:** Swedish and English corporate financial reports
- **Apply to pipeline:** (1) Kill conditions เป็น SPO triplets: Subject="gross margin", Predicate="falls below", Object="40% for 2 consecutive quarters" — Vera fact-check = "does this triplet exist in verified source?" (2) **Vera prompt fix ทันที:** สั่ง Vera ให้ flip passive constructions เป็น active ก่อน check subject identity — ไม่ต้องเปลี่ยน code เลย
- **Tag:** **IMPLEMENT** *(priority 2 — passive voice fix ทำได้วันนี้)*

---

### Theme C: Multi-Agent Debate Protocol Optimization

#### Multi-Agent Debate for LLM Judges with Adaptive Stability Detection — Hu et al. (2025)
- **Source:** arXiv:2510.12697
- **Method:** หลาย LLM agents propose judgments และ critique กัน iteratively; Beta-Binomial mixture model track consensus dynamics; Kolmogorov-Smirnov test detect ว่า opinion distribution stabilize แล้วหรือยัง → early stopping เมื่อ stable
- **Key finding:** Adaptive stopping ชนะ fixed-round debate และ majority voting บน judgment accuracy พร้อม computational cost ต่ำกว่า
- **Dataset:** LLM evaluation benchmarks (not financial-specific — transfer plausible but not validated)
- **Apply to pipeline:** Chris critique ปัจจุบัน run fixed passes — ใช้ stability criterion แทน: track ว่า claims ไหน flip จาก disputed → accepted ใน แต่ละ round; stop เมื่อ flip rate ต่ำกว่า threshold → ป้องกัน Chris over-critique arguments ที่ถูกต้อง
- **Tag:** **IMPLEMENT** *(medium complexity — ต้องออกแบบ flip-tracking mechanism)*

#### Can LLM Agents Really Debate? Controlled Study of Multi-Agent Debate — Wu, Li & Li (2025)
- **Source:** arXiv:2511.07784
- **Method:** ใช้ Knight-Knave-Spy logic puzzles เป็น controlled testbed ทดสอบ 6 variables: team composition, information transparency, discussion order, conversation length, confidence visibility, problem complexity
- **Key finding:** Reasoning strength + group diversity = dominant drivers; structural parameters (turn order, confidence visibility) = marginal; majority opinion suppresses individual corrections = conformity bias คือ failure mode หลัก
- **Dataset:** Logic puzzles (controlled setting — not financial domain)
- **Apply to pipeline:** **2 design rules:** (1) Chris และ Vera ต้องใช้ different system prompts หรือ different base models เพื่อ genuine diversity — ถ้า share reasoning patterns = echo agreement ไม่ใช่ real critique (2) **ห้าม share Chris critique กับ Vera ก่อน Vera รัน fact-check** — run parallel, reconcile หลัง; sequential sharing = conformity bias
- **Tag:** **IMPLEMENT** *(low complexity — เปลี่ยน pipeline execution order)*

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **Vera passive-voice fix (2602.11886)** → เพิ่ม instruction ใน Vera prompt: "ก่อน check subject identity ของ claim ให้ flip passive constructions เป็น active ก่อน" → complexity: **low** — 1 บรรทัดใน stock-content.md
2. **Chris + Vera parallel execution (2511.07784)** → เปลี่ยน pipeline ให้ Chris และ Vera run independently (ไม่ share ก่อน) แล้วค่อย reconcile → complexity: **low** — เปลี่ยน execution order ใน stock-content.md
3. **KPI Extraction Agent ระหว่าง Reese→Vera (2505.19197)** → เพิ่ม Extraction step: Reese output → convert bull/bear claims เป็น schema records → Vera audit schema records แทน free text → complexity: **medium** — เพิ่ม step ใหม่ใน stock-content.md + define schema format
4. **Kill conditions as SPO triplets (2602.11886)** → นิยาม kill condition format เป็น SPO: Subject+Predicate+Object+TimeHorizon+Source → Vera checks triplet against source → complexity: **medium** — เปลี่ยน kill condition template
5. **MAD adaptive stopping สำหรับ Chris debate (2510.12697)** → track claim flip-rate ระหว่าง Chris rounds; stop เมื่อ stable → complexity: **high** — ต้องออกแบบ flip-tracking schema

---

## Gaps

- ไม่มี paper เกี่ยวกับ "kill condition generation" เป็น formal ML task โดยตรง — B1's KPI schema เป็น closest analog แต่ยังไม่ใช่ threshold-condition records
- C1+C2 ทดสอบบน logic puzzles ไม่ใช่ financial claim auditing — transfer ไป domain จริงยังไม่ validated
- ยังขาด: calibration / confidence estimation สำหรับ Nick conviction levels (High/Med/Low ยังไม่มี probabilistic grounding)

---

*Scope: 3 themes | Searches: 5/5 | Papers: 7 total — 4 IMPLEMENT, 2 REFERENCE, 1 AGING*
