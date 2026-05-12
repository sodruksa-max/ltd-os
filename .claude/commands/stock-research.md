---
description: Deep-dive research on a single stock ticker. Chains researcher → fills stock-research template → saves to vault/20_investment/. Suggests /challenge after.
---

# /stock-research

Invoke researcher agent to gather info on a ticker, fill in `stock-research.md` template, save to vault.

## Usage
- `/stock-research NVDA`
- `/stock-research TSM — focus on foundry competition`

## Language rule

**ตอบเป็นภาษาเดียวกับที่ user พิมพ์** — Thai เมื่อ user พิมพ์ Thai, English เมื่อ English. Technical terms (ticker, EPS, P/E, FCF ฯลฯ) ใช้ภาษาอังกฤษเสมอ. เนื้อหาในไฟล์ที่ save ให้ใช้ภาษาเดียวกับที่ตอบ user.

## Steps

### 1. Parse input

- **Ticker** (required): ตัวพิมพ์ใหญ่ เช่น `ONDS`, `NVDA`
- **Focus angle** (optional): ถ้ามี เช่น `— focus on foundry competition` → ใช้แคบ scope ของ researcher ในขั้น 3 (ไม่ใช่แค่ parse แล้วทิ้ง)

### 2. ตรวจ vault ก่อน

**2a. ตรวจ note เดิมของ ticker:**
```bash
ls vault/20_investment/ | grep -i <TICKER>
```
- ถ้ามี: ถาม user "มี note อยู่แล้วที่ `<path>` — อัปเดต หรือสร้าง version ใหม่?"
- ถ้าไม่มี: ดำเนินต่อ

**2b. ตรวจ KB + sector notes ที่เกี่ยวข้อง:**
```bash
grep -ri "<TICKER>\|<SECTOR_KEYWORD>" vault/Knowledge/ vault/10_research/ vault/20_investment/ --include="*.md" -l
```
ตรวจเป็นลำดับ:
1. `vault/Knowledge/THESIS_TRACKER.md` — TICKER นี้อยู่ใน active thesis ไหม?
2. `vault/Knowledge/INDEX_insights.md` — มี insight atoms เกี่ยวข้องไหม?
3. `vault/Knowledge/contradiction-registry.md` — มี contradiction ที่รู้แล้วไหม?
4. `vault/10_research/` + `vault/20_investment/` — papers และ notes ที่มีอยู่

ถ้าพบ → โหลดเป็น context ก่อนวิจัย (อย่า re-research สิ่งที่มีอยู่แล้ว)

### 3. Invoke researcher

**Budget: 5 web searches max, 10 vault reads max**

**ถ้ามี focus angle** → จำกัด searches ให้อยู่ใน focus นั้น (เช่น focus foundry = ค้นเรื่อง foundry competition เป็นหลัก ไม่ต้องลงลึก segment อื่น)

**Search scope หลัก (ปรับตาม focus ถ้ามี):**

| หัวข้อ | Query ตัวอย่าง |
|---|---|
| ธุรกิจ + segment | `<TICKER> business model revenue segments 2025` |
| 10-K / 10-Q | `<TICKER> 10-K annual report latest` |
| Earnings call | `<TICKER> earnings call transcript latest` |
| Bear case + short thesis | `<TICKER> bear case short thesis risks` |
| Valuation + peers | `<TICKER> valuation P/E EV/EBITDA sector peers` |
| Reddit DD | `<TICKER> site:reddit.com/r/wallstreetbets OR site:reddit.com/r/stocks DD analysis` |
| Reddit bear | `<TICKER> site:reddit.com short thesis bear case` |
| GitHub analysis | `<TICKER> site:github.com analysis financial model` |

**แหล่งข้อมูลเพิ่มเติม (รันควบคู่กับ search หลัก):**
- **Reddit** — r/wallstreetbets, r/stocks, r/SecurityAnalysis, r/investing: ดู retail sentiment, DD ที่คนทำเอง, bear thesis ที่อาจพลาดจาก mainstream
- **GitHub** — หา financial model, DCF spreadsheet, alternative data scraper, หรือ analysis repo ที่คนทำเกี่ยวกับ ticker นั้น
- ถ้า Reddit หรือ GitHub ให้ข้อมูลขัดแย้งกับ mainstream → flag ⚠️ และแสดงทั้งสองมุม

