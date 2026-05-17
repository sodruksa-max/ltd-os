---
description: หา academic papers มาพัฒนา project — search arXiv/SSRN/Scholar/PapersWithCode/OpenReview/HuggingFace + citation check + Connected Papers expansion. Save to vault/10_research/papers/.
---

# /paper-survey

ค้นหา academic papers ที่เกี่ยวข้องกับ project → summarize → จัดกลุ่มตาม theme → แนะนำว่า implement อะไรก่อน

**Search budget ปรับอัตโนมัติตาม scope** — ไม่ต้องเลือก mode

## Usage

```
/paper-survey <topic> [— context: <project description>]
```

ตัวอย่าง:
- `/paper-survey crypto momentum trading — context: btc bot ใช้ Binance ccxt`
- `/paper-survey stock screener factor investing — context: S&P 500 weekly screener ใช้ Alpaca`
- `/paper-survey options volatility forecasting — context: พัฒนา IV model สำหรับ short premium`

---

## Steps

### 1. Parse input

- **Topic** (required): หัวข้อหลักที่ต้องการหา papers
- **Context** (optional, หลัง `—`): project ที่กำลังพัฒนา — ใช้แคบ scope การค้นหาและกำหนด relevance
- ถ้าไม่มี context → ถาม user 1 คำถาม: "project นี้ทำอะไรอยู่?" แล้ว proceed

### 2. ตรวจ vault ก่อน

```bash
ls vault/10_research/papers/
grep -ri "<TOPIC_KEYWORDS>" vault/10_research/papers/ --include="*.md" -l
```

- ถ้ามี survey ของ topic นี้แล้ว → ถาม: "มี survey อยู่แล้วที่ `<path>` — อัพเดต หรือสร้างใหม่?"
- ถ้ามี papers บางตัวในโน้ตอื่น → โหลดเป็น context (อย่า re-research)
- **vault coverage ลด search budget** — theme ที่มีอยู่แล้วในวอลต์ไม่ต้อง search ซ้ำ

### 3. ประเมิน scope → กำหนด search budget อัตโนมัติ

วิเคราะห์ topic + context แล้วนับ **จำนวน distinct technical themes** ที่ project ต้องการ:

| Themes ที่ต้องครอบคลุม | Search budget | Papers target | ตัวอย่าง |
|---|---|---|---|
| 1–2 themes (narrow) | **5 searches** | ~5 papers | "momentum signal สำหรับ crypto" |
| 3–4 themes (typical feature) | **10 searches** | ~10 papers | "btc bot: signal + risk + execution" |
| 5+ themes (full system) | **15 searches** | ~15 papers | "crypto trading system ตั้งแต่ต้นจนจบ" |

**สิ่งที่ช่วยเพิ่ม themes:**
- context บอกว่าเป็น "full project" / "ระบบ" / "bot" → +themes
- topic มีหลาย component เชื่อมกัน (เช่น signal + execution + risk) → +themes
- vault ยังไม่มี coverage เลย → +themes

**สิ่งที่ลด themes:**
- vault มี papers ครอบคลุมบางส่วนอยู่แล้ว → ลด budget ตามสัดส่วน
- topic เป็น technique เดียวที่แคบ (เช่น "Kalman filter เท่านั้น") → ลด

**แจ้ง user ก่อน search:**
> Scope: [N themes] → ใช้ X searches, target ~Y papers
> Themes: [list themes ที่จะครอบคลุม]

แล้วดำเนิน search ต่อเลย ไม่ต้องรอ confirm

### 4. Search papers

แบ่ง search budget ตาม themes — **1-2 searches ต่อ theme หลัก** + 1-2 searches สำหรับ cross-theme / survey papers

**Query patterns (ปรับตาม theme จริง):**

