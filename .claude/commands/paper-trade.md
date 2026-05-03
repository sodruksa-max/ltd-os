---
description: Log a new paper trade entry — creates trade file in real-trades/, tracked by /eod
---

# /paper-trade

Create a paper trade log entry. Tracked by `/eod` exactly like real trades.

## Usage

```
/paper-trade TICKER [DIRECTION]
```

- `TICKER` — stock symbol (e.g. NVDA, SPY, AAPL)
- `DIRECTION` — long (default) or short

## Steps

### 1. Ask for trade details

If not provided in the command args, ask the user:

```
Ticker: [from args or ask]
Direction: long / short [default: long]
Entry price (USD): ?
Shares: ?
Stop loss (USD): ?
Target (USD): ?
Setup source: [e.g. "2026-05-03-premarket Setup 1" or leave blank]
```

Calculate and show before writing:
- **Risk per share** = |entry - stop|
- **R-multiple at target** = (target - entry) / |entry - stop|  [long] or (entry - target) / |entry - stop| [short]
- **Total risk** = risk per share × shares
- If R-multiple < 1.5 → warn: "R:R ต่ำกว่า 1.5 — ยังคุ้มที่จะเข้าไหม?"
- If total risk > 5% of 100K (= $5,000 / THB equivalent) → warn: "Risk เกิน 5% ของ trading capital"

Ask: "ยืนยันสร้าง paper trade? (y/n)"

### 2. Create trade file

File path: `vault/20_investment/_journal/real-trades/YYYY-MM-DD-TICKER-DIRECTION-paper.md`

Use this template:

```markdown
---
ticker: TICKER
direction: DIRECTION
status: open
type: paper
date_open: YYYY-MM-DD
date_close: ~
entry_usd: ENTRY
shares: SHARES
fees_usd: 0
stop_usd: STOP
target_usd: TARGET
exit_usd: ~
exit_fees_usd: ~
result: ~
setup_source: "SETUP_SOURCE"
---

# Paper Trade — TICKER (LONG/SHORT) — YYYY-MM-DD
*Paper trade (ไม่ใช่เงินจริง) | type: paper*

---

## ข้อมูล Trade

| Field | Value |
|---|---|
| **Ticker** | TICKER |
| **Direction** | Long / Short |
| **Status** | Open (Paper) |
| **Date opened** | YYYY-MM-DD |
| **Date closed** | — |
| **Setup source** | SETUP_SOURCE |

---

## ราคา

| | ราคา USD | หมายเหตุ |
|---|---|---|
| **Entry** | $ENTRY | |
| **Stop loss** | $STOP | -X% จาก entry |
| **Target** | $TARGET | +X% จาก entry |
| **Exit** | — | *กรอกตอนปิด* |

---

## Position

| | Value |
|---|---|
| **Shares** | SHARES หุ้น |
| **Cost basis** | $COST (entry × shares) |
| **Fees ซื้อ** | $0 (paper) |

---

## R:R Summary
- Risk per share: $RISK_PER_SHARE
- R-multiple at target: RMULTIPLE R
- Total risk: $TOTAL_RISK

---

## Notes

### เหตุผลที่เข้า
[trigger, setup, confluence — อ้างอิง premarket ถ้ามี]

### เหตุผลที่ออก
—

### Lesson (1 ประโยค)
—
```

### 3. Report

```
Paper trade logged: vault/20_investment/_journal/real-trades/YYYY-MM-DD-TICKER-DIRECTION-paper.md
Risk: $TOTAL_RISK | R:R = RMULTIPLE:1
Run /eod to see it in the position monitor.
```

## Closing a paper trade

When user says "close paper trade TICKER":
1. Read the trade file
2. Ask: exit price?
3. Calculate realized gain/loss + R-multiple achieved
4. Update frontmatter: status → closed, date_close, exit_usd, result
5. Append to Notes → เหตุผลที่ออก + Lesson

## Constraints

- `type: paper` field is mandatory — distinguishes from real trades in future analytics
- `fees_usd: 0` always for paper trades
- Never create a paper trade file with `type: real` or without `type:` field
- If R:R < 1.5 or risk > 5% capital, warn but still create if user confirms
