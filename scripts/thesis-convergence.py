#!/usr/bin/env python3
"""
Thesis Convergence Detector
Reads vault/Knowledge/insight-atoms/ → finds when 2+ independent sources
confirm the same macro theme or thesis → surfaces as high-conviction signal.

Nick reads vault/Knowledge/thesis-convergence.md during /nick-weekly KB sweep.

Usage:
    python scripts/thesis-convergence.py              # write output file
    python scripts/thesis-convergence.py --dry-run    # print only
"""

import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
ATOMS_DIR = ROOT / "vault/Knowledge/insight-atoms"
OUTPUT_FILE = ROOT / "vault/Knowledge/thesis-convergence.md"

sys.stdout.reconfigure(encoding="utf-8")

# Macro themes: name → keywords to detect in claim+implication text
THEMES = {
    "AI Capex / Hyperscaler Spend": [
        "capex", "hyperscaler", "ai infrastructure", "datacenter", "training",
        "gpu demand", "blackwell", "h100", "h200", "compute demand",
    ],
    "Custom Silicon / ASIC": [
        "asic", "custom silicon", "tpu", "xpu", "mtia", "inferentia",
        "custom chip", "in-house silicon",
    ],
    "AI Networking": [
        "networking", "ethernet", "infiniband", "interconnect",
        "roce", "800g", "400g", "ai networking",
    ],
    "Semiconductor Moats": [
        "euv", "lithography", "etch", "deposition", "fab",
        "wafer", "process node", "node", "tsmc", "foundry",
    ],
    "AI Software Monetization": [
        "aip", "software monetization", "enterprise ai", "ai platform",
        "ai deployment", "workflow automation", "llm enterprise",
    ],
    "China / Export Risk": [
        "china", "export control", "export ban", "tariff",
        "geopolit", "taiwan", "supply chain risk",
    ],
    "Valuation Compression Risk": [
        "multiple compression", "p/e compression", "overvalued",
        "premium valuation", "ev/revenue", "p/s", "re-rating",
    ],
    "Government / Defense Spend": [
        "government contract", "dod", "defense", "classified",
        "national security", "military", "federal", "doge",
    ],
    "Space / Launch": [
        "launch", "rocket", "orbital", "satellite", "neutron",
        "falcon", "reusable", "launch cadence",
    ],
    "Quantum Computing": [
        "quantum", "qubit", "coherence", "error correction",
        "fault-tolerant", "quantum advantage",
    ],
    "Memory / Storage": [
        "hbm", "dram", "nand", "memory bandwidth", "high bandwidth",
        "memory demand", "storage",
    ],
    "Datacenter Cooling": [
        "cooling", "thermal", "liquid cooling", "heat",
        "power density", "immersion cooling",
    ],
}


# Maps convergence theme → tickers that directly benefit
# Used to generate the Candidate Mapper section in the report
THEME_CANDIDATES: dict[str, dict[str, list[str]]] = {
    "AI Capex / Hyperscaler Spend": {
        "direct":    ["NVDA", "AMD", "AVGO", "SMCI", "MU"],
        "secondary": ["LRCX", "MRVL", "DELL", "HPE", "MOD"],
        "action":    "Size up T1/T2 conviction — structural multi-year tailwind confirmed",
    },
    "AI Networking": {
        "direct":    ["CRDO", "MRVL", "AVGO"],
        "secondary": ["NVDA", "AMD"],
        "action":    "CRDO/MRVL = direct Ethernet switch ASIC beneficiaries",
    },
    "Semiconductor Moats": {
        "direct":    ["NVDA", "ASML", "LRCX", "ARM"],
        "secondary": ["MU", "CRDO", "AEIS", "UCTT"],
        "action":    "Hold T2 names through cycle — pricing power structural",
    },
    "Memory / Storage": {
        "direct":    ["MU", "WDC"],
        "secondary": ["LRCX", "AEIS"],
        "action":    "MU = primary HBM beneficiary — check entry signal",
    },
    "Space / Launch": {
        "direct":    ["RKLB", "ASTS", "LUNR"],
        "secondary": ["KTOS", "BBAI", "HAWK"],
        "action":    "RKLB = launch cadence play; ASTS = connectivity; speculative tier",
    },
    "Quantum Computing": {
        "direct":    ["IONQ", "RGTI", "QBTS", "QUBT"],
        "secondary": ["IBM"],
        "action":    "Pre-commercial, high binary risk — size MED conviction max",
    },
    "Government / Defense Spend": {
        "direct":    ["PLTR", "KTOS", "BBAI", "AVAV"],
        "secondary": ["RKLB", "ASTS"],
        "action":    "PLTR = AI decision layer for gov; KTOS = autonomous defense systems",
    },
    "AI Software Monetization": {
        "direct":    ["PLTR", "CRM", "SNOW"],
        "secondary": [],
        "action":    "Verify RS before adding — PLTR RS↓ currently; SNOW RS↑ watch",
    },
    "Valuation Compression Risk": {
        "direct":    [],
        "secondary": [],
        "warning":   ["PLTR", "MOD", "QUBT", "RGTI"],
        "action":    "HIGH-MULTIPLE RISK — reduce or avoid adding to these names",
    },
    "Custom Silicon / ASIC": {
        "direct":    ["AVGO", "MRVL", "AMD"],
        "secondary": ["NVDA"],
        "action":    "AVGO = custom ASIC leader for hyperscalers; competitive threat to NVDA watch",
    },
    "Datacenter Cooling": {
        "direct":    ["MOD"],
        "secondary": ["DELL", "HPE"],
        "action":    "MOD = highest direct exposure but valuation compressed — size carefully",
    },
}