| ประเภท | Query pattern |
|---|---|
| Theme-specific | `<theme> arXiv paper method <year-1> <year>` |
| Cross-asset empirical | `<topic> empirical study equity crypto <year>` |
| Survey / review | `<topic> survey review paper state of the art` |
| Implementation | `<topic> algorithm backtesting performance` |
| Recent advances | `<topic> machine learning deep learning <year>` |

**แหล่งที่เน้น (priority order):**
1. arXiv.org (q-fin.PM, q-fin.ST, cs.LG, stat.ML)
2. SSRN (finance/econ empirical)
3. Google Scholar / Semantic Scholar
4. Journal of Finance, Journal of Portfolio Management, Quantitative Finance
5. **Papers With Code** (paperswithcode.com) — ตรวจว่า paper มี official code repo ไหม; ถ้ามี = IMPLEMENT โอกาสสูง, ถ้าไม่มี = complexity สูงกว่า; query: `<topic> site:paperswithcode.com`
6. **OpenReview** (openreview.net) — NeurIPS/ICLR/ICML papers ที่ยัง under review ก่อน arXiv; จับ papers ใหม่ที่ยังไม่ดัง; query: `<topic> site:openreview.net`
7. **Hugging Face Papers** (huggingface.co/papers) — **เฉพาะ topic ที่เกี่ยวกับ LLM/agent/token/transformer** (auto-detect); trending papers + community upvotes เป็น quality signal ก่อน citations สะสม; query: `<topic> site:huggingface.co/papers`
8. **GitHub** — หา implementation repo, backtesting code, alternative data pipeline ที่คนทำแล้ว (`<topic> site:github.com trading strategy implementation`)
9. **Reddit** — r/algotrading, r/MachineLearning, r/quant: ดู practitioner discussion, paper recommendations จาก community, ข้อจำกัด real-world ที่ paper ไม่พูดถึง (`<topic> site:reddit.com/r/algotrading`)

**Papers With Code check (บังคับสำหรับทุก IMPLEMENT candidate):**
ก่อน tag paper เป็น IMPLEMENT → search `<paper title> paperswithcode` หรือ `<arXiv ID> site:paperswithcode.com`:
- พบ code repo → เพิ่ม `**Code:** [repo URL]` ใน paper entry + confirm IMPLEMENT
- ไม่พบ code → note `[no official code]` — ยัง IMPLEMENT ได้แต่ complexity สูงกว่า

**Citation count check via Semantic Scholar (บังคับสำหรับทุก IMPLEMENT candidate):**
ดึง citation count จาก Semantic Scholar: `<paper title> citations semanticscholar.org` หรือ `api.semanticscholar.org/graph/v1/paper/arXiv:<ID>?fields=citationCount`
- paper อายุ < 6 เดือน → citation count ไม่สำคัญ (ยังไม่มีเวลาสะสม) — ใช้ upvotes/likes จาก HF Papers หรือ community signal แทน
- paper อายุ 6-18 เดือน: citations < 10 → note `[low citations — unvalidated]`; citations ≥ 50 → `[well-cited ✓]`
- paper อายุ > 18 เดือน: citations < 20 → downgrade เป็น REFERENCE ถ้าไม่มีเหตุผลพิเศษ; citations ≥ 100 → `[highly-cited ✓]`
- เพิ่ม `**Citations:** N` ใน paper entry ทุกตัว (ถ้าหาได้)

**Venue quality check (บังคับสำหรับทุก paper):**
ระบุ venue + tier ใน paper entry — tier กำหนด weight ของ claim:

| Tier | Venue | ความหมาย |
|---|---|---|
| A | NeurIPS/ICML/ICLR oral, Nature, Science | peer-reviewed + competitive selection — claim น่าเชื่อมาก |
| B | NeurIPS/ICML/ICLR poster, ACL/EMNLP, AAAI, top journals | peer-reviewed — claim น่าเชื่อ |
| C | Workshop paper, non-top conferences | limited review — verify ก่อน implement |
| D | arXiv preprint (no venue) | ไม่ผ่าน peer review — treat เป็น REFERENCE จนกว่าจะมี citation/code หนุน |

