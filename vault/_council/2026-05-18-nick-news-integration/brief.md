# Council Brief — Nick Real-Time News Integration
*2026-05-18 | lens: engineer*

## Context

Nick คือ blinded thesis portfolio manager ที่อ่านเฉพาะ KB — ปัจจุบัน Nick ไม่มีระบบรับข่าวใดๆ เลย ต้องอาศัยข้อมูลที่ user manually update เข้า vault เท่านั้น

### Infrastructure ที่มีอยู่แล้ว
- `scripts/news-snapshot.py` — Alpaca News API, fetches macro/market news สำหรับ ETF proxies (SPY, QQQ, XLE, USO, GLD, TLT ฯลฯ) **ไม่ใช่ individual stocks**
- `scripts/nick-monitor.py` — มี `load_current_holdings()` function ที่ parse holdings จาก weekly-rec.md อยู่แล้ว
- Alpaca News API — supports `symbols` parameter → สามารถ query news per ticker ได้
- yfinance — มี `ticker.news` API per ticker, free, no additional API key
- Nick search budget: 15 web searches/session

### ปัญหาที่แท้จริง
Nick ต้องรับรู้ทั้ง 2 ประเภทของข่าวที่มีผลต่อ kill conditions:
1. **Company-specific** — earnings surprise, CEO change, contract win/loss, guidance cut สำหรับ holdings แต่ละตัว
2. **Macro/geopolitical** — สงครามอิหร่าน, Trump เยือนจีน, Fed policy shift — เหตุการณ์ที่กระทบ thesis ทั้งหมดพร้อมกัน โดยไม่มี ticker ที่ชัดเจน

### Prior council decisions
- 2026-05-16: Nick thesis design (financial_risk lens) — status: open
- 2026-05-10: Nick Auto-Trader system — status: open
- ไม่มี council เรื่อง news integration มาก่อน

## Goal

ออกแบบระบบที่ Nick สามารถรับรู้ข่าวทั้ง company-level และ macro/geopolitical **ก่อน weekly review** โดยไม่ break blinded mandate และไม่เพิ่ม maintenance burden มากเกินไป

## Constraints

- Nick ต้องยัง blinded จาก real trade history / real portfolio positions
- ห้ามอ่านข้อมูลจาก BLOCKLIST (journal, trade-log.json, OUTCOMES.md, PREFERENCES.md)
- Nick มี search budget 15 searches/session — ต้องอนุรักษ์ไว้สำหรับ kill condition verification
- ต้องใช้ infrastructure ที่มีอยู่ให้มากที่สุด (DRY principle)
- ระบบต้องทำงานได้แม้ user ไม่ได้รัน /pre-market ก่อน
- ไม่ต้องการ API key ใหม่ถ้าหลีกเลี่ยงได้

## Stakes

- **Low**: Nick ยังไม่รู้ข่าว → kill condition trigger ช้า → ขาดทุน
- **High**: ระบบซับซ้อนเกินไป → maintenance burden → ไม่ได้ใช้จริง
- **Medium**: บางข่าวโดน filter ผิด → noise มากเกิน → Nick เสียสมาธิจาก thesis

## Open Questions

1. News ควร auto-fetch (script รัน cron ทุกวัน) หรือ on-demand (รันเมื่อ nick-weekly เริ่ม)?
2. ถ้า news-snapshot.py รันแล้ว Nick อ่านไฟล์นั้นตรงๆ ได้ไหม — หรือต้องกรอง?
3. Macro news ที่ไม่มี ticker — วิธีไหนดีที่สุด: web search vs Alpaca broad query vs prebuilt topic list?
4. Nick ควร weight company news กับ macro news ต่างกันไหม?

## Prior decisions context
ไม่มี prior council entries ที่ match topic นี้โดยตรง
