# Trade Journal

Every buy/sell/adjust logged as one file. Separate from research files (which capture thesis).

## Rules
- **Filename**: `YYYY-MM-DD-<action>-<TICKER>.md`
- **Template**: `vault/_templates/trade-journal.md` (Templater auto-loads if folder rule set)
- **Link to thesis**: each trade journal links back to the active research file in `../`
- **Post-mortem**: fill the bottom section after exit

## Why separate from research
- Research captures **what I believe** (current)
- Journal captures **what I did and why at that moment** (historical)
- Research gets updated; journal entries are immutable

## Dataview dashboard
Add to `vault/20_investment/README.md`:

````markdown
## Recent trades

```dataview
TABLE action, ticker, price, outcome, file.ctime as "Date"
FROM "20_investment/_journal"
SORT file.ctime DESC
LIMIT 20
```

## Win rate (last 50 closed)

```dataview
TABLE count(rows) as "Count"
FROM "20_investment/_journal"
WHERE outcome != "open"
GROUP BY outcome
```
````
