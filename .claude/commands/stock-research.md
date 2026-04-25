---
description: Deep-dive research on a single stock ticker. Chains researcher → fills stock-research template → saves to vault/20_investment/. Suggests /challenge after.
---

# /stock-research

Invoke researcher agent to gather info on a ticker, fill in `stock-research.md` template, save to vault.

## Usage
- `/stock-research NVDA`
- `/stock-research TSM — focus on foundry competition`

## Steps

1. **Parse ticker** from user input (required). Parse angle/focus if provided (optional).

2. **Check existing vault note** first:
   ```bash
   ls vault/20_investment/ | grep -i <TICKER>
   ```
   - If exists: ask user "Note exists at <path>. Update it, or create new dated version?"
   - If not: proceed to new note

3. **Invoke researcher** with scope:
   - Company basics (business model, revenue segments, geo)
   - Latest 10-K / 10-Q highlights (search "<TICKER> 10-K")
   - Latest earnings call (search "<TICKER> earnings call transcript")
   - Competitive position (named competitors + moat)
   - Bear case (search "<TICKER> bear case" — steelman)
   - Current valuation (P/E, EV/EBITDA, vs. history)
   
   Budget: 5 web searches max, 10 vault reads max.

4. **Fill template** `vault/_templates/stock-research.md`:
   - Save to: `vault/20_investment/<TICKER>-YYYY-MM-DD.md`
   - Populate ALL sections with researcher's findings
   - Leave "Thesis" section for user to write themselves — this is THEIR investment call, not Claude's
   - Mark any section where info is missing with `❓ verify`

5. **Report back**:
   ```
   Stock research saved: vault/20_investment/<TICKER>-YYYY-MM-DD.md
   
   Filled sections:
   ✓ Business, Numbers, Competitive position, Bull case, Bear case
   ❓ Needs verification: <list>
   ❗ Left for you to fill: Thesis, Decision log, Position sizing
   
   Before you act on this:
   → Write your thesis in the Thesis section
   → Run: /challenge vault/20_investment/<TICKER>-YYYY-MM-DD.md
   
   Researcher used: N searches, M vault reads
   ```

## Constraints

- **Do NOT write the thesis for the user** — that's the point, they decide
- **Do NOT recommend buy/sell** — present info, user decides
- **Flag uncertainty** — if P/E from different sources disagree, say so
- **Don't invent numbers** — if researcher couldn't find a metric, leave `❓` instead of guessing
- **One ticker per invocation** — multi-ticker comparison is a different command

## When user asks follow-up questions

After initial research, questions like "what about margins?" → use existing note as context first (read it), add section if needed, save. Don't re-research from scratch.