def parse_frontmatter(text: str) -> dict:
    """Extract frontmatter key:value pairs."""
    fm = {}
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def load_contradiction_signals() -> dict[tuple[str, str], int]:
    """
    Parse vault/Knowledge/contradiction-registry.md → return {(source_file_stem, theme_keyword): weight}
    weight = -1 if that source contradicts that theme, +1 if explicit corroboration.

    Registry entry format:
    [YYYY-MM-DD] [TICKER/MARKET] — <claim> | Source A: <value> vs Source B: <value> | Thesis link: T#

    Simple heuristic: if registry entry mentions a ticker AND a theme keyword → mark that ticker's
    atom source as contradicting that theme (weight -1).
    """
    registry_path = ROOT / "vault/Knowledge/contradiction-registry.md"
    signals: dict[tuple[str, str], int] = {}

    if not registry_path.exists():
        return signals

    try:
        text = registry_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return signals

    # Each line: [DATE] [TICKER] — claim | Source A: X vs Source B: Y | Thesis: T#
    entry_re = re.compile(r"^\[[\d-]+\]\s+\[([^\]]+)\].*?\|.*?Thesis link:\s*(T\d+)", re.IGNORECASE)
    for line in text.splitlines():
        m = entry_re.match(line.strip())
        if not m:
            continue
        ticker = m.group(1).strip().upper()
        # Map ticker → likely source file stems (e.g. "LRCX" → files containing "lrcx")
        # We'll key on ticker string, resolved later against atom source_file
        for theme, keywords in THEMES.items():
            line_lower = line.lower()
            if any(kw in line_lower for kw in keywords):
                signals[(ticker.lower(), theme)] = -1  # contradiction weight

    return signals