- Tier D paper ที่มี code + citations ≥ 50 → upgrade เป็น Tier C สำหรับ tagging purposes
- Tier A/B = signal แรงพอที่จะ IMPLEMENT โดยไม่ต้องการ code repo
- Tier C/D = ต้องการ code + citations ก่อน IMPLEMENT

**Adversarial check — "ใครพยายาม disprove paper นี้?" (บังคับสำหรับทุก IMPLEMENT candidate):**
search 1 query: `"<method name>" OR "<paper title>" limitation failed replication criticism 2024 2025 2026`
- พบ critic paper ที่ valid (peer-reviewed หรือ well-cited) → note `⚠️ [CRITIC: <title>]` + พิจารณา downgrade เป็น REFERENCE
- พบแค่ blog/opinion → note `[opinion criticism only — not downgraded]`
- ไม่พบ critic → `[no known critics ✓]`
- ใช้ 1 search slot จาก budget; batch หลาย papers เข้า query เดียวได้ถ้า budget ตึง

**สำหรับแต่ละ paper ที่พบ ดึงข้อมูล:**
- Title, Authors, Year, Source (arXiv ID หรือ DOI — บังคับ ห้ามละ)
- Venue: [venue name] Tier [A/B/C/D]
- Citations: N [signal label] (จาก Semantic Scholar)
- Code: [repo URL] / [no official code] (จาก Papers With Code)
- Critics: [no known critics ✓] / [⚠️ CRITIC: title]
- Method ใน 1-2 ประโยค
- Key finding / contribution
- Dataset (ตลาด, period, frequency)
- Apply to project: concrete implementation idea
- Tag: IMPLEMENT / REFERENCE / SKIP

**Paper staleness rule:**
- Year ≥ current_year - 2 → ✅ Recent
- Year = current_year - 3 → ⚠️ AGING — ระบุ "check for follow-up work"
- Year ≤ current_year - 4 → ⚠️ OLDER PAPER — ระบุ "may be superseded; search `<method> <year-1> <year>` ก่อน implement"
- ถ้าหา arXiv ID หรือ DOI ไม่ได้ → mark `[source-unverified]` และ tag เป็น REFERENCE ไม่ใช่ IMPLEMENT

**Connected Papers expansion (optional — รันเมื่อมี seed papers แล้ว):**
ถ้า user ให้ seed paper มา หรือ survey พบ 2+ papers แล้ว → ใช้ Connected Papers (connectedpapers.com) เพื่อหา adjacent work:
- query: `<arXiv ID> connectedpapers` หรือ fetch `https://www.connectedpapers.com/main/<arXiv-ID>/graph`
- จับ papers ที่ cite/cited-by seed แต่ยังไม่อยู่ใน survey — เพิ่มถ้า relevant
- ใช้ 1 search slot จาก budget; ข้ามถ้า budget ตึง (narrow scope)

**ถ้าต้องการวิเคราะห์ PDF ลึก (> 30 หน้า):**
> แนะนำ NotebookLM — paste summary กลับมาแล้วรัน `/import-notebooklm`

### 5. Organize ตาม theme + tag

จัดกลุ่มตาม themes ที่กำหนดไว้ใน Step 3 แต่ละ theme มี 1-4 papers

| Tag | ความหมาย |
|---|---|
| **IMPLEMENT** | นำไปใช้ได้ทันที — method ชัด, dataset ตรง, complexity พอดี |
| **REFERENCE** | ดีสำหรับ background / ปรับปรุงทีหลัง |
| **SKIP** | relevant น้อย หรือ complexity สูงเกิน project scope ปัจจุบัน |

### 6. Save survey file

Save to: `vault/10_research/papers/<topic-slug>-survey.md`

Slug rule: lowercase, dash-separated, เอา stop words ออก
- "crypto momentum trading bot" → `crypto-momentum-survey.md`
- "options volatility forecasting" → `options-vol-survey.md`

