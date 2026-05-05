# MEMORY.md — Index

<!-- Load only entries relevant to current task (see CLAUDE.md §8 task-scoped loading) -->

## Feedback (load for any task)
- [Always recommend the best option](feedback_recommend_best.md) — เมื่อถาม ให้ระบุทางที่ดีที่สุดชัดเจน ไม่ใช่แค่ list ตัวเลือก
- [Show exact change before asking approval](feedback_approval_context.md) — ทุก y/n prompt ต้องแสดงว่าถ้า approve แล้วจะเกิดอะไร ก่อนถามเสมอ
- [Verify workflow feasibility before proposing](feedback_verify_workflow_before_proposing.md) — ต้อง verify ทุก step ว่าทำได้จริงใน interface ที่ user ใช้ ก่อนเสนอ workflow
- [User values cost efficiency](user_cost_conscious.md) — ชอบความคุ้มค่า ใช้ token ให้หมดก่อนปิด อย่าแค่บอกให้ปิด — เสนองานเล็กๆ ที่ทำได้แทน | related: feedback_cross_apply_improvements.md
- [Cross-apply improvements to related systems](feedback_cross_apply_improvements.md) — เมื่อ improvement ทำงานได้ดี ให้ scan และแนะนำส่วนอื่นที่ควรได้รับ pattern เดียวกัน | related: user_cost_conscious.md

## Project (load for code/project tasks)
- [Trading bot direction](project_trading_bot_direction.md) — เพิ่ม crypto bot (Binance/ccxt) ต่อจาก stock screener ที่เก็บไว้ครบ | related: vault/20_investment/_journal/
- [Investment sector focus](project_sector_focus.md) — Semicon/AI/Datacenter universe: NVDA AMD MU AVGO ARM ASML SMCI PLTR | load for any trading/research task
