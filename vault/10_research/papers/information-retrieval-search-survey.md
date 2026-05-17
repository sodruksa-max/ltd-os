# Paper Survey — Information Retrieval and Search Quality
*Project context: LTD-OS research pipeline (web search + vault Grep/Glob) ที่ใช้ค้นหาข้อมูลหุ้น/thesis ก่อนส่ง Reese สังเคราะห์ | 2026-05-17 | Scope: 3 themes | 7 searches | 8 papers*

*Note: arXiv:2510.25518 (Agentic RAG keyphrase) + arXiv:2506.18959 (RL query formulation) ครอบคลุมแล้วใน `agent-portfolio-autonomy-survey.md` — survey นี้เฉพาะ 3 gaps ที่เหลือ*

*ปัญหาที่แก้: (1) web search ได้ข้อมูลบางหรือซ้ำ, (2) vault Grep/Glob หา atoms ไม่ครบ — keyword-only ไม่ใช่ semantic, (3) ไม่รู้ว่า coverage ครบหรือยัง*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | FinSearch (arXiv:2502.15684) | Query Reform. | Adaptive rewriter — หลังแต่ละ search ดูว่ายังขาดอะไรแล้ว reformulate ทันที; ใช้ได้ทันทีเป็น prompt pattern |
| 2 | ExpandSearch (arXiv:2510.10009) | Query Reform. | Generate 4-5 parallel sub-queries ต่อ search turn แทน 1 — ลดผลลัพธ์ซ้ำทันที |
| 3 | Metadata-contextual RAG (arXiv:2510.24402) | Dense Retrieval | Embed vault atoms พร้อม frontmatter metadata → vault lookup หา atoms ที่ tag-match ได้ฟรี |
| 4 | Deep Search Agents Survey (arXiv:2508.05668) | Coverage Gap | Coverage matrix framework — หยุด search เมื่อ evidence ครบ ไม่ใช่ fixed iteration count |

---

## Papers by Theme

### Theme A: Query Expansion / Reformulation

#### FinSearch: Agent Framework for Real-Time Financial Information Searching — Li et al. (2025)
- **Source:** arXiv:2502.15684
- **Method:** แบ่งคำถามเป็น sub-queries ตาม source type (news, SEC filing, market data) ด้วย graph representation; Adaptive Query Rewriter reformulate sub-query แต่ละอันตาม intermediate results ที่ได้มาแล้ว + temporal weighting ลดน้ำหนัก results เก่า; ทดสอบบน FinSearchBench-24 (1,500 คำถาม Jun–Oct 2024)
- **Key finding:** Adaptive rewriting loop ชนะ static query plan อย่างชัดเจน โดยเฉพาะเมื่อ sub-query แรกได้ผลลัพธ์คุณภาพต่ำ — temporal weighting ป้องกัน stale guidance เด้งขึ้นมา
- **Dataset:** FinSearchBench-24; financial news, SEC filings, market data
- **Apply to pipeline:** Researcher agent ปัจจุบันใช้ fixed query plan — เพิ่ม adaptive rewriter loop: หลังแต่ละ search call ให้ agent ตรวจว่ายังขาดข้อมูล dimension ไหน → reformulate sub-query ใหม่ก่อน call ถัดไป ไม่ต้องรัน fixed 5 queries เสมอ
- **Tag:** **IMPLEMENT** *(priority 1 — เป็น prompt pattern ไม่ต้องเขียน code)*

#### ExpandSearch: Train LLM for Query Expansion with Reinforcement Learning — Zhao, Yu & Xu (2025)
- **Source:** arXiv:2510.10009
- **Method:** RL-trained LLM generate parallel query variants หลายตัวต่อ search turn พร้อมกัน (ไม่ใช่ sequential); "Squeezer" distillation model อ่าน retrieved docs แล้ว extract เฉพาะ reasoning-critical content → search agent focus ที่ query diversification ล้วนๆ; 3B-parameter model ให้ผลดีเพราะ squeezer offload cognitive load
- **Key finding:** +4.4% avg improvement บน 7 QA benchmarks; ผล oustanding บน multi-hop tasks ที่ต้องการ diverse evidence
- **Dataset:** 7 QA benchmarks (multi-hop focus)
- **Apply to pipeline:** แทนที่จะสั่ง researcher agent ค้น "NVDA revenue growth 2025" เพียงอันเดียว → สั่งให้ generate 4-5 parallel sub-queries ที่ semantic-distinct ("Nvidia data center Q1 2025", "Jensen Huang FY2026 guidance", "NVDA gross margin trend", "NVDA China export impact") แล้วรันพร้อมกัน — ทำได้เป็น prompt rule ไม่ต้อง RL retraining
- **Tag:** **IMPLEMENT** *(priority 2 — prompt rule เพิ่มใน /stock-content Step 2)*

