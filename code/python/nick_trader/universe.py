"""
Nick v3 universe — Tier 1 (active thesis) + Tier 2 (growth expansion).
Tier 3 (momentum wildcard) is generated dynamically via RS scan.

news-snapshot.py --universe-news imports TIER1/TIER2 directly — no manual sync needed.
"""

# ---- Tier 1: Active thesis tickers (~40) — scanned DAILY ----

TIER1 = [
    # T1 — AI Capex Supercycle
    "NVDA", "AMD", "AVGO", "SMCI", "MU", "MRVL", "LRCX", "MOD", "DELL", "HPE",
    # T2 — Semiconductor Moats
    "ASML", "ARM", "CRDO", "AEIS", "UCTT", "WDC", "ONTO",
    # T3 — Space & Defense AI
    "RKLB", "ASTS", "LUNR", "KTOS", "BBAI",
    # T4 — AI Software Monetization
    "PLTR", "CRM", "SNOW",
    # T5 — Quantum Computing
    "IONQ", "RGTI", "QBTS", "QUBT",
    # T6 — Robotics & Automation
    "ISRG", "TER", "CGNX", "ROK", "SYM", "PATH", "AVAV",
]

# ---- Tier 2: Growth expansion (~30) — scanned WEEKLY (Mondays only) ----

TIER2 = [
    # Biotech / Gene Editing
    "MRNA", "CRSP", "BEAM", "RXRX",
    # Cybersecurity
    "CRWD", "PANW", "ZS", "NET", "OKTA",
    # Fintech / Crypto
    "COIN", "HOOD", "SOFI", "SQ",
    # Energy / Grid / Nuclear
    "CEG", "VST", "SMR", "NNE", "ETN",
    # Consumer / Growth Platform
    "SHOP", "MELI", "SE",
    # Defense Advanced
    "AXON", "HII",
    # Other High-Growth
    "DKNG", "DUOL", "TTD",
]

# ---- Ticker → primary thesis mapping ----

TICKER_THESIS: dict[str, str] = {
    # T1
    "NVDA": "T1", "AMD": "T1", "AVGO": "T1", "SMCI": "T1",
    "MU": "T1", "MRVL": "T1", "LRCX": "T1", "MOD": "T1", "DELL": "T1", "HPE": "T1",
    # T2
    "ASML": "T2", "ARM": "T2", "CRDO": "T2", "AEIS": "T2",
    "UCTT": "T2", "WDC": "T2", "ONTO": "T2",
    # T3
    "RKLB": "T3", "ASTS": "T3", "LUNR": "T3", "KTOS": "T3", "BBAI": "T3",
    # T4
    "PLTR": "T4", "CRM": "T4", "SNOW": "T4",
    # T5
    "IONQ": "T5", "RGTI": "T5", "QBTS": "T5", "QUBT": "T5",
    # T6
    "ISRG": "T6", "TER": "T6", "CGNX": "T6", "ROK": "T6",
    "SYM": "T6", "PATH": "T6", "AVAV": "T6",
    # Tier 2 — growth expansion (no core thesis)
    "MRNA": "T_BIO", "CRSP": "T_BIO", "BEAM": "T_BIO", "RXRX": "T_BIO",
    "CRWD": "T_CYBER", "PANW": "T_CYBER", "ZS": "T_CYBER", "NET": "T_CYBER", "OKTA": "T_CYBER",
    "COIN": "T_FIN", "HOOD": "T_FIN", "SOFI": "T_FIN", "SQ": "T_FIN",
    "CEG": "T_ENERGY", "VST": "T_ENERGY", "SMR": "T_ENERGY", "NNE": "T_ENERGY", "ETN": "T_ENERGY",
    "SHOP": "T_GROWTH", "MELI": "T_GROWTH", "SE": "T_GROWTH",
    "AXON": "T_DEF", "HII": "T_DEF",
    "DKNG": "T_GROWTH", "DUOL": "T_GROWTH", "TTD": "T_GROWTH",
}


def get_universe(tiers: tuple[int, ...] = (1,)) -> list[str]:
    """Return deduplicated ticker list for given tiers."""
    result: list[str] = []
    seen: set[str] = set()
    if 1 in tiers:
        for t in TIER1:
            if t not in seen:
                seen.add(t)
                result.append(t)
    if 2 in tiers:
        for t in TIER2:
            if t not in seen:
                seen.add(t)
                result.append(t)
    return result