def parse_atoms_from_file(path: Path) -> list[dict]:
    """
    Parse individual atom sections from a file.
    Returns list of dicts with: source, theses, claim, implication, date
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    fm = parse_frontmatter(text)
    source = fm.get("ticker") or fm.get("topic") or path.stem
    file_date = fm.get("date") or fm.get("created") or "unknown"

    atoms = []
    # Each atom is a ## section
    sections = re.split(r"\n## ", text)
    for section in sections[1:]:  # skip file header
        lines = section.strip().splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])

        # Thesis links (may be "T1, T2" or "T1")
        thesis_m = re.search(r"\*\*Thesis link:\*\*\s*([^\n]+)", body)
        theses = []
        if thesis_m:
            theses = [t.strip() for t in thesis_m.group(1).split(",") if re.match(r"T\d+", t.strip())]

        claim_m = re.search(r"\*\*Claim:\*\*\s*(.+?)(?=\n\*\*|\Z)", body, re.DOTALL)
        claim = claim_m.group(1).strip()[:250] if claim_m else ""

        impl_m = re.search(r"\*\*Implication:\*\*\s*(.+?)(?=\n\*\*|\Z)", body, re.DOTALL)
        implication = impl_m.group(1).strip()[:250] if impl_m else ""

        date_m = re.search(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})", body)
        atom_date = date_m.group(1) if date_m else file_date

        if not claim:
            continue

        atoms.append({
            "source": source,
            "source_file": path.name,
            "theses": theses,
            "title": title,
            "claim": claim,
            "implication": implication,
            "date": atom_date,
        })

    return atoms


def match_themes(atom: dict) -> list[str]:
    """Return macro themes this atom matches based on claim + implication."""
    text = (atom["claim"] + " " + atom["implication"]).lower()
    return [theme for theme, keywords in THEMES.items()
            if any(kw in text for kw in keywords)]


def generate_candidate_section(cross_thesis: list) -> list[str]:
    """Generate Candidate Mapper section for STRONG convergence signals only."""
    lines = [
        "---",
        "",
        "## Candidate Mapper — STRONG Signals -> Direct Beneficiaries",
        "",
        "*Nick: ใช้ section นี้ใน Step 6 เพื่อ map signal -> ticker action*",
        "",
    ]

    strong_themes = [
        (theme, atoms, theses, sources, strength)
        for theme, atoms, theses, sources, strength, *_ in cross_thesis
        if strength == "STRONG"
    ]

    if not strong_themes:
        lines.append("*ยังไม่มี STRONG convergence signals — ยังไม่มี candidate mapping*")
        lines.append("")
        return lines

    lines += [
        "| Convergence Signal | Strength | Direct Beneficiaries | Secondary | Nick Action |",
        "|---|---|---|---|---|",
    ]

    for theme, atoms, theses, sources, strength in strong_themes:
        mapping = THEME_CANDIDATES.get(theme)
        if not mapping:
            continue

        badge = "STRONG"
        direct = ", ".join(mapping.get("direct", [])) or "—"
        secondary = ", ".join(mapping.get("secondary", [])) or "—"
        warning = ", ".join(mapping.get("warning", []))
        if warning:
            direct = f"WARN: {warning}"
            secondary = "—"
        action = mapping.get("action", "—")
        lines.append(f"| {theme} | {badge} | {direct} | {secondary} | {action} |")

    lines.append("")
    return lines


def main():
    dry_run = "--dry-run" in sys.argv

    atom_files = [f for f in sorted(ATOMS_DIR.glob("*.md")) if f.name != "README.md"]
    all_atoms = []
    for f in atom_files:
        all_atoms.extend(parse_atoms_from_file(f))

    if not all_atoms:
        print("No insight atoms found.")
        return

    # Load contradiction signals (KARMA weighting)
    contradiction_signals = load_contradiction_signals()

    # --- Build: theme → list of atoms ---
    theme_map: dict[str, list[dict]] = defaultdict(list)
    for atom in all_atoms:
        for theme in match_themes(atom):
            theme_map[theme].append(atom)

    # --- Build: thesis → list of source files confirming it ---
    thesis_sources: dict[str, set[str]] = defaultdict(set)
    for atom in all_atoms:
        for t in atom["theses"]:
            thesis_sources[t].add(atom["source_file"])

    # --- Convergence signals (KARMA weighted — arXiv:OpenReview:k0wyi4cOGy) ---
    cross_thesis = []
    for theme, atoms in sorted(theme_map.items()):
        distinct_theses = sorted({t for a in atoms for t in a["theses"]})
        distinct_sources = sorted({a["source_file"] for a in atoms})

        # KARMA: compute net weight = sum(+1 corroborate / -1 contradict per source)
        net_weight = 0
        contradiction_count = 0
        for source_file in distinct_sources:
            source_stem = source_file.lower().replace(".md", "")
            # Check if this source contradicts this theme
            contradicts = any(
                signals < 0
                for (ticker, t), signals in contradiction_signals.items()
                if t == theme and ticker in source_stem
            )
            if contradicts:
                net_weight -= 1
                contradiction_count += 1
            else:
                net_weight += 1

        # Threshold: need net_weight ≥ 2 AND enough sources (contradiction can downgrade)
        if net_weight >= 2 and (len(distinct_theses) >= 2 or len(distinct_sources) >= 3):
            if contradiction_count > 0:
                # Contradictions present — cap at MODERATE unless overwhelming corroboration
                strength = "STRONG" if net_weight >= 4 else "MODERATE"
            else:
                strength = "STRONG" if len(distinct_theses) >= 3 or len(distinct_sources) >= 4 else "MODERATE"
            cross_thesis.append((theme, atoms, distinct_theses, distinct_sources, strength, net_weight, contradiction_count))
        elif net_weight < 2 and len(distinct_sources) >= 3:
            # Was strong but contradictions reduced it — show as CONTESTED
            cross_thesis.append((theme, atoms, distinct_theses, distinct_sources, "CONTESTED", net_weight, contradiction_count))

    cross_thesis.sort(key=lambda x: (x[4] not in ("STRONG",), -x[5], -len(x[2])))

    # Within-thesis multi-source confirmation
    within_thesis = [(t, srcs) for t, srcs in sorted(thesis_sources.items())
                     if len(srcs) >= 2]

    # --- Format report ---
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    today = now[:10]

    lines = [
        "---",
        "type: kb-convergence",
        f"updated: {today}",
        "source: scripts/thesis-convergence.py",
        "---",
        "",
        "# Thesis Convergence Report",
        f"*Auto-generated {now} — Nick อ่านไฟล์นี้ใน /nick-weekly Step 5 (KB sweep)*",
        "",
        f"Atoms analyzed: **{len(all_atoms)}** across **{len(atom_files)}** files | "
        f"Themes detected: **{len([t for t in theme_map if theme_map[t]])}**",
        "",
        "---",
        "",
    ]

    # Cross-thesis convergences
    lines.append("## Cross-Thesis Convergence")
    lines.append("")
    if cross_thesis:
        for theme, atoms, theses, sources, strength, net_weight, contradiction_count in cross_thesis:
            if strength == "STRONG":
                badge = "🔴 STRONG"
            elif strength == "MODERATE":
                badge = "🟡 MODERATE"
            else:
                badge = "⚠️ CONTESTED"

            theses_str = " + ".join(theses) if theses else "multiple"
            weight_str = f"net={net_weight:+d}"
            if contradiction_count > 0:
                weight_str += f" ({contradiction_count} contradicting source{'s' if contradiction_count > 1 else ''})"
            lines.append(f"### {theme} [{badge}]")
            lines.append(f"- **Theses:** {theses_str} | **Sources:** {len(sources)} | **KARMA weight:** {weight_str}")
            # Top 3 claims
            seen_sources = set()
            shown = 0
            for a in atoms:
                if a["source_file"] in seen_sources or shown >= 3:
                    continue
                seen_sources.add(a["source_file"])
                claim_short = a["claim"][:130].rstrip() + ("..." if len(a["claim"]) > 130 else "")
                src = a["source"].upper() if len(a["source"]) <= 6 else a["source"]
                lines.append(f"- **{src}** ({a['date']}): {claim_short}")
                shown += 1
            if len(sources) > 3:
                lines.append(f"- *...+{len(sources)-3} more sources*")
            # Nick implication
            if strength == "STRONG":
                lines.append(f"- **Nick:** {len(theses)} theses confirm — treat as structural macro tailwind, not single-thesis risk")
            else:
                lines.append(f"- **Nick:** 2 theses align — watch for 3rd confirmation before sizing up")
            lines.append("")
    else:
        lines.append("*ยังไม่พบ convergence (ต้องการ ≥2 theses หรือ ≥3 sources ชี้มาที่ theme เดียวกัน)*")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Within-thesis confirmations
    lines.append("## Within-Thesis Multi-Source Confirmation")
    lines.append("")
    if within_thesis:
        for thesis, source_files in within_thesis:
            count = len(source_files)
            badge = "✅" if count >= 3 else "🔵"
            srcs_display = ", ".join(sorted(source_files))
            lines.append(f"- {badge} **{thesis}** — confirmed by {count} independent files: `{srcs_display}`")
        lines.append("")
    else:
        lines.append("*ยังไม่มี thesis ที่ confirmed โดย 2+ source files*")
        lines.append("")

    lines.append("---")
    lines.append("")

    lines.extend(generate_candidate_section(cross_thesis))
    lines.append(f"*{len(all_atoms)} atoms | {len(atom_files)} files | Generated: {now}*")

    output = "\n".join(lines)
    print(output)

    if not dry_run:
        OUTPUT_FILE.write_text(output, encoding="utf-8")
        print(f"\n→ Saved: {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
