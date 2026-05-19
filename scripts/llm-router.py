#!/usr/bin/env python3
"""
llm-router.py, LTD-OS command routing engine (BEST-Route inspired)

Decides per command: LOCAL (Ollama) vs CLOUD (Claude API)
Based on complexity classification from arXiv:2506.22716 (BEST-Route, ICML 2025)

Usage:
  python scripts/llm-router.py --command daily-brief        -> LOCAL or CLOUD
  python scripts/llm-router.py --command council --verbose  -> decision + reason
  python scripts/llm-router.py --check                      -> Ollama status
  python scripts/llm-router.py --list                       -> all routing assignments

Returns exit code 0=LOCAL, 1=CLOUD, 2=FALLBACK (Ollama unreachable -> cloud)
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Literal

try:
    import requests
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

# ── Ollama endpoint ───────────────────────────────────────────────────────────
OLLAMA_BASE    = "http://localhost:11434"
OLLAMA_MODEL   = "qwen2.5:14b"
OLLAMA_TIMEOUT = 2  # seconds, fast ping

# ── Routing table ─────────────────────────────────────────────────────────────
# Complexity classification adapted from BEST-Route (arXiv:2506.22716)
# LOCAL  = factual retrieval, simple synthesis, vault reads, Qwen2.5 14B sufficient
# CLOUD  = multi-step reasoning, financial judgment, multi-agent pipelines
# ADAPTIVE = try local first; escalate to cloud for heavy follow-ups

ROUTING: dict[str, dict] = {
    # ── LOCAL tier ─────────────────────────────────────────────────────────
    "daily-brief": {
        "tier": "LOCAL",
        "reason": "vault reads + simple synthesis, no multi-step reasoning",
    },
    "handoff": {
        "tier": "LOCAL",
        "reason": "session state serialization, factual, no judgment",
    },
    "context": {
        "tier": "LOCAL",
        "reason": "token count check, no LLM call needed; Ollama as fallback display",
    },
    "weekly-learnings": {
        "tier": "LOCAL",
        "reason": "summarize daily notes, compression task Qwen handles well",
    },
    "market-log": {
        "tier": "LOCAL",
        "reason": "lite daily log entry, structured fill, no analysis",
    },
    "import-notebooklm": {
        "tier": "LOCAL",
        "reason": "vault filing of pre-processed text, no synthesis needed",
    },
    "youtube-transcript": {
        "tier": "LOCAL",
        "reason": "transcript summarization, extractive, not generative reasoning",
    },
    "onboard": {
        "tier": "LOCAL",
        "reason": "interview + fill PREFERENCES.md, Q&A, no complex reasoning",
    },
    # ── ADAPTIVE tier ──────────────────────────────────────────────────────
    "brainstorm": {
        "tier": "ADAPTIVE",
        "reason": "creative synthesis, local ok for rough ideas, cloud for depth",
    },
    "connect": {
        "tier": "ADAPTIVE",
        "reason": "note connection, local for obvious links, cloud for subtle ones",
    },
    "deep-dive": {
        "tier": "ADAPTIVE",
        "reason": "topic exploration, local if vault-only, cloud if web research needed",
    },
    "wild-thesis": {
        "tier": "ADAPTIVE",
        "reason": "lateral thinking, local for first pass, cloud for structured output",
    },
    "condense": {
        "tier": "ADAPTIVE",
        "reason": "vault condensation, local for summarization, cloud for complex restructure",
    },
    # ── CLOUD tier ─────────────────────────────────────────────────────────
    "council": {
        "tier": "CLOUD",
        "reason": "6-phase multi-agent debate, requires deep reasoning + coherence across phases",
    },
    "nick-weekly": {
        "tier": "CLOUD",
        "reason": "portfolio kill condition analysis, financial judgment, 40+ cognitive steps",
    },
    "nick-quarterly": {
        "tier": "CLOUD",
        "reason": "full thesis audit, complex financial reasoning across multiple domains",
    },
    "nick-init": {
        "tier": "CLOUD",
        "reason": "portfolio initialization, one-time critical decision, needs best quality",
    },
    "stock-content": {
        "tier": "CLOUD",
        "reason": "Reese+Chris+Vera+Indie pipeline, multi-persona reasoning, fact audit",
    },
    "stock-research": {
        "tier": "CLOUD",
        "reason": "investment research, financial judgment + kill conditions must be precise",
    },
    "pre-market": {
        "tier": "CLOUD",
        "reason": "trading setup, scenario analysis + position sizing = high-stakes",
    },
    "post-market": {
        "tier": "CLOUD",
        "reason": "prediction calibration + KB sync, requires accuracy, not just speed",
    },
    "paper-survey": {
        "tier": "CLOUD",
        "reason": "academic research synthesis, complex multi-source reasoning",
    },
    "weekly-calibration": {
        "tier": "CLOUD",
        "reason": "trading rule updates, must not degrade with lower-quality model",
    },
    "weekly-market": {
        "tier": "CLOUD",
        "reason": "market analysis, sector rotation + macro synthesis needs Claude quality",
    },
    "screen": {
        "tier": "CLOUD",
        "reason": "screener analysis, position sizing + trade setup = financial judgment",
    },
    "eod": {
        "tier": "CLOUD",
        "reason": "end-of-day report, P&L + stop distance calculation",
    },
    "paper-trade": {
        "tier": "CLOUD",
        "reason": "trade execution, irreversible action, needs best quality",
    },
    "challenge": {
        "tier": "CLOUD",
        "reason": "devils_advocate, steelman requires deep reasoning quality",
    },
    "analyst": {
        "tier": "CLOUD",
        "reason": "cost analysis + system improvements, strategic judgment",
    },
    "new-formula": {
        "tier": "CLOUD",
        "reason": "fertilizer formula creation, technical domain, precision matters",
    },
    "new-recipe": {
        "tier": "CLOUD",
        "reason": "recipe formulation, culinary precision + safety",
    },
    "workflow-design": {
        "tier": "CLOUD",
        "reason": "deep workflow analysis, complex multi-step design",
    },
}

Tier = Literal["LOCAL", "CLOUD", "ADAPTIVE", "FALLBACK", "UNKNOWN"]


def ollama_available() -> bool:
    if not _HAS_REQUESTS:
        return False
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/version", timeout=OLLAMA_TIMEOUT)
        return r.status_code == 200
    except Exception:
        return False


def route(command: str) -> tuple[Tier, str]:
    """Return (effective_tier, reason). ADAPTIVE -> LOCAL if Ollama up, else CLOUD."""
    entry = ROUTING.get(command)
    if entry is None:
        return "UNKNOWN", f"command '{command}' not in routing table, defaulting to CLOUD"

    tier: Tier = entry["tier"]
    reason: str = entry["reason"]

    if tier in ("LOCAL", "ADAPTIVE"):
        if not ollama_available():
            return "FALLBACK", f"Ollama unreachable -> CLOUD fallback ({reason})"
        effective: Tier = "LOCAL"
        return effective, reason

    return tier, reason


def main() -> None:
    parser = argparse.ArgumentParser(description="LTD-OS LLM routing engine")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--command", "-c", help="slash command name (without /)")
    group.add_argument("--check", action="store_true", help="check Ollama status")
    group.add_argument("--list", action="store_true", help="list all routing assignments")
    parser.add_argument("--verbose", "-v", action="store_true", help="show reason")
    parser.add_argument("--json", action="store_true", help="output as JSON")
    args = parser.parse_args()

    if args.check:
        up = ollama_available()
        if args.json:
            print(json.dumps({"ollama": up, "endpoint": OLLAMA_BASE, "model": OLLAMA_MODEL}))
        else:
            status = "ONLINE" if up else "OFFLINE"
            print(f"Ollama: {status} ({OLLAMA_BASE})")
            print(f"Model:  {OLLAMA_MODEL}")
        sys.exit(0 if up else 1)

    if args.list:
        ollama_up = ollama_available()
        print(f"Ollama: {'ONLINE' if ollama_up else 'OFFLINE'}\n")
        tiers: dict[str, list[str]] = {"LOCAL": [], "ADAPTIVE": [], "CLOUD": []}
        for cmd, entry in sorted(ROUTING.items()):
            tiers[entry["tier"]].append(cmd)
        for tier_name, cmds in tiers.items():
            print(f"-- {tier_name} --")
            for cmd in cmds:
                print(f"  /{cmd}")
            print()
        sys.exit(0)

    # --command mode
    effective, reason = route(args.command)

    if args.json:
        print(json.dumps({"command": args.command, "decision": effective, "reason": reason,
                          "ollama_model": OLLAMA_MODEL, "ollama_endpoint": OLLAMA_BASE}))
    elif args.verbose:
        print(f"/{args.command} -> {effective}")
        print(f"Reason: {reason}")
        if effective == "LOCAL":
            print(f"Model:  {OLLAMA_MODEL} @ {OLLAMA_BASE}")
        elif effective in ("CLOUD", "FALLBACK", "UNKNOWN"):
            print(f"Model:  Claude API")
    else:
        print(effective)

    # Exit codes: 0=LOCAL, 1=CLOUD/FALLBACK/UNKNOWN
    sys.exit(0 if effective == "LOCAL" else 1)


if __name__ == "__main__":
    main()
