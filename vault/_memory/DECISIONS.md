---
type: memory-index
updated: auto
---

# Locked Decisions

Claude reads this every session. These are decisions already made — **do not re-ask or re-debate** unless user brings them up.

## Rules
- One-line each, add newest on top
- Format: `YYYY-MM-DD — <decision> — reason (optional)`
- If a decision is reversed: move old line to `DECISIONS_REVERSED.md`, add new one here

---

## Architecture / system

- 2026-04-25 — v0.3.9: เพิ่ม /council command + 4 agents (optimist, pragmatist, skeptic, synthesizer) — multi-agent debate สำหรับ decisions ใหญ่ ไม่ตัดสินใจให้ user
- 2026-04-25 — v0.3.8: เพิ่ม vault/_assets/ folder (5 subfolders) + .gitignore template สำหรับ binary exclusion (commented out)
- 2026-04-25 — v0.3.7: เพิ่ม OUTCOMES.md + WORKFLOWS.md + AI_PORTABILITY.md — vault เป็น "AI-portable knowledge base" ใช้ได้ทุก LLM
- 2026-04-25 — v0.3.7: ไม่เก็บ conversation logs ใน vault — privacy + signal-to-noise ต่ำ
- 2026-04-25 — v0.3.6: เพิ่ม /onboard command — ใช้ครั้งเดียวหลัง install เติม PREFERENCES.md แทน manual edit
- 2026-04-25 — v0.3.5: ใช้ Obsidian Smart Connections plugin สำหรับ semantic search แทน build RAG เอง — ประหยัด 1-2 วัน build + $$
- 2026-04-25 — v0.3.5: Full RAG (ChromaDB/sqlite-vec) defer ไว้ รอ trigger 5 ข้อ (vault > 500 notes, Smart Connections recall ตก, etc.)
- 2026-04-25 — v0.3.4: Phase 1 Proactive Automation (daily-brief vault-only) + Phase 2 ถูก defer รอ 2+ อาทิตย์ของ Phase 1 usage
- 2026-04-25 — v0.3.4: ไม่เอา Docker sandbox (veto ครั้งที่ 3) — reasons เดิม
- 2026-04-25 — v0.3.3: coder บังคับ pin version (`==X.Y.Z`) ทุก dependency + `timeout` ทุกการรัน code
- 2026-04-25 — v0.3.3: ไม่เอา Docker sandbox — WSL2 + venv + reviewer + timeout เพียงพอ
- 2026-04-25 — v0.3.2: coder มี self-correction loop (max 5 iterations, hard cap) + detect non-retryable errors
- 2026-04-25 — v0.3.2: dependency management อยู่ใน coder agent (ไม่สร้าง toolmaker แยก)
- 2026-04-25 — v0.3.2: ไม่ install system tools (sudo) auto — report คำสั่งให้ user run เอง
- 2026-04-25 — v0.3.1: เพิ่ม /weekly-learnings (manual) แทน auto-condensation ของ log — ปลอดภัยกว่า
- 2026-04-25 — v0.3.1: reviewer เช็ค header doc บน script ใหม่ (warn ไม่ block) แทนสร้าง librarian agent
- 2026-04-25 — ไม่สร้าง librarian agent — redundant กับ reviewer + executor ที่มีอยู่
- 2026-04-25 — ใช้ WSL2 Ubuntu (ไม่ใช่ Windows native) — tooling compatibility
- 2026-04-25 — Obsidian + git เป็น knowledge base (ไม่ใช่ plain markdown อย่างเดียว)
- 2026-04-25 — 7 agents ceiling (planner/researcher/writer/coder/executor/reviewer/devils_advocate)
- 2026-04-25 — Writer = 1 agent + format param (thread/longform/hook/newsletter) ไม่แยก 3 agents
- 2026-04-25 — ใช้ Claude อย่างเดียวก่อน ไม่ทำ multi-provider fallback ตอนนี้
- 2026-04-25 — ไม่ทำ browser automation NotebookLM (ToS risk)
- 2026-04-25 — ไม่ใช้ local LLM fallback (AMD GPU + quality gap)
- 2026-04-25 — ไม่ใช้ voice input

## Workflow

- 2026-04-28 — self-review bias mitigation: เดือนละครั้งอ่าน /post-market review ตาเปล่า (ไม่ผ่าน Claude) เพื่อ verify logic ไม่ rationalize
- 2026-04-28 — paper trade 2 สัปดาห์ก่อน scale up: ทุก setup ที่ build ต้อง paper trade ก่อน slippage + emotion + execution lag = blind spots
- 2026-04-28 — command iteration freeze หลัง v5: ห้ามแก้ /pre-market 1-2 สัปดาห์ — validate ที่ /weekly-learnings (~4 พ.ค.) ก่อน iterate ต่อ
- 2026-04-28 — /pre-market confidence cap (v5): event risk count → ceiling: 0-1 = ดุลพินิจปกติ, 2 = cap medium, 3+ = cap low — multi-event days = uncertainty compounds, source: 04-28 over-confident verdict
- 2026-04-28 — decision tree merge เข้า /pre-market (v4): 2 prompts/วัน = friction; tree ต้อง derive จาก brief เสมอ → atomic operation
- 2026-04-28 — /post-market แยกจาก /pre-market: รวม = ปรับ prediction ตอนเขียน review = bias; แยก = honest calibration
- 2026-04-28 — council recommendation อยู่ใน /post-market เท่านั้น (ไม่ใช่ /pre-market): post มี reality evidence → specific; pre ไม่มี evidence → generic
- 2026-04-28 — Most Likely Scenario บังคับเลือก 1 ห้าม "ไม่แน่ใจ": hedge = no value; "อะไรจะทำให้ผิด" section รับหน้าที่หลีกเลี่ยง false certainty แทน
- 2026-04-28 — /pre-market แยกจาก /daily-brief: daily-brief = vault-only ทุกวัน light; pre-market = live data fetch เฉพาะวัน trade US heavy; รวม = overload วันที่ไม่ trade
- 2026-04-25 — NotebookLM ย่อย PDF ยาว → copy → /import-notebooklm (manual)
- 2026-04-25 — Git commit ผ่าน safe-commit.sh เท่านั้น (ไม่ commit ตรง)
- 2026-04-25 — Conventional commits (feat/fix/docs/refactor/chore)
- 2026-04-25 — devils_advocate ผ่าน /challenge เท่านั้น (ไม่ auto)
- 2026-04-25 — Condensation = semi-auto (user approve ก่อนทุกครั้ง)

## Style / conventions

- 2026-04-25 — ภาษา: Thai เมื่อ user พิมพ์ Thai, English เมื่อ English. Technical terms ใน English เสมอ
- 2026-04-25 — ไม่ใช้ emoji ถ้า user ไม่ใช้ก่อน
- 2026-04-25 — Writer หลีกเลี่ยง AI-tells ("let's dive in", "in today's fast-paced world", excess em-dashes)
