---
type: reese-research-doc
topic: AI Networking — MRVL + CRDO (Ethernet Rebellion vs InfiniBand)
date: 2026-05-11
thesis_link: T1, T2
chris_verdict: "✅ Pass"
vera_flags: 4
---

# AI Networking — MRVL & CRDO Research Doc

## Narrative

AI data center มี 2 networks: front-end (internet-facing) และ back-end ที่เชื่อม GPU ทุกตัวเข้าหากันเหมือน supercomputer เดียว ตลาดนี้กำลังเกิด "Ethernet Rebellion" ที่สั่นสะเทือน InfiniBand monopoly ของ NVIDIA

ประวัติศาสตร์: InfiniBand ครองตลาด AI back-end เพราะ ultra-low latency (<2μs) และ zero packet loss ผ่าน Credit-Based Flow Control แต่ hardware cost สูงกว่า Ethernet 3x และ ecosystem ปิด → hyperscaler ทุกรายผลักดัน Ethernet แทน ใน June 2025 Ultra Ethernet Consortium (UEC) ปล่อย UEC 1.0 — reconstruct network stack ทั้งหมดให้ match InfiniBand performance ใน open ecosystem Microsoft ประกาศ transition เต็ม 100% ไป Ethernet by summer 2026

Speed roadmap: 400G (2024) → 800G (2025) → 1.6T (2026) → 3.2T (2027) ทุก transition ทำให้ copper ใช้ไม่ได้ (copper works ≤5m at 800G) → optical interconnect เป็น necessity

**MRVL:** เป็น secondary Ethernet switch supplier (AVGO 80%, MRVL ~20%) แต่ **ครองตลาด 800G optical interconnects** ซึ่งเป็น bottleneck ถัดไป ใน cluster ขนาด 1M processors ต้องใช้ optical ทั้งหมด — MRVL กำลัง demo optical links ระหว่าง data centers ห่างกัน 300 ไมล์

**CRDO:** ❓ ไม่มีข้อมูล specific ใน notebook แต่จาก T2 research เดิม: ถือ 73% AEC (Active Electrical Cable) market สำหรับ GPU rack interconnect อยู่ใน transition zone ระหว่าง copper → optical

## Bull case

1. **Ethernet adoption โดย hyperscaler ทุกราย → MRVL ได้ share จาก Ethernet switch + optical** Microsoft transition 100% Ethernet by summer 2026 "All the largest guys have moved to Ethernet" — anonymous network executive Network chips projected เพิ่มจาก 5-10% เป็น 15-20% ของ AI chip budget ใน $100B cluster MRVL Teralynx 10 (51.2 Tbps) เป็น next-gen switch ที่ hyperscaler ใช้แทน AVGO ใน specific configurations

2. **MRVL leads 800G optical — copper เป็น dead end ใน large clusters** ที่ speeds 800G+ copper ทำงานได้เพียง ≤5m ทำให้ cluster >100K GPUs บังคับใช้ optics ทั้งหมด MRVL มี strong lead ใน 800G interconnects (IEEE ComSoc source) Co-Packaged Optics (CPO) เป็น next frontier — MRVL กำลัง scale CPO products สำหรับ 1.6T+ era

3. **CRDO AEC moat ใน GPU rack short-reach (<5m) ที่ยังต้องการ copper** AEC (Active Electrical Cable) ยัง cost-effective สำหรับ intra-rack connections ≤5m ในขณะที่ optical เป็น overkill ถ้า CRDO มี 73% AEC share จริง (❓) → มี captive revenue stream จาก GPU rack buildout ที่ scale up ทุกปี

## Bear case

1. **AVGO ครอง 80% Ethernet switch — MRVL ไม่ใช่ primary beneficiary ของ Ethernet rebellion** Broadcom Tomahawk 6 (102.4 Tbps, 2025) นำหน้า NVIDIA Spectrum-X1600 ที่จะออก H2 2026 ถึง 1 ปี MRVL Teralynx อยู่ที่ 51.2 Tbps — ยังตามหลัง AVGO รุ่นล่าสุด ถ้า Ethernet rebellion ชนะ → ผู้ชนะหลักคือ AVGO ไม่ใช่ MRVL

2. **Optical transition อาจทำลาย CRDO AEC moat เร็วกว่าคาด** AEC ใช้ copper → ถ้า optical adoption เร็ว AEC market หดตัว CRDO ไม่มี photonics roadmap ที่ชัดเจน (❓) = ถ้า optical กลายเป็น standard ก่อน 2027 → CRDO ต้อง reinvent ตัวเอง

3. **NVIDIA Spectrum-X เป็น defensive moat ที่ยังครอง InfiniBand customer base** NVIDIA มี captive InfiniBand ecosystem ใน training clusters (H100/H200) ที่ hyperscaler deploy ไปแล้ว switching cost สูง ถ้า NVIDIA Spectrum-X1600 (102.4 Tbps Ethernet, H2 2026) launch ดี → NVIDIA กลับมาแข่งใน Ethernet ด้วย = pressure ทั้ง MRVL และ AVGO

## Kill conditions

| Kill condition | สถานะ |
|---|---|
| AVGO ออก optical interconnect product ที่แข่ง MRVL 800G โดยตรง | กำลัง develop — watch |
| CRDO market share ใน AEC ลดจาก 73% เพราะ optical cannibalization | ยังไม่มีข้อมูล — ❓ |
| NVIDIA Spectrum-X recapture >30% ของ new Ethernet cluster deployments | ยังไม่เกิด — NVDA ยังตาม 1 ปี |
| Hyperscaler หยุด CapEx growth 2 ไตรมาสติดกัน | ยังไม่เกิด |

## Data gaps

- ❓ CRDO revenue, margins, market share specifics — ไม่มีใน notebook; จาก T2 research เดิม: "73% AEC share" แต่ source ไม่ verified ครบ
- ❓ MRVL optical interconnect revenue mix — เป็น % เท่าไหร่ของ total MRVL revenue?
- ❓ Timeline ที่ CPO จะกลายเป็น majority ของ optical market — 2026 หรือ 2027+?
- ❓ CRDO photonics strategy — มีหรือไม่ ถ้าไม่มี = strategic gap ใหญ่

## Sources

- IEEE ComSoc Technology Blog: Networking chips and modules for AI data centers (Jan 2025)
- TrendForce: InfiniBand vs Ethernet: Broadcom and NVIDIA Scale-Out Tech War
- FinancialContent: Broadcom's AI Nervous System — $18B Revenue + $73B Backlog (Dec 2025)
- NotebookLM AI Capex Cycle 2026 notebook query (May 2026)