**ถ้าไฟล์มีอยู่แล้ว** → append section ใหม่ด้านล่างพร้อม date header ไม่ใช่ overwrite

Template:

```markdown
# Paper Survey — <Topic>
*Project context: <context> | <YYYY-MM-DD> | Scope: <N themes> | <X> searches | <M> papers*

---

## TL;DR — Top Picks (implement first)

| # | Paper | Theme | Why |
|---|---|---|---|
| 1 | [Title] (Year) | [theme] | [1-line reason] |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |

---

## Papers by Theme

### <Theme 1: e.g. Signal Generation>

#### [Paper Title] — Authors (Year)
- **Source:** arXiv:XXXX.XXXXX / SSRN / [Journal]
- **Venue:** [venue] Tier [A/B/C/D]
- **Citations:** N [well-cited ✓ / low citations / unverified] (Semantic Scholar)
- **Code:** [repo URL] / [no official code] (Papers With Code)
- **Critics:** [no known critics ✓] / [⚠️ CRITIC: title]
- **Method:** [1-2 ประโยค]
- **Key finding:** [1-2 ประโยค]
- **Dataset:** [ตลาด, period, frequency]
- **Apply to project:** [concrete implementation idea]
- **Tag:** IMPLEMENT / REFERENCE / SKIP

...

### <Theme 2>
...

---

## Implementation Roadmap

เรียงตาม impact สูง → complexity ต่ำก่อน:

1. **[Paper]** → implement: [อะไร] → complexity: low/medium/high
2. ...

---

## Gaps

หัวข้อที่ยังไม่ครอบคลุม — search เพิ่มถ้าต้องการ:
- [gap 1]
- [gap 2]

---

*Scope: <N themes> | Searches: X/<budget> | Papers: M total — A IMPLEMENT, B REFERENCE, C SKIP*
```

### 7. Report back

```
บันทึกแล้ว: vault/10_research/papers/<slug>-survey.md

Scope: <N themes> | Searches used: X/<budget> | Papers: M (A implement, B reference, C skip)
Top pick: [Paper] — [why implement นี้ก่อน]

Gaps ที่ยังขาด:
- [gap] → รัน /paper-survey <subtopic> ถ้าต้องการครอบคลุม

ขั้นตอนถัดไป:
→ implement [top paper] ใน <project path>
```

---

## Constraints

- **Search budget ตาม scope** — ประเมินก่อน search ทุกครั้ง ไม่ hard-cap ที่ 5
- **ห้าม fabricate paper** — ถ้าหาไม่เจอ ใส่ `[unverified]` ไม่สร้าง citation ปลอม
- **ห้าม recommend implement โดยไม่มี evidence** — ทุก IMPLEMENT tag ต้องอ้างอิง method จาก paper จริง
- **Vault-first เสมอ** — theme ที่มี coverage อยู่แล้วไม่ต้อง search ซ้ำ
- **Note size:** warn ถ้า > 2000 words; ถ้า > 5000 words ให้แยก theme เป็น survey แยกไฟล์

## Anti-patterns

- ❌ ใช้ search budget ตาม default เดิมโดยไม่ประเมิน scope ก่อน
- ❌ List paper ให้ครบทั้งที่หลายตัว SKIP — คัดเลือก relevant จริงๆ เท่านั้น
- ❌ Summarize ทั้ง paper ทั้ง PDF — abstract + key sections พอ
- ❌ Implementation Roadmap ที่ไม่ผูกกับ project จริง
- ❌ ข้าม Gaps section — ต้องระบุเสมอแม้จะบอกว่า "ครอบคลุมแล้ว"
- ❌ รอ confirm scope จาก user — ประเมินแล้วแจ้ง แล้ว search เลย

## Commit

หลัง /review ผ่าน → รัน:
```bash
bash scripts/safe-commit.sh "notes: paper-survey <topic>"
```
