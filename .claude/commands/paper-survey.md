---
description: หา academic papers มาพัฒนา project — search arXiv/SSRN/Scholar, summarize, จัดกลุ่มตาม theme, แนะนำลำดับ implement. Save to vault/10_research/papers/.
---

# /paper-survey

ค้นหา academic papers ที่เกี่ยวข้องกับ project → summarize → จัดกลุ่มตาม theme → แนะนำว่า implement อะไรก่อน

## Usage

```
/paper-survey <topic> [— context: <project description>]
```

ตัวอย่าง:
- `/paper-survey crypto momentum trading Binance`
- `/paper-survey stock screener factor investing — context: S&P 500 weekly screener ใช้ Alpaca`
- `/paper-survey options volatility forecasting — context: พัฒนา IV model สำหรับ short premium`

---

## Steps

### 1. Parse input

- **Topic** (required): หัวข้อหลักที่ต้องการหา papers
- **Context** (optional, หลัง `—`): project ที่กำลังพัฒนา — ใช้แคบ scope การค้นหาและกำหนด relevance
- ถ้าไม่มี context → ถาม user ก่อน 1 คำถาม: "project นี้ทำอะไรอยู่?" แล้ว proceed

### 2. ตรวจ vault ก่อน

```bash
ls vault/10_research/papers/
grep -ri "<TOPIC_KEYWORDS>" vault/10_research/papers/ --include="*.md" -l
```

- ถ้ามี survey ของ topic นี้แล้ว → ถาม: "มี survey อยู่แล้วที่ `<path>` — อัพเดต หรือสร้างใหม่?"
- ถ้ามี papers บางตัวในโน้ตอื่น → โหลดเป็น context (อย่า re-research)

### 3. Search papers

**Budget: 5 searches max** — เน้น quality over quantity

Run searches ตาม topic และ context เหล่านี้ (ปรับตาม topic จริง):

| Priority | Query pattern |
|---|---|
| 1 (required) | `<topic> arXiv paper <current_year-1> <current_year>` |
| 2 (required) | `<topic> academic research method algorithm` |
| 3 | `<subtopic_1> paper finance trading strategy` |
| 4 | `<subtopic_2> quantitative method empirical` |
| 5 (optional) | `<topic> survey review paper state of the art` |

**แหล่งที่เน้น (priority order):**
1. arXiv.org (cs.AI, q-fin, stat.ML)
2. SSRN (finance/econ papers)
3. Google Scholar / Semantic Scholar
4. Journal of Finance, Journal of Financial Economics, Journal of Portfolio Management

**สำหรับแต่ละ paper ที่พบ ดึงข้อมูล:**
- Title, Authors, Year, Source (arXiv ID หรือ DOI ถ้ามี)
- Method ใน 1-2 ประโยค
- Key finding / contribution
- Dataset ที่ใช้ (crypto, equity, options ฯลฯ) + time period
- ความเกี่ยวข้องกับ project: IMPLEMENT / REFERENCE / SKIP

**Cap: 10 papers ต่อ survey** — ถ้าพบมากกว่านั้น → เลือกที่ relevant ที่สุด ไม่ใช่ครบทุกตัว

**ถ้าต้องการวิเคราะห์ PDF ลึก (> 30 หน้า):**
> แนะนำให้ใช้ NotebookLM — paste summary กลับมาแล้วรัน `/import-notebooklm`

### 4. Organize ตาม theme

จัดกลุ่ม papers เป็น 2-4 themes ตาม project context ตัวอย่าง:
- Signal Generation / Alpha Model
- Risk Management / Position Sizing
- Execution / Market Impact
- Feature Engineering / Data
- Regime Detection / Macro Filter

แต่ละ theme มี 1-4 papers

### 5. Tag แต่ละ paper

| Tag | ความหมาย |
|---|---|
| **IMPLEMENT** | นำไปใช้ได้ทันที — method ชัด, dataset ตรง, complexity พอดี |
| **REFERENCE** | ดีสำหรับ background / ปรับปรุงทีหลัง |
| **SKIP** | relevant น้อย หรือ complexity สูงเกิน project scope |

### 6. Save survey file

Save to: `vault/10_research/papers/<topic-slug>-survey.md`

Slug rule: lowercase, dash-separated, เอา stop words ออก เช่น "crypto momentum trading" → `crypto-momentum-survey.md`

**ถ้าไฟล์มีอยู่แล้ว** → append section ใหม่ด้านล่าง พร้อม date header ไม่ใช่ overwrite

ใช้ template:

```markdown
# Paper Survey — <Topic>
*Project context: <context> | <YYYY-MM-DD> | <N> papers reviewed*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Why |
|---|---|---|
| 1 | [Title] (Year) | [1-line reason] |
| 2 | ... | ... |
| 3 | ... | ... |

---

## Papers by Theme

### <Theme 1>

#### [Paper Title] — Authors (Year)
- **Source:** arXiv:XXXX.XXXXX / SSRN / [Journal]
- **Method:** [1-2 ประโยค — algorithm/approach]
- **Key finding:** [1-2 ประโยค — main result/contribution]
- **Dataset:** [ตลาด, period, frequency]
- **Apply to project:** [concrete ว่าจะ implement ยังไงกับ project นี้]
- **Tag:** IMPLEMENT / REFERENCE / SKIP

#### [Next paper...]
...

### <Theme 2>
...

---

## Implementation Roadmap

ลำดับที่แนะนำให้ implement โดยเรียงจาก impact/complexity:

1. **[Paper short title]** → implement: [อะไร] → estimated complexity: [low/medium/high]
2. ...

---

## Gaps

หัวข้อที่ยังไม่ครอบคลุมโดย papers ที่พบ — search เพิ่มถ้าต้องการ:
- [gap 1]
- [gap 2]

---

*Searches used: N/5 | Papers reviewed: M | Tags: X IMPLEMENT, Y REFERENCE, Z SKIP*
```

### 7. Report back

```
บันทึกแล้ว: vault/10_research/papers/<slug>-survey.md

Papers: <N> รายการ (<X> IMPLEMENT, <Y> REFERENCE, <Z> SKIP)
Top pick: [Paper] — [why]

ขั้นตอนถัดไป:
→ implement [top paper] ใน <project path>
→ รัน /paper-survey <related topic> ถ้าต้องการขยาย coverage

Searches used: N/5
```

---

## Constraints

- **5 searches max** — vault-first เสมอ, อย่า re-search สิ่งที่มีใน vault แล้ว
- **10 papers max per run** — คัดเลือก ไม่ใช่ครบทุกตัว
- **ห้าม fabricate paper** — ถ้าหาไม่เจอ ใส่ `[unverified]` ไม่สร้าง citation ปลอม
- **ห้าม recommend implement โดยไม่มี evidence** — ทุก IMPLEMENT tag ต้องมีเหตุผลชัดว่า apply กับ project ยังไง
- **Note size:** warn ถ้า > 2000 words

## Anti-patterns

- ❌ List paper ให้ครบ 10 ตัวทั้งที่หลายตัว SKIP — เลือก relevant จริงๆ เท่านั้น
- ❌ Summarize ทั้ง paper ทั้ง PDF — abstract + key sections พอ
- ❌ Implementation Roadmap ที่ไม่ผูกกับ project จริง — ต้องอ้างอิง context ที่ user ให้
- ❌ ข้าม Gaps section — ต้องระบุเสมอว่า search ครั้งนี้ไม่ครอบคลุมอะไร
