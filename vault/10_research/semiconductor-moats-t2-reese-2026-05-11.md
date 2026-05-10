---
type: reese-research-doc
topic: Semiconductor Moats Beyond NVDA/ASML — ARM, CRDO, LRCX, AEIS, UCTT, ONTO
date: 2026-05-11
thesis_link: T2
chris_verdict: "✅ Pass"
vera_flags: 5
---

# Semiconductor Moats Beyond NVDA/ASML — T2 Extended

## Narrative

T2's core (NVDA training monopoly + ASML EUV) is already documented. The uncovered half of T2 is the picks-and-shovels layer: companies whose moats derive not from chip design dominance but from irreplaceable positions in the semiconductor manufacturing supply chain.

The AI capex supercycle is building more fabs (TSMC Arizona, Samsung Texas, Intel Ohio) and pushing every node to more complex geometries (GAA transistors, 3D NAND 300+ layers). Each step up in complexity requires more specialized equipment, more steps per wafer, and more process control — expanding the TAM for every T2 sub-supplier even if wafer starts stay flat. This is the "content per wafer" secular tailwind that makes WFE a structural growth story inside the cycle.

ARM sits apart from the others: it is a pure IP moat — 95%+ gross margins, architecture lock-in via a 280B+ device install base and the entire mobile/AI chip developer ecosystem. Its royalty step-up from Armv8 (~2.5%) to Armv9/CSS (north of 10%) is the compounding mechanism. The risk is not near-term but structural: RISC-V is royalty-free and gaining share in custom ASIC design.

## Bull case

1. **LRCX owns the irreplaceable etch step for 3D NAND and GAA.** High-aspect-ratio etch at 60:1+ aspect ratios with nanometer precision has no competitive alternative. Market share: ~80%+ in advanced node etch. As 3D NAND goes from 200 to 300+ layers and GAA transistors replace FinFET, etch steps per wafer increase even on flat wafer starts. WFE market growing from ~$110B (2025) to ~$135B (2027) per CEO guidance. JPMorgan target $315 citing supercycle.

2. **CRDO has 73% share in the fastest-growing AI datacenter interconnect category.** Active Electrical Cables (AEC) are the copper alternative to optical fiber for rack-to-rack GPU interconnect inside AI clusters. CRDO owns the full stack — SerDes IP + Retimer + AEC manufacturing — giving it the lowest-cost, fastest-innovation position. ~73% AEC market share as of Q2 2025. Priced at 17.5x forward P/S, reflecting the dominance premium.

3. **AEIS has a cycle-diversifying second engine: AI server power.** Power delivery systems for WFE OEMs (Applied Materials, Lam, KLA) is the legacy moat — high switching costs because re-qualifying a power system requires months of process revalidation. But AEIS's Data Center Computing revenue (AI server power) grew 113% YoY to $171.6M in Q3 2025, now 37% of total sales. If WFE spending softens, the datacenter power business partially offsets — a structural advantage UCTT lacks.

## Bear case

1. **RISC-V is the existential long-term risk to ARM's royalty model.** RISC-V hit ~25% global unit share (❓ primarily embedded/IoT, not datacenter) in Jan 2026, growing ~80% annually. It is royalty-free and modular — custom AI instruction extensions can be baked in without paying ARM CSS rates. ARM's own move into merchant silicon (competing with licensees like Qualcomm, Apple, NVDA) could push major customers toward RISC-V as a defensive hedge. The timeline is 5-10 years, not 1-2.

2. **Optical interconnect is the structural threat to CRDO's AEC moat.** Marvell's Celestial AI acquisition (photonic fabric platform, close Q1 FY2027) is a direct bet that optics will displace copper AEC at short reach as AI cluster bandwidth scales. CRDO has no photonics answer. At 17.5x P/S, even a credible Marvell optical win at one hyperscaler would be a significant de-rating event.

3. **AEIS and UCTT amplify WFE cycle swings, not dampen them.** Sub-tier suppliers to OEMs lag Tier 1 WFE orders by 1-2 quarters. When OEMs digest inventory, AEIS and UCTT feel it faster than LRCX or ASML. UCTT has no cycle offset (unlike AEIS datacenter revenue), making it more exposed to memory capex cuts.

## Kill conditions

| Company | Kill condition | Current status |
|---|---|---|
| ARM | Apple/Qualcomm/NVDA publicly commit to RISC-V R&D at scale | NOT triggered |
| ARM | CSS revenue share declines 2 consecutive quarters | NOT triggered |
| CRDO | Marvell wins hyperscaler pilot with optical interconnect | NOT triggered — watch |
| CRDO | Any hyperscaler announces short-reach optical transition roadmap | NOT triggered |
| LRCX | 2 consecutive quarters of NAND capex cuts from Samsung/SK Hynix/Micron | NOT triggered |
| LRCX | TSMC revises advanced node capacity expansion downward | NOT triggered |
| AEIS | WFE downturn + AI server power misses simultaneously | NOT triggered |
| ONTO | KLA releases competitive GAA 3D metrology tool | NOT triggered — watch |

## Data gaps

- ❓ WDC (Western Digital) listed in T2 — unclear why it belongs in Semicon Moats vs AI Capex; flash storage is not a moat business in the same category. Needs separate review.
- ❓ CRDO photonics roadmap — none found; may not exist
- ❓ ARM CSS adoption rate among chip designers (% of licensees using CSS vs legacy Armv8) — management says "north of 10%" royalty but CSS penetration rate unverified
- ❓ UCTT gross margin profile and OEM customer concentration — not confirmed
- ❓ ONTO revenue split: GAA-specific vs legacy node metrology — not disclosed
- ❓ RISC-V 25% "global unit share" — almost certainly dominated by IoT/embedded; datacenter-specific RISC-V share is much lower

## Sources

- BeyondSPX: ARM royalty acceleration & RISC-V risk (2026)
- Motley Fool: ARM own-chip plan, Nov 2025
- FinancialContent: ARM downgrade, April 2026
- Yahoo Finance: CRDO vs MRVL connectivity analysis
- FinancialContent: Credo Technology deep dive, April 2026
- Edgen: LRCX picks-and-shovels AI fabs, 2026
- 247 Wall St: JPMorgan LRCX $315 target, April 2026
- BeyondSPX: AEIS AI power surge analysis
- EverytTicker/BeyondSPX: UCTT semiconductor partnership analysis
- GlobalTechResearch: KLAC vs ONTO process control
- SemiAnalysis: How ONTO gains share from KLA
