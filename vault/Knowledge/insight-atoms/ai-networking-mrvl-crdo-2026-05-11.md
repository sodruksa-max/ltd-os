---
type: insight-atoms
topic: MRVL + CRDO — AI Networking Interconnect
date: 2026-05-11
source_doc: vault/10_research/ai-networking-mrvl-crdo-reese-2026-05-11.md
thesis_link: T1, T2
---

# Insight Atoms: MRVL + CRDO — AI Networking Layer

## Ethernet Rebellion: Hyperscalers Abandoning InfiniBand

**Claim:** ทุก major hyperscaler กำลัง transition จาก InfiniBand → Ethernet ใน AI back-end network; Microsoft ประกาศ 100% Ethernet by summer 2026
**Evidence:** Ultra Ethernet Consortium (UEC) ปล่อย UEC 1.0 เดือน Jun 2025; "All the largest guys have moved to Ethernet" — anonymous network executive; InfiniBand cost 3x Ethernet
**Implication:** Ethernet switch + optical interconnect market จะ expand dramatically; AVGO (80% share) คือผู้ได้ประโยชน์หลัก แต่ MRVL ได้ spill-over ใน optical
**Source:** TrendForce (InfiniBand vs Ethernet analysis); IEEE ComSoc (Jan 2025); NotebookLM query (May 2026)
**Date:** 2026-05-11
**Thesis link:** T1, T2

---

## Copper Is Dead at 800G+ — Optical Is Mandatory

**Claim:** ที่ความเร็ว 800G+ copper ทำงานได้เพียง ≤5 เมตร ทำให้ cluster ที่ใหญ่กว่า 100K GPUs ต้องใช้ optical interconnect ทั้งหมด
**Evidence:** IEEE ComSoc report (Jan 2025); speed roadmap: 400G (2024) → 800G (2025) → 1.6T (2026) → 3.2T (2027)
**Implication:** ทุก cluster ที่ scale เกิน 100K GPUs = ต้องซื้อ optical; MRVL ที่ lead 800G optical = structural beneficiary ของ cluster size growth
**Source:** IEEE ComSoc Technology Blog (Jan 2025); NotebookLM AI Capex Cycle 2026 notebook
**Date:** 2026-05-11
**Thesis link:** T1, T2

---

## Broadcom Holds 80% Ethernet Switch — Real Beneficiary of Rebellion

**Claim:** AVGO ครอง ~80% ของ Ethernet switch market ใน AI datacenter; MRVL อยู่ที่ ~20%
**Evidence:** Broadcom Tomahawk 6 (102.4 Tbps, 2025) นำหน้า MRVL Teralynx 10 (51.2 Tbps); AVGO $73B backlog (Dec 2025)
**Implication:** Ethernet rebellion เป็น narrative ที่ถูกต้อง แต่ investor ที่ซื้อ MRVL เพราะ Ethernet switch อาจเข้าใจผิด — primary winner คือ AVGO; MRVL thesis ต้องพิง optical interconnect ไม่ใช่ switch
**Source:** FinancialContent AVGO AI Nervous System report (Dec 2025); TrendForce
**Date:** 2026-05-11
**Thesis link:** T1, T2

---

## MRVL Leads 800G Optical — Key Differentiation from AVGO

**Claim:** MRVL มีความได้เปรียบใน 800G optical interconnects ขณะที่ AVGO ยังไม่มี optical product ที่แข่งขันโดยตรง
**Evidence:** IEEE ComSoc ระบุ MRVL strong lead ใน 800G interconnects; MRVL กำลัง demo optical links ระหว่าง datacenter ห่างกัน 300 ไมล์; กำลัง scale CPO (Co-Packaged Optics) สำหรับ 1.6T+ era
**Implication:** ถ้า AVGO ออก optical product โดยตรง → MRVL optical advantage หมดอายุ; watch AVGO photonics roadmap เป็น primary kill condition ของ MRVL
**Source:** IEEE ComSoc Technology Blog (Jan 2025); NotebookLM query (May 2026)
**Date:** 2026-05-11
**Thesis link:** T1, T2

---

## CRDO AEC Moat: 73% Share in Short-Reach GPU Rack ❓

**Claim:** CRDO ถือ ~73% market share ใน AEC (Active Electrical Cable) สำหรับ GPU rack short-reach interconnect (≤5m)
**Evidence:** ❓ Source ไม่ verified ครบ — จาก T2 research เดิม; ไม่มีข้อมูล specific ใน NotebookLM notebook
**Implication:** ถ้า claim จริง → CRDO มี captive revenue stream จาก GPU rack buildout; ถ้า optical adoption เร็ว → AEC market หดตัวก่อน 2027 และ CRDO ต้อง reinvent ตัวเอง ❓ CRDO photonics roadmap?
**Source:** [unverified] T2 research prior to 2026-05-11 — ต้อง verify ก่อน trade
**Date:** 2026-05-11
**Thesis link:** T2
