## Pragmatist Proposal

### Recommendation

อย่าเพิ่ม AH criterion ตอนนี้ แต่ให้เก็บ data อีก 3-5 case ก่อน แล้วค่อยตัดสิน ระหว่างนี้เพิ่ม **soft filter** ที่ไม่ block trigger แต่บันทึก weighted AH pp ทุกครั้ง

### Core argument

1 case study (Apr 29) พิสูจน์ได้แค่ว่า setup นี้ "อาจพลาด" ไม่ใช่ว่า "พลาดบ่อย" การเปลี่ยน rule จาก n=1 คือ overfitting ต่อ noise ปัญหาจริงคือ setup ยังไม่มี base rate ของตัวเอง — ต้องสะสมก่อน ส่วน AH data ก็มี value แต่เป็น noisy predictor เพราะ AH liquidity ต่ำ และมักพลิกกลับในวันถัดไป

### Supporting evidence / base rates

- งานวิจัยด้าน gap trading (Shareplanner, StockCharts) พบว่า large gap-down หลัง earnings ไม่ได้ fill เสมอ แต่ QQQ ยัง "fell from open-to-close 58% of the time" บน big gap-down days ซึ่งหมายความว่า 42% ของเวลาพลิกกลับ ความเชื่อมั่นต่ำกว่า 60/40 ไม่พอสร้าง rule
- "Sell the news" ใน mega-cap tech เป็น episodic ไม่ใช่ structural: GOOGL AH +7% ในคืนเดียวกับที่ META -7% แสดงว่า AH signal ขัดแย้งกันในตะกร้าเดียว การ aggregate เป็น weighted pp แก้ปัญหาบางส่วนแต่ยังต้องการ threshold ที่ยังไม่มีข้อมูลรองรับ
- Apr 29 AH net -0.30pp แต่ QQQ วัน Apr 30 จริงขึ้น/ลงเท่าไหร่? ถ้ายังไม่รู้ outcome ของ case เดียวที่มีอยู่ การเปลี่ยน rule ก็ยิ่งไม่มีฐาน

### Suggested rule

ยังไม่เปลี่ยน trigger condition แต่เพิ่ม observation field ใน journal ทุก Setup 3 entry:

```
AH weighted impact (pp): [คำนวณทุกครั้ง]
AH signal: [positive / negative / mixed]
Actual next-day QQQ result: [%]
```

หลังได้ 5 case: ถ้า AH negative pp correlates กับ negative next-day QQQ ≥60% → เพิ่ม criterion อย่างเป็นทางการ ถ้าไม่ถึง → ทิ้ง AH เป็น criterion แล้วหา variable อื่น

### Expected outcome (realistic)

ใน 6 เดือน paper trading จะมี Mag7 earnings season อีกประมาณ 1-2 รอบ Setup 3 จะ trigger 2-4 ครั้ง ถ้าเก็บ AH data ทุกครั้งตั้งแต่ตอนนี้ จะมีข้อมูลพอประเมิน AH criterion ได้จริงก่อน go-live เดือน 7 โดยไม่เสียโอกาส entry ดีๆ ระหว่างทาง

### What you're uncertain about

- QQQ Apr 30 actual close ยังไม่รู้ ถ้า Apr 30 QQQ ลงจริงหนัก นั่นถึงจะเป็นหลักฐาน case ที่ครบวงจร ตอนนี้ยังเป็นแค่ "AH negative" ไม่ใช่ "trade แพ้"
- Weighted AH pp threshold ที่เหมาะสม (เช่น ≤-0.5pp?) ยังต้องการข้อมูลมากกว่านี้ก่อนตั้งค่า
- "Sell the news" ใน AI capex cycle อาจเป็น structural ในช่วงนี้ แต่จะหายไปหลัง capex peak ในอีก 6-12 เดือน ถ้าเป็นอย่างนั้น AH criterion จะใช้ได้เฉพาะบางช่วง ไม่ใช่ rule ถาวร
