# Paper Survey — LLM Agent Evaluation, Self-Improvement & Workflow Orchestration
*Project context: LTD-OS multi-agent pipeline (Reese→Chris→Vera→Indie สำหรับ research, Nick สำหรับ portfolio) — ต้องการวิธีวัดคุณภาพ agent output โดยไม่มี ground truth, meta-learning สำหรับ prompt, self-improving orchestration, และ hallucination detection | 2026-05-16 | Scope: 4 themes | 10 searches | 10 papers*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | Agent-as-a-Judge (arXiv:2508.02994) | Evaluation | Chris+Vera → structured judge scoring ทันที, ต่ำ complexity |
| 2 | FAITH Financial Hallucination (arXiv:2508.05201) | Hallucination | Vera ใช้ตรวจ numerical claims ใน Reese docs — ตรงที่สุด |
| 3 | Low-Cost Black-Box Hallucination (arXiv:2605.05134) | Hallucination | Single-pass consistency score ไม่ต้องมี external KB |
| 4 | Learning to Evolve / TPGO (arXiv:2604.20714) | Self-Improvement | Textual gradient จาก Chris feedback → update Reese prompt อัตโนมัติ |
| 5 | System Prompt Meta-Learning (arXiv:2505.09666) | Meta-Learning | ปรับปรุง nick-soul.md อย่างเป็นระบบแทนที่จะ append แบบ manual |

---

## Papers by Theme

### Theme 1: Agent Output Evaluation Without Ground Truth

