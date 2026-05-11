---
name: NotebookLM URL fallback — text source
description: เมื่อเพิ่ม URL ใน NotebookLM ไม่ได้ ให้ fetch content แล้วเพิ่มเป็น text source แทน
type: feedback
---

เมื่อหา source สำหรับ NotebookLM: ลอง source_add URL ก่อน ถ้า error "Could not add url source" → ใช้ WebFetch ดึง content มาแล้วเพิ่มด้วย source_type=text แทนทันที ไม่ต้องลอง URL อื่นซ้ำๆ

**Why:** Site อย่าง Tom's Hardware, blocksandfiles.com, storagenewsletter.com, businesswire.com ล้วนโดนบล็อคโดย NotebookLM (Cloudflare/paywall detection) การ fetch content แล้ว paste เป็น text ได้ผลเสมอ

**How to apply:**
1. ลอง source_add ด้วย URL → ถ้า success ดี
2. ถ้า error → WebFetch URL นั้นทันที → source_add ด้วย source_type=text พร้อม title ชัดเจน (ชื่อ article + เดือน/ปี + publisher)
3. ไม่ต้อง refresh_auth หรือลอง URL อื่นก่อน — error "Could not add url source" = บล็อค ไม่ใช่ auth
4. Error "Could not add text source" + "Failed to get notebook: Authentication expired" = auth หมด → บอก user รัน `! nlm login`
