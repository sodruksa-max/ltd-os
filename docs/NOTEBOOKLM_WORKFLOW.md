# NotebookLM + Claude Code Workflow

กลยุทธ์: **ใช้ NotebookLM ทำงานหนัก ใช้ Claude Code ทำงานฉลาด**

---

## ทำไม split แบบนี้

| เครื่องมือ | เก่งอะไร | ราคา |
|---|---|---|
| NotebookLM | ย่อย PDF ยาว, multi-source Q&A, audio overview | ฟรี (tier ใจดี) |
| Claude Code | เข้าใจ vault คุณ, ทำ coding, เขียน content, synthesize ข้าม note | จ่ายต่อ token |

**กฎง่ายๆ**: ถ้า input เป็น PDF/audio/video ยาว → NotebookLM ก่อน แล้วค่อย import เข้า vault ผ่าน Claude

---

## Workflow ใช้งานจริง

### Case 1: อ่าน paper ใหม่

```
1. ไปที่ NotebookLM → สร้าง notebook ใหม่ → upload PDF
2. ถาม NotebookLM: "สรุป paper นี้, key points, methodology, limitations"
3. Copy output ทั้งหมด
4. ใน Claude Code terminal: /import-notebooklm
5. Claude ถามว่า source คืออะไร → บอก
6. Claude ทำให้:
   - Save เข้า vault/10_research/papers/YYYY-MM-DD-<slug>.md
   - Link ไป note ที่เกี่ยวข้องใน vault
   - เพิ่ม tag ที่เหมาะสม
7. จบ — Token Claude ที่ใช้: น้อยมาก (แค่ organize ไม่ได้ summarize)
```

### Case 2: วิจัยหุ้น (ใช้เอกสารหลายชิ้น)

```
1. NotebookLM → notebook ใหม่ → upload: 10-K + earnings call transcript + 3-5 บทความ
2. ถาม NotebookLM หลายคำถาม:
   - "สรุปธุรกิจและ revenue breakdown"
   - "moat คืออะไร ฝ่ายบริหารพูดถึงยังไง"
   - "risks หลักที่ระบุใน 10-K"
   - "guidance ล่าสุดจาก earnings call"
3. Copy แต่ละ answer
4. Claude Code: บอก "ทำ stock research note สำหรับ <TICKER> 
   จากสรุป NotebookLM นี้ ใช้ template stock-research.md"
5. paste สรุปจาก NotebookLM
6. Claude จัดใส่ template + link ไป macro notes ที่เกี่ยวข้อง
```

### Case 3: ทำ content จาก research

```
1. Claude Code: "อ่าน notes ใน vault/10_research/ ที่ tag :AI 
   แล้ว draft Twitter thread เรื่อง X"
2. Claude ใช้ vault ของคุณเป็น context โดยตรง → เขียนด้วย voice คุณ
3. ไม่ต้องไป NotebookLM เพราะ research ย่อยและเก็บไว้แล้ว
```

### Case 4: ถามย้อน research เก่า

```
Claude Code: "เคยอ่านเรื่อง LLM agents ไปแล้วบ้าง อยู่ที่ไหน?"
→ Claude grep vault → ตอบ พร้อม link ไปยัง notes
→ Token น้อยมาก เพราะแค่ค้นหา ไม่ได้ re-read raw sources
```

---

## ที่ควรใช้ NotebookLM (token saver)

- PDF > 20 หน้า
- หนังสือ / ebook
- Audio / video ยาว > 30 นาที
- 5+ เอกสารที่ต้องสังเคราะห์
- เอกสารที่คุณจะกลับไปถามหลายรอบ (keep as notebook, ย่อยที่ NotebookLM)

## ที่ควรใช้ Claude Code ตรงๆ (ไม่ต้องผ่าน NotebookLM)

- เว็บ article สั้น (< 3000 คำ)
- ย่อยคลิป YouTube สั้น (ใช้ transcript)
- ถามข้ามหลาย note ใน vault
- เขียน content draft
- Code / debug
- Formatting / organizing

---

## Workflow schematic

```
┌────────────────┐
│ Raw sources    │  PDF, audio, long docs, multi-source research
│ (heavy to      │
│  process)      │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ NotebookLM     │  ย่อย, Q&A, audio overview
│ (free tier)    │
└────────┬───────┘
         │ (paste สรุป)
         ▼
┌────────────────┐
│ Claude Code    │  /import-notebooklm
│ /import        │  organize, tag, link ไป vault
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ Obsidian vault │  markdown + git
│ (long-term     │  ← Claude Code อ่านกลับมาได้ทุก session
│  memory)       │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ Claude Code    │  synthesize, write, code, Q&A
│ (daily work)   │  ใช้ vault เป็น context → token ต่ำ
└────────────────┘
```

---

## Tips ประหยัด token เพิ่มเติม

1. **อย่าให้ Claude re-read** note ที่อ่านไปแล้วใน session เดียวกัน — บอก "use note ที่เพิ่งอ่าน"
2. **ใช้ `/clear` ใน Claude Code** เมื่อเปลี่ยน topic — reset context
3. **Vault note ควรสั้น** (< 2000 คำ) — แตก note ที่ยาวเกินเป็นหลาย note + เชื่อม wikilink
4. **Tag อย่างจริงจัง** — ทำให้ grep/Dataview หาเจอเร็ว ไม่ต้องสแกนทั้ง vault
5. **Weekly review** ช่วยย้าย inbox เข้าที่ → Claude ไม่ต้องเดา structure
6. **สร้าง MOC (Map of Content)** สำหรับ topic ใหญ่ๆ — Claude อ่าน MOC ก่อน แล้วค่อย drill down

---

## เมื่อไหร่ควร re-ย่อยด้วย Claude (ไม่ใช้ NotebookLM)

- Source สั้นมาก (< 5 หน้า)
- ต้องการสรุปในรูปแบบเฉพาะที่ NotebookLM ทำไม่ได้ (e.g. ใส่ wikilink อัตโนมัติ)
- Source เป็น code / technical docs ที่ NotebookLM ไม่ถนัด
- ต้องการ output ภาษาไทยเฉพาะทาง
