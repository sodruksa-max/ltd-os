---
type: reese-research-doc
topic: Memory Semiconductors — MU, WDC, HBM cycle
date: 2026-05-11
thesis_link: T1, T2
chris_verdict: "✅ Pass"
vera_flags: 6
---

# Memory Semiconductors — MU & WDC Research Doc

## Narrative

Memory semiconductor ในปี 2026 ไม่ใช่แค่ cycle rebound ธรรมดา — มี structural shift สำคัญที่ AI สร้างขึ้น 2 ชั้น: ชั้นแรก HBM (High Bandwidth Memory) กลายเป็น critical infrastructure สำหรับทุก AI GPU โดยเฉพาะ NVDA Blackwell และ Vera Rubin ราคา HBM3E สูงกว่า DRAM ทั่วไป 5-8 เท่า และ capacity ทั้งอุตสาหกรรมถูกจองหมดแล้วถึงปลายปี 2026 ชั้นที่สอง classical DRAM และ NAND flash ก็กำลังขาดแคลนจาก AI datacenter demand ที่ผลักให้ data center เป็นส่วนใหญ่ของ TAM เป็นครั้งแรกในประวัติศาสตร์

MU (Micron) เป็น pure-play U.S. memory ที่ได้รับประโยชน์ตรงๆ: Q2 FY2026 revenue $23.9B (+196% YoY) ❓ เป็นตัวเลขที่สูงผิดปกติ — อาจเป็น quarterly ไม่ใช่ annual run-rate ต้องยืนยัน FY2026 projection อยู่ที่ $74-76B (เทียบ $37.4B ใน FY2025) HBM capacity sold out ถึงปลาย 2026 และ HBM annualized revenue run-rate ประมาณ $8B WDC (Western Digital) หลัง spin-off Sandisk กลายเป็น pure-play enterprise HDD ที่ตลาด AI storage ต้องการ ราคาหุ้นขึ้น +115% YTD 2026 revenue Q3 $3.3B (+45% YoY) gross margin 46.1% และ sold out ทั้งปี 2026

ความเสี่ยงหลักไม่ใช่ demand ใกล้ๆ — แต่เป็น cycle ที่จะมาในปี 2027-2028 เมื่อ mega-fabs ของ Samsung และ SK Hynix เริ่มผลิต ประวัติศาสตร์ memory industry ไม่เคยมี supercycle ที่ไม่จบด้วย oversupply

## Bull case

1. **MU HBM capacity sold out ถึงปลาย 2026 + HBM TAM $62B — MU มีส่วนแบ่ง ~24%** AI GPU ทุกตัวต้องการ HBM และไม่มีทางเลือกอื่น NVDA Blackwell ใช้ HBM3E จาก SK Hynix, Samsung, MU ทั้งสามราย ราคา HBM สูงกว่า commodity DRAM 5-8x ทำให้ margin ขยายอย่างมีนัยสำคัญ มีเพียง 3 บริษัทในโลกที่ผลิต HBM ได้ = barrier to entry สูงมาก

2. **WDC เป็น pure-play AI storage duopoly (WDC + Seagate) หลัง Sandisk spinoff** WDC กำจัด low-margin NAND business ออกไป เหลือแต่ HDD enterprise ที่ gross margin 46-48% AI datacenter ต้องการ mass storage สำหรับ training data และ inference logs 89% revenue มาจาก hyperscaler AI cloud HAMR technology (44TB → 100TB+ roadmap) สร้าง technology moat ที่ NAND ไม่สามารถแทนที่ได้ในระดับ $/GB สำหรับ cold storage

3. **Supply tightening 2026 กดราคา DRAM ขึ้น 30-60% — classical DRAM ยังเป็นส่วนใหญ่ของ MU revenue** Samsung DRAM inventory เหลือ 6 สัปดาห์ (ปกติ 10-12 สัปดาห์) SK Hynix DRAM inventory 2-3 สัปดาห์ ความขาดแคลนนี้ดีต่อ ASP ของ MU ทั้งใน HBM และ classical DRAM ซึ่งยังเป็นส่วนใหญ่ของ revenue รวม

## Bear case

