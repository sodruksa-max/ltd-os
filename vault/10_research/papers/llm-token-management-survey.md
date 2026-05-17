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
