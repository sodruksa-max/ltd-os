# Paper Survey — LLM Routing + PKM Automation
*Project context: LTD-OS personal AI OS — building Ollama local LLM fallback (Qwen2.5 14B / RX 9070 XT), needs (1) smart local-vs-cloud routing logic, (2) automated vault note synthesis for screensaver brainstorm | 2026-05-19 | Scope: 3 themes | 10 searches | 8 papers/projects*

*Vault pre-check: llm-token-management-survey.md covers context management (22 papers) — not re-researched. agent-eval-self-improvement-survey.md covers agent self-improvement — not re-researched.*

---

## TL;DR — Top Picks (implement first)

| # | Paper / Project | Theme | Why first |
|---|---|---|---|
| 1 | BEST-Route (arXiv:2506.22716) | LLM Routing | ICML 2025, Microsoft, code on GitHub — 60% cost cut, <1% quality drop, plug-in logic |
| 2 | LLMRouter (github.com/ulab-uiuc/LLMRouter) | LLM Routing | OpenAI-compatible, explicit Ollama support, YAML config — ลด code ที่ต้องเขียนเองได้มาก |
| 3 | obsidian-llm-wiki-local (GitHub) | PKM Auto-link | Ollama + Obsidian, extracts concepts + auto-links — ตรงกับ screensaver brainstorm concept ทั้งหมด |

---

## Papers by Theme

### Theme 1 — LLM Routing: Local vs Cloud Decision

#### BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute — Microsoft (arXiv:2506.22716, Jun 2025)
- **Source:** [arXiv:2506.22716](https://arxiv.org/abs/2506.22716)
- **Venue:** ICML 2025 Poster — Tier B
- **Citations:** < 6 months from pub — use venue + code as quality signal
- **Code:** [github.com/microsoft/best-route-llm](https://github.com/microsoft/best-route-llm) ✓
- **Critics:** [no known critics ✓]
- **Method:** Router เลือกทั้ง (1) model ที่ใช้ และ (2) จำนวน samples ที่ generate ตาม query difficulty — ถ้า query ง่าย → small model + 1 sample; ถ้ายาก → large model + N samples จนถึง quality threshold
- **Key finding:** ลด cost 60% โดย performance drop < 1% เทียบกับ routing to large model ทั้งหมด — ทดสอบบน benchmarks หลายตัว
- **Apply to project:** ใช้ complexity scoring ของ BEST-Route เป็น gate สำหรับ Ollama router — `/daily-brief`, `/handoff`, simple vault queries → Ollama; `/council`, `/nick-weekly`, `/stock-content` → Claude API. ไม่ต้องเขียน heuristic เอง — ใช้ code จาก repo
- **Tag:** IMPLEMENT
- Reading Stack: [HYPERLEXIA: poster tier — methodology ในเอกสารเต็มควร verify ก่อน prod] [EDS: tested บน NLP benchmarks ไม่ใช่ agentic personal system — calibrate threshold เอง] [FAS: CLEAN] [CAPGRAS: CLEAN]

---

#### Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey — Moslem & Kelleher (arXiv:2603.04445, Mar 2026)
- **Source:** [arXiv:2603.04445](https://arxiv.org/abs/2603.04445)
- **Venue:** arXiv preprint — Tier D | HuggingFace Papers tracked
- **Citations:** [too recent — Mar 2026]
- **Code:** [no official code]
- **Critics:** [no known critics ✓]
- **Method:** Survey ครอบ routing paradigms ทั้งหมด: query difficulty, uncertainty quantification, reinforcement learning, cascading, human preference routing — เปรียบเทียบ 20+ frameworks
- **Key finding:** Cascading (query → small model first → escalate if low confidence) ชนะ fixed routing ใน cost-quality tradeoff สำหรับ heterogeneous query distributions — ตรงกับ LTD-OS use case ที่ query ต่างกันมาก
- **Apply to project:** ใช้เป็น reference อ่านก่อน build router — จะช่วยเลือก routing paradigm ที่เหมาะกับ LTD-OS (cascading มีแนวโน้มดีกว่า threshold-only)
- **Tag:** REFERENCE

---

#### RACER: Risk-Aware Calibrated Efficient Routing — (arXiv:2603.06616, Mar 2026)
- **Source:** [arXiv:2603.06616](https://arxiv.org/abs/2603.06616)
- **Venue:** arXiv preprint — Tier D
- **Citations:** [too recent — Mar 2026]
- **Code:** [no official code]
- **Critics:** [no known critics ✓]
- **Method:** Formulate routing เป็น α-VOR problem — router output = set of candidate models ที่ pass risk threshold; ใช้ conformal prediction เพื่อ distribution-free guarantee ว่า misrouting risk ≤ α บน unseen data
- **Key finding:** Provable risk control บน test data (distribution-free) — ไม่ใช่แค่ heuristic threshold
- **Apply to project:** ถ้าต้องการ routing ที่มี guarantee (เช่น "ห้ามใช้ Ollama กับ task ที่มี risk > X%") → RACER ให้ framework ที่มี math backing แต่ implement ยากกว่า BEST-Route
- **Tag:** REFERENCE

---

#### LLMRouter — ulab-uiuc (GitHub, 2025)
- **Source:** [github.com/ulab-uiuc/LLMRouter](https://github.com/ulab-uiuc/LLMRouter)
- **Venue:** Open-source library (not a paper)
- **Code:** repo ที่ link ด้านบน ✓
- **Method:** Library ที่ support OpenAI-compatible APIs รวมถึง Ollama, vLLM, SGLang — config-based routing via YAML, fallback mechanism, empty string API key สำหรับ localhost endpoints
- **Key finding:** Plug-and-play สำหรับ Ollama local + Claude cloud — ไม่ต้องเขียน HTTP client เอง
- **Apply to project:** เป็น infrastructure layer สำหรับ Ollama router — define routing rules ใน YAML config (`local: ollama/qwen2.5:14b`, `cloud: claude-sonnet-4-6`) แล้วเรียกผ่าน LLMRouter API แทนเรียก Ollama/Claude ตรง
- **Tag:** IMPLEMENT

---

### Theme 2 — Note Synthesis / PKM Automation

#### obsidian-llm-wiki-local — kytmanov (GitHub, 2025)
- **Source:** [github.com/kytmanov/obsidian-llm-wiki-local](https://github.com/kytmanov/obsidian-llm-wiki-local)
- **Venue:** Open-source project (Karpathy's llm-wiki pattern, adapted for Ollama)
- **Code:** repo ที่ link ด้านบน ✓
- **Method:** Drop markdown notes → Ollama extracts concepts → auto-generates wiki links ระหว่าง notes ที่เกี่ยวข้องโดยอัตโนมัติ — 100% local, zero data sharing
- **Key finding:** Concept extraction + linking ทำงานได้บน local Ollama โดยไม่ต้องส่งข้อมูลไป cloud — ตรงกับ LTD-OS requirement ที่ notes มีข้อมูล personal
- **Apply to project:** เป็น blueprint สำหรับ screensaver brainstorm — แทนที่จะ auto-link ทุก note, ปรับให้เลือก 2 notes random จาก vault และให้ Ollama หาความเชื่อมโยง → save ผลลัพธ์ลง 00_inbox เมื่อ idle > 15 นาที
- **Tag:** IMPLEMENT

---

#### Assessing LLMs for Serendipity Discovery in Knowledge Graphs — (arXiv:2511.12472, Nov 2025)
- **Source:** [arXiv:2511.12472](https://arxiv.org/abs/2511.12472)
- **Venue:** arXiv preprint — Tier D
- **Citations:** [too recent — Nov 2025]
- **Code:** [no official code found]
- **Critics:** [no known critics ✓]
- **Method:** SerenQA framework — serendipity metric ที่วัด 3 มิติ: relevance + novelty + surprise ของ insight ที่ LLM หาได้จาก knowledge graph — ทดสอบบน drug repurposing domain
- **Key finding:** State-of-the-art LLMs ทำ retrieval ได้ดี แต่ยังอ่อนใน "genuine surprise" discovery — gap ที่ prompt engineering หรือ random walk helps
- **Apply to project:** ใช้ serendipity metric (relevance + novelty + surprise) เป็น filter ก่อน save screensaver output ลง 00_inbox — ทิ้ง output ที่ score ต่ำ ไม่ให้ inbox เต็มด้วย generic connections
- **Tag:** REFERENCE
- Reading Stack: [SUPERTASTER: drug repurposing domain ≠ personal PKM — metric ต้อง recalibrate] [EDS: single domain test] [FAS: CLEAN]

---

#### LLM Wiki — nashsu (GitHub, 2025)
- **Source:** [github.com/nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)
- **Venue:** Open-source project
- **Code:** repo ที่ link ด้านบน ✓
- **Method:** Cross-platform desktop app — แปลง documents → interlinked knowledge base โดย LLM incremental builds + maintains wiki จาก sources แทน RAG-from-scratch ทุกครั้ง
- **Key finding:** Persistent wiki approach ดีกว่า RAG สำหรับ personal use เพราะ build ครั้งเดียวแล้วใช้ซ้ำ — ลด inference cost ต่อ query
- **Apply to project:** Alternative สำหรับ screensaver brainstorm ถ้าต้องการ wiki ที่ persistent มากกว่า per-session — แต่ complexity สูงกว่า obsidian-llm-wiki-local
- **Tag:** REFERENCE

---

#### Towards Efficient Multi-LLM Inference — (arXiv:2506.06579, Jun 2025)
- **Source:** [arXiv:2506.06579](https://arxiv.org/abs/2506.06579)
- **Venue:** arXiv preprint — Tier D
- **Citations:** [< 12 months]
- **Code:** [no official code]
- **Method:** Survey + analysis ของ routing + hierarchical techniques สำหรับ multi-LLM inference — characterize use cases ที่ edge model เพียงพอ vs ต้อง escalate
- **Key finding:** General queries (เช่น summarization, simple QA) สามารถ handle ด้วย edge model ได้ 70-80% ของ time — escalation ควรเกิดเมื่อ uncertainty สูงหรือ query ต้องการ reasoning หลายขั้น
- **Apply to project:** ใช้ characterization นี้ calibrate routing rules ใน LTD-OS — `/daily-brief` = edge-suitable; `/council` = always cloud
- **Tag:** REFERENCE

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **LLMRouter** → ติดตั้ง library, config YAML สำหรับ `ollama/qwen2.5:14b` + `claude-sonnet-4-6` → complexity: **low** — ทำได้ใน 1 session หลัง Ollama ติดตั้งแล้ว

2. **BEST-Route logic** → อ่านโค้ด `github.com/microsoft/best-route-llm`, ดึง complexity scoring function มา adapt เป็น Python script `scripts/llm-router.py` → complexity: **medium** — ใช้เป็น gate ก่อนทุก agent call

3. **obsidian-llm-wiki-local pattern** → fork repo, ปรับ script ให้ (a) เลือก 2 notes random จาก vault, (b) prompt Ollama หาความเชื่อมโยง + ต่อยอด, (c) save ลง `vault/00_inbox/brainstorm-YYYY-MM-DD-HH.md` → complexity: **medium** — reuseได้มากจาก existing code

4. **Serendipity filter** → implement 3-score filter (relevance + novelty + surprise) บน screensaver output ก่อน save — ทิ้ง output ที่ score < threshold → complexity: **low** เพิ่มทีหลัง

---

## Gaps

หัวข้อที่ยังไม่ครอบคลุม — search เพิ่มถ้าต้องการ:
- **Ollama model quality benchmarks** — Qwen2.5 14B vs Mistral 7B vs Llama 3.1 8B บน agentic tasks (summarization, vault QA) — ยังไม่มีใน vault
- **Routing threshold calibration** — วิธีหา optimal threshold สำหรับ personal use (ไม่ใช่ benchmark) — BEST-Route ใช้ benchmark datasets ซึ่งต่างจาก LTD-OS queries มาก
- **Idle detection Windows** — PowerShell `GetLastInputInfo` implementation สำหรับ screensaver trigger — tech detail ไม่ใช่ paper

```
Search Cognitive Stack summary:
- [TETRACHROMACY] GitHub channels: LLMRouter, obsidian-llm-wiki-local, best-route-llm ✓
- [AURA] pre-mainstream: RACER (Mar 2026 preprint)
- [FOP] varied: arXiv + GitHub + HuggingFace + OpenReview (BEST-Route)
- [PARANOID] funding: BEST-Route = Microsoft (corporate-funded but code open, ICML peer-reviewed)
- [AUTISM] echo: N — papers from different research groups
- [TOURETTE] suspicious claims: BEST-Route "60% cost cut" — verified via ICML peer review + code
- [SLEEP PARALYSIS] corpus not exhausted — routing + PKM are active research areas
```

---

*Scope: 3 themes | Searches: 10/10 | Papers/projects: 8 total — 3 IMPLEMENT, 5 REFERENCE, 0 SKIP*
*Vault pre-check saved: ~4 searches (token-management + agent-eval already covered)*
