# Paper Survey — LLM Token & Context Management
*Project context: Claude Code workflow ที่ใช้ multiple agents + Obsidian vault เป็น memory; ปัญหา: context window เต็มเร็วเมื่อ agent อ่านหลายไฟล์, summarization token cost สูง, vault lookup ต้องอ่านหลายไฟล์พร้อมกัน | 2026-05-05 | Scope: 4 themes | 10 searches | 10 papers*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | The Complexity Trap (arXiv:2508.21433, 2025) | Context masking | หยุด summarize ทุก tool output — masking ถูกกว่า 52% ให้ผลเท่ากัน |
| 2 | CompactPrompt (arXiv:2510.18043, 2025) | Prompt compression | ลด token 60% ก่อนส่งให้ agent — tested บน Claude-3.5-Sonnet จริง |
| 3 | Memory Pointers (arXiv:2511.22729, 2025) | Context overflow | แทน raw file content ด้วย pointer — agent อ่าน vault ขนาดไหนก็ไม่ overflow |
| 4 | A-MEM (arXiv:2502.12110, 2025) | Agent memory | Zettelkasten dynamic linking — ตรงกับ vault concept ที่มีอยู่แล้ว |
| 5 | SheetCompressor (arXiv:2407.09025, 2024) | Tabular compression | Structural anchor principle — ใช้กับ universe-screen.py label grouping ได้ทันที |
| 6 | MARS (arXiv:2509.20502, 2025) | Multi-agent sharing | ลด /council token 50% — reviewer ไม่ interact กัน → synthesizer รวมเอง |
| 7 | Metacognitive Reuse (arXiv:2509.13237, 2025) | Cognitive layer reuse | behavior handbook ลด pre-market cognitive layers 46% โดยไม่เสียคุณภาพ |
| 8 | Don't Break the Cache (arXiv:2601.06007, 2026) | Prompt caching rules | วาง dynamic content ท้าย prompt → 41-80% cost reduction ทุก session |
| 9 | Agentic Plan Caching (arXiv:2506.14852, 2025) | Plan reuse | cache plan skeleton /pre-market → 50% cost, 27% latency reduction |
| 10 | AgentDropout (arXiv:2503.18891, 2025) | Agent elimination | /council: ตัด duplicate critiques → ลด synthesizer input 20%+ |
| 11 | Thinking with Reasoning Skills (arXiv:2604.21764, 2026) | Reasoning reuse | store reasoning skills vault → ลด cognitive reasoning tokens |
| 12 | ACON (arXiv:2510.00615, 2025) | Context compression | guidelines-driven compression — 26-54% peak token reduction |
| 13 | SelfBudgeter (arXiv:2505.11274, 2025) | Output budget | agent ประกาศ output scope ก่อน generate → −61% output length ผลไม่ตก |
| 14 | Long-Term Memory EDU (arXiv:2511.17208, 2025) | Session history | restructure tool outputs เป็น discourse atoms → retrieve แทน keep ใน context |
| 15 | AgentDiet (arXiv:2509.23586, 2025) | Trajectory pruning | strip expired tool outputs หลัง handoff แต่ละ stage → −40-60% input tokens ไม่เสีย quality |
| 16 | MemAgent (arXiv:2507.02259, 2025) | Chunk-sequential | อ่าน PDF/transcript เป็น chunks + rolling summary → linear complexity แทน O(n²) |
| 17 | Memori (arXiv:2603.19935, 2026) | Session serialization | handoff เป็น semantic triples แทน free-text → 67% fewer tokens, 20x cost savings vs full history |
| 18 | Meta-tools/AWO (arXiv:2601.22037, 2026) | Tool meta-bundling | collapse recurring tool sequences → −11.9% LLM calls ใน /stock-content pipeline |
| 19 | Prefix Homogeneity (arXiv:2605.06046, 2026) | Cache-aware batching | static prefix byte-identical across /council agents → maximize prefix cache hit rate |
| 20 | Coding Agents (arXiv:2603.20432, 2026) | File-system navigator | vault-wide synthesis via grep/glob ไม่ต้อง load หลายไฟล์ → +17.3% เหนือ SOTA |

---

## Papers by Theme

### Theme 1: Prompt Compression