#### Hypothetical Documents or Knowledge Leakage? Rethinking LLM-based Query Expansion — Yoon et al. (2025)
- **Source:** arXiv:2504.14175 (ACL 2025 Findings)
- **Method:** ทดสอบว่า gain จาก HyDE-style query expansion (generate hypothetical document → search) มาจาก retrieval improvement จริงหรือจาก LLM memorized ground-truth ระหว่าง training; วัด entailment overlap ระหว่าง generated doc กับ gold evidence
- **Key finding:** Gain ส่วนใหญ่จาก HyDE อยู่ใน cases ที่ generated doc มี sentences ที่ entailed by gold evidence → benchmark contamination; เมื่อ knowledge leakage absent, gain หดตัวมาก
- **Dataset:** Fact-verification benchmarks
- **Apply to pipeline:** ⚠️ Calibration warning ก่อนใช้ HyDE สำหรับ stock queries — ถ้า LLM รู้คำตอบอยู่แล้ว HyDE เป็น circular loop; **ข้อยกเว้นที่ปลอดภัย:** ใช้ HyDE เฉพาะ recency-gated queries (earnings หลัง model cutoff, recent filing) ซึ่ง knowledge leakage เป็นไปไม่ได้ structurally
- **Tag:** REFERENCE *(อ่านก่อน implement HyDE ใดๆ)*

---

### Theme B: Dense / Semantic Retrieval แทน Keyword Grep

#### Metadata-Driven RAG for Financial Question Answering — Dadopoulos et al. (2025)
- **Source:** arXiv:2510.24402
- **Method:** Benchmark metadata-augmented RAG variants บน annual reports + 10-Ks: (1) pre-retrieval filtering ด้วย structured metadata, (2) post-retrieval reranking ด้วย LLM-generated metadata scores, (3) contextual chunk embedding — embed "[metadata] + [chunk text]" ด้วยกัน; lightweight metadata reranker เป็น cost-efficient alternative
- **Key finding:** Contextual chunk embedding (embed metadata พร้อม text) ให้ single biggest improvement; combined pre-filter + contextual embedding = best overall
- **Dataset:** Corporate annual reports, 10-K filings
- **Apply to pipeline:** vault atoms มี frontmatter อยู่แล้ว (ticker, date, thesis, source) — ตอนนี้ Grep ใช้แค่ text ไม่ใช้ metadata; **fix:** embed atom ด้วย "[ticker:NVDA, date:2025-Q1, thesis:T1] NVDA gross margin expanded..." แทน text เปล่า → embedding รู้ว่า atom นี้คือ T1 atom ไม่ใช่แค่มีคำว่า NVDA; ทำได้ด้วย one-time re-embedding pass
- **Tag:** **IMPLEMENT** *(priority 3 — one-time script, no infrastructure change)*

#### IMRNNs: Interpretable Dense Retrieval via Embedding Modulation — Saxena et al. (2026)
- **Source:** arXiv:2601.20084 (EACL 2026)
- **Method:** Adapter modules ที่ inference time: หนึ่งตัว condition document embeddings ตาม query, อีกตัว refine query embeddings ด้วย corpus feedback — bidirectional dynamic modulation โดยไม่ต้องมี post-hoc reranking; interpretable weights แสดงว่า document dimension ไหน align กับ query term ไหน
- **Key finding:** +6.35% nDCG, +7.14% recall, +7.04% MRR เฉลี่ยบน 7 benchmarks; interpretability เป็น bonus — เห็นว่า query "AI chip demand" activate atom ไหนด้วยเหตุผลอะไร
- **Dataset:** 7 BEIR-style benchmarks
- **Apply to pipeline:** Upgrade path สำหรับ vault lookup ระยะยาว — embed vault once แล้ว re-modulate per query ที่ inference time ไม่ต้อง full reindex; "AI capex supercycle" query surface NVDA atoms แม้ atom จะไม่มีคำนั้น
- **Tag:** REFERENCE *(ต้องการ vector store — implement หลัง B2)*

#### SPLATE: Sparse Late Interaction Retrieval — ACM SIGIR 2024
- **Source:** DOI:10.1145/3626772.3657968 [source-unverified — ACM DL only]
- **Method:** ผสม SPLADE (learned sparse representations) กับ ColBERT (late interaction scoring) — inverted index compatible กับ infrastructure เดิม แต่ inject learned term weights เพื่อ semantic recall
- **Key finding:** Near-ColBERT accuracy ที่ near-BM25 cost; เหมาะกับ local vault ที่ไม่อยาก setup vector database
- **Tag:** ⚠️ AGING (2024) + [source-unverified] — REFERENCE เท่านั้น; ดู B2 ก่อน

---

### Theme C: Coverage Gap Detection