#### When AIs Judge AIs: The Rise of Agent-as-a-Judge Evaluation for LLMs — Fangyi Yu (2025)
- **Source:** [arXiv:2508.02994](https://arxiv.org/abs/2508.02994)
- **Method:** Survey ที่ trace วิวัฒนาการจาก single-model judge → dynamic multi-agent debate frameworks สำหรับ evaluate LLM output; ครอบคลุม reliability, cost, human alignment ใน real-world deployments (medicine, law, finance)
- **Key finding:** Agent-as-a-judge ให้ scalable evaluation ที่ไม่ต้องมี gold labels; multi-agent debate judges ชนะ single judges บน nuanced tasks; finance domain คือ high-value deployment zone
- **Apply to LTD-OS:** Chris ปัจจุบัน critique Reese docs แบบ informal — เพิ่ม structured judge scoring ต่อ dimension (kill condition measurability, claim verifiability, bull/bear balance) ด้วย explicit rubric → output score 1-5 ต่อ dimension แทน narrative เท่านั้น
- **Tag:** **IMPLEMENT**

#### Collective Reasoning Among LLMs: Answer Validation Without Ground Truth — (2025)
- **Source:** [arXiv:2502.20758](https://arxiv.org/abs/2502.20758)
- **Method:** 4 LLMs rotate เป็น question-generator และ answerer; aggregate ด้วย majority voting + weighted consensus (Fleiss' Kappa, chi-square test) — validate quality โดยไม่มี reference answer
- **Key finding:** Agreement across diverse models = reliable signal for output quality; simple majority voting underperforms weighted consensus เมื่อ models มี different capability levels
- **Apply to LTD-OS:** Nick kill condition verdict ที่ "Evolving" (borderline) → ให้ Nick reason จาก bull perspective + bear perspective + KB evidence แยก แล้ว weight ตาม source quality ก่อน finalize — informal version ของ weighted consensus
- **Tag:** REFERENCE

---

### Theme 2: Automated Prompt Optimization / Meta-Learning

#### System Prompt Optimization with Meta-Learning — Choi, Baek & Hwang (2025)
- **Source:** [arXiv:2505.09666](https://arxiv.org/abs/2505.09666)
- **Method:** Bilevel optimization framework: upper-level optimizes system prompt over diverse user prompts/tasks; lower-level iteratively updates user prompts; meta-trains ให้ system prompt generalize ไป unseen tasks โดยไม่ต้อง re-optimize
- **Key finding:** Generalizes effectively ไป 14 unseen datasets, 5 domains; meta-learning ทำให้ adaptation ต้องการ optimization steps น้อยลง vs. standard prompt tuning
- **Apply to LTD-OS:** nick-soul.md คือ system prompt ของ Nick ที่ append แบบ manual — meta-learning framework = ทดสอบ candidate updates ใน nick-soul.md กับ past weekly decisions ก่อน commit; เก็บเฉพาะ update ที่ improve decision consistency
- **Tag:** **IMPLEMENT**

#### Meta-Prompt Optimization for LLM-Based Sequential Decision Making (EXPO) — (2025)
- **Source:** [arXiv:2502.00728](https://arxiv.org/abs/2502.00728)
- **Method:** EXPO (EXPonential-weight algorithm for prompt Optimization) — adversarial bandit algorithm ที่ handle non-stationary rewards ระหว่าง sequential decision-making; EXPO-ES ขยาย optimize exemplars (interaction history) ด้วย
- **Key finding:** Non-stationarity ใน reward observations คือ obstacle หลักของ meta-prompt optimization สำหรับ agents; EXPO ชนะ fixed meta-prompt อย่างมีนัยสำคัญ
- **Apply to LTD-OS:** Nick weekly process คือ sequential decision-making ที่ exact — market changes (non-stationary rewards) ทำให้ fixed kill condition prompts ล้าหลัง; EXPO-style: weight recent successful kill condition verifications มากกว่า stale ones เมื่อเลือก search strategy
- **Tag:** REFERENCE

---

### Theme 3: Self-Improving Workflow Orchestration

#### Learning to Evolve: Self-Improving Multi-Agent Systems via TPGO — (2026)
- **Source:** [arXiv:2604.20714](https://arxiv.org/abs/2604.20714)
- **Method:** Textual Parameter Graph Optimization (TPGO) — models multi-agent system เป็น graph ของ optimizable nodes (agents, tools, workflows); ใช้ "textual gradients" (structured NL feedback จาก execution traces) + Group Relative Agent Optimization (GRAO) meta-learning จาก historical optimization experiences
- **Key finding:** TPGO ชนะ state-of-the-art บน GAIA + MCP-Universe; ระบบเรียนรู้วิธี optimize ตัวเองได้ดีขึ้นเรื่อยๆ จาก experience (meta-learning of optimization)
- **Apply to LTD-OS:** Reese→Chris pipeline: เมื่อ Chris flag Reese doc ว่า "kill condition vague" หรือ "TAM ไม่ quantify" → extract structured textual gradient ("ล้มเหลวด้านนี้เพราะ X") → feed กลับเป็น update candidate สำหรับ Reese prompt → ทดสอบกับ doc ถัดไปก่อน commit ถาวร
- **Tag:** **IMPLEMENT**

#### From Static Templates to Dynamic Runtime Graphs: Workflow Optimization Survey — (2026)
- **Source:** [arXiv:2603.22386](https://arxiv.org/abs/2603.22386)
- **Method:** Survey จัด LLM workflow optimization ตาม 3 dimensions: (1) when structure is determined (pre-deploy vs. runtime), (2) what is optimized (components, dependencies, flow), (3) evaluation signals (task metrics, verifier, preferences, trace-derived)
- **Key finding:** Static workflows = reusable แต่ไม่ adapt; dynamic workflows = flexible แต่ต้อง robust fallback; hybrid (static scaffold + dynamic fill-in) คือ practical optimum สำหรับ production systems
- **Apply to LTD-OS:** LTD-OS slash commands เป็น static templates ทั้งหมด — survey ช่วย identify จุดที่ควร dynamize ก่อน: Nick's kill condition check (dynamic search budget ตาม KB freshness) vs. Reese research structure (static scaffold ดีพอ); ใช้ taxonomy นี้ก่อนตัดสินใจ build dynamic feature ใดๆ
- **Tag:** REFERENCE

#### A Survey of Self-Evolving Agents — (2025–2026)
- **Source:** [arXiv:2507.21046](https://arxiv.org/abs/2507.21046)
- **Method:** Survey ครอบคลุม self-evolving agents ตาม 3 axes: WHAT to evolve (models, memory, tools, architecture), WHEN (intra-test-time vs. inter-test-time), HOW (scalar rewards, textual feedback, single/multi-agent); ครอบคลุม evaluation metrics + benchmarks เฉพาะสำหรับ self-evolving agents
- **Key finding:** Field กำลังย้ายจาก static agents → adaptive agents; textual feedback loop (ไม่ใช่ numerical reward) คือ practical path สำหรับ systems ที่ไม่ใช่ RL; nick-soul.md pattern ตรงกับ "inter-test-time memory evolution"
- **Apply to LTD-OS:** ใช้ taxonomy นี้ audit nick-soul.md: WHAT กำลัง evolve อยู่ (memory ✓, prompts ✓) แต่ WHERE to evolve ยังไม่ชัด; survey แนะนำให้ track evolution quality เพิ่ม — เพิ่ม "effectiveness flag" ต่อ entry ใน nick-soul.md (✓/✗ หลังทดสอบ 2 sessions)
- **Tag:** REFERENCE

---

### Theme 4: Hallucination Detection for Financial Agents

#### FAITH: Framework for Assessing Intrinsic Tabular Hallucinations in Finance — (2025)
- **Source:** [arXiv:2508.05201](https://arxiv.org/abs/2508.05201)
- **Method:** สร้าง hallucination evaluation tasks อัตโนมัติจาก financial annual reports จริง — ground truth คือ numerical values ที่ explicit ใน reports; ทดสอบ factual accuracy ของ LLMs ต่อ company size + financial period
- **Key finding:** State-of-the-art LLMs มักผิดพลาดบน numerical financial claims (EPS, revenue growth, TAM); models ใหญ่ไม่ได้ hallucinate น้อยกว่า models เล็กบน structured financial data
- **Apply to LTD-OS:** Vera's fact audit ปัจจุบันใช้ manual ❓ flagging — FAITH approach: สำหรับทุก numerical claim ใน Reese doc ("revenue grew 45% YoY", "market cap $X"), verify ด้วย cross-multiplication จาก raw source data ก่อน mark ✓ — ถ้า verify ไม่ได้ → flag ⚠️ UNVERIFIED NUMERIC
- **Tag:** **IMPLEMENT**

#### Low-Cost Black-Box Hallucination Detection via Dynamical System Prediction — Wilson & Akrout (2026)
- **Source:** [arXiv:2605.05134](https://arxiv.org/abs/2605.05134)
- **Method:** Treats LLM เป็น black-box dynamical system; project responses ไป high-dimensional manifold via embedding; ใช้ Koopman operator theory fit transition operators สำหรับ factual vs. hallucinated regimes; differential residual score = hallucination signal; preference-aware calibration threshold
- **Key finding:** Single-sample pass (ไม่ต้อง secondary sampling หรือ external KB); state-of-the-art performance บน 3 benchmarks ด้วย resource overhead ต่ำกว่า SelfCheckGPT
- **Apply to LTD-OS:** Vera สามารถ run consistency check บน Reese doc ด้วย single-pass embedding comparison — ถ้า claim score สูง = likely factual; ถ้าต่ำ = flag สำหรับ manual verify; ลด Vera's search budget ได้เพราะไม่ต้อง re-search ทุก claim
- **Tag:** **IMPLEMENT**

#### Deficiency of Large Language Models in Finance: Empirical Examination of Hallucination — (2023)
- **Source:** [arXiv:2311.15548](https://arxiv.org/abs/2311.15548)
- **Method:** Empirical examination ของ LLM hallucination บน financial tasks — categorizes factuality vs. faithfulness hallucinations, quantifies error rates ต่อ task type
- **Key finding:** Financial domain hallucination rates สูงกว่า general domain; numerical reasoning คือ weakness หลัก; RAG ลด hallucination แต่ไม่กำจัด
- **Apply to LTD-OS:** Background context สำหรับ Vera's scope — justify ทำไม Vera ต้องมีอยู่ใน pipeline
- **Tag:** ⚠️ AGING (2023 — check for follow-up: FAITH 2025 เป็น direct follow-up ที่ดีกว่า)

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **Agent-as-a-Judge rubric สำหรับ Chris (2508.02994)** → เพิ่ม structured scoring dimensions ใน `/stock-content` Chris step: kill condition measurability (1-5), claim verifiability (1-5), bull/bear balance (1-5) → complexity: **low** — เพิ่ม rubric ใน stock-content.md
2. **FAITH numerical verification ใน Vera (2508.05201)** → Vera ต้อง cross-verify numerical claims ก่อน mark ✓ — ถ้าตัวเลขไม่ match source → ⚠️ UNVERIFIED NUMERIC → complexity: **low** — เพิ่ม instruction ใน Vera section ของ stock-content.md
3. **nick-soul.md meta-learning update (2505.09666)** → เพิ่ม "test candidate update กับ 2 past sessions ก่อน commit" ใน nick-soul.md update protocol → complexity: **medium** — ปรับ nick.md + nick-soul.md header
4. **Effectiveness flag ใน nick-soul.md (2507.21046)** → เพิ่ม ✓/✗ flag ต่อ standing principle หลังทดสอบ 2 sessions → complexity: **low** — format change ใน nick-soul.md template
5. **TPGO textual gradient จาก Chris → Reese (2604.20714)** → เมื่อ Chris flag weakness patterns → extract structured feedback → propose Reese prompt update ใน session → complexity: **high** — ต้องออกแบบ feedback extraction schema

---

## Gaps

- ยังไม่ครอบคลุม: Calibration / confidence estimation สำหรับ Nick's conviction levels (High/Med/Low conviction = informal — ไม่มี probabilistic calibration)
- ยังไม่ครอบคลุม: Multi-agent communication optimization — information flow ระหว่าง Reese→Chris→Vera→Indie ยังไม่ efficient (Vera re-reads doc ที่ Chris อ่านไปแล้ว)
- ยังไม่ครอบคลุม: Online learning / continual adaptation สำหรับ Nick signals (nick-signals.md เป็น snapshot ไม่ใช่ streaming)

---

*Scope: 4 themes | Searches: 10/10 | Papers: 10 total — 5 IMPLEMENT, 4 REFERENCE, 1 AGING*