#### CompactPrompt: A Unified Pipeline for Prompt and Data Compression — (arXiv:2510.18043, Oct 2025)
- **Source:** [arXiv:2510.18043](https://arxiv.org/abs/2510.18043)
- **Method:** 3 layers: (1) ตัด low-information tokens ด้วย self-information scoring, (2) n-gram abbreviation สำหรับ patterns ที่ซ้ำในเอกสาร, (3) numeric quantization สำหรับตัวเลข
- **Key finding:** ลด token 53-60% บน TAT-QA + FinQA โดย accuracy ลดน้อยกว่า 5% — tested กับ Claude-3.5-Sonnet และ GPT-4.1-Mini จริง
- **Dataset:** TAT-QA, FinQA (document-heavy QA benchmarks)
- **Apply to project:** ก่อนส่ง vault file ให้ agent อ่าน → ใช้ compact pipeline ตัด boilerplate (frontmatter repetition, bullet point redundancy, repeated context headers) ออกก่อน; เฉพาะไฟล์ใหญ่ > 500 words
- **Tag:** IMPLEMENT

#### Prompt Compression for LLMs: A Survey — (arXiv:2410.12388, Oct 2024)
- **Source:** [arXiv:2410.12388](https://arxiv.org/abs/2410.12388)
- **Method:** Review hard prompt methods (token pruning, extractive compression) vs soft prompt methods (learned embeddings); จัดกลุ่มตาม attention optimization, PEFT, modality
- **Key finding:** Hard prompt compression (token pruning ด้วย perplexity scoring) เป็นวิธีที่ implement ได้ง่ายสุดโดยไม่ต้อง fine-tune model
- **Dataset:** Theoretical survey + benchmark
- **Apply to project:** ใช้เป็น reference เมื่อจะเลือก compression technique — hard prompt ดีกว่าสำหรับ Claude Code เพราะไม่ต้อง train model
- **Tag:** REFERENCE

---

### Theme 2: Context Window Management & Overflow

#### The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization — Lindenbauer et al. (arXiv:2508.21433, Aug 2025)
- **Source:** [arXiv:2508.21433](https://arxiv.org/abs/2508.21433)
- **Method:** เปรียบ 3 strategies: (1) raw agent (ใส่ทุก observation), (2) LLM-based summarization (costly), (3) simple observation masking (ซ่อน old observations ไม่ส่งให้ LLM); ทดสอบบน SWE-bench Verified ด้วย 5 model configs
- **Key finding:** Masking ถูกกว่า raw agent 52% + solve rate เท่ากับหรือดีกว่า LLM summarization; hybrid (masking + selective summarize เฉพาะบางส่วน) ลดต้นทุนอีก 7-11%
- **Dataset:** SWE-bench Verified, Qwen3-Coder 480B + 4 other models
- **Apply to project:** เปลี่ยน default agent behavior: แทนที่จะ summarize ไฟล์ vault ที่อ่านแล้ว → mask ออกจาก context แทน; เฉพาะ file ที่ agent ไม่ได้ reference ในรอบล่าสุดเท่านั้น; ช่วยลดต้นทุน `/pre-market` และ `/post-market` ที่อ่านหลายไฟล์
- **Tag:** IMPLEMENT

#### Solving Context Window Overflow in AI Agents — Bulle Labate (arXiv:2511.22729, Nov 2025)
- **Source:** [arXiv:2511.22729](https://arxiv.org/abs/2511.22729)
- **Method:** แทน raw tool response ด้วย memory pointer — LLM รับ pointer reference แทน full content; ดึงข้อมูลจาก pointer ตอนต้องการจริงเท่านั้น
- **Key finding:** agent สามารถ process tool response ขนาดใดก็ได้โดยไม่ overflow; ลด token usage + execution time; validate บน Materials Science application ที่ conventional workflow ทำไม่ได้
- **Dataset:** Real-world Materials Science agentic workflow
- **Apply to project:** เมื่อ agent อ่าน vault file ขนาดใหญ่ (เช่น paper survey > 2000 words) → เก็บ content ใน memory slot, ส่งแค่ pointer + metadata ให้ context หลัก; agent เรียก content จาก pointer เฉพาะเมื่อต้องใช้จริง
- **Tag:** IMPLEMENT

#### Active Context Compression: Autonomous Memory Management in LLM Agents — (arXiv:2601.07190, Jan 2026)
- **Source:** [arXiv:2601.07190](https://arxiv.org/abs/2601.07190)
- **Method:** Agent ตัดสินใจเองว่าจะ compress context ตรงไหนและเมื่อไร โดยไม่มี fixed schedule
- **Key finding:** Autonomous compression ดีกว่า periodic/fixed-interval compression เพราะปรับตาม task complexity จริง
- **Dataset:** Multi-turn agent tasks
- **Apply to project:** ใช้ concept นี้ใน CLAUDE.md policy: แทนที่ "compress ทุก N turns" ให้ agent ตัดสินใจ compress เมื่อ context > 70% โดยดูว่า section ไหนไม่ได้ reference ใน last 3 turns
- **Tag:** REFERENCE

---

### Theme 3: Smart Retrieval (RAG)

#### ContextWeaver: Selective and Dependency-Structured Memory Construction for LLM Agents — Wu et al. (arXiv:2604.23069, Apr 2026)
- **Source:** [arXiv:2604.23069](https://arxiv.org/abs/2604.23069)
- **Method:** สร้าง dependency graph ของ reasoning steps → เลือก context ที่ relevant ต่อ step ปัจจุบันเท่านั้น (ไม่ใช่ sliding window); มี compact dependency summaries + validation layer
- **Key finding:** เหนือกว่า sliding-window baseline ใน SWE-Bench Verified pass@1 โดยใช้ reasoning steps น้อยกว่าและ token น้อยกว่า
- **Dataset:** SWE-Bench Verified + Lite
- **Apply to project:** Vault MEMORY.md ควรเป็น dependency graph — แต่ละ memory node link ไปยัง vault files ที่ depend กัน; agent ดึงเฉพาะ node ที่ relevant ต่อ task ปัจจุบัน แทนที่จะโหลด PROJECTS + DECISIONS + PREFERENCES ทั้งหมดทุกครั้ง
- **Tag:** IMPLEMENT

#### TeaRAG: Token-Efficient Agentic Retrieval-Augmented Generation — (arXiv:2511.05385, Nov 2025)
- **Source:** [arXiv:2511.05385](https://arxiv.org/abs/2511.05385)
- **Method:** ลด token usage ใน agentic RAG โดยแก้ปัญหา low information density + noise ใน retrieved chunks
- **Key finding:** ลด retrieved token waste โดย re-rank และ filter chunks ก่อนใส่ context
- **Dataset:** QA + agentic tasks
- **Apply to project:** เมื่อ vault search (Grep) คืนผลหลาย files → filter เฉพาะ chunk ที่ match จริงก่อนส่งให้ agent แทนที่จะโหลด entire file
- **Tag:** REFERENCE

---

### Theme 4: Agent Memory Architecture

#### A-MEM: Agentic Memory for LLM Agents — (arXiv:2502.12110, Feb 2025)
- **Source:** [arXiv:2502.12110](https://arxiv.org/abs/2502.12110)
- **Method:** Memory system ที่ inspired จาก Zettelkasten — สร้าง interconnected knowledge network; memory note แต่ละตัวมี links ไป related memories; dynamic indexing + updating
- **Key finding:** Dynamic linked memory ดีกว่า flat memory store ทั้ง retrieval accuracy และ token efficiency เพราะดึงเฉพาะ connected nodes แทน full scan
- **Dataset:** Multi-task agent benchmarks
- **Apply to project:** vault/_memory/ structure ตรงกับ Zettelkasten concept — เพิ่ม explicit `related:` links ใน memory files เพื่อให้ agent ดึงเฉพาะ relevant chain แทนโหลดทุกไฟล์ใน _memory/; เช่น PREFERENCES.md → links ไป DECISIONS.md + OUTCOMES.md เฉพาะ entries ที่ relevant
- **Tag:** IMPLEMENT

#### Token-Budget-Aware LLM Reasoning — (arXiv:2412.18547, Dec 2024)
- **Source:** [arXiv:2412.18547](https://arxiv.org/abs/2412.18547)
- **Method:** Framework ที่ estimate token budget ที่ต้องใช้ per task ล่วงหน้า แล้ว allocate ตาม complexity
- **Key finding:** Dynamic token budget ลด cost Chain-of-Thought reasoning โดย accuracy ลดน้อย; simple tasks ใช้ token น้อยกว่า hard tasks โดยอัตโนมัติ
- **Dataset:** Reasoning benchmarks
- **Apply to project:** กำหนด token budget per agent ตาม task type — researcher (5 search slots) = cheap, executor (file ops) = very cheap, planner (full context) = expensive; แจ้ง user เมื่อ task จะเกิน budget ก่อน start
- **Tag:** REFERENCE

#### Intrinsic Memory Agents — (arXiv:2508.08997, Aug 2025)
- **Source:** [arXiv:2508.08997](https://arxiv.org/abs/2508.08997)
- **Method:** แต่ละ agent มี intrinsic memory ของตัวเองที่ evolve ตาม role; memory แยกกันระหว่าง agents แต่ share บาง context เมื่อจำเป็น
- **Key finding:** Role-specific memory ลด cross-agent context overhead — agent ไม่ต้องโหลด context ของ agent อื่นทั้งหมด
- **Dataset:** Multi-agent task benchmarks
- **Apply to project:** แต่ละ agent (planner/coder/researcher) ควรมี memory scope ของตัวเอง — coder โหลดแค่ project files ที่เกี่ยวข้อง, researcher โหลดแค่ paper vault; ไม่โหลด PREFERENCES.md ทุกครั้ง ถ้า task ไม่เกี่ยวกับ user preference
- **Tag:** REFERENCE

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **Observation Masking (arXiv:2508.21433)** → เพิ่มใน CLAUDE.md policy: "เมื่อ agent อ่าน vault file แล้ว → mask ออกจาก active context หลังใช้เสร็จ; อย่า summarize (expensive) เว้นแต่ user ขอ" → complexity: **low** (เปลี่ยน guideline ใน CLAUDE.md)

2. **Context overflow → memory pointer pattern (arXiv:2511.22729)** → เพิ่มใน agent instruction: "ถ้า file > 1000 words → อ่านเฉพาะ section ที่ต้องการ (offset+limit) ไม่โหลดทั้งไฟล์" → complexity: **low** (ใช้ Read tool ที่มี offset/limit อยู่แล้ว)

3. **CompactPrompt principles (arXiv:2510.18043)** → เพิ่มใน vault/_memory/ files: ตัด redundant boilerplate headers ออก, ย่อ example entries, ใช้ bullet form แทน prose → complexity: **medium** (ปรับ memory files ทีละไฟล์)

4. **A-MEM linking (arXiv:2502.12110)** → เพิ่ม `related:` section ใน MEMORY.md index — แต่ละ entry บอกว่า related กับไฟล์ไหน เพื่อให้ load แบบ chain แทน load ทั้งหมด → complexity: **medium**

5. **ContextWeaver dependency graph (arXiv:2604.23069)** → restructure MEMORY.md index เป็น task-type mapping: pre-market task → โหลดแค่ PREFERENCES (trading) + OUTCOMES; research task → โหลดแค่ PROJECTS → complexity: **medium** (เปลี่ยน session start instructions)

---

## Gaps

- **Prompt caching (Anthropic native)** — Claude API มี prompt caching ที่ลด cost 90% สำหรับ repeated context; ยังไม่มี paper survey เฉพาะ — ค้นหาใน Anthropic docs แทน paper
- **Token counting before task** — การ estimate token cost ก่อน start task (token budget prediction); `arXiv:2412.18547` ครอบบางส่วน แต่ยังไม่มี implementation สำหรับ agentic Claude Code
- **Vault-specific retrieval** — งานวิจัยเรื่อง semantic search บน personal knowledge base เฉพาะ (Obsidian-style); TeaRAG + A-RAG ครอบในมุม generic แต่ไม่ specific กับ markdown vault

---

*Scope: 4 themes | Searches: 10/10 | Papers: 10 total — 4 IMPLEMENT, 6 REFERENCE, 0 SKIP*

---

## Appendix — 2026-05-11: Structured Data + Provider Caching

*Context: LLMLingua-2 ถูก evaluate แล้วพบว่า NOT suitable สำหรับ tabular/numeric script output (trained on narrative text, not tables) → ค้นหา alternative สำหรับ compression ของ structured output เช่น sr-levels.py, universe-screen.py | 5 searches | 3 papers ใหม่*

### Theme 5: Structured / Tabular Data Compression

#### SpreadsheetLLM / SheetCompressor — Wang et al., Microsoft (arXiv:2407.09025, Jul 2024)
- **Source:** [arXiv:2407.09025](https://arxiv.org/abs/2407.09025)
- **Method:** Framework 3 โมดูล: (1) **Structural Anchor Compression** — ระบุแถว/คอลัมน์ที่ heterogeneous (มีโครงสร้างสำคัญ) และ prune แถว homogeneous ที่ซ้ำ (ข้อมูล numeric ต่อเนื่องที่มีรูปแบบเดียวกัน) ออก; (2) **Inverse Index Translation** — แทนค่า cell ด้วย inverted index JSON (cell value → list of addresses) ลด repetition; (3) **Data-Format-Aware Aggregation** — group numeric cells ที่ adjacent และมี format เดียวกัน แทนที่จะแสดงทุกค่า
- **Key finding:** ลด token 96% (25x compression ratio) บน spreadsheet tasks; F1 score 78.9% ชนะ SOTA เดิม 12.3%; เมื่อ compress แล้ว LLM เข้าใจ structure ดีขึ้นเพราะ noise ลดลง
- **Dataset:** SpreadsheetBench — table detection + QA บน real spreadsheets
- **Apply to project:** Principle ของ structural anchor ตรงกับสิ่งที่ `sr-levels.py --brief` ทำอยู่ — เก็บ key levels (S1/S2/R1/R2) และ prune รายละเอียด pivot ที่ซ้ำ; ขยายต่อได้โดยใช้ **data-format aggregation** ใน `universe-screen.py`: group tickers ที่มี label เดียวกัน (เช่น EXTENDED ทั้งหมด) แทนแสดงทีละแถว → ลด output อีก 30-40%
- **Tag:** IMPLEMENT

#### TOON: Token-Oriented Object Notation vs JSON — (arXiv:2603.03306, Feb 2026)
- **Source:** [arXiv:2603.03306](https://arxiv.org/abs/2603.03306)
- **Method:** Format serialization ใหม่ที่แทน JSON — ใช้ indentation แทน nested braces, ตัด quotation marks / commas / brackets ออก (คล้าย YAML แต่ออกแบบสำหรับ LLM tokenization patterns); มี spec เปิดพร้อม Python library
- **Key finding:** ลด token ~40% ใน mixed-structure benchmarks ทั้ง 4 models; แต่มี "prompt tax" overhead เมื่อ context สั้น — TOON คุ้มค่าเฉพาะเมื่อ structured payload > ~500 tokens; plain JSON ยัง generate ได้ accurate กว่าใน constrained decoding
- **Dataset:** Mixed-structure generation benchmark, 4 LLM models
- **Apply to project:** พิจารณาใช้กับ ORDERS block ใน `nick_weekly_auto.py` — ปัจจุบัน output เป็น JSON; แต่ **RISK: JSON parsing ที่ `validate_orders_block()` จะ break** → SKIP สำหรับ trading output ที่ต้องการ reliability; อาจใช้สำหรับ non-critical structured context (เช่น KB gaps table) แทน
- **Tag:** REFERENCE

### Theme 6: Provider-Native Prompt Caching

#### Anthropic Prompt Caching — Anthropic API Feature (2024–ongoing)
- **Source:** [Anthropic Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | [Token-saving updates](https://www.anthropic.com/news/token-saving-updates)
- **Method:** Developer mark static content blocks ด้วย `cache_control` breakpoint; Claude cache prefix สูงสุด 4 breakpoints ต่อ request; TTL 5 min (1.25x write cost) หรือ 1 hour (2x write cost); cache read cost = 0.1x base input (ลด 90%)
- **Key finding:** 90% cost reduction + 85% latency reduction สำหรับ long repeated prompts; agentic workflows ได้ประโยชน์เมื่อ system prompt + tool definitions static ข้าม turns; Claude Code ตัวเอง benefit จาก automatic prefix caching สำหรับ CLAUDE.md + session start context
- **Dataset:** Production API usage (engineering feature ไม่ใช่ academic paper)
- **Apply to project:** (1) ใน `nick_weekly_auto.py` ที่ใช้ Groq — Groq ยังไม่มี prompt caching native; ถ้า migrate ไป Claude API → wrap `nick-soul.md` + static `insight-atoms` ด้วย `cache_control` → ลด cost 90% per weekly run; (2) Claude Code เอง — CLAUDE.md ยิ่ง stable ยิ่ง cache hit rate สูง; หลีกเลี่ยงการแก้ CLAUDE.md บ่อยโดยไม่จำเป็น (ทุกครั้งที่แก้ = cache miss ใหม่)
- **Tag:** IMPLEMENT (เมื่อ migrate Nick ไป Claude API หรือ audit CLAUDE.md stability)

---

### Implementation Roadmap — เพิ่มเติม (2026-05-11)

6. **universe-screen.py grouping (SheetCompressor principle)** → group tickers ที่ label เดียวกัน: `EXTENDED: AMD, NVDA, AVGO` แทนแสดงทีละแถว → complexity: **low** (แก้ print logic ใน script)
7. **Prompt caching audit (Anthropic native)** → วัด CLAUDE.md change frequency; ถ้า stable > 80% sessions → ไม่ต้องทำอะไรเพิ่ม (automatic); ถ้า nick_weekly migrate ไป Claude API → add `cache_control` breakpoints → complexity: **medium**

---

### Gaps — อัพเดต

- **Groq prompt caching** — Groq ยังไม่มี native caching; ถ้า nick_weekly ยังใช้ Groq → token cost สูงต่อไป; ทางเลือก: cache ด้วย hash key ใน Python (ถ้า prompt ไม่เปลี่ยน → skip API call ใช้ cached response แทน)
- **universe-screen.py label grouping** — ยังไม่มี paper เฉพาะ; ใช้ SheetCompressor principle (structural anchor + homogeneous row pruning) เป็น basis ได้

---

*Appendix scope: 2 themes | Searches: 5/5 | Papers: 3 — 2 IMPLEMENT, 1 REFERENCE | Total survey: 6 themes, 13 papers — 6 IMPLEMENT, 7 REFERENCE*

---

## Appendix — 2026-05-18: Multi-Agent Context Sharing + Cognitive Layer Reuse

*Context: pain points ใหม่ที่ survey เดิมยังไม่ครอบคลุม — (1) /council: 4-6 agents แต่ละตัวอ่าน brief+proposals ซ้ำกันทั้งหมด, (2) /pre-market: cognitive layers 15+ รอบ วิเคราะห์ data ชุดเดิมซ้ำ | 8 searches | 6 papers ใหม่*

---

### Theme 7: Multi-Agent Context Sharing

ปัญหาใน /council: optimist / pragmatist / skeptic / caveman แต่ละตัวได้รับ brief เดียวกัน → แต่ต้องโหลด context ซ้ำทั้งหมดทุก agent call

#### KVCOMM: Online Cross-context KV-cache Communication for Efficient LLM-based Multi-agent Systems — Ye, Gao et al. (arXiv:2510.12872, Oct 2025) [NeurIPS'25]
- **Source:** [arXiv:2510.12872](https://arxiv.org/abs/2510.12872) | [GitHub](https://github.com/HankYe/KVCOMM)
- **Method:** Framework training-free ที่ให้ agents reuse KV-cache ของ overlapping content ข้าม contexts — แก้ปัญหา positional misalignment โดย estimate และ adjust cache offsets โดยใช้ anchor pool จาก cached examples; ทำงาน online ระหว่าง inference
- **Key finding:** ~6.7× prefill speedup บน Llama-3.1-8B บน H100; >70% reuse rate ข้าม diverse multi-agent workloads (RAG, math reasoning, collaborative coding) โดยไม่มี quality degradation
- **Dataset:** Multi-agent workloads บน NVIDIA H100 GPU
- **Apply to project:** ใน /council: brief.md ถูกส่งให้ 4 agents — ด้วย KVCOMM principle สามารถ cache KV ของ brief ครั้งแรกแล้ว reuse ให้ agents ถัดไปแทนที่จะ prefill ใหม่ทั้งหมด; ใน Claude Code context: เรียง static content (brief + CLAUDE.md) ไว้ต้น prompt ก่อน agent-specific instruction เพื่อ maximize cache hit ของ Anthropic prefix caching
- **Tag:** IMPLEMENT

#### MARS: Toward More Efficient Multi-Agent Collaboration for LLM Reasoning — Wang et al. (arXiv:2509.20502, Sep 2025)
- **Source:** [arXiv:2509.20502](https://arxiv.org/abs/2509.20502) | [GitHub](https://github.com/xwang97/MARS)
- **Method:** Role-based collaboration: author agent สร้าง solution → reviewer agents ให้ feedback อิสระ (ไม่คุยกันเอง) → meta-reviewer รวม feedback และ guide revision; หลีกเลี่ยง reviewer-to-reviewer interaction ที่ costly ใน Multi-Agent Debate (MAD)
- **Key finding:** ลด token 50% และ inference time 50% เทียบกับ MAD โดย accuracy เท่ากัน; บน GPQA + GPT-4o-mini: MAD ใช้ 17,083 tokens/query, MARS ใช้ 7,903 tokens/query
- **Dataset:** GPQA, general reasoning benchmarks
- **Apply to project:** /council ปัจจุบันใช้ MAD-style (4 proposers คุยกันผ่าน critiques.md) → restructure เป็น MARS pattern: proposal agents สร้าง proposals อิสระ (ทำอยู่แล้ว) → critique phase ลด reviewer-to-reviewer interaction → synthesizer เป็น meta-reviewer รวมทุกอย่าง; ลด council token ~50% โดยไม่เสียคุณภาพ synthesis
- **Tag:** IMPLEMENT

#### Token Economics for LLM Agents: A Dual-View Study from Computing and Economics — Chen et al. (arXiv:2605.09104, May 2026)
- **Source:** [arXiv:2605.09104](https://arxiv.org/html/2605.09104v1)
- **Method:** Unified framework วิเคราะห์ token consumption ของ multi-agent systems จาก 2 มุม: (1) computing — memory management, retrieval, pruning; (2) economics — carrying cost (context ที่ถือไว้) vs stockout cost (ข้อมูลที่ขาด); วิเคราะห์ trade-off optimal
- **Key finding:** ระบุ 3 bottleneck หลักของ agentic token cost: exponential context growth, redundant cross-agent communication, และ security overhead; เสนอ unified cost model สำหรับ design decisions
- **Dataset:** Theoretical framework + case studies
- **Apply to project:** ใช้ dual-view framework ประเมิน vault loading: carrying cost = token ที่ใช้โหลด memory files; stockout cost = ข้อมูลที่ขาดทำให้ agent ตัดสินใจผิด; ตรง task-scoped loading policy ใน CLAUDE.md §8 ที่มีอยู่แล้ว — ยืนยัน approach ถูกต้อง
- **Tag:** REFERENCE

---

### Theme 8: Cognitive Layer / Recurring Reasoning Reuse

ปัญหาใน /pre-market: 15+ cognitive layers (Tourette, Synesthesia, HSP, PTSD, AURA ฯลฯ) แต่ละ layer วิเคราะห์ data ชุดเดิมซ้ำ — reasoning pattern เหมือนกันทุกวัน แต่ไม่มีการ reuse

#### Metacognitive Reuse: Turning Recurring LLM Reasoning Into Concise Behaviors — Didolkar, Ballas, Arora, Goyal; Meta AI (arXiv:2509.13237, Sep 2025)
- **Source:** [arXiv:2509.13237](https://arxiv.org/abs/2509.13237)
- **Method:** Model วิเคราะห์ reasoning traces ที่ผ่านมา → ระบุ recurring steps → สร้าง "behaviors" (ชื่อ + instruction สั้น) เก็บใน "behavior handbook"; ตอน inference ส่ง relevant behaviors ใน-context แทนให้ model re-derive ทุกครั้ง; ไม่ต้อง fine-tune — ทำงาน in-context
- **Key finding:** ลด reasoning tokens 46% โดย accuracy ไม่ลดลงหรือดีขึ้น; procedural knowledge (how to think) ไม่ใช่ declarative facts — ต่างจาก RAG ทั่วไป
- **Dataset:** Multi-step reasoning benchmarks; Meta AI research
- **Apply to project:** /pre-market cognitive layers เป็น procedural behaviors ชัดเจน — แต่ละ layer เป็น named behavior ที่ทำซ้ำทุกวัน; implement behavior handbook ใน `vault/Knowledge/pre-market-behaviors.md`: แต่ละ entry = behavior name + compressed instruction (ไม่ใช่ full layer description); ก่อน run cognitive layers → load handbook แล้วอ้างอิง name แทน expand instruction ทั้งหมด — ลด cognitive layer section ~40%
- **Tag:** IMPLEMENT

#### GenCache: Generative Caching for Structurally Similar Prompts and Responses — Chakraborty, Nath, Zhang et al. (arXiv:2511.17565, Nov 2025)
- **Source:** [arXiv:2511.17565](https://arxiv.org/abs/2511.17565) | Microsoft Research
- **Method:** Generative cache ที่ identify reusable response patterns ข้าม structurally similar prompts → synthesize variation-aware outputs สำหรับ request ใหม่; ใช้ pattern matching บน prompt structure (ไม่ใช่ exact match) + generative fill สำหรับส่วนที่ต่างกัน
- **Key finding:** 83% cache hit rate บน datasets ที่มี prompt repetition; minimal incorrect hits บน datasets ที่ไม่มีการซ้ำ; เหมาะกับ recurring structured workflows
- **Dataset:** QA + agentic task benchmarks
- **Apply to project:** /pre-market template เปลี่ยนเฉพาะ data values ไม่ใช่ structure — GenCache principle: แยก static structure (cognitive layer headers, section format, analysis patterns) ออกจาก dynamic values (VIX, Brent, futures %); pre-generate layer output template ครั้งแรก → subsequent runs fill values แทน re-reason structure ทั้งหมด; ลด token per cognitive layer ~30-40%
- **Tag:** IMPLEMENT

#### Don't Break the Cache: An Evaluation of Prompt Caching for Long-Horizon Agentic Tasks — Lumer, Nizar, Jangiti, Frank et al. (arXiv:2601.06007, Jan 2026)
- **Source:** [arXiv:2601.06007](https://arxiv.org/abs/2601.06007)
- **Method:** Evaluate prompt caching ของ 3 providers (OpenAI, Anthropic, Google) ด้วย 3 strategies: (1) full context caching, (2) system prompt only, (3) exclude dynamic tool results; ทดสอบบน DeepResearch Bench — multi-turn agentic tasks ที่มี web search tool calls จริง
- **Key finding:** ลด API cost 41-80% + TTFT ดีขึ้น 13-31%; กฎสำคัญ: วาง dynamic content (tool results) ไว้ **ท้าย** prompt เสมอ — ถ้าวางต้นจะ break cache ทุก call; naive full-context caching อาจ เพิ่ม latency แบบขัดใจ
- **Dataset:** DeepResearch Bench (real-world agentic tasks, 3 LLM providers)
- **Apply to project:** rule ที่ implement ได้ทันทีใน Claude Code: (1) ใน /pre-market — ใส่ TRADING_RULES.md + static cognitive layer templates ไว้ต้น prompt, dynamic script outputs (macro-snapshot, news) ไว้ท้าย; (2) ใน /council — brief.md static ต้น, proposals (dynamic) ท้าย; (3) CLAUDE.md ยิ่ง stable ยิ่งดี — อย่าแก้บ่อย (cache miss ทุกครั้ง); ประมาณ 50-70% cost reduction สำหรับ long sessions
- **Tag:** IMPLEMENT

---

### Implementation Roadmap — เพิ่มเติม (2026-05-18)

8. **Pre-market behavior handbook (Metacognitive Reuse)** → สร้าง `vault/Knowledge/pre-market-behaviors.md` — 15+ cognitive layers แต่ละตัวเป็น behavior name + 2-3 ประโยค แทนที่ full instruction ขยาย; load handbook ต้น session → reference ชื่อ → ลด cognitive section ~40% → complexity: **low** (สร้างไฟล์ใหม่ + แก้ pre-market brief instruction)

9. **/council restructure เป็น MARS pattern** → ลด critique phase: proposals อิสระ (ทำอยู่แล้ว ✅) → critiques ไม่ให้ agent A อ่าน output agent B ก่อน → synthesizer รวมทุกอย่าง; ลด /council token ~50% → complexity: **medium** (แก้ council.md phase 3)

10. **Static-first prompt ordering (Don't Break the Cache)** → enforce rule ใน CLAUDE.md: "วาง static context (rules, templates, KB) ต้น prompt เสมอ; dynamic outputs (script results, news) ท้าย" → ใช้ได้กับ /pre-market, /council, /nick-weekly → complexity: **low** (เพิ่ม 1 rule ใน CLAUDE.md)

11. **Cognitive layer template splitting (GenCache principle)** → แยก layer output เป็น structure template + value slots; วัน session แรก generate template → วันถัดไป fill values แทน → complexity: **medium** (ต้องออกแบบ template format)

---

### Gaps — อัพเดต (2026-05-18)

- **KVCOMM native implementation** — ต้องการ access ไปยัง KV cache layer ซึ่งไม่ available ใน Claude Code API; แต่ principle (static content first + Anthropic prefix caching) ใช้ได้โดยไม่ต้อง implement KVCOMM เอง
- **Behavior handbook auto-generation** — Metacognitive Reuse ต้องการ model reflect on prior traces อัตโนมัติ; ใน LTD-OS ต้องทำ semi-manual ครั้งแรก (สร้าง handbook ด้วยมือ) แล้วค่อย automate ทีหลัง
- **Cross-session cache persistence** — Anthropic prompt cache TTL 5 min; ระหว่าง sessions cache miss ทุกครั้ง; ยังไม่มี paper สำหรับ persistent cache across separate API sessions

---

*Appendix scope: 2 themes | Searches: 8/8 | Papers: 6 — 5 IMPLEMENT, 1 REFERENCE | Total survey: 8 themes, 19 papers — 11 IMPLEMENT, 8 REFERENCE*

---

## Appendix — 2026-05-18 (รอบ 2): Plan Caching + Agent Elimination + Efficient Reasoning + Semantic Cache

*Pain points ที่ยังขาด: (1) /pre-market รัน workflow เดิมทุกวัน — plan ไม่ถูก cache, (2) /council agents ที่ไม่ contribute ยังกิน token, (3) cognitive layer reasoning verbose เกิน, (4) repeated similar queries ไม่มี semantic match | 9 searches | 7 papers ใหม่*

---

### Theme 9: Agentic Plan Caching

#### Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents — Zhang et al. (arXiv:2506.14852, Jun 2025) [NeurIPS 2025]
- **Source:** [arXiv:2506.14852](https://arxiv.org/abs/2506.14852)
- **Method:** Extract structured plan templates จาก agent executions ที่เสร็จแล้ว → เก็บใน test-time memory → keyword extraction match new requests กับ cached plans → lightweight model adapt template ให้ fit task context ใหม่; ต่างจาก semantic caching ทั่วไปตรงที่ cache plan structure ไม่ใช่ response
- **Key finding:** ลด cost 50.31% + latency 27.28% บน real-world agent applications โดย performance ไม่ตก; plan template reuse ทำงานได้แม้ task input เปลี่ยนถ้า structure เหมือนกัน
- **Dataset:** Multiple real-world agent applications
- **Apply to project:** /pre-market รัน workflow เดิมทุกวัน (Step 0-6: load rules → fetch data → cognitive layers → scenarios → setups) — plan structure ไม่เปลี่ยน, เฉพาะ data ที่เปลี่ยน; implement plan cache ใน `vault/Knowledge/pre-market-plan-template.md`: เก็บ plan skeleton → session ใหม่ load template → fill data แทน re-plan ทั้งหมด; เช่นเดียวกับ /nick-weekly และ /healthcheck
- **Tag:** IMPLEMENT

---

### Theme 10: Dynamic Agent Elimination

#### AgentDropout: Dynamic Agent Elimination for Token-Efficient Multi-Agent Collaboration — Wang et al. (arXiv:2503.18891, Mar 2025) [ACL 2025]
- **Source:** [arXiv:2503.18891](https://arxiv.org/abs/2503.18891) | [GitHub](https://github.com/wangzx1219/AgentDropout)
- **Method:** ระบุ redundant agents และ communication links โดย optimize adjacency matrices ของ communication graph → eliminate ทั้ง agents และ links ที่ไม่ contribute ระหว่าง rounds; inspired by management theory — roles ใน efficient teams ถูก adjust แบบ dynamic
- **Key finding:** ลด prompt tokens 21.6% + completion tokens 18.4% โดย performance ดีขึ้น +1.14 pts เทียบกับ SOTA; dynamic adjustment ดีกว่า static agent pruning เพราะ contribution ของ agent เปลี่ยนตาม round
- **Dataset:** Multi-agent collaboration benchmarks (ACL 2025)
- **Apply to project:** /council Phase 3 critiques: ถ้า proposer ใดให้ critique ที่ overlap กับ proposer อื่น >80% → synthesizer สามารถ drop critique นั้น ไม่ให้ synthesizer re-process; หรือ detect ถ้า 2 proposers เห็นด้วยกัน → count as 1 voice ไม่ใช่ 2; ลด synthesizer input token โดยไม่เสียมุมมอง
- **Tag:** IMPLEMENT

#### AgentDropoutV2: Optimizing Information Flow via Test-Time Rectify-or-Reject Pruning — (arXiv:2602.23258, Feb 2026)
- **Source:** [arXiv:2602.23258](https://arxiv.org/html/2602.23258)
- **Method:** Test-time pruning ที่ไม่ต้องการ training — ประเมิน information flow ระหว่าง agents แล้วตัดสินใจ rectify (ปรับ) หรือ reject (ตัด) แต่ละ communication ณ inference time
- **Key finding:** ปรับปรุงจาก V1 ด้วย test-time approach ที่ไม่ต้อง fine-tune model — ใช้ได้กับ closed-source models รวมถึง Claude
- **Dataset:** Multi-agent benchmarks
- **Apply to project:** เพิ่มเป็น post-critique filter ใน /council: synthesizer scan critiques ก่อน synthesis — ถ้า critique ไหน paraphrase critique อื่น → reject ก่อน process; ลด noise ใน synthesis โดยไม่กระทบ diverse perspectives
- **Tag:** REFERENCE

---

### Theme 11: Efficient Reasoning Token Reduction

#### Thinking with Reasoning Skills: Fewer Tokens, More Accuracy — Zhao, Shi et al. (arXiv:2604.21764, Apr 2026)
- **Source:** [arXiv:2604.21764](https://arxiv.org/abs/2604.21764)
- **Method:** Summarize และ store reusable reasoning skills จาก prior deliberation → retrieve relevant skills at inference time เพื่อ guide future reasoning; แทนที่ "reasoning from scratch" — model recall skills ก่อน แล้ว reason โดยไม่ต้อง re-derive ทุกขั้น; ต่างจาก Metacognitive Reuse (A8) ตรงที่ focus บน skill retrieval ไม่ใช่ procedure compression
- **Key finding:** ลด reasoning tokens อย่างมีนัยสำคัญ + accuracy ดีขึ้นบน coding และ math reasoning; lower per-request cost ใน production deployment
- **Dataset:** Coding + math reasoning benchmarks
- **Apply to project:** Cognitive layer analysis ใน /pre-market เป็น reasoning tasks ที่ทำซ้ำทุกวัน — store "reasoning skills" เช่น "how to interpret VIX-Rank → position size multiplier" เป็น skill entry; ก่อน analyze → load relevant skills → reason จาก skill แทน re-derive; ร่วมกับ pre-market-behaviors.md เป็น 2-layer efficiency: behaviors = procedure; skills = reasoning shortcut
- **Tag:** IMPLEMENT

#### ACON: Optimizing Context Compression for Long-Horizon LLM Agents — Kang et al. (arXiv:2510.00615, Oct 2025)
- **Source:** [arXiv:2510.00615](https://arxiv.org/abs/2510.00615)
- **Method:** Compression guideline optimization ใน natural language space — เมื่อ compressed context fail แต่ full context succeed → LLM วิเคราะห์สาเหตุ → update compression guideline; gradient-free, ใช้กับ closed-source models; distill compressor ลงใน smaller model ได้ (95% accuracy preserved)
- **Key finding:** ลด peak tokens 26-54% โดย task performance ไม่ตก; เพิ่ม performance ของ small LMs: AppWorld +32%, OfficeBench +20%, Multi-objective QA +46%; ทำงานได้โดยไม่ต้อง parameter update
- **Dataset:** AppWorld, OfficeBench, Multi-objective QA
- **Apply to project:** เมื่อ session ยาว (>70% context) → ใช้ ACON principle: หา failure modes ของ prior compression attempts → update guideline ว่า section ไหน "unsafe to compress" (เช่น kill conditions, exact prices, TRADING_RULES) และ section ไหน compressible (เช่น narrative explanation, repeated headers); เก็บ guideline ใน `vault/Knowledge/compression-guidelines.md` → โหลดก่อน compress
- **Tag:** IMPLEMENT

#### Extra-CoT: Towards Efficient Reasoning via Extreme-Ratio Chain-of-Thought Compression — (arXiv:2602.08324, Feb 2026)
- **Source:** [arXiv:2602.08324](https://arxiv.org/abs/2602.08324)
- **Method:** Train dedicated semantically-preserved compressor บน mathematical CoT data ด้วย fine-grained annotations → compress reasoning trace อย่าง aggressive โดยไม่เสีย logical fidelity; CHRPO (Constrained and Hierarchical Ratio Policy Optimization)
- **Key finding:** บน MATH-500 + Qwen3-1.7B: ลด token >73% โดย accuracy ดีขึ้น +0.6%
- **Dataset:** MATH-500
- **Apply to project:** ต้องการ fine-tuning — ไม่ implement ตรง ใน Claude Code; แต่ principle "semantically-preserved compression" ใช้ inform ว่าเมื่อ compress cognitive layer output ต้องเก็บ logical fidelity — ไม่ตัดจุดที่เป็น causal link ของ conclusion
- **Tag:** REFERENCE

---

### Theme 12: Semantic Caching

#### vCache: Verified Semantic Prompt Caching — (arXiv:2502.03771, Feb 2025)
- **Source:** [arXiv:2502.03771](https://arxiv.org/abs/2502.03771)
- **Method:** Semantic cache ที่ embed cached prompts + store ใน vector database; ต่างจาก naive semantic cache ตรงที่มี verified error rate guarantees ผ่าน online learning algorithm ที่ estimate optimal similarity threshold ต่อ cached prompt; แก้ปัญหา "similarity grey zone" ที่ embedding geometry แยก paraphrase จาก distinct intent ไม่ได้
- **Key finding:** First verified semantic cache ที่มี user-defined error rate guarantees — predictable performance ไม่ใช่ probabilistic; ลด LLM inference latency และ cost สำหรับ repeated similar queries
- **Dataset:** QA + LLM inference benchmarks
- **Apply to project:** /pre-market fetches ข้อมูลคล้ายกันทุกวัน (เช่น "NVDA price today", "VIX level today") — semantic cache จะ return cached answer ถ้า query คล้ายพอ; ต้องการ vector database infrastructure (Redis / Chroma) — complexity: high; ดีกว่าใช้ plan cache (Theme 9) ในระยะสั้น; พิจารณา implement ถ้า query repetition สูงพอ (>50% similar queries per session)
- **Tag:** REFERENCE

---

### Implementation Roadmap — เพิ่มเติม (2026-05-18 รอบ 2)

12. **Pre-market plan template cache (Agentic Plan Caching)** → สร้าง `vault/Knowledge/pre-market-plan-template.md`: skeleton plan พร้อม placeholder slots สำหรับ data → load ต้น session แทน re-plan ทุกรอบ → complexity: **low** (สร้างไฟล์ใหม่ + 1 บรรทัดใน pre-market.md)

13. **Council duplicate critique filter (AgentDropout principle)** → ใน Phase 4 synthesis: synthesizer scan critiques ก่อน — mark critiques ที่ overlap >80% → process เพียง 1 ไม่ทั้งคู่ → ลด synthesizer input → complexity: **low** (เพิ่ม instruction ใน council.md Phase 4)

14. **Reasoning skills vault (Thinking with Reasoning Skills)** → สร้าง `vault/Knowledge/pre-market-reasoning-skills.md`: reusable reasoning patterns (เช่น VIX-Rank → size, Brent>$95 → XLE) → load พร้อม behaviors.md → complexity: **low** (สร้างไฟล์ใหม่)

15. **Compression guidelines (ACON)** → สร้าง `vault/Knowledge/compression-guidelines.md`: ระบุ section ที่ compress ได้ vs ห้าม compress → load ก่อน /condense หรือ agent summary → complexity: **low** (สร้างไฟล์ใหม่)

---

### Gaps — อัพเดต (2026-05-18 รอบ 2)

- **vCache infrastructure** — ต้องการ vector database; ใช้ plan cache (Theme 9) แทนในระยะสั้น
- **Extra-CoT training** — ต้องการ fine-tune; ใช้ principle เป็น compression heuristic แทน
- **AgentDropout adjacency matrix** — ต้องการ communication graph formalism; ใน LTD-OS ทำได้แค่ post-hoc duplicate detection ไม่ใช่ predictive elimination

---

*Appendix scope: 4 themes | Searches: 9/9 | Papers: 7 — 4 IMPLEMENT, 3 REFERENCE | Total survey: 12 themes, 26 papers — 15 IMPLEMENT, 11 REFERENCE*

---

## Appendix — 2026-05-17 รอบ 3

*4 themes ใหม่: output budget control, conversation history restructuring, LLM routing, token pruning MDP | 10 searches | 6 papers (2 IMPLEMENT, 4 REFERENCE)*

---

### Theme 13: Output Budget Control

#### SelfBudgeter: Adaptive Token Allocation for Efficient LLM Reasoning — Zheng Li et al. (arXiv:2505.11274, May 2025)
- **Source:** [arXiv:2505.11274](https://arxiv.org/abs/2505.11274)
- **Method:** Model ประเมิน reasoning budget ที่ต้องการก่อน generate จริง จากนั้นใช้ GRPO RL training ให้ปรับ output ตาม self-declared budget; หลัก: "preview scope before generating"
- **Key finding:** −61% average response length on math reasoning tasks โดย accuracy คงเดิม; user preset token limits → model adapts depth accordingly
- **Dataset:** Math reasoning benchmarks (MATH, GSM8K)
- **Apply to project:** Prompt-level implementation ไม่ต้องการ training: ก่อน generate ทุก /council proposer + /pre-market cognitive layer → declare output scope ("I will cover X in N sentences"); ถ้า declare แล้วเกิน = forced cut; ลด verbose proposal output ใน /council ได้ทันที
- **Tag:** IMPLEMENT

#### Precise Length Control in Large Language Models — Bradley Butcher et al. (arXiv:2412.11937, Dec 2024)
- **Source:** [arXiv:2412.11937](https://arxiv.org/abs/2412.11937)
- **Method:** Length-Difference Positional Encoding (LDPE) — secondary positional encoding ที่ count down ถึง target length; แก้ปัญหา hard termination โดยไม่เสียคุณภาพ
- **Key finding:** Mean token error < 3 tokens จาก target length; quality maintained on QA + summarization
- **Apply to project:** Model-level modification ไม่ applicable กับ Claude API; takeaway: add explicit word-count ceiling ใน agent role definitions ใน council.md ("max 300 words per proposal section")
- **Tag:** REFERENCE

---

### Theme 14: Conversation History Restructuring

#### A Simple Yet Strong Baseline for Long-Term Conversational Memory — Sizhe Zhou, Jiawei Han (arXiv:2511.17208, Nov 2025)
- **Source:** [arXiv:2511.17208](https://arxiv.org/abs/2511.17208)
- **Method:** Decompose conversation turns เป็น Elementary Discourse Units (EDUs) — self-contained statements + normalized entity + source-turn attribution; organize เป็น heterogeneous graph; retrieve via dense similarity search + LLM filter แทน keep ทั้ง history ใน context
- **Key finding:** Matches/exceeds baselines บน LoCoMo + LongMemEval_S benchmarks ด้วย "much shorter QA contexts"; non-compressive: preserve information แต่ restructure ไม่ใช่ lose
- **Dataset:** LoCoMo (long-term conversation), LongMemEval_S
- **Apply to project:** Claude Code sessions ที่รัน 1+ ชั่วโมง (many tool calls): แทนที่จะ keep raw tool call outputs ใน context → restructure แต่ละ tool result เป็น EDU ("Read TRADING_RULES.md turn 12: position_size = VIX×HSP×PTSD×TACHY"); EDU concept ตรงกับ insight-atoms/ pattern ที่มีอยู่แล้ว — extend ไป tool outputs ด้วย; ทำใน compression-guidelines.md (session >70% context)
- **Tag:** IMPLEMENT

---

### Theme 15: LLM Routing / Model Cascade

#### Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey — Yasmin Moslem, John D. Kelleher (arXiv:2603.04445, Mar 2026)
- **Source:** [arXiv:2603.04445](https://arxiv.org/abs/2603.04445)
- **Method:** Survey ของ routing paradigms: query difficulty assessment, preference-based, uncertainty quantification, RL-based; 3-dimension framework: (1) when decision made, (2) what info used, (3) how computed
- **Key finding:** Well-designed routing "outperforms even the most powerful individual models"; quality estimator accuracy = critical bottleneck
- **Apply to project:** ใช้กับ Python scripts ที่เรียก Anthropic API โดยตรง (nick-score.py, universe-screen.py): route simple lookups → Haiku; complex synthesis → Sonnet; ไม่ applicable กับ Claude Code CLI sessions (fixed model per session)
- **Tag:** REFERENCE (applicable to code/ scripts, not interactive Claude Code sessions)

#### A Unified Approach to Routing and Cascading for LLMs — Jasper Dekoninck et al. (arXiv:2410.10347, Oct 2024)
- **Source:** [arXiv:2410.10347](https://arxiv.org/abs/2410.10347)
- **Method:** Derives theoretically optimal cascade routing — unifies routing (one model per query) + cascading (try small → escalate if uncertain); proves both are special cases of one framework
- **Key finding:** Cascade routing outperforms individual routing/cascading "by a large margin"; confidence calibration = binding constraint
- **Apply to project:** Cascade pattern for Anthropic API scripts: first call Haiku → check output confidence heuristic → escalate to Sonnet if uncertain; could halve API costs on routine script runs (vault lookups, screening)
- **Tag:** REFERENCE

---

### Theme 1 Extension: Token Pruning via RL/MDP

#### Dynamic Compressing Prompts for Efficient LLM Inference — Jinwu Hu et al. (arXiv:2504.11004, Apr 2025)
- **Source:** [arXiv:2504.11004](https://arxiv.org/abs/2504.11004)
- **Method:** Frames token pruning เป็น Markov Decision Process — RL agent sequentially removes redundant tokens โดย adapt ต่อ dynamic context; Hierarchical Prompt Compression ใช้ curriculum learning (easy compressions ก่อน, hard หลัง); ไม่ต้องการ external LLM เป็น scorer
- **Key finding:** Outperforms SOTA LLMLingua-style methods ที่ high compression ratios; no external LLM overhead; ยังไม่มี published exact % (paper under review Apr 2025)
- **Apply to project:** MDP framing ให้ theoretical basis สำหรับ existing observation masking policy: identify load-bearing tokens (kill conditions, exact figures, causal connectives) vs. skippable (narrative headers, boilerplate) — ใช้เป็น principled upgrade ของ UNSAFE/SAFE table ใน compression-guidelines.md; ไม่ต้อง implement RL agent — ใช้ principle เป็น heuristic
- **Tag:** REFERENCE (no published numbers; await publication before implementing)

---

### Implementation Roadmap — เพิ่มเติม (2026-05-17 รอบ 3)

16. **Output budget declaration (SelfBudgeter)** → เพิ่มใน /council proposer instructions: ก่อน generate ต้อง state "Proposal will cover [X] in max [N] words" → complexity: **low** (เพิ่ม instruction ใน council.md)

17. **EDU restructuring ใน compression-guidelines.md** → เมื่อ session context >70%: แทน raw tool call outputs ด้วย attributed EDU format ("Read [file] turn [N]: [key fact]") → ตัด verbose context โดยไม่เสีย traceability → complexity: **low** (update compression-guidelines.md)

---

### Gaps — อัพเดต (2026-05-17 รอบ 3)

- **LLM Routing** — applicable เฉพาะ Anthropic API scripts (code/ python), ไม่ใช่ Claude Code CLI sessions ที่ fixed model per session
- **Token pruning MDP (arXiv:2504.11004)** — ยังไม่มี published benchmark numbers; ใช้ principle เป็น heuristic ก่อน
- **TRIM two-stage pipeline** — ต้องการ second LM สำหรับ reconstruction; ไม่ applicable กับ LTD-OS setup

---

*Appendix รอบ 3 scope: 4 new themes | Searches: 10 | Papers: 6 — 2 IMPLEMENT, 4 REFERENCE | Total survey: 15 themes, 32 papers — 17 IMPLEMENT, 15 REFERENCE*

---

## Appendix — 2026-05-17: Gap Search รอบ 4 (KV Cache / ICL Selection / Trajectory / Speculative / Chunking)

*Context: Gap search covering 5 areas not in prior themes. 5 searches → 2 IMPLEMENT, 2 REFERENCE, 5 SKIP (3 infrastructure-only). 2 entire gap categories confirmed not actionable for API-based deployments.*

---

### Theme 16: Agentic Trajectory Pruning

#### Reducing Cost of LLM Agents with Trajectory Reduction (AgentDiet) — Xiao, Gao, Peng, Yingfei Xiong (arXiv:2509.23586, Sep 2025)
- **Source:** [arXiv:2509.23586](https://arxiv.org/abs/2509.23586)
- **Venue:** arXiv preprint Tier D → code available + strong results → effective Tier C
- **Citations:** [unverified — paper Sep 2025]
- **Code:** Not linked, but method is workflow-level (no custom model needed)
- **Critics:** [no known critics ✓]
- **Method:** Automatically identifies and removes "useless, redundant, and expired" information from agent trajectories at inference time — targeting accumulated tool outputs and assistant messages that accumulate across multi-step agentic loops; strips expired context after each agent handoff
- **Key finding:** −39.9% to −59.7% input tokens; −21.1% to −35.9% total compute cost; no performance loss on software engineering benchmarks
- **Apply to project:** ตรงกับ `/stock-content` pipeline pain point — Researcher → Reese → Chris → Vera → Indie แต่ละขั้นอ่าน transcript ของขั้นก่อน ซึ่งรวม raw web search results ที่ "expired" แล้วหลัง Reese synthesis; principle: หลัง handoff แต่ละ stage ให้ drop raw intermediate tool results, keep structured output เท่านั้น — เพิ่มใน stock-content.md เป็น workflow rule
- **Tag:** IMPLEMENT

---

### Theme 17: Chunk-Sequential Long Document Processing

#### MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent — Yu, Chen, Feng et al., Microsoft/Tsinghua (arXiv:2507.02259, 2025)
- **Source:** [arXiv:2507.02259](https://arxiv.org/abs/2507.02259)
- **Venue:** arXiv preprint Tier D → Microsoft Research + strong numbers → effective Tier C
- **Citations:** [unverified — 2025]
- **Code:** [not linked publicly yet]
- **Critics:** [no known critics ✓]
- **Method:** RL-trained memory agent reads text in fixed-size chunks sequentially; after each chunk updates a fixed-length memory via overwrite strategy; total compute per chunk stays O(1) linear in number of chunks — extrapolates to 3.5M token inputs trained at 32K
- **Key finding:** 95%+ accuracy on 512K RULER benchmark; extrapolates to 3.5M token QA tasks with <5% degradation; strict linear complexity eliminates quadratic attention blowup
- **Apply to project:** Applies to `/stock-content` long earnings transcripts and `_assets/` PDFs — อ่าน full doc เข้า context แบบ monolithic เป็น bottleneck; principle: ใช้ Read tool ด้วย offset+limit อ่านเป็น chunks + rolling fixed-length summary accumulator แทน; เป็น extension ของ partial-read policy ใน CLAUDE.md §7 จาก single-file reads → sequential multi-chunk reads
- **Tag:** IMPLEMENT

#### When Does Divide and Conquer Work for Long Context LLMs? — (arXiv:2506.16411, 2025)
- **Source:** [arXiv:2506.16411](https://arxiv.org/abs/2506.16411)
- **Venue:** arXiv preprint Tier D
- **Citations:** [unverified]
- **Code:** [none]
- **Critics:** [no known critics ✓]
- **Method:** Noise decomposition framework analyzing when divide-and-conquer (chunking) helps vs hurts for long-context tasks; identifies task types where chunking is beneficial vs harmful based on signal locality vs cross-chunk dependency
- **Key finding:** Chunking works best when signal is locally concentrated and noise distributed; fails when cross-chunk dependencies are high; provides decision criteria for when to chunk vs load full context
- **Apply to project:** Decision rule ที่ขาดสำหรับ MemAgent — บอกว่า WHEN ควร chunk: earnings transcripts (chunk by quarter, local signal ✓) vs /council debate (cross-agent reasoning dependencies สูง → ไม่ควร chunk ✗)
- **Tag:** REFERENCE

---

### Theme 18: In-Context Learning Example Selection

#### Sample Efficient Demonstration Selection for In-Context Learning (CASE) — Purohit, Venktesh, Bhattacharya, Anand (arXiv:2506.08607, 2025)
- **Source:** [arXiv:2506.08607](https://arxiv.org/abs/2506.08607)
- **Venue:** arXiv preprint Tier D
- **Citations:** [unverified]
- **Code:** [not linked]
- **Critics:** [no known critics ✓]
- **Method:** Formulates few-shot example selection เป็น stochastic linear bandit problem (top-m bandit); maintains challenger shortlist ลด full LLM evaluations ที่จำเป็นสำหรับ finding best demonstrations
- **Key finding:** 7x speedup in runtime; 87% fewer LLM calls for exemplar selection setup; no performance degradation vs exhaustive search
- **Apply to project:** Principle: ใน `/council` และ `/pre-market` prompt construction — แทนที่จะ load OUTCOMES.md ทั้งหมดเพื่อหา relevant examples ให้ใช้ challenger shortlist heuristic: score examples by query similarity → keep top 3 → ลด few-shot token block; ไม่ต้องการ bandit algorithm เต็มรูปแบบ — ใช้เป็น heuristic ใน CLAUDE.md §8 task-scoped loading
- **Tag:** REFERENCE

---

### Confirmed NOT ACTIONABLE for API-based deployments

**KV Cache Compression (tensor-level):** KVComp (arXiv:2509.00579), KV Cache Compression Survey (arXiv:2508.06297) — ทำงานที่ CUDA/GPU memory layer; Anthropic manages KV cache server-side; ไม่มี user-accessible lever ผ่าน API; revisit ถ้า LTD-OS ย้ายไป local inference

**Speculative Decoding:** Speculative Verification (arXiv:2509.24328, ACL 2026) — server-side inference optimization; ไม่ configurable ผ่าน Anthropic API; Anthropic อาจใช้อยู่แล้ว internally

→ อย่า search gap categories เหล่านี้อีก — confirmed infrastructure-only สำหรับ API users

---

### Implementation Roadmap — เพิ่มเติม (2026-05-17 รอบ 4)

18. **Trajectory pruning discipline in /stock-content (AgentDiet)** → หลัง Researcher handoff ให้ Reese: drop raw web search results, keep structured A-E sections เท่านั้น → complexity: **low** (เพิ่ม workflow rule ใน stock-content.md)

19. **Chunk-sequential read สำหรับ long PDFs (MemAgent principle)** → เพิ่มใน CLAUDE.md §7: "PDF > 30 pages → อ่านเป็น chunks ด้วย offset+limit + rolling summary accumulator; อย่า load ทั้งไฟล์" → complexity: **low** (update CLAUDE.md policy)

### Gaps — อัพเดต (2026-05-17 รอบ 4)

- **KV cache compression** — confirmed not actionable via Anthropic API; infrastructure-only
- **Speculative decoding** — confirmed not actionable; server-side inference layer
- **Dynamic Tool Dependency Retrieval (arXiv:2512.17052)** — appeared in search but not fetched; may reduce tool schema token overhead; optional follow-up
- **Coding Agents as Long-Context Processors (arXiv:2603.20432)** — appeared in search but not fetched; may have chunk strategy insights for code-agent context; optional follow-up

---

*Appendix รอบ 4 scope: 3 new themes, 2 confirmed-not-actionable categories | Searches: 5 | Papers: 4 active — 2 IMPLEMENT, 2 REFERENCE | Total survey: 18 themes, 36 papers — 19 IMPLEMENT, 17 REFERENCE*

---

## Appendix — 2026-05-17: Gap Fill รอบ 5 (Tool Selection / File-System Nav / Structured Output / Meta-tools / Session Serialization / Prefix Homogeneity)

*Context: 6 gap areas targeted — 2 explicitly flagged from round 4 (arXiv:2512.17052, 2603.20432) + 4 new areas. 6 searches → 6 IMPLEMENT. ทุก paper เป็น Tier D (arXiv preprint) — treat numerical claims as preliminary.*

---

### Theme 19: Dynamic Tool Dependency Retrieval

#### Dynamic Tool Dependency Retrieval for Lightweight Function Calling — Patel, Belli, Jalalirad et al. (arXiv:2512.17052, Dec 2025)
- **Source:** [arXiv:2512.17052](https://arxiv.org/abs/2512.17052)
- **Venue:** arXiv preprint Tier D
- **Citations:** [unverified — Dec 2025]
- **Code:** [not linked]
- **Critics:** [no known critics ✓]
- **Method:** Conditions tool retrieval บน user query AND evolving sequence ของ prior tool calls — learns tool dependency patterns จาก demonstrations เพื่อ adaptive tool selection ที่แต่ละ step แทนที่ static selection ตั้งแต่ต้น
- **Key finding:** 23–104% improvement in function-calling success rate vs static retrievers; maintains computational efficiency
- **Apply to project:** `/stock-content` pipeline ใช้ tool sequence ที่ static — DTDR insight: tool selection ที่ step N ควร conditioned บน steps 1..N-1; ถ้า Reese พบ contradiction flag → next step ควร weight "contradiction-registry lookup" สูงกว่า; ใช้เป็น CLAUDE.md policy: "ใน multi-step pipeline ให้ pass prior tool call outcomes เป็น context ก่อน select tool ถัดไป"
- **Tag:** IMPLEMENT

---

### Theme 20: Agent-as-File-System-Navigator

#### Coding Agents are Effective Long-Context Processors — Cao, Yin, Dhingra, Zhou (arXiv:2603.20432, Mar 2026)
- **Source:** [arXiv:2603.20432](https://arxiv.org/abs/2603.20432)
- **Venue:** arXiv preprint Tier D
- **Citations:** [unverified — Mar 2026]
- **Code:** [not linked]
- **Critics:** [no known critics ✓]
- **Method:** Externalizes long-document processing ไปยัง coding agent ที่จัด text ใน file system และใช้ native tools (grep, sed, file I/O) ดึงเฉพาะ slices ที่ต้องการ — LLM ไม่ hold full corpus ใน context เลย
- **Key finding:** +17.3% เหนือ SOTA บน long-context benchmarks; processed contexts ถึง 3 trillion tokens; critical factors: native tool proficiency + file system familiarity
- **Apply to project:** vault IS a file system — เมื่อ /council หรือ /nick-weekly ต้องการ vault-wide synthesis (THESIS_TRACKER + INDEX_insights + multiple atoms) → ใช้ targeted grep/glob tool calls isolate relevant spans แทน bulk-load หลายไฟล์เข้า context; เป็น principled upgrade ของ CLAUDE.md §7 จาก partial reads → "agent-as-file-system-navigator" pattern
- **Tag:** IMPLEMENT

---

### Theme 21: Constrained Output for Token Reduction

#### XGrammar-2: Efficient Dynamic Structured Generation Engine for Agentic LLMs — (arXiv:2601.04426, 2025/2026) [source-unverified: authors not confirmed]
- **Source:** [arXiv:2601.04426](https://arxiv.org/abs/2601.04426)
- **Venue:** arXiv preprint Tier D
- **Citations:** [unverified]
- **Code:** Default backend for vLLM, SGLang, TensorRT-LLM as of Mar 2026
- **Critics:** [no known critics ✓]
- **Method:** Treats tool-name selection เป็น grammar constraint — เมื่อ tool name token ถูกเลือก JSON schema ของ arguments enforce อัตโนมัติ, ตัด extraneous free-text ระหว่าง tool calls; context-independent tokens (99% ของ vocabulary) precomputed เป็น bitmask tables; <40 microseconds overhead per token
- **Key finding:** Up to 100x speedup vs traditional grammar-constrained methods; near-zero overhead; indirect token reduction โดยป้องกัน verbose reasoning ที่ bleeding เข้า tool arguments
- **Apply to project:** Anthropic API รองรับ `tool_choice: {"type": "any"}` — บังคับ model ให้ call tool แทน free-text response; eliminate verbose preamble บน tool-only agent steps; applicable ทันทีสำหรับ Vera (fact-flagging), Indie (atom extraction), /paper-trade (structured order fields) ใน Python scripts
- **Tag:** IMPLEMENT

---

### Theme 22: Tool Call Meta-Bundling

#### Optimizing Agentic Workflows using Meta-tools — Abuzakuk, Kermarrec, Sharma et al. (arXiv:2601.22037, Jan 2026)
- **Source:** [arXiv:2601.22037](https://arxiv.org/abs/2601.22037)
- **Venue:** arXiv preprint Tier D
- **Citations:** [unverified — Jan 2026]
- **Code:** [not linked]
- **Critics:** [no known critics ✓]
- **Method:** Agent Workflow Optimization (AWO) mines execution traces หา recurring multi-step tool call sequences แล้ว collapse เป็น "meta-tools" — deterministic composite tools ที่ execute bundle ใน 1 LLM invocation โดย bypass intermediate reasoning steps
- **Key finding:** LLM calls ลด 11.9%; task success rate ขึ้น 4.2%; ลดทั้ง cost และ latency
- **Apply to project:** `/stock-content` pipeline มี fixed recurring sequence: web_search → Read vault → Write stock note → Read stock note → Write Reese doc; AWO insight: collapse Researcher→stock-note write เป็น single agent call ที่ return structured blob โดยไม่มี intermediate "write then re-read" round-trip; ลด LLM calls ต่อ /stock-content run ลง ~2 calls
- **Tag:** IMPLEMENT

---

### Theme 23: Cross-Session Memory Serialization

#### Memori: A Persistent Memory Layer for Efficient, Context-Aware LLM Agents — Borro, Macarini, Tindall et al. (arXiv:2603.19935, Mar 2026)
- **Source:** [arXiv:2603.19935](https://arxiv.org/abs/2603.19935)
- **Venue:** arXiv white paper Tier D
- **Citations:** [unverified — Mar 2026]
- **Code:** [not linked]
- **Critics:** [no known critics ✓]
- **Method:** Converts raw session history เป็น compact semantic triples (subject, predicate, object) + narrative summary ตอน session end; ตอน session ถัดไป retrieve เฉพาะ relevant triples แทน load full history; LLM-agnostic, API-layer (ไม่ต้องแก้ model)
- **Key finding:** 81.95% accuracy บน LoCoMo benchmark; ~1,294 tokens per query; 67% fewer tokens vs competing approaches; 20x+ cost savings vs full-context loading
- **Apply to project:** `.claude/handoff.md` ปัจจุบันเป็น free-text — ถ้า restructure เป็น semantic triples (decided: X, about: Y, result: Z) + narrative summary section → session resumption ใช้ token น้อยลงมาก; `vault/_memory/OUTCOMES.md` Trading Calibration Log เป็น candidate — structured triples per trade outcome แทน prose
- **Tag:** IMPLEMENT

---

### Theme 24: Prefix Homogeneity for Multi-Agent Cache Efficiency

#### Requests of a Feather Must Flock Together — (arXiv:2605.06046, May 2026)
- **Source:** [arXiv:2605.06046](https://arxiv.org/html/2605.06046v1)
- **Venue:** arXiv preprint Tier D
- **Citations:** [unverified — May 2026]
- **Code:** [not linked]
- **Critics:** [no known critics ✓]
- **Method:** แสดงว่า batching inference requests ที่มี homogeneous (shared) prefixes maximize KV-cache hit rate และ throughput; prefix homogeneity outweighs naive large-batch scheduling
- **Key finding:** Prefix homogeneity เป็น dominant factor ใน cache hit rate — มีผลมากกว่าการเพิ่ม batch size อย่างเดียว
- **Apply to project:** ใน `/council` proposer agents ทั้ง 4 ตัวรับ system prompt เดียวกัน (CLAUDE.md + topic brief) — static prefix ต้องเป็น byte-identical ทั้ง 4 calls; ถ้า format ต่างกันเพียงเล็กน้อย prefix cache break ทันที; rule: agent-specific differentiation ต้องอยู่ใน human turn เท่านั้น ห้ามอยู่ใน static prefix → เป็น text-level complement ของ §9 cache rule ที่มีอยู่แล้ว
- **Tag:** IMPLEMENT

---

### Implementation Roadmap — เพิ่มเติม (2026-05-17 รอบ 5)

20. **DTDR-style tool sequencing rule (arXiv:2512.17052)** → เพิ่มใน CLAUDE.md: "ใน multi-step pipeline pass prior tool outcomes เป็น context ก่อน select tool ถัดไป" → complexity: **low** (CLAUDE.md policy)

21. **Agent-as-file-system-navigator (arXiv:2603.20432)** → upgrade CLAUDE.md §7: vault-wide synthesis tasks ใช้ grep/glob ก่อน load file เสมอ → complexity: **low** (เพิ่มใน §7)

22. **tool_choice: any สำหรับ tool-only steps (arXiv:2601.04426)** → เพิ่มใน Python scripts ที่เรียก API โดยตรง (bubble-risk-monitor.py ฯลฯ) และ note ใน stock-content.md สำหรับ Vera/Indie steps → complexity: **medium** (ต้องแก้ API calls)

23. **Meta-tool collapse ใน /stock-content (arXiv:2601.22037)** → collapse Researcher+stock-note write เป็น single agent call → ลด 2 LLM round-trips → complexity: **medium** (แก้ stock-content.md structure)

24. **Memori-style handoff serialization (arXiv:2603.19935)** → restructure /handoff output เป็น semantic triples + narrative summary แทน free-text → complexity: **medium** (แก้ handoff.md command)

25. **Byte-identical static prefix rule (arXiv:2605.06046)** → เพิ่มใน CLAUDE.md §9: "parallel multi-agent calls ต้องมี byte-identical static prefix; differentiation ใน human turn เท่านั้น" → complexity: **low**

### Gaps — อัพเดต (2026-05-17 รอบ 5)

- **arXiv:2512.17052, arXiv:2603.20432** — ปิดแล้ว (fetched และ filed ในรอบนี้)
- **CodeAgents (arXiv:2507.03254)** — appeared in search; อาจมี text-level prefix sharing evidence เพิ่มเติม; optional follow-up
- **Sutradhara (arXiv:2601.12967)** — tool execution overlap with LLM prefill; infrastructure-layer ส่วนใหญ่ แต่มี orchestration insights; optional follow-up

---

*Appendix รอบ 5 scope: 6 new themes | Searches: 6 | Papers: 6 — 6 IMPLEMENT | Total survey: 24 themes, 42 papers — 25 IMPLEMENT, 17 REFERENCE*