#### A Survey of LLM-based Deep Search Agents — Xi et al. (2025)
- **Source:** arXiv:2508.05668
- **Method:** Survey mapping architecture space ของ deep search agents; ครอบคลุม: (a) solvability detectors — ตรวจว่า sub-task มี evidence พอหรือยัง, (b) completeness detectors — identify missing key information, (c) non-redundancy detectors — prune overlapping evidence ก่อน synthesis; พบว่า agent ส่วนใหญ่หยุดที่ fixed iteration หรือ token budget ไม่ใช่ evidence coverage
- **Key finding:** Completeness detection และ non-redundancy filtering เป็น unsolved problem ในระบบส่วนใหญ่ — agent ไม่รู้ว่าตัวเองค้นครบแล้วหรือยัง
- **Dataset:** Survey (multi-paper, no single dataset)
- **Apply to pipeline:** เพิ่ม coverage check หลังแต่ละ search round: prompt "Given $TICKER thesis, which aspects are still unaddressed: [revenue growth / margin / competitive moat / macro / management / valuation]?" + deduplication prompt "Which retrieved passages say the same thing?" → หยุดเมื่อ coverage check return empty ไม่ใช่ fixed 5 searches
- **Tag:** **IMPLEMENT** *(priority 4 — เพิ่ม coverage-check prompt ใน Step 2 stock-content.md)*

#### A Systematic Review of Key RAG Systems — Oche et al. (2025)
- **Source:** arXiv:2507.18910
- **Method:** Systematic review RAG research 2017–mid-2025; ใช้ taxonomy-based gap mapping: แผนที่ paper ต่อ capability taxonomy แล้วหา cells ที่ sparse/empty
- **Key finding:** 3 persistent gaps ใน 2025 literature: (1) retrieval quality metrics สำหรับ private document stores, (2) multi-hop completeness, (3) detecting when context insufficient vs. incorrect — ข้อ 3 ตรงกับปัญหา search coverage โดยตรง
- **Apply to pipeline:** Coverage matrix template: rows = thesis dimensions (revenue, margin, moat, macro, management, valuation), columns = sources checked (web news, SEC, vault atoms, macro KB) → หลัง researcher run ให้ fill matrix ว่า cell ไหน has evidence / empty; empty cells = gaps ที่ flag ให้ Reese
- **Tag:** REFERENCE *(framework สำหรับ implement coverage matrix)*

#### Multi-Agent LLMs for Generating Research Limitations — Al-Azher et al. (2025)
- **Source:** arXiv:2601.11578 ⚠️ [source-unverified — ID จาก search snippet, abstract page ไม่ verified]
- **Method:** Multi-agent LLM setup identify สิ่งที่ research ไม่ครอบคลุม ("limitations and gaps" generation); agents reason เกี่ยวกับ evidence ที่ NOT found
- **Key finding:** Multi-agent deliberation ชนะ single-agent บน gap identification เพราะ agents ต่างกัน identify gap ต่าง class (methodological / domain / temporal)
- **Apply to pipeline:** หลัง synthesis เขียน Reese doc → run gap-identification agent: "What aspects of $TICKER thesis are NOT addressed by sources gathered?" รัน 3 รอบ (bear case gaps, macro sensitivity gaps, technical competitive gaps) → output เป็น ❓ list ใน Data gaps section
- **Tag:** REFERENCE ⚠️ [source-unverified — verify arXiv abstract ก่อน implement]

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **ExpandSearch parallel sub-queries (2510.10009)** → เพิ่มใน Step 2 (Researcher) ของ stock-content.md: "generate 4-5 semantically distinct sub-queries ก่อน search" → complexity: **low** — 2 บรรทัดใน search instruction
2. **FinSearch adaptive rewriter (2502.15684)** → เพิ่ม adaptive loop ใน Step 2: หลังแต่ละ search → ตรวจว่าขาด dimension ไหน → reformulate ถ้าจำเป็น → complexity: **low** — prompt rule
3. **Coverage matrix check (2508.05668 + 2507.18910)** → เพิ่ม coverage-check prompt ท้าย Step 2: 6 dimensions × sources matrix → flag gaps ให้ Reese → complexity: **low** — prompt rule
4. **Metadata-contextual vault embedding (2510.24402)** → สร้าง script embed vault atoms ด้วย frontmatter prepended → ใช้แทน Grep ใน Step 1B → complexity: **medium** — Python script + embedding model call
5. **Dense retrieval upgrade (2601.20084)** → ใช้ IMRNNs สำหรับ vault lookup ทั้งหมด → complexity: **high** — ต้องการ vector store + reindex

---

## Gaps

- ไม่มี paper ที่ benchmark query expansion บน **equity research** หรือ **earnings call retrieval** โดยตรง — papers ทดสอบบน financial QA ทั่วไป (FiQA, FinQA)
- SIGIR 2025 proceedings สำหรับ novelty/redundancy detection ใน agentic IR ไม่ accessible — gap นี้ยังเปิดอยู่
- arXiv:2601.11578 ยัง [source-unverified] — verify ก่อน implement

---

*Scope: 3 themes | Searches: 7/7 | Papers: 8 total — 4 IMPLEMENT, 3 REFERENCE, 1 AGING+unverified*
