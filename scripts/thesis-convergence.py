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


def main():
    dry_run = "--dry-run" in sys.argv

    atom_files = [f for f in sorted(ATOMS_DIR.glob("*.md")) if f.name != "README.md"]
    all_atoms = []
    for f in atom_files:
        all_atoms.extend(parse_atoms_from_file(f))

    if not all_atoms:
        print("No insight atoms found.")
        return

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

    # --- Convergence signals ---
    # Cross-thesis: theme appears in atoms from ≥2 distinct thesis groups
    cross_thesis = []
    for theme, atoms in sorted(theme_map.items()):
        distinct_theses = sorted({t for a in atoms for t in a["theses"]})
        distinct_sources = sorted({a["source_file"] for a in atoms})
        if len(distinct_theses) >= 2 or len(distinct_sources) >= 3:
            strength = "STRONG" if len(distinct_theses) >= 3 or len(distinct_sources) >= 4 else "MODERATE"
            cross_thesis.append((theme, atoms, distinct_theses, distinct_sources, strength))

    cross_thesis.sort(key=lambda x: (x[4] != "STRONG", -len(x[2]), -len(x[3])))

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
        for theme, atoms, theses, sources, strength in cross_thesis:
            badge = "🔴 STRONG" if strength == "STRONG" else "🟡 MODERATE"
            lines.append(f"### {theme} [{badge}]")
            theses_str = " + ".join(theses) if theses else "multiple"
            lines.append(f"- **Theses:** {theses_str} | **Sources:** {len(sources)} independent files")
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
    lines.append(f"*{len(all_atoms)} atoms | {len(atom_files)} files | Generated: {now}*")

    output = "\n".join(lines)
    print(output)

    if not dry_run:
        OUTPUT_FILE.write_text(output, encoding="utf-8")
        print(f"\n→ Saved: {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