1. **MU ไม่ได้รับ supply share ใน Nvidia Vera Rubin platform รุ่นแรก** Q1 2026 SK Hynix 70% / Samsung 30% / MU 0% ❓ ใน initial Vera Rubin launch ถ้า pattern นี้ซ้ำใน HBM4 generation MU จะสูญเสีย revenue growth trajectory ที่ตลาดกำลัง price in

2. **Oversupply cycle 2027-2028 กำลังถูก build ขึ้นตอนนี้** SK Hynix + Samsung mega-fabs เริ่ม production 2027 MU Japan plant ปลาย 2028 capex รวมอุตสาหกรรม 2026: $58B+ SK Hynix ลด HBM investment 50% YoY แล้วเพราะกลัว 2027 oversupply ประวัติศาสตร์ทุก memory boom จบด้วย bust เสมอ

3. **WDC SSD/NAND market ถูก Sandisk แยกออก = ไม่ได้ประโยชน์จาก NAND price recovery** Sandisk ถือ NAND flash business ทั้งหมดรวมถึง partnership กับ Kioxia WDC เป็นแค่ HDD = ถ้า NAND price spike ดีกว่า HDD ผู้ถือหุ้น WDC ไม่ได้ประโยชน์ นอกจากนี้ HDD ยังต้องการขยาย HAMR volume production ซึ่งยัง qualify กับลูกค้าเพียง 4 รายเท่านั้น ❓ ความล่าช้าของ HAMR volume production = margin compression risk

## Kill conditions

| บริษัท | Kill condition | สถานะ |
|---|---|---|
| MU | HBM market share ลดต่ำกว่า 15% ใน 2 ไตรมาสติดกัน | ยังไม่เกิด — อยู่ที่ ~21-24% |
| MU | MU ไม่ได้รับ HBM4 qualification จาก NVDA (Vera Rubin + รุ่นต่อไป) | ❓ ต้องติดตาม Vera Rubin supply split ใน 2026 |
| MU | DRAM/NAND ASP ลดมากกว่า 20% ใน 2 ไตรมาสติดกัน | ยังไม่เกิด — ราคายังขึ้น |
| WDC | HAMR volume production ล่าช้าเกิน Q1 2027 | ยังไม่เกิด — qualification กับ 4 ลูกค้า |
| WDC | Hyperscaler ลด HDD procurement เพราะ NAND/SSD ถูกกว่าในระดับ cold storage | ยังไม่เกิด |
| ทั้งสอง | Samsung/SK Hynix ประกาศเพิ่ม capex ใหม่อีก round ก่อน 2027 mega-fabs เต็มกำลัง | ยังไม่เกิด — watch |

## Data gaps

- ❓ Q2 FY2026 Micron revenue $23.9B ขัดกับ FY2026 projection $74-76B — ตัวเลข quarterly vs annual ต้องยืนยันจาก IR โดยตรง
- ❓ MU HBM revenue mix ใน total revenue — HBM $8B annualized vs FY2026 $74-76B = ~11% ของ revenue? classical DRAM/NAND ยังเป็นส่วนใหญ่
- ❓ MU Vera Rubin supply share — "0% share" จาก ainvest.com แหล่งเดียว ต้องยืนยัน
- ❓ WDC revenue FY2026 full year projection — มีแค่ quarterly ไม่มีตัวเลข annual consensus
- ❓ HAMR customer qualification status — WDC บอก "4 customers" แต่ไม่ระบุว่าเป็นรายใหญ่ระดับ hyperscaler หรือไม่
- ❓ Sandisk (spinoff) performance post-split — ถ้าถือ WDC ก่อน spinoff ได้ Sandisk shares ด้วย thesis จะต่างกัน

## Sources

- Futurum Group: Micron Q2 FY2026 earnings — AI-led memory demand
- Tech-Insider: Micron Q2 2026 record revenue analysis
- TradingKey: Micron vs Samsung vs SK Hynix best memory stock 2026
- Tom's Hardware: Samsung + SK Hynix warn AI-driven shortage through 2027+
- NAND Research: Memory supply constraints Nov 2025
- Astute Group: SK Hynix 62% HBM share, Micron overtakes Samsung
- 247wallst.com: Micron +68% YTD HBM demand sustainability
- FinancialContent: WDC "The Great Decoupling" HDD renaissance
- TIKR: Western Digital +115% in 2026
- Vdura: WDC + Seagate Q3 2026 earnings AI storage analysis
- Investing.com: WDC Q3 2026 beats forecasts