**ข้อมูลที่ต้องดึงมา (ครบทุกข้อ หรือใส่ ❓ verify):**

- Company basics: business model, revenue segments, geography
- ตัวเลขการเงิน: revenue TTM, growth YoY, gross margin, FCF, net debt, P/E, EV/EBITDA
- **Valuation vs. peers:** เทียบกับ sector median + historical range 3 ปี (อย่าแค่รายงานตัวเลขเปล่า)
- **Next earnings date:** วันประกาศผลรอบถัดไป + consensus EPS estimate ถ้ามี
- **Short interest:** % of float ที่ short + เทียบกับ average (สัญญาณ squeeze หรือ smart money)
- **Insider ownership + dilution history:** % insider holding, การซื้อ/ขายหุ้นของ insider ล่าสุด, จำนวนหุ้นที่ออกใหม่ใน 2-3 ปีที่ผ่านมา
- **Management quality:** CEO background, track record ในบริษัทนี้ หรือบริษัทก่อนหน้า, red flags (เช่น ลาออกบ่อย, restatement)
- Competitive position + moat
- Bull case (3 ข้อ)
- Bear case / steelman (3 ข้อ — steelman ไม่ใช่ strawman)
- Key catalysts 6-12 เดือน

### 4. Fill template

- Template: `vault/_templates/stock-research.md`
- Save to: `vault/20_investment/<TICKER>-YYYY-MM-DD.md`
- กรอกทุก section ด้วยข้อมูลจาก researcher
- **ห้ามเขียน Thesis ให้ user** — เว้นไว้ว่างๆ พร้อม note ว่าเป็นของ user
- ใส่ `❓ verify` ทุกที่ที่ไม่มีข้อมูลยืนยัน
- **Kill conditions:** กรอกเงื่อนไขที่ชัดเจน (metric/event) จากข้อมูล bear case + risk — ต้องวัดได้ ไม่ใช่ vague
- **ถ้า TICKER อยู่ใน THESIS_TRACKER:** note thesis link ใน Decision log

### 5. Report back

```
บันทึกแล้ว: vault/20_investment/<TICKER>-YYYY-MM-DD.md

ส่วนที่กรอกแล้ว:
✓ <list ของ section ที่กรอก>
❓ ต้องตรวจสอบเพิ่ม: <list>
❗ เหลือให้คุณกรอกเอง: Thesis, Decision log, Position sizing

ความน่าเชื่อถือของ research: <High / Medium / Low>
— High = ข้อมูลสำคัญครบ sources ตรงกัน
— Medium = ข้อมูลหลักครบ แต่มี ❓ หลายจุด
— Low = หาข้อมูลได้จำกัด (micro-cap / ข่าวน้อย / แหล่งขัดแย้งกัน)

ก่อนตัดสินใจ:
→ เขียน Thesis ในไฟล์ก่อน
→ รัน: /challenge vault/20_investment/<TICKER>-YYYY-MM-DD.md

Researcher ใช้: N searches, M vault reads
```

---

## Constraints

- **ห้ามเขียน thesis ให้ user** — การตัดสินใจลงทุนเป็นของ user เท่านั้น
- **ห้ามแนะนำ buy/sell** — นำเสนอข้อมูล user ตัดสินใจเอง
- **Flag ความขัดแย้ง** — ถ้า P/E หรือตัวเลขอื่นจาก sources ต่างกัน ให้แสดงทั้งสองค่าและ flag ⚠️ CONFLICT
- **ห้ามสร้างตัวเลข** — ถ้าหาไม่ได้ใส่ `❓` ไม่ใช่เดา
- **One ticker per invocation** — เปรียบเทียบหลาย ticker ใช้คำสั่งอื่น
- **ภาษา:** ตาม language rule ด้านบน

## When user asks follow-up questions

หลัง research แล้ว ถ้า user ถามเพิ่ม เช่น "margin เป็นยังไง?" → อ่าน note ที่มีอยู่ก่อน → เพิ่ม section ถ้าจำเป็น → save. ห้าม re-research ทั้งหมดใหม่

## Commit

หลัง /review ผ่าน → รัน:
```bash
bash scripts/safe-commit.sh "notes: stock-research <TICKER>"
```
